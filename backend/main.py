from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from models import Member, MemberCreate, MemberUpdate, Contact, ContactCreate, City, CityCreate
from auth.routes import router as auth_router
from auth.dependencies import get_current_user, get_current_active_user, require_admin, require_role
from auth.permissions import is_admin, can_edit_member

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
    return user

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
async def create_member(member: MemberCreate):
    """Crear un nuevo miembro del club"""
    try:
        member_data = member.dict()
        member_data["created_at"] = datetime.utcnow()
        member_data["updated_at"] = datetime.utcnow()
        
        result = members_collection.insert_one(member_data)
        new_member = members_collection.find_one({"_id": result.inserted_id})
        return member_helper(new_member)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="El miembro ya existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear miembro: {str(e)}")

@app.get("/api/members", response_model=List[dict])
async def get_members(skip: int = 0, limit: int = 100):
    """Obtener lista de miembros"""
    try:
        members = list(members_collection.find().skip(skip).limit(limit))
        return [member_helper(m) for m in members]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener miembros: {str(e)}")

@app.get("/api/members/{member_id}", response_model=dict)
async def get_member(member_id: str):
    """Obtener un miembro por ID"""
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        member = members_collection.find_one({"_id": ObjectId(member_id)})
        if not member:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        return member_helper(member)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener miembro: {str(e)}")

@app.put("/api/members/{member_id}", response_model=dict)
async def update_member(member_id: str, member_update: MemberUpdate):
    """Actualizar información de un miembro"""
    try:
        if not ObjectId.is_valid(member_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        update_data = member_update.dict(exclude_unset=True)
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
async def deactivate_member(member_id: str):
    """Inactivar un miembro (soft delete) - El miembro queda con estado inactivo"""
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
async def activate_member(member_id: str):
    """Reactivar un miembro inactivo"""
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
async def delete_member(member_id: str):
    """Eliminar un miembro"""
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
async def create_contact(contact: ContactCreate):
    """Crear un nuevo contacto en el directorio"""
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
async def get_cities(include_inactive: bool = False):
    """Obtener lista de ciudades de Colombia"""
    try:
        query = {} if include_inactive else {"is_active": True}
        cities = list(cities_collection.find(query).sort("name", 1))
        return [city_helper(c) for c in cities]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ciudades: {str(e)}")

@app.post("/api/cities", response_model=dict, status_code=201)
async def create_city(city: CityCreate):
    """Crear una nueva ciudad (para administración)"""
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