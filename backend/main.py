from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List, Optional
from fastapi import status
from datetime import datetime
import os
from dotenv import load_dotenv
from models import Member, MemberCreate, MemberUpdate, Contact, ContactCreate, City, CityCreate, UserRole
from auth.routes import router as auth_router
from auth.dependencies import get_current_user, get_current_active_user, require_admin, require_role
from auth.permissions import is_admin, can_edit_member
from auth.security import get_password_hash
from utils.email import send_credentials_email
from utils.password_generator import generate_temporary_password

load_dotenv()

app = FastAPI(
    title="Club Volkswagen Jetta Colombia API",
    description="API para el club de carros Volkswagen Jetta en Colombia",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "jetta_club")

# Inicializar variables globales
client = None
db = None
members_collection = None
contacts_collection = None
users_collection = None

def connect_to_mongodb():
    """Conectar a MongoDB y crear las colecciones"""
    global client, db, members_collection, contacts_collection, cities_collection, users_collection
    
    try:
        if not MONGODB_URI or MONGODB_URI == "mongodb://localhost:27017/":
            print("⚠️  MONGODB_URI no configurado. Usando localhost por defecto.")
            print("   Para usar MongoDB Atlas, crea un archivo .env con tu connection string")
        
        # Configurar conexión con parámetros SSL y timeout aumentado
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=30000,  # 30 segundos
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            retryWrites=True,
            tls=True,
            tlsAllowInvalidCertificates=False
        )
        db = client[DB_NAME]
        
        # Verificar conexión
        client.admin.command('ping')
        print(f"✅ Conectado a MongoDB: {DB_NAME}")
        
        # Inicializar colecciones
        members_collection = db.members
        contacts_collection = db.contacts
        cities_collection = db.cities
        users_collection = db.users
        
        # Crear índices para mejorar rendimiento
        try:
            members_collection.create_index("email", unique=True, sparse=True)
            members_collection.create_index("join_date")
            contacts_collection.create_index("category")
            cities_collection.create_index("name", unique=True)
            cities_collection.create_index("is_active")
            users_collection.create_index("username", unique=True)
            users_collection.create_index("email", unique=True, sparse=True)
        except Exception as idx_error:
            # Los índices pueden ya existir, no es crítico
            print(f"⚠️  Nota sobre índices: {idx_error}")
        
        return True
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        print("   Verifica que:")
        print("   1. El archivo .env existe en la carpeta backend/")
        print("   2. MONGODB_URI está correctamente configurado")
        print("   3. Tu IP está en la whitelist de MongoDB Atlas (0.0.0.0/0 para permitir todas)")
        print("   4. Las credenciales son correctas")
        print("   5. MongoDB Atlas permite conexiones desde Render.com")
        return False

# Conectar al iniciar
connect_to_mongodb()

# Registrar routers
app.include_router(auth_router)

# Helper function to convert ObjectId to string
def member_helper(member) -> dict:
    if member:
        member["id"] = str(member["_id"])
        del member["_id"]
    return member

def contact_helper(contact) -> dict:
    if contact:
        contact["id"] = str(contact["_id"])
        del contact["_id"]
    return contact

def city_helper(city) -> dict:
    if city:
        city["id"] = str(city["_id"])
        del city["_id"]
    return city

def user_helper(user) -> dict:
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
        # Nunca devolver el password_hash
        if "password_hash" in user:
            del user["password_hash"]
        # Asegurar que must_change_password esté presente
        if "must_change_password" not in user:
            user["must_change_password"] = False
    return user

def filter_member_public(member: dict) -> dict:
    """
    Filtrar datos sensibles de un miembro para vista pública
    Solo muestra: name, nickname, description, birthday, join_date, car info
    Oculta: email, phone, city, is_active, created_at, updated_at
    """
    from datetime import datetime
    
    public_data = {
        "id": member.get("id") or str(member.get("_id", "")),
        "name": member.get("name", ""),
        "nickname": member.get("nickname"),
        "description": member.get("description"),
        "birthday": member.get("birthday"),
        "join_date": member.get("join_date"),
        "car_year": member.get("car_year"),
        "car_model": member.get("car_model"),
        "car_color": member.get("car_color"),
    }
    
    # Calcular años de membresía si hay join_date
    if public_data.get("join_date"):
        try:
            join_date = datetime.strptime(public_data["join_date"], "%Y-%m-%d")
            years = (datetime.utcnow() - join_date).days // 365
            public_data["membership_years"] = max(0, years)
        except:
            public_data["membership_years"] = None
    
    # Eliminar campos None para respuesta más limpia
    return {k: v for k, v in public_data.items() if v is not None or k == "id"}

# ============ MEMBERS ENDPOINTS ============

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API del Club Volkswagen Jetta Colombia",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    try:
        client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except:
        return {"status": "unhealthy", "database": "disconnected"}

# ============ ENDPOINTS DE PRUEBA: SISTEMA DE ROLES ============
# TODO: Eliminar estos endpoints después de probar

@app.get("/api/test/current-user")
async def test_current_user(user: dict = Depends(get_current_user)):
    """Prueba: Cualquier usuario autenticado puede acceder"""
    return {
        "message": "✅ Acceso permitido",
        "user": {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role")
        }
    }

@app.get("/api/test/active-user")
async def test_active_user(user: dict = Depends(get_current_active_user)):
    """Prueba: Solo usuarios activos pueden acceder"""
    return {
        "message": "✅ Usuario activo",
        "user": {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role"),
            "is_active": user.get("is_active")
        }
    }

@app.get("/api/test/admin-only")
async def test_admin_only(user: dict = Depends(require_admin)):
    """Prueba: Solo admin puede acceder"""
    return {
        "message": "✅ Eres administrador",
        "user": {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role")
        }
    }

@app.get("/api/test/admin-or-user")
async def test_admin_or_user(user: dict = Depends(require_role(["admin", "user"]))):
    """Prueba: Admin o user pueden acceder"""
    return {
        "message": "✅ Tienes un rol válido (admin o user)",
        "user": {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role")
        }
    }

@app.get("/api/test/permissions")
async def test_permissions(user: dict = Depends(get_current_active_user)):
    """Prueba: Verificar helpers de permisos"""
    return {
        "message": "✅ Helpers de permisos",
        "user": {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role"),
            "member_id": user.get("member_id")
        },
        "permissions": {
            "is_admin": is_admin(user),
            "can_edit_member_123": can_edit_member(user, "123"),
            "can_edit_own_member": can_edit_member(user, user.get("member_id")) if user.get("member_id") else False
        }
    }

@app.post("/api/members", response_model=dict, status_code=201)
async def create_member(member: MemberCreate, user: dict = Depends(require_admin)):
    """
    Crear un nuevo miembro del club - Solo administradores
    Si create_user=True, también crea un usuario asociado y envía credenciales por email
    """
    print(f"\n{'='*60}")
    print(f"🆕 [CREAR MIEMBRO] Nueva solicitud de creación de miembro")
    print(f"   - Solicitado por: {user.get('username', 'unknown')} (rol: {user.get('role', 'unknown')})")
    print(f"{'='*60}")
    
    try:
        member_dict = member.dict()
        create_user = member_dict.pop("create_user", False)
        user_role = member_dict.pop("user_role", UserRole.USER.value)
        
        print(f"📋 [CREAR MIEMBRO] Datos recibidos:")
        print(f"   - Nombre: {member_dict.get('name', 'N/A')}")
        print(f"   - Email: {member_dict.get('email', 'N/A')}")
        print(f"   - Crear usuario: {create_user}")
        print(f"   - Rol de usuario: {user_role}")
        
        # Validar que si se quiere crear usuario, haya email
        if create_user and not member_dict.get("email"):
            print(f"❌ [CREAR MIEMBRO] Validación fallida: Se requiere email para crear usuario")
            raise HTTPException(
                status_code=400,
                detail="Se requiere un email para crear un usuario asociado"
            )
        
        member_data = member_dict
        member_data["created_at"] = datetime.utcnow()
        member_data["updated_at"] = datetime.utcnow()
        
        # Crear el miembro
        print(f"💾 [CREAR MIEMBRO] Insertando miembro en base de datos...")
        result = members_collection.insert_one(member_data)
        new_member = members_collection.find_one({"_id": result.inserted_id})
        member_id = str(result.inserted_id)
        print(f"✅ [CREAR MIEMBRO] Miembro creado con ID: {member_id}")
        
        # Si se solicita crear usuario
        if create_user:
            print(f"📝 [CREAR USUARIO] Iniciando creación de usuario para miembro {member_id}")
            print(f"   - Email del miembro: {member_data.get('email', 'NO PROPORCIONADO')}")
            print(f"   - Rol solicitado: {user_role}")
            
            try:
                # Generar username (usar email o nombre)
                email = member_data.get("email", "")
                if not email:
                    print("❌ [CREAR USUARIO] No hay email, no se puede crear usuario")
                    raise ValueError("Email requerido para crear usuario")
                
                username_base = email.split("@")[0] if email else member_data.get("name", "").lower().replace(" ", "")
                print(f"   - Username base generado: {username_base}")
                
                # Asegurar que el username sea único
                username = username_base
                counter = 1
                while users_collection.find_one({"username": username}):
                    print(f"   - Username '{username}' ya existe, probando variante...")
                    username = f"{username_base}{counter}"
                    counter += 1
                
                print(f"✅ [CREAR USUARIO] Username final: {username}")
                
                # Generar contraseña temporal
                print("🔐 [CREAR USUARIO] Generando contraseña temporal...")
                temporary_password = generate_temporary_password()
                print(f"   - Contraseña temporal generada: {temporary_password[:3]}*** (oculta por seguridad)")
                password_hash = get_password_hash(temporary_password)
                print("   - Hash de contraseña generado correctamente")
                
                # Crear usuario
                user_data = {
                    "username": username,
                    "email": email,
                    "password_hash": password_hash,
                    "role": user_role,
                    "member_id": member_id,
                    "is_active": True,
                    "must_change_password": True,  # Debe cambiar contraseña al primer login
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "last_login": None
                }
                
                print(f"💾 [CREAR USUARIO] Insertando usuario en base de datos...")
                result = users_collection.insert_one(user_data)
                print(f"✅ [CREAR USUARIO] Usuario creado con ID: {result.inserted_id}")
                
                # Enviar email con credenciales (no bloquea si falla)
                if email:
                    print(f"📧 [ENVIAR EMAIL] Intentando enviar email a: {email}")
                    try:
                        # Intentar enviar email, pero no bloquear si falla
                        email_sent = send_credentials_email(email, username, temporary_password)
                        if email_sent:
                            print(f"✅ [ENVIAR EMAIL] Email enviado exitosamente a {email}")
                        else:
                            print(f"⚠️  [ENVIAR EMAIL] Email NO enviado (verificar configuración Resend)")
                            print(f"   Credenciales para {email}:")
                            print(f"   - Username: {username}")
                            print(f"   - Password: {temporary_password}")
                    except Exception as email_error:
                        # Si falla el envío, solo loguear (no bloquear la respuesta)
                        print(f"⚠️  [ENVIAR EMAIL] Error al enviar email: {email_error}")
                        print(f"   Tipo: {type(email_error).__name__}")
                        print(f"   El miembro y usuario se crearon correctamente")
                        print(f"   Credenciales para {email}:")
                        print(f"   - Username: {username}")
                        print(f"   - Password: {temporary_password}")
                else:
                    print("⚠️  [ENVIAR EMAIL] No hay email, no se puede enviar credenciales")
                
            except DuplicateKeyError as e:
                # Si el username ya existe, no crear usuario pero sí el miembro
                print(f"❌ [CREAR USUARIO] Usuario con username '{username}' ya existe. Miembro creado sin usuario.")
                print(f"   Error: {str(e)}")
            except ValueError as e:
                print(f"❌ [CREAR USUARIO] Error de validación: {str(e)}")
                print(f"   Miembro creado sin usuario.")
            except Exception as e:
                # No fallar la creación del miembro si falla la creación del usuario
                print(f"❌ [CREAR USUARIO] Error inesperado al crear usuario: {str(e)}")
                print(f"   Tipo de error: {type(e).__name__}")
                import traceback
                print(f"   Traceback completo:")
                traceback.print_exc()
                print(f"   Miembro creado sin usuario.")
        else:
            print(f"ℹ️  [CREAR MIEMBRO] No se solicitó crear usuario (create_user=False)")
        
        print(f"✅ [CREAR MIEMBRO] Proceso completado exitosamente")
        print(f"{'='*60}\n")
        return member_helper(new_member)
    except HTTPException:
        print(f"❌ [CREAR MIEMBRO] Error HTTP - Re-lanzando excepción")
        print(f"{'='*60}\n")
        raise
    except DuplicateKeyError as e:
        print(f"❌ [CREAR MIEMBRO] Error: El miembro ya existe")
        print(f"   Detalle: {str(e)}")
        print(f"{'='*60}\n")
        raise HTTPException(status_code=400, detail="El miembro ya existe")
    except Exception as e:
        print(f"❌ [CREAR MIEMBRO] Error inesperado: {str(e)}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Error al crear miembro: {str(e)}")

@app.get("/api/members", response_model=List[dict])
async def get_members(
    skip: int = 0, 
    limit: int = 100,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Obtener lista de miembros
    - Admin: Ve todos los miembros (activos e inactivos)
    - User/No autenticado: Solo ve miembros activos con datos públicos
    """
    try:
        from typing import Optional as Opt
        
        # Si es admin, puede ver todos (activos e inactivos)
        if current_user and is_admin(current_user):
            members = list(members_collection.find().skip(skip).limit(limit))
            return [member_helper(m) for m in members]
        
        # Si no es admin, solo activos y datos públicos
        members = list(members_collection.find({"is_active": True}).skip(skip).limit(limit))
        return [filter_member_public(member_helper(m)) for m in members]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener miembros: {str(e)}")

@app.get("/api/members/{member_id}", response_model=dict)
async def get_member(
    member_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Obtener un miembro por ID
    - Admin: Ve todos los datos
    - User (propio perfil): Ve todos los datos
    - User (otro perfil): Solo datos públicos
    - No autenticado: Solo datos públicos
    """
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        member = members_collection.find_one({"_id": ObjectId(member_id)})
        if not member:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        member_dict = member_helper(member)
        
        # Si es admin, mostrar todo
        if current_user and is_admin(current_user):
            return member_dict
        
        # Si es el dueño del perfil, mostrar todo
        if current_user and can_edit_member(current_user, member_id):
            return member_dict
        
        # Si no, solo datos públicos
        return filter_member_public(member_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener miembro: {str(e)}")

@app.put("/api/members/{member_id}", response_model=dict)
async def update_member(
    member_id: str, 
    member_update: MemberUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Actualizar información de un miembro
    - Admin: Puede editar cualquier miembro
    - User: Solo puede editar su propio perfil (excepto is_active y join_date)
    """
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        # Verificar permisos
        if not can_edit_member(current_user, member_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes editar tu propio perfil"
            )
        
        update_data = member_update.dict(exclude_unset=True)
        
        # Si no es admin, no puede cambiar is_active ni join_date
        if not is_admin(current_user):
            update_data.pop("is_active", None)
            update_data.pop("join_date", None)
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = members_collection.update_one(
            {"_id": ObjectId(member_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        updated_member = members_collection.find_one({"_id": ObjectId(member_id)})
        return member_helper(updated_member)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar miembro: {str(e)}")

@app.patch("/api/members/{member_id}/deactivate", response_model=dict)
async def deactivate_member(member_id: str, user: dict = Depends(require_admin)):
    """Inactivar un miembro (soft delete) - Solo administradores"""
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        result = members_collection.update_one(
            {"_id": ObjectId(member_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        updated_member = members_collection.find_one({"_id": ObjectId(member_id)})
        return member_helper(updated_member)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inactivar miembro: {str(e)}")

@app.patch("/api/members/{member_id}/activate", response_model=dict)
async def activate_member(member_id: str, user: dict = Depends(require_admin)):
    """Reactivar un miembro inactivo - Solo administradores"""
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        result = members_collection.update_one(
            {"_id": ObjectId(member_id)},
            {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        updated_member = members_collection.find_one({"_id": ObjectId(member_id)})
        return member_helper(updated_member)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al reactivar miembro: {str(e)}")

@app.delete("/api/members/{member_id}", status_code=204)
async def delete_member(member_id: str, user: dict = Depends(require_admin)):
    """Eliminar un miembro - Solo administradores"""
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        result = members_collection.delete_one({"_id": ObjectId(member_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar miembro: {str(e)}")

# ============ CONTACTS ENDPOINTS ============

@app.post("/api/contacts", response_model=dict, status_code=201)
async def create_contact(contact: ContactCreate, user: dict = Depends(require_admin)):
    """Crear un nuevo contacto en el directorio - Solo administradores"""
    try:
        contact_data = contact.dict()
        contact_data["created_at"] = datetime.utcnow()
        contact_data["updated_at"] = datetime.utcnow()
        
        result = contacts_collection.insert_one(contact_data)
        new_contact = contacts_collection.find_one({"_id": result.inserted_id})
        return contact_helper(new_contact)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear contacto: {str(e)}")

@app.get("/api/contacts", response_model=List[dict])
async def get_contacts(category: Optional[str] = None):
    """Obtener lista de contactos, opcionalmente filtrados por categoría"""
    try:
        query = {}
        if category:
            query["category"] = category
        
        contacts = list(contacts_collection.find(query))
        return [contact_helper(c) for c in contacts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contactos: {str(e)}")

@app.get("/api/contacts/categories", response_model=List[str])
async def get_categories():
    """Obtener lista de categorías disponibles"""
    try:
        categories = contacts_collection.distinct("category")
        return sorted(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

# ============ CITIES ENDPOINTS ============

@app.get("/api/cities", response_model=List[dict])
async def get_cities(
    include_inactive: bool = False,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Obtener lista de ciudades de Colombia
    - Admin: Puede ver todas (activas e inactivas) si include_inactive=True
    - User/No autenticado: Solo ve ciudades activas
    """
    try:
        # Si es admin y pide incluir inactivas, mostrar todas
        if current_user and is_admin(current_user) and include_inactive:
            query = {}
        else:
            # Si no es admin o no pidió inactivas, solo activas
            query = {"is_active": True}
        
        cities = list(cities_collection.find(query).sort("name", 1))
        return [city_helper(c) for c in cities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ciudades: {str(e)}")

@app.post("/api/cities", response_model=dict, status_code=201)
async def create_city(city: CityCreate, user: dict = Depends(require_admin)):
    """Crear una nueva ciudad - Solo administradores"""
    try:
        city_data = city.dict()
        city_data["created_at"] = datetime.utcnow()
        city_data["updated_at"] = datetime.utcnow()
        
        result = cities_collection.insert_one(city_data)
        new_city = cities_collection.find_one({"_id": result.inserted_id})
        return city_helper(new_city)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="La ciudad ya existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear ciudad: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)