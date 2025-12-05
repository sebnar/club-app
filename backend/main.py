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
from models import Member, MemberCreate, MemberUpdate, Contact, ContactCreate

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

def connect_to_mongodb():
    """Conectar a MongoDB y crear las colecciones"""
    global client, db, members_collection, contacts_collection
    
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
        
        # Crear índices para mejorar rendimiento
        try:
            members_collection.create_index("email", unique=True, sparse=True)
            contacts_collection.create_index("category")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

