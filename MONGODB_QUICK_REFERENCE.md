# 🚀 Referencia Rápida: Crear Admin en MongoDB

## 📋 Documento JSON Listo para MongoDB Atlas

Copia y pega esto directamente en MongoDB Atlas (Insert Document → JSON view):

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

**Credenciales de prueba:**
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANTE:** Este hash es válido para la contraseña "admin123". Después del primer login, cambia la contraseña por seguridad.

**⚠️ IMPORTANTE:** 
- Este hash es para la contraseña "admin123"
- Cambia la contraseña después del primer login
- Para generar tu propio hash, usa: `python backend/scripts/generate_hash.py`

## 📍 Pasos en MongoDB Atlas

1. Ve a tu cluster en MongoDB Atlas
2. Click en **Browse Collections**
3. Selecciona base de datos: `jetta_club`
4. Si no existe, crea la colección: `users`
5. Click en **Insert Document**
6. Selecciona vista **{}** (JSON)
7. Pega el documento JSON de arriba
8. Click en **Insert**

## ✅ Verificar

```javascript
use jetta_club
db.users.findOne({username: "admin"})
```

Deberías ver el documento creado.

## 🔑 Generar Hash para Otra Contraseña

Si quieres usar otra contraseña:

```python
# Ejecuta esto en Python
from passlib.context import CryptContext
pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
print(pwd.hash('tu_contraseña'))
```

O usa el script:
```bash
python backend/scripts/generate_hash.py
```

## 📊 Índices (Se crean automáticamente, pero puedes crearlos manualmente)

```javascript
use jetta_club

// Índice único en username
db.users.createIndex({ "username": 1 }, { unique: true })

// Índice único en email (sparse - permite null)
db.users.createIndex({ "email": 1 }, { unique: true, sparse: true })
```

## 🎯 Siguiente Paso

Una vez creado el usuario:
1. Despliega el backend en Render
2. Prueba el login: `POST /api/auth/login`
3. Prueba el endpoint: `GET /api/auth/me`
