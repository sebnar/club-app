"""
Script para probar la conexión a MongoDB
Ejecuta este script para verificar que tu configuración es correcta
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError

# Cargar variables de entorno desde el directorio del script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "jetta_club")

def test_connection():
    print("🔍 Probando conexión a MongoDB...")
    print(f"📍 URI: {MONGODB_URI[:50]}..." if MONGODB_URI and len(MONGODB_URI) > 50 else f"📍 URI: {MONGODB_URI}")
    print(f"📦 Base de datos: {DB_NAME}")
    print("-" * 50)
    
    if not MONGODB_URI:
        print("❌ ERROR: MONGODB_URI no está configurado")
        print("\n💡 Solución:")
        print("   1. Crea un archivo .env en la carpeta backend/")
        print("   2. Agrega: MONGODB_URI=tu_connection_string")
        return False
    
    try:
        print("⏳ Conectando...")
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Probar conexión
        client.admin.command('ping')
        print("✅ Conexión exitosa!")
        
        # Listar bases de datos
        db_list = client.list_database_names()
        print(f"📚 Bases de datos disponibles: {', '.join(db_list)}")
        
        # Verificar/crear base de datos
        db = client[DB_NAME]
        collections = db.list_collection_names()
        print(f"📁 Colecciones en '{DB_NAME}': {', '.join(collections) if collections else 'Ninguna (se crearán automáticamente)'}")
        
        # Probar escritura
        test_collection = db.test_connection
        test_collection.insert_one({"test": True, "timestamp": "now"})
        test_collection.delete_one({"test": True})
        print("✅ Prueba de escritura exitosa")
        
        print("\n🎉 ¡Todo está configurado correctamente!")
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ ERROR: No se pudo conectar al servidor")
        print("\n💡 Posibles causas:")
        print("   1. Tu IP no está en la whitelist de MongoDB Atlas")
        print("   2. La URI es incorrecta")
        print("   3. Problemas de red")
        return False
        
    except ConfigurationError as e:
        print(f"❌ ERROR: Configuración inválida - {e}")
        print("\n💡 Verifica que la URI tenga el formato correcto:")
        print("   mongodb+srv://usuario:password@cluster.mongodb.net/")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__} - {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if not success:
        print("\n📖 Consulta MONGODB_SETUP.md para más ayuda")
        exit(1)

