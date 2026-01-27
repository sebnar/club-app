# 🧪 Probar Autenticación - Guía Rápida

## ✅ Paso 1: Verificar que el Backend está Corriendo

Reemplaza `TU_BACKEND_URL` con la URL de tu backend en Render (ej: `https://jetta-club-backend.onrender.com`)

```bash
curl https://TU_BACKEND_URL/api/health
```

**Respuesta esperada:**
```json
{"status": "healthy", "database": "connected"}
```

Si ves esto, el backend está funcionando ✅

---

## ✅ Paso 2: Verificar que el Usuario Admin Existe

**Opción A: Desde MongoDB Atlas**
1. Ve a MongoDB Atlas Dashboard
2. Browse Collections → `jetta_club` → `users`
3. Deberías ver el usuario `admin`

**Opción B: Desde la API (después de crear el usuario)**
```bash
# Esto solo funcionará si implementamos un endpoint para listar usuarios
# Por ahora, verifica manualmente en MongoDB
```

---

## ✅ Paso 3: Crear el Usuario Admin en MongoDB (Si aún no lo has hecho)

1. Ve a MongoDB Atlas
2. Browse Collections → `jetta_club`
3. Si no existe la colección `users`, créala
4. Click en **Insert Document**
5. Selecciona vista **{}** (JSON)
6. Copia y pega el contenido de `ADMIN_USER_READY.json`:

```json
{
  "username": "admin",
  "email": "admin@jetta-club.com",
  "password_hash": "$2b$12$sB.21i6giAxUeeZBIjNNdOdsU/t6.M.9vxlM3eIVqD6Q2XZSQs2Ae",
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

7. Click en **Insert**

---

## ✅ Paso 4: Probar el Login

```bash
curl -X POST https://TU_BACKEND_URL/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Respuesta esperada (éxito):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Si hay error:**
- 401: Usuario o contraseña incorrectos
- 500: Error del servidor (revisa logs en Render)

**Guarda el token:**
```bash
# En PowerShell
$TOKEN = "el_token_que_recibiste"
```

---

## ✅ Paso 5: Probar el Endpoint /api/auth/me

```bash
# En PowerShell
curl https://TU_BACKEND_URL/api/auth/me `
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada:**
```json
{
  "id": "65a1b2c3d4e5f6g7h8i9j0k1",
  "username": "admin",
  "email": "admin@jetta-club.com",
  "role": "admin",
  "member_id": null,
  "is_active": true,
  "created_at": "2026-01-26T...",
  "updated_at": "2026-01-26T...",
  "last_login": "2026-01-26T..."
}
```

Si ves esto, la autenticación funciona correctamente ✅

---

## ✅ Paso 6: Probar con Credenciales Incorrectas

```bash
curl -X POST https://TU_BACKEND_URL/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=wrong"
```

**Respuesta esperada:** Error 401
```json
{
  "detail": "Usuario o contraseña incorrectos"
}
```

---

## ✅ Paso 7: Probar con Token Inválido

```bash
curl https://TU_BACKEND_URL/api/auth/me \
  -H "Authorization: Bearer token_invalido_12345"
```

**Respuesta esperada:** Error 401
```json
{
  "detail": "No se pudo validar las credenciales"
}
```

---

## 🎯 Usando Postman o Thunder Client (VS Code)

### Login
- **Method:** POST
- **URL:** `https://TU_BACKEND_URL/api/auth/login`
- **Headers:**
  - `Content-Type: application/x-www-form-urlencoded`
- **Body (x-www-form-urlencoded):**
  - `username`: `admin`
  - `password`: `admin123`

### Obtener Usuario Actual
- **Method:** GET
- **URL:** `https://TU_BACKEND_URL/api/auth/me`
- **Headers:**
  - `Authorization: Bearer TU_TOKEN_AQUI`

---

## 🐛 Solución de Problemas

### Error: "MongoDB connection failed"
- Verifica que `MONGODB_URI` esté correcto en Render
- Verifica que la IP de Render esté en la whitelist de MongoDB Atlas
- Revisa los logs en Render Dashboard

### Error: "No se pudo validar las credenciales"
- Verifica que el usuario existe en MongoDB
- Verifica que el `password_hash` sea correcto
- Verifica que `SECRET_KEY` esté configurado en Render

### Error: "ModuleNotFoundError" en logs
- Verifica que `requirements.txt` incluya todas las dependencias
- Revisa los logs de build en Render

### El backend no responde
- Verifica que el servicio esté "Live" en Render
- Revisa los logs en tiempo real
- Verifica que el puerto sea correcto (`$PORT`)

---

## ✅ Checklist de Validación

- [ ] Backend responde en `/api/health`
- [ ] Usuario admin existe en MongoDB
- [ ] Login funciona con credenciales correctas
- [ ] Login falla con credenciales incorrectas
- [ ] Endpoint `/api/auth/me` devuelve usuario con token válido
- [ ] Endpoint `/api/auth/me` falla con token inválido
- [ ] El token contiene información correcta (username, role)

---

## 🎉 Si Todo Funciona

¡Felicidades! El sistema de autenticación básico está funcionando. 

**Próximos pasos:**
1. Cambiar la contraseña del admin por una más segura
2. Implementar sistema de roles y permisos
3. Proteger endpoints existentes
4. Implementar frontend de autenticación
