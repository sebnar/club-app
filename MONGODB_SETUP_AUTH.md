# 🗄️ Configuración de MongoDB para Autenticación

## 📋 Colecciones Necesarias

El sistema de autenticación requiere las siguientes colecciones en MongoDB:

1. **users** - Usuarios del sistema (autenticación)
2. **members** - Miembros del club (ya existente)
3. **contacts** - Directorio de contactos (ya existente)
4. **cities** - Ciudades de Colombia (ya existente)

## 🔐 Crear Usuario Administrador Manualmente

### Opción 1: Usando MongoDB Atlas Web Interface

1. Ve a [MongoDB Atlas](https://cloud.mongodb.com/)
2. Selecciona tu cluster
3. Click en **Browse Collections**
4. Selecciona la base de datos `jetta_club`
5. Si no existe la colección `users`, créala:
   - Click en **Create Collection**
   - Nombre: `users`
   - Database: `jetta_club`
6. Click en **Insert Document**
7. Selecciona **{}** (JSON view)
8. Pega el siguiente documento:

```json
{
  "username": "admin",
  "email": "admin@jetta-club.com",
  "password_hash": "TU_PASSWORD_HASH_AQUI",
  "role": "admin",
  "member_id": null,
  "is_active": true,
  "created_at": {
    "$date": "2026-01-26T00:00:00.000Z"
  },
  "updated_at": {
    "$date": "2026-01-26T00:00:00.000Z"
  },
  "last_login": null
}
```

**⚠️ IMPORTANTE:** Reemplaza `TU_PASSWORD_HASH_AQUI` con el hash generado (ver abajo).

### Opción 2: Usando MongoDB Shell (mongosh)

```javascript
use jetta_club

db.users.insertOne({
  "username": "admin",
  "email": "admin@jetta-club.com",
  "password_hash": "TU_PASSWORD_HASH_AQUI",
  "role": "admin",
  "member_id": null,
  "is_active": true,
  "created_at": new Date(),
  "updated_at": new Date(),
  "last_login": null
})
```

### Opción 3: Usando Python (Script temporal)

Crea un archivo `create_admin_mongo.py`:

```python
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "jetta_club")
PASSWORD = "admin123"  # Cambia esto por tu contraseña deseada

# Conectar
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Generar hash
password_hash = pwd_context.hash(PASSWORD)

# Crear usuario
user = {
    "username": "admin",
    "email": "admin@jetta-club.com",
    "password_hash": password_hash,
    "role": "admin",
    "member_id": None,
    "is_active": True,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
    "last_login": None
}

result = db.users.insert_one(user)
print(f"✅ Usuario creado: {result.inserted_id}")
print(f"Username: admin")
print(f"Password: {PASSWORD}")
```

Ejecuta:
```bash
python create_admin_mongo.py
```

## 🔑 Generar Password Hash

### Método 1: Python (Recomendado)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "admin123"  # Tu contraseña
hash_result = pwd_context.hash(password)
print(hash_result)
```

Ejecuta:
```bash
python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(pwd_context.hash('admin123'))"
```

### Método 2: Usando el módulo de seguridad

```python
from auth.security import get_password_hash

password = "admin123"
hash_result = get_password_hash(password)
print(hash_result)
```

## 📊 Índices Necesarios

Los índices se crean automáticamente cuando el backend inicia, pero puedes crearlos manualmente:

### Colección: users

```javascript
use jetta_club

// Índice único en username
db.users.createIndex({ "username": 1 }, { unique: true })

// Índice único en email (sparse - permite null)
db.users.createIndex({ "email": 1 }, { unique: true, sparse: true })
```

### Colección: members (ya existente)

```javascript
// Índice único en email (sparse)
db.members.createIndex({ "email": 1 }, { unique: true, sparse: true })

// Índice en join_date
db.members.createIndex({ "join_date": 1 })
```

### Colección: contacts (ya existente)

```javascript
// Índice en category
db.contacts.createIndex({ "category": 1 })
```

### Colección: cities (ya existente)

```javascript
// Índice único en name
db.cities.createIndex({ "name": 1 }, { unique: true })

// Índice en is_active
db.cities.createIndex({ "is_active": 1 })
```

## ✅ Verificar que Todo Está Correcto

### 1. Verificar que el usuario existe

```javascript
use jetta_club
db.users.find().pretty()
```

Deberías ver algo como:
```json
{
  "_id": ObjectId("..."),
  "username": "admin",
  "email": "admin@jetta-club.com",
  "role": "admin",
  "is_active": true,
  ...
}
```

### 2. Verificar índices

```javascript
use jetta_club

// Ver índices de users
db.users.getIndexes()

// Ver índices de members
db.members.getIndexes()

// Ver índices de contacts
db.contacts.getIndexes()

// Ver índices de cities
db.cities.getIndexes()
```

### 3. Probar que el username es único

```javascript
// Intentar crear otro usuario con el mismo username debería fallar
db.users.insertOne({
  "username": "admin",  // Mismo username
  "password_hash": "...",
  "role": "user"
})
// Debería dar error de clave duplicada
```

## 📝 Documento Completo de Ejemplo (Admin)

### Ejemplo Listo para Copiar (Password: "admin123")

**✅ Hash generado y listo para usar**

```json
{
  "username": "admin",
  "email": "admin@jetta-club.com",
  "password_hash": "$2b$12$ZrBy6QPNHY5.HWRLhYvJkO.FcjFV/sur5mrtl.LMHNghdxmnYuQAm",
  "role": "admin",
  "member_id": null,
  "is_active": true,
  "created_at": {
    "$date": "2026-01-26T00:00:00.000Z"
  },
  "updated_at": {
    "$date": "2026-01-26T00:00:00.000Z"
  },
  "last_login": null
}
```

**Credenciales:**
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANTE:** 
- Este hash es válido para la contraseña "admin123"
- **Cambia la contraseña después del primer login** por seguridad
- Este es solo para desarrollo/pruebas iniciales

**Para generar tu propio password_hash:**

1. **Opción A: Usando Python directamente**
   ```python
   from passlib.context import CryptContext
   pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
   print(pwd.hash('tu_contraseña_aqui'))
   ```

2. **Opción B: Usando el script**
   ```bash
   python backend/scripts/generate_hash.py
   ```

3. **Opción C: En MongoDB Atlas**
   - Usa el script `create_admin_manual.py` que está en este documento
   - O genera el hash localmente y cópialo

## 🔄 Crear Usuario Regular (user)

Para crear un usuario regular (no admin), usa el mismo formato pero cambia:

```json
{
  "username": "usuario1",
  "email": "usuario1@jetta-club.com",
  "password_hash": "TU_PASSWORD_HASH_AQUI",
  "role": "user",  // ← Cambiar a "user"
  "member_id": "OBJECT_ID_DEL_MIEMBRO",  // ← Opcional: ID del miembro asociado
  "is_active": true,
  "created_at": {
    "$date": "2026-01-26T00:00:00.000Z"
  },
  "updated_at": {
    "$date": "2026-01-26T00:00:00.000Z"
  },
  "last_login": null
}
```

**Nota:** Si el usuario está asociado a un miembro, `member_id` debe ser el `_id` (ObjectId) del documento en la colección `members`.

## 🛠️ Script Completo para Crear Admin

Crea `create_admin_manual.py`:

```python
"""
Script para crear usuario admin manualmente
Ejecutar una vez para crear el admin inicial
"""
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "jetta_club")

# Credenciales del admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # ⚠️ Cambiar después del primer login
ADMIN_EMAIL = "admin@jetta-club.com"

try:
    # Conectar
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    users_collection = db.users
    
    # Verificar conexión
    client.admin.command('ping')
    print(f"✅ Conectado a MongoDB: {DB_NAME}\n")
    
    # Verificar si ya existe
    existing = users_collection.find_one({"username": ADMIN_USERNAME})
    if existing:
        print(f"⚠️  El usuario '{ADMIN_USERNAME}' ya existe.")
        print(f"   ID: {existing['_id']}")
        return
    
    # Generar hash
    password_hash = pwd_context.hash(ADMIN_PASSWORD)
    
    # Crear usuario
    user = {
        "username": ADMIN_USERNAME,
        "email": ADMIN_EMAIL,
        "password_hash": password_hash,
        "role": "admin",
        "member_id": None,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None
    }
    
    result = users_collection.insert_one(user)
    print(f"✅ Usuario administrador creado exitosamente!")
    print(f"   ID: {result.inserted_id}")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"\n📝 Credenciales:")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print(f"\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
```

## 📋 Checklist de Configuración

Antes de probar la autenticación, verifica:

- [ ] Base de datos `jetta_club` existe en MongoDB Atlas
- [ ] Colección `users` existe (se crea automáticamente o manualmente)
- [ ] Usuario admin creado con password_hash correcto
- [ ] Índice único en `username` creado
- [ ] Índice único en `email` creado (sparse)
- [ ] Variable `MONGODB_URI` configurada en Render
- [ ] Variable `SECRET_KEY` configurada en Render
- [ ] Variable `DB_NAME` configurada en Render (o usa el default: `jetta_club`)

## 🔍 Comandos Útiles de MongoDB

```javascript
// Ver todos los usuarios
db.users.find().pretty()

// Buscar usuario específico
db.users.findOne({username: "admin"})

// Contar usuarios
db.users.countDocuments()

// Ver usuarios activos
db.users.find({is_active: true}).pretty()

// Ver solo admins
db.users.find({role: "admin"}).pretty()

// Eliminar usuario (cuidado!)
// db.users.deleteOne({username: "admin"})

// Actualizar contraseña de un usuario
// db.users.updateOne(
//   {username: "admin"},
//   {$set: {password_hash: "NUEVO_HASH_AQUI", updated_at: new Date()}}
// )
```

## 🎯 Próximos Pasos

Una vez creado el usuario admin:

1. Desplegar el backend en Render
2. Verificar que la conexión a MongoDB funciona
3. Probar el login con las credenciales del admin
4. Probar el endpoint `/api/auth/me`
5. Continuar con la implementación de roles y permisos
