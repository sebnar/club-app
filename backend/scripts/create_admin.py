"""
Script para crear el primer usuario administrador
Este script se puede ejecutar una vez en Render o localmente para crear el admin inicial

Uso en Render (via SSH o en un one-off job):
  python backend/scripts/create_admin.py

O ejecutar localmente antes del primer despliegue
"""
import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from auth.security import get_password_hash
from models import UserRole

load_dotenv()

# Configuración de MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "jetta_club")

def create_admin():
    """Crear usuario administrador inicial"""
    try:
        # Conectar a MongoDB
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        users_collection = db.users
        
        # Verificar conexión
        client.admin.command('ping')
        print(f"✅ Conectado a MongoDB: {DB_NAME}\n")
        
        # Verificar si ya existe un admin
        existing_admin = users_collection.find_one({"role": "admin"})
        if existing_admin:
            print(f"⚠️  Ya existe un usuario administrador: {existing_admin['username']}")
            print("   Si deseas crear otro, usa el endpoint de la API o modifica este script.")
            return
        
        # Valores por defecto (puedes modificar estos)
        username = os.getenv("ADMIN_USERNAME", "admin")
        password = os.getenv("ADMIN_PASSWORD", "admin123")
        email = os.getenv("ADMIN_EMAIL", None)
        
        # Verificar si el usuario ya existe
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            print(f"⚠️  El usuario '{username}' ya existe.")
            overwrite = input("¿Desea actualizar la contraseña? (s/n): ").strip().lower() if sys.stdin.isatty() else 'n'
            if overwrite == 's':
                password_hash = get_password_hash(password)
                users_collection.update_one(
                    {"username": username},
                    {
                        "$set": {
                            "password_hash": password_hash,
                            "role": UserRole.ADMIN.value,
                            "email": email,
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
                print(f"✅ Usuario '{username}' actualizado a administrador")
            return
        
        # Crear nuevo usuario admin
        password_hash = get_password_hash(password)
        user_data = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role": UserRole.ADMIN.value,
            "member_id": None,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None
        }
        
        result = users_collection.insert_one(user_data)
        print(f"\n✅ Usuario administrador creado exitosamente!")
        print(f"   ID: {result.inserted_id}")
        print(f"   Username: {username}")
        print(f"   Email: {email or 'No especificado'}")
        print(f"\n📝 IMPORTANTE: Cambia la contraseña después del primer login")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        
    except Exception as e:
        print(f"\n❌ Error al crear usuario administrador: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_admin()
