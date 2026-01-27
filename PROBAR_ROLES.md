# 🧪 Guía para Probar el Sistema de Roles

## 📋 Endpoints de Prueba

He creado endpoints temporales para probar el sistema de roles. Úsalos para verificar que todo funciona antes de aplicarlo a los endpoints reales.

**Base URL:** `https://jetta-club-backend.onrender.com`

---

## ✅ Prueba 1: `get_current_user` (Cualquier usuario autenticado)

### En Postman:
- **Method:** `GET`
- **URL:** `https://jetta-club-backend.onrender.com/api/test/current-user`
- **Headers:**
  - `Authorization: Bearer TU_TOKEN`

### Con cURL:
```bash
curl https://jetta-club-backend.onrender.com/api/test/current-user \
  -H "Authorization: Bearer TU_TOKEN"
```

**Respuesta esperada:**
```json
{
  "message": "✅ Acceso permitido",
  "user": {
    "id": "...",
    "username": "admin",
    "role": "admin"
  }
}
```

**Prueba:**
- ✅ Con token válido → Debe funcionar
- ❌ Sin token → Error 401

---

## ✅ Prueba 2: `get_current_active_user` (Solo usuarios activos)

### En Postman:
- **Method:** `GET`
- **URL:** `https://jetta-club-backend.onrender.com/api/test/active-user`
- **Headers:**
  - `Authorization: Bearer TU_TOKEN`

### Con cURL:
```bash
curl https://jetta-club-backend.onrender.com/api/test/active-user \
  -H "Authorization: Bearer TU_TOKEN"
```

**Respuesta esperada:**
```json
{
  "message": "✅ Usuario activo",
  "user": {
    "id": "...",
    "username": "admin",
    "role": "admin",
    "is_active": true
  }
}
```

**Prueba:**
- ✅ Con usuario activo → Debe funcionar
- ❌ Con usuario inactivo → Error 403

---

## ✅ Prueba 3: `require_admin` (Solo administradores)

### En Postman:
- **Method:** `GET`
- **URL:** `https://jetta-club-backend.onrender.com/api/test/admin-only`
- **Headers:**
  - `Authorization: Bearer TOKEN_ADMIN`

### Con cURL:
```bash
curl https://jetta-club-backend.onrender.com/api/test/admin-only \
  -H "Authorization: Bearer TOKEN_ADMIN"
```

**Respuesta esperada (con admin):**
```json
{
  "message": "✅ Eres administrador",
  "user": {
    "id": "...",
    "username": "admin",
    "role": "admin"
  }
}
```

**Prueba:**
- ✅ Con token de admin → Debe funcionar
- ❌ Con token de user → Error 403 "Se requiere rol de administrador"

**Para probar con user:**
1. Crea un usuario con rol "user" en MongoDB
2. Haz login con ese usuario
3. Intenta acceder a este endpoint → Debe dar 403

---

## ✅ Prueba 4: `require_role` (Admin o User)

### En Postman:
- **Method:** `GET`
- **URL:** `https://jetta-club-backend.onrender.com/api/test/admin-or-user`
- **Headers:**
  - `Authorization: Bearer TU_TOKEN`

### Con cURL:
```bash
curl https://jetta-club-backend.onrender.com/api/test/admin-or-user \
  -H "Authorization: Bearer TU_TOKEN"
```

**Respuesta esperada:**
```json
{
  "message": "✅ Tienes un rol válido (admin o user)",
  "user": {
    "id": "...",
    "username": "admin",
    "role": "admin"
  }
}
```

**Prueba:**
- ✅ Con token de admin → Debe funcionar
- ✅ Con token de user → Debe funcionar
- ❌ Sin token → Error 401

---

## ✅ Prueba 5: Helpers de Permisos

### En Postman:
- **Method:** `GET`
- **URL:** `https://jetta-club-backend.onrender.com/api/test/permissions`
- **Headers:**
  - `Authorization: Bearer TU_TOKEN`

### Con cURL:
```bash
curl https://jetta-club-backend.onrender.com/api/test/permissions \
  -H "Authorization: Bearer TU_TOKEN"
```

**Respuesta esperada (con admin):**
```json
{
  "message": "✅ Helpers de permisos",
  "user": {
    "id": "...",
    "username": "admin",
    "role": "admin",
    "member_id": null
  },
  "permissions": {
    "is_admin": true,
    "can_edit_member_123": true,
    "can_edit_own_member": false
  }
}
```

**Prueba:**
- Verifica que `is_admin` sea `true` para admin
- Verifica que `can_edit_member_123` sea `true` para admin (puede editar cualquier miembro)

---

## 🧪 Checklist de Pruebas

### Con Usuario Admin:
- [ ] `/api/test/current-user` → ✅ Funciona
- [ ] `/api/test/active-user` → ✅ Funciona
- [ ] `/api/test/admin-only` → ✅ Funciona
- [ ] `/api/test/admin-or-user` → ✅ Funciona
- [ ] `/api/test/permissions` → ✅ `is_admin: true`

### Con Usuario Regular (user):
- [ ] `/api/test/current-user` → ✅ Funciona
- [ ] `/api/test/active-user` → ✅ Funciona
- [ ] `/api/test/admin-only` → ❌ Error 403
- [ ] `/api/test/admin-or-user` → ✅ Funciona
- [ ] `/api/test/permissions` → ✅ `is_admin: false`

### Sin Token:
- [ ] Todos los endpoints → ❌ Error 401

---

## 📝 Crear Usuario "user" para Probar

Si necesitas crear un usuario con rol "user" para probar:

1. Ve a MongoDB Atlas
2. Colección `users` → Insert Document
3. Usa este JSON (reemplaza el password_hash):

```json
{
  "username": "usuario1",
  "email": "usuario1@test.com",
  "password_hash": "$2b$12$ZrBy6QPNHY5.HWRLhYvJkO.FcjFV/sur5mrtl.LMHNghdxmnYuQAm",
  "role": "user",
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

**Nota:** El `password_hash` es para "admin123" (mismo que el admin por ahora).

Luego haz login con:
- Username: `usuario1`
- Password: `admin123`

---

## ✅ Si Todas las Pruebas Pasan

Si todos los endpoints de prueba funcionan correctamente, significa que:

1. ✅ El sistema de roles está funcionando
2. ✅ Las dependencias están correctas
3. ✅ Los helpers de permisos funcionan
4. ✅ Podemos aplicar esto a los endpoints reales

**Próximo paso:** Proteger los endpoints existentes con estas dependencias.

---

## 🗑️ Después de Probar

Una vez que verifiques que todo funciona, podemos eliminar estos endpoints de prueba y aplicar el sistema a los endpoints reales.

**¿Listo para probar?** 🚀
