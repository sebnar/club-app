# 🗺️ Roadmap de Implementación: Autenticación y Roles

## 📌 Filosofía de Trabajo

**Principios:**
1. ✅ **Una tarea a la vez** - Completar y validar antes de continuar
2. ✅ **Tareas pequeñas** - Máximo 30-60 minutos cada una
3. ✅ **Validación inmediata** - Probar cada cambio antes de seguir
4. ✅ **Commits frecuentes** - Guardar progreso después de cada tarea
5. ✅ **Rollback fácil** - Si algo falla, volver al estado anterior

---

## 🎯 Fase 1: Fundamentos de Autenticación (Backend)

### ✅ Tarea 1.1: Instalar Dependencias
**Objetivo:** Agregar librerías necesarias para autenticación

**Acciones:**
1. Agregar a `backend/requirements.txt`:
   ```
   python-jose[cryptography]==3.3.0
   passlib[bcrypt]==1.7.4
   python-multipart==0.0.6
   ```
2. Instalar: `pip install -r requirements.txt`

**Validación:**
```bash
# Verificar que se instalaron correctamente
python -c "from jose import jwt; from passlib.context import CryptContext; print('✅ OK')"
```

**Criterio de éxito:** ✅ No hay errores de importación

---

### ✅ Tarea 1.2: Crear Modelos de Usuario
**Objetivo:** Definir estructura de datos para usuarios

**Acciones:**
1. Agregar a `backend/models.py`:
   - `UserBase`, `UserCreate`, `UserLogin`, `UserResponse`
   - Enum `UserRole` con valores `admin` y `user`

**Validación:**
```bash
# Probar que los modelos se pueden importar
python -c "from models import UserCreate, UserLogin, UserRole; print('✅ OK')"
```

**Criterio de éxito:** ✅ Modelos se importan sin errores

---

### ✅ Tarea 1.3: Crear Módulo de Seguridad
**Objetivo:** Funciones para hash de contraseñas y JWT

**Acciones:**
1. Crear `backend/auth/__init__.py` (vacío)
2. Crear `backend/auth/security.py` con:
   - `get_password_hash(password)` - Hash con bcrypt
   - `verify_password(plain, hashed)` - Verificar contraseña
   - `create_access_token(data)` - Generar JWT
   - `decode_access_token(token)` - Decodificar JWT

**Validación:**
```python
# Test manual en Python
from auth.security import get_password_hash, verify_password, create_access_token

# Test hash
hash1 = get_password_hash("test123")
assert verify_password("test123", hash1) == True
assert verify_password("wrong", hash1) == False
print("✅ Hash OK")

# Test JWT
token = create_access_token({"user_id": "123", "role": "admin"})
decoded = decode_access_token(token)
assert decoded["user_id"] == "123"
print("✅ JWT OK")
```

**Criterio de éxito:** ✅ Hash y JWT funcionan correctamente

---

### ✅ Tarea 1.4: Crear Colección de Usuarios en MongoDB
**Objetivo:** Preparar base de datos para usuarios

**Acciones:**
1. En `backend/main.py`, agregar:
   - `users_collection = db.users` en `connect_to_mongodb()`
   - Índice único en `username`
   - Índice único en `email` (sparse)

**Validación:**
```bash
# Iniciar backend y verificar conexión
python backend/main.py
# En otra terminal:
curl http://localhost:8000/api/health
# Debe responder {"status": "healthy", "database": "connected"}
```

**Criterio de éxito:** ✅ Backend inicia sin errores, MongoDB conectado

---

### ✅ Tarea 1.5: Crear Endpoint de Login (Sin Protección)
**Objetivo:** Endpoint básico que valida credenciales y devuelve token

**Acciones:**
1. Crear `backend/auth/routes.py` con:
   - `POST /api/auth/login` - Recibe username/password, devuelve token
2. Registrar router en `main.py`

**Validación:**
```bash
# 1. Crear usuario manualmente en MongoDB (temporal)
# 2. Probar login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "test123"}'
# Debe devolver: {"access_token": "...", "token_type": "bearer"}
```

**Criterio de éxito:** ✅ Login funciona y devuelve token válido

---

### ✅ Tarea 1.6: Crear Endpoint GET /api/auth/me
**Objetivo:** Endpoint que devuelve usuario actual (requiere token)

**Acciones:**
1. Crear función `get_current_user()` básica (sin validar rol aún)
2. Agregar `GET /api/auth/me` que usa `get_current_user()`

**Validación:**
```bash
# 1. Obtener token del login anterior
TOKEN="tu_token_aqui"

# 2. Probar /api/auth/me
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
# Debe devolver información del usuario (sin password)
```

**Criterio de éxito:** ✅ Endpoint devuelve usuario correcto con token válido

---

## 🎯 Fase 2: Sistema de Roles y Permisos (Backend)

### ✅ Tarea 2.1: Crear Dependencias de Autenticación
**Objetivo:** Funciones reutilizables para validar usuarios

**Acciones:**
1. Crear `backend/auth/dependencies.py` con:
   - `get_current_user()` - Obtiene usuario del token
   - `get_current_active_user()` - Solo usuarios activos

**Validación:**
```python
# Test manual: Intentar usar en un endpoint
# Debe funcionar correctamente
```

**Criterio de éxito:** ✅ Dependencias se pueden usar en endpoints

---

### ✅ Tarea 2.2: Agregar Sistema de Roles
**Objetivo:** Validar roles en dependencias

**Acciones:**
1. Agregar a `auth/dependencies.py`:
   - `require_role(roles: List[str])` - Valida que usuario tenga uno de los roles
   - `require_admin()` - Atajo para requerir rol admin

**Validación:**
```bash
# Crear 2 usuarios: uno admin, uno user
# Probar endpoint protegido con admin -> ✅ OK
# Probar endpoint protegido con user -> ❌ 403
```

**Criterio de éxito:** ✅ Roles se validan correctamente

---

### ✅ Tarea 2.3: Crear Script de Usuario Admin Inicial
**Objetivo:** Poder crear primer usuario admin fácilmente

**Acciones:**
1. Crear `backend/scripts/create_admin.py`:
   - Script que crea usuario admin desde línea de comandos
   - Pide username, password, email

**Validación:**
```bash
python backend/scripts/create_admin.py
# Crear usuario admin
# Verificar en MongoDB que se creó correctamente
# Probar login con ese usuario
```

**Criterio de éxito:** ✅ Se puede crear admin y hacer login

---

## 🎯 Fase 3: Proteger Endpoints Existentes (Backend)

### ✅ Tarea 3.1: Crear Modelo MemberPublic
**Objetivo:** Modelo para vista limitada de miembros

**Acciones:**
1. Agregar a `backend/models.py`:
   - `MemberPublic` - Solo campos públicos
   - Función helper `filter_member_public(member)` - Filtra campos sensibles

**Validación:**
```python
# Test manual
from models import MemberPublic, filter_member_public

member = {
    "name": "Juan",
    "email": "juan@test.com",  # Sensible
    "phone": "123456",  # Sensible
    "description": "Mi descripción"
}

public = filter_member_public(member)
assert "email" not in public
assert "phone" not in public
assert "name" in public
print("✅ Filtrado OK")
```

**Criterio de éxito:** ✅ Campos sensibles se filtran correctamente

---

### ✅ Tarea 3.2: Modificar GET /api/members
**Objetivo:** Filtrar datos según rol del usuario

**Acciones:**
1. Modificar `GET /api/members`:
   - Si no hay auth: devolver lista pública (solo activos)
   - Si es admin: devolver lista completa
   - Si es user: devolver lista pública

**Validación:**
```bash
# Sin token
curl http://localhost:8000/api/members
# Debe devolver lista pública (sin email, phone, etc.)

# Con token admin
curl http://localhost:8000/api/members \
  -H "Authorization: Bearer $ADMIN_TOKEN"
# Debe devolver lista completa

# Con token user
curl http://localhost:8000/api/members \
  -H "Authorization: Bearer $USER_TOKEN"
# Debe devolver lista pública
```

**Criterio de éxito:** ✅ Datos se filtran según rol correctamente

---

### ✅ Tarea 3.3: Modificar GET /api/members/{id}
**Objetivo:** Mostrar perfil completo solo si es admin o el propio perfil

**Acciones:**
1. Modificar `GET /api/members/{id}`:
   - Si es admin: perfil completo
   - Si es user y es su propio perfil: completo
   - Si es user y es otro: solo público
   - Si no hay auth: solo público

**Validación:**
```bash
# User viendo su propio perfil
curl http://localhost:8000/api/members/$USER_MEMBER_ID \
  -H "Authorization: Bearer $USER_TOKEN"
# Debe mostrar email, phone, etc.

# User viendo otro perfil
curl http://localhost:8000/api/members/$OTHER_MEMBER_ID \
  -H "Authorization: Bearer $USER_TOKEN"
# NO debe mostrar email, phone
```

**Criterio de éxito:** ✅ Permisos de visualización funcionan correctamente

---

### ✅ Tarea 3.4: Proteger POST /api/members
**Objetivo:** Solo admin puede crear miembros

**Acciones:**
1. Agregar `require_admin()` a `POST /api/members`

**Validación:**
```bash
# Admin creando miembro
curl -X POST http://localhost:8000/api/members \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Nuevo Miembro"}'
# Debe funcionar ✅

# User intentando crear
curl -X POST http://localhost:8000/api/members \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Nuevo Miembro"}'
# Debe devolver 403 ❌
```

**Criterio de éxito:** ✅ Solo admin puede crear miembros

---

### ✅ Tarea 3.5: Proteger PUT /api/members/{id}
**Objetivo:** Admin puede editar cualquiera, user solo su perfil

**Acciones:**
1. Modificar `PUT /api/members/{id}`:
   - Verificar si es admin O si es su propio perfil
   - Si es user editando otro: 403

**Validación:**
```bash
# User editando su perfil
curl -X PUT http://localhost:8000/api/members/$USER_MEMBER_ID \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"name": "Nuevo Nombre"}'
# Debe funcionar ✅

# User editando otro perfil
curl -X PUT http://localhost:8000/api/members/$OTHER_MEMBER_ID \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"name": "Nuevo Nombre"}'
# Debe devolver 403 ❌
```

**Criterio de éxito:** ✅ Permisos de edición funcionan correctamente

---

### ✅ Tarea 3.6: Proteger DELETE y Activate/Deactivate
**Objetivo:** Solo admin puede eliminar y activar/desactivar

**Acciones:**
1. Agregar `require_admin()` a:
   - `DELETE /api/members/{id}`
   - `PATCH /api/members/{id}/activate`
   - `PATCH /api/members/{id}/deactivate`

**Validación:**
```bash
# Admin puede eliminar ✅
# User no puede eliminar ❌
# Admin puede activar/desactivar ✅
# User no puede activar/desactivar ❌
```

**Criterio de éxito:** ✅ Solo admin tiene permisos administrativos

---

### ✅ Tarea 3.7: Proteger Endpoints de Contactos
**Objetivo:** Solo admin puede crear/editar contactos

**Acciones:**
1. `GET /api/contacts` - Público (todos pueden ver)
2. `POST /api/contacts` - Solo admin

**Validación:**
```bash
# Verificar que user puede ver contactos pero no crear
```

**Criterio de éxito:** ✅ Permisos de contactos funcionan

---

### ✅ Tarea 3.8: Proteger Endpoints de Ciudades
**Objetivo:** Solo admin puede crear ciudades

**Acciones:**
1. `GET /api/cities` - Público (solo activas si no es admin)
2. `POST /api/cities` - Solo admin

**Validación:**
```bash
# Verificar permisos
```

**Criterio de éxito:** ✅ Permisos de ciudades funcionan

---

## 🎯 Fase 4: Frontend - Autenticación Básica

### ✅ Tarea 4.1: Crear AuthContext
**Objetivo:** Contexto React para manejar estado de autenticación

**Acciones:**
1. Crear `frontend/src/contexts/AuthContext.jsx`:
   - Estado: `user`, `token`, `loading`
   - Funciones: `login()`, `logout()`, `isAuthenticated()`, `isAdmin()`

**Validación:**
```javascript
// En consola del navegador
// Verificar que el contexto se puede usar
```

**Criterio de éxito:** ✅ Contexto se crea sin errores

---

### ✅ Tarea 4.2: Configurar Interceptor de Axios
**Objetivo:** Agregar token automáticamente a requests

**Acciones:**
1. Modificar `frontend/src/services/api.js`:
   - Interceptor que agrega `Authorization: Bearer <token>`
   - Manejar errores 401 (token inválido) -> logout

**Validación:**
```javascript
// Hacer request y verificar en Network tab que header se agrega
```

**Criterio de éxito:** ✅ Token se agrega automáticamente a requests

---

### ✅ Tarea 4.3: Crear Página de Login
**Objetivo:** Formulario básico de login

**Acciones:**
1. Crear `frontend/src/pages/Login.jsx`:
   - Formulario: username, password
   - Llamar a `/api/auth/login`
   - Guardar token en localStorage
   - Redirigir a home

**Validación:**
```bash
# 1. Ir a /login
# 2. Ingresar credenciales
# 3. Verificar que redirige a home
# 4. Verificar que token se guarda en localStorage
```

**Criterio de éxito:** ✅ Login funciona y redirige correctamente

---

### ✅ Tarea 4.4: Crear Componente ProtectedRoute
**Objetivo:** Proteger rutas que requieren autenticación

**Acciones:**
1. Crear `frontend/src/components/ProtectedRoute.jsx`:
   - Verifica si hay token
   - Si no hay: redirige a `/login`
   - Si hay: renderiza children

**Validación:**
```bash
# 1. Sin login, intentar acceder a /members
# 2. Debe redirigir a /login
# 3. Después de login, debe permitir acceso
```

**Criterio de éxito:** ✅ Rutas protegidas funcionan correctamente

---

### ✅ Tarea 4.5: Integrar AuthContext en App
**Objetivo:** Usar contexto en toda la aplicación

**Acciones:**
1. Envolver App con `AuthProvider`
2. Agregar rutas protegidas
3. Agregar botón de logout en Navbar

**Validación:**
```bash
# Verificar que toda la app tiene acceso al contexto
```

**Criterio de éxito:** ✅ Contexto disponible en toda la app

---

## 🎯 Fase 5: Frontend - UI con Permisos

### ✅ Tarea 5.1: Ocultar Botones Según Rol
**Objetivo:** Mostrar/ocultar acciones según permisos

**Acciones:**
1. En `Members.jsx`: Ocultar botón "Crear" si no es admin
2. En `MemberProfile.jsx`: Ocultar "Editar" si no es admin ni propietario
3. En `MemberProfile.jsx`: Ocultar "Eliminar" si no es admin

**Validación:**
```bash
# Login como user -> Verificar que botones se ocultan
# Login como admin -> Verificar que botones se muestran
```

**Criterio de éxito:** ✅ UI se adapta según rol

---

### ✅ Tarea 5.2: Crear Vista Pública de Perfiles
**Objetivo:** Mostrar datos limitados para usuarios no-admin

**Acciones:**
1. Modificar `MemberProfile.jsx`:
   - Si es admin o propio perfil: mostrar todo
   - Si es otro perfil: mostrar solo campos públicos

**Validación:**
```bash
# User viendo su perfil -> Todo visible
# User viendo otro perfil -> Solo público
# Admin viendo cualquier perfil -> Todo visible
```

**Criterio de éxito:** ✅ Datos se filtran correctamente en frontend

---

### ✅ Tarea 5.3: Manejar Errores 403/401
**Objetivo:** Mostrar mensajes apropiados cuando no hay permisos

**Acciones:**
1. Agregar manejo de errores en:
   - Interceptor de axios (401 -> logout)
   - Componentes (403 -> mensaje de permiso denegado)

**Validación:**
```bash
# Intentar acción sin permisos -> Ver mensaje apropiado
```

**Criterio de éxito:** ✅ Errores se manejan correctamente

---

## 📋 Checklist de Validación Final

Antes de considerar completada la implementación:

- [ ] ✅ Backend inicia sin errores
- [ ] ✅ Se puede crear usuario admin
- [ ] ✅ Login funciona (admin y user)
- [ ] ✅ Token se valida correctamente
- [ ] ✅ Admin puede hacer CRUD completo
- [ ] ✅ User puede ver su perfil completo
- [ ] ✅ User puede editar su perfil
- [ ] ✅ User ve datos limitados de otros miembros
- [ ] ✅ User NO puede editar otros miembros
- [ ] ✅ User NO puede eliminar miembros
- [ ] ✅ Frontend muestra/oculta botones según rol
- [ ] ✅ Rutas protegidas redirigen a login
- [ ] ✅ Logout funciona correctamente
- [ ] ✅ Errores 401/403 se manejan apropiadamente

---

## 🚨 Reglas de Trabajo

1. **Una tarea a la vez** - No pasar a la siguiente hasta validar la actual
2. **Commit después de cada tarea** - Guardar progreso frecuentemente
3. **Probar manualmente** - Cada tarea debe tener validación antes de continuar
4. **Si algo falla** - Detenerse, revisar, corregir, validar de nuevo
5. **Documentar problemas** - Si encuentras algo inesperado, anotarlo

---

## 📝 Notas

- Cada tarea está diseñada para ser independiente
- Si una tarea falla, las anteriores siguen funcionando
- Las validaciones son manuales por ahora (podemos agregar tests después)
- Este roadmap puede ajustarse según necesidades

**¿Empezamos con la Tarea 1.1?** 🚀
