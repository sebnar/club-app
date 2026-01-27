# 🧪 Guía de Pruebas en Render: Sistema de Autenticación

## 🚀 Despliegue en Render

### 1. Verificar que estás en la rama correcta

```bash
git status
# Asegúrate de estar en tu rama de desarrollo (no main)
```

### 2. Hacer commit y push de los cambios

```bash
git add .
git commit -m "feat: implementar sistema de autenticación básico"
git push origin tu-rama
```

### 3. Render detectará los cambios automáticamente

- Si tienes auto-deploy activado, Render iniciará el despliegue
- Si no, puedes iniciarlo manualmente desde el dashboard

### 4. Verificar variables de entorno en Render

Asegúrate de tener configuradas:
- `MONGODB_URI` - Connection string de MongoDB Atlas
- `DB_NAME` - `jetta_club`
- `SECRET_KEY` - Una clave secreta para JWT (genera una aleatoria)

**Para generar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 👤 Crear Usuario Administrador Inicial

### Opción 1: Usando Script (Recomendado)

Una vez desplegado, puedes ejecutar el script via SSH en Render:

1. En el dashboard de Render, ve a tu servicio
2. Abre la consola/terminal
3. Ejecuta:

```bash
cd /opt/render/project/src  # Ajusta según tu estructura
python backend/scripts/create_admin.py
```

O configura variables de entorno en Render:
- `ADMIN_USERNAME` - Username del admin (default: "admin")
- `ADMIN_PASSWORD` - Password del admin (default: "admin123")
- `ADMIN_EMAIL` - Email del admin (opcional)

Y ejecuta el script (usará las variables de entorno).

### Opción 2: Crear manualmente en MongoDB

1. Conecta a MongoDB Atlas
2. Ve a la colección `users` en la base de datos `jetta_club`
3. Inserta un documento:

```json
{
  "username": "admin",
  "email": "admin@test.com",
  "password_hash": "<hash_generado>",
  "role": "admin",
  "member_id": null,
  "is_active": true,
  "created_at": ISODate(),
  "updated_at": ISODate(),
  "last_login": null
}
```

**Para generar el password_hash:**
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("tu_password_aqui"))
```

## 🧪 Probar los Endpoints

### 1. Verificar que el backend está corriendo

```bash
curl https://tu-backend.onrender.com/api/health
```

Debería responder:
```json
{"status": "healthy", "database": "connected"}
```

### 2. Probar el Login

```bash
curl -X POST https://tu-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Guardar el token:**
```bash
TOKEN="tu_token_aqui"
```

### 3. Probar el Endpoint /api/auth/me

```bash
curl https://tu-backend.onrender.com/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada:**
```json
{
  "id": "...",
  "username": "admin",
  "email": "admin@test.com",
  "role": "admin",
  "member_id": null,
  "is_active": true,
  "created_at": "2026-01-26T...",
  "updated_at": "2026-01-26T...",
  "last_login": "2026-01-26T..."
}
```

### 4. Probar con Credenciales Incorrectas

```bash
curl -X POST https://tu-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=wrong"
```

**Respuesta esperada:** Error 401

### 5. Probar con Token Inválido

```bash
curl https://tu-backend.onrender.com/api/auth/me \
  -H "Authorization: Bearer token_invalido"
```

**Respuesta esperada:** Error 401

## ✅ Checklist de Validación

- [ ] Backend desplegado en Render sin errores
- [ ] Health check responde correctamente
- [ ] Usuario administrador creado
- [ ] Login funciona con credenciales correctas
- [ ] Login falla con credenciales incorrectas
- [ ] Endpoint /api/auth/me devuelve usuario con token válido
- [ ] Endpoint /api/auth/me falla con token inválido
- [ ] El token contiene la información correcta (user_id, username, role)

## 🔍 Verificar en MongoDB Atlas

1. Ve a MongoDB Atlas Dashboard
2. Navega a tu cluster → Browse Collections
3. Selecciona la base de datos `jetta_club`
4. Ve a la colección `users`
5. Verifica que el usuario se creó correctamente

## 🐛 Solución de Problemas

### Error: "MongoDB connection failed"
- Verifica que `MONGODB_URI` esté correctamente configurado en Render
- Verifica que la IP de Render esté en la whitelist de MongoDB Atlas
- Verifica que las credenciales sean correctas

### Error: "No se pudo validar las credenciales"
- Verifica que el usuario existe en MongoDB
- Verifica que la contraseña sea correcta
- Verifica que `SECRET_KEY` esté configurado en Render

### Error: "ModuleNotFoundError" en Render
- Verifica que `requirements.txt` incluya todas las dependencias
- Revisa los logs de build en Render

### El backend no inicia
- Revisa los logs en Render Dashboard
- Verifica que el comando de inicio sea correcto
- Verifica que el puerto sea `$PORT` (Render lo asigna automáticamente)

## 📝 Notas Importantes

- **SECRET_KEY**: Debe ser una cadena aleatoria y segura. Nunca la compartas.
- **Primer usuario**: El script `create_admin.py` solo crea el primer admin. Para más usuarios, usa la API (cuando implementemos el endpoint protegido).
- **Contraseñas**: Siempre se almacenan hasheadas. Nunca en texto plano.
- **Tokens JWT**: Expiran después de 24 horas por defecto.

## 🎯 Próximos Pasos

Una vez que las pruebas básicas funcionen:
1. Implementar sistema de roles y permisos
2. Proteger endpoints existentes
3. Crear endpoint para crear usuarios (solo admin)
4. Implementar frontend de autenticación
