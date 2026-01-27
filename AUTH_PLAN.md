# 🔐 Plan de Implementación: Sistema de Autenticación y Roles

## 📋 Resumen Ejecutivo

Implementar un sistema de autenticación con roles para el Club Volkswagen Jetta Colombia, permitiendo:
- **Administrador**: Acceso completo CRUD a todos los recursos
- **Usuario**: Acceso limitado a su propio perfil y vista pública de otros miembros
- **Arquitectura extensible**: Preparada para agregar más roles en el futuro

---

## 🎯 Roles y Permisos

### 1. **ADMINISTRADOR** (`admin`)
**Permisos completos:**
- ✅ CRUD completo de miembros (crear, leer, actualizar, eliminar, activar/desactivar)
- ✅ CRUD completo de contactos
- ✅ CRUD completo de ciudades
- ✅ Ver toda la información de todos los miembros (sin restricciones)
- ✅ Gestionar roles de usuarios (futuro)
- ✅ Acceso a estadísticas y reportes (futuro)

### 2. **USUARIO** (`user`)
**Permisos limitados:**

**Sobre su propio perfil:**
- ✅ Ver su perfil completo (todos los campos)
- ✅ Editar su propio perfil (excepto `is_active` y `join_date` - solo admin)
- ❌ No puede eliminarse a sí mismo

**Sobre otros miembros:**
- ✅ Ver lista de miembros activos
- ✅ Ver perfil público de otros miembros (campos limitados):
  - ✅ Nombre completo
  - ✅ Apodo/nickname
  - ✅ Descripción
  - ✅ Cumpleaños
  - ✅ Longevidad en el club (calculada desde `join_date`)
  - ✅ Información del vehículo (año, modelo, color)
  - ❌ **NO** email
  - ❌ **NO** teléfono
  - ❌ **NO** ciudad
  - ❌ **NO** `is_active`
  - ❌ **NO** `created_at` / `updated_at`
- ❌ No puede editar otros miembros
- ❌ No puede eliminar otros miembros
- ❌ No puede activar/desactivar otros miembros

**Sobre otros recursos:**
- ✅ Ver directorio de contactos (solo lectura)
- ✅ Ver categorías de contactos
- ✅ Ver ciudades activas
- ❌ No puede crear/editar/eliminar contactos
- ❌ No puede crear/editar/eliminar ciudades

---

## 🏗️ Arquitectura Propuesta

### 1. **Modelo de Usuario (User Model)**

**Nueva colección en MongoDB: `users`**

```python
User {
    _id: ObjectId
    username: str (único, para login)
    email: str (único, opcional)
    password_hash: str (bcrypt)
    role: str (enum: "admin", "user") # Extensible a más roles
    member_id: ObjectId (referencia a members collection, opcional)
    is_active: bool
    last_login: datetime (opcional)
    created_at: datetime
    updated_at: datetime
}
```

**Relación con Members:**
- Un `User` puede estar vinculado a un `Member` mediante `member_id`
- Esto permite que el usuario vea/edite su propio perfil de miembro
- El admin puede no tener `member_id` (es solo administrador)
- Un usuario regular debe tener `member_id` para acceder a su perfil

### 2. **Sistema de Autenticación**

**Tecnología:** JWT (JSON Web Tokens)

**Flujo:**
1. Usuario hace login con `username` y `password`
2. Backend valida credenciales
3. Backend genera JWT con payload:
   ```json
   {
     "user_id": "string",
     "username": "string",
     "role": "admin" | "user",
     "member_id": "string" | null,
     "exp": timestamp
   }
   ```
4. Frontend almacena token (localStorage o httpOnly cookie)
5. Frontend envía token en header: `Authorization: Bearer <token>`
6. Backend valida token en cada request protegido

**Endpoints de Autenticación:**
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión (opcional, más que nada frontend)
- `GET /api/auth/me` - Obtener usuario actual
- `POST /api/auth/refresh` - Renovar token (futuro)

### 3. **Sistema de Autorización**

**Middleware/Dependencies en FastAPI:**

```python
# Dependencias propuestas:
- get_current_user() -> User
- get_current_active_user() -> User (solo usuarios activos)
- require_role(roles: List[str]) -> User
- require_admin() -> User
- require_owner_or_admin(member_id: str) -> User
```

**Estrategia:**
- Usar `Depends()` de FastAPI para inyectar validaciones
- Decoradores personalizados para verificar permisos
- Funciones helper para filtrar datos según rol

### 4. **Modelos Pydantic**

**Nuevos modelos necesarios:**

```python
# Auth Models
- UserBase
- UserCreate (con password)
- UserLogin (username, password)
- UserResponse (sin password_hash)
- Token (access_token, token_type)
- TokenData (para decodificar JWT)

# Member Models (modificar)
- MemberPublic (vista limitada para usuarios)
- MemberPrivate (vista completa para admin/propietario)
```

### 5. **Modificaciones a Endpoints Existentes**

**Endpoints de Miembros:**

| Endpoint | Admin | Usuario (propio) | Usuario (otros) |
|----------|-------|------------------|-----------------|
| `GET /api/members` | ✅ Lista completa | ✅ Lista pública | ✅ Lista pública |
| `GET /api/members/{id}` | ✅ Completo | ✅ Completo | ✅ Solo público |
| `POST /api/members` | ✅ Permitido | ❌ Denegado | ❌ Denegado |
| `PUT /api/members/{id}` | ✅ Permitido | ✅ Solo propio | ❌ Denegado |
| `PATCH /api/members/{id}/activate` | ✅ Permitido | ❌ Denegado | ❌ Denegado |
| `PATCH /api/members/{id}/deactivate` | ✅ Permitido | ❌ Denegado | ❌ Denegado |
| `DELETE /api/members/{id}` | ✅ Permitido | ❌ Denegado | ❌ Denegado |

**Endpoints de Contactos:**

| Endpoint | Admin | Usuario |
|----------|-------|---------|
| `GET /api/contacts` | ✅ Completo | ✅ Solo lectura |
| `GET /api/contacts/categories` | ✅ Permitido | ✅ Permitido |
| `POST /api/contacts` | ✅ Permitido | ❌ Denegado |

**Endpoints de Ciudades:**

| Endpoint | Admin | Usuario |
|----------|-------|---------|
| `GET /api/cities` | ✅ Completo | ✅ Solo activas |
| `POST /api/cities` | ✅ Permitido | ❌ Denegado |

### 6. **Vista Pública de Miembros**

**Campos visibles para usuarios no-admin:**
```python
MemberPublic {
    id: str
    name: str
    nickname: Optional[str]
    description: Optional[str]
    birthday: Optional[str]
    join_date: Optional[str]  # Para calcular longevidad
    car_year: Optional[int]
    car_model: Optional[str]
    car_color: Optional[str]
    # Campos calculados:
    membership_years: int  # Calculado desde join_date
}
```

**Campos ocultos:**
- ❌ email
- ❌ phone
- ❌ city
- ❌ is_active
- ❌ created_at
- ❌ updated_at

---

## 📁 Estructura de Archivos Propuesta

```
backend/
├── main.py                 # Endpoints principales (modificar)
├── models.py              # Modelos existentes + nuevos modelos de auth
├── auth/
│   ├── __init__.py
│   ├── dependencies.py    # get_current_user, require_role, etc.
│   ├── security.py        # JWT, password hashing (bcrypt)
│   └── routes.py          # Endpoints de autenticación
├── utils/
│   └── permissions.py    # Helpers para verificar permisos
└── requirements.txt       # Agregar: python-jose[cryptography], passlib[bcrypt], python-multipart
```

---

## 🔧 Dependencias Nuevas

```txt
python-jose[cryptography]  # Para JWT
passlib[bcrypt]            # Para hash de contraseñas
python-multipart           # Para form data en login
```

---

## 🎨 Consideraciones de Frontend

### 1. **Contexto de Autenticación**
- Crear `AuthContext` para manejar estado de usuario
- Almacenar token en localStorage
- Interceptor de axios para agregar token a requests

### 2. **Rutas Protegidas**
- Componente `ProtectedRoute` que verifica autenticación
- Componente `AdminRoute` que verifica rol admin
- Redirección a `/login` si no autenticado

### 3. **Vistas Diferentes**
- Vista de perfil propio vs. perfil de otros
- Botones de editar/eliminar solo visibles según permisos
- Formularios con campos deshabilitados según rol

### 4. **Página de Login**
- Formulario simple: username/password
- Manejo de errores
- Redirección después de login exitoso

---

## 🔄 Flujo de Usuario Típico

### Usuario Regular:
1. Visita la app → Redirigido a `/login`
2. Ingresa credenciales → Obtiene token
3. Ve lista de miembros → Solo información pública
4. Hace clic en su perfil → Ve información completa
5. Edita su perfil → Solo puede editar campos permitidos
6. Intenta editar otro miembro → Recibe error 403

### Administrador:
1. Visita la app → Redirigido a `/login`
2. Ingresa credenciales → Obtiene token
3. Ve lista de miembros → Información completa
4. Puede crear/editar/eliminar cualquier miembro
5. Tiene acceso a todas las funciones administrativas

---

## 🚀 Fases de Implementación

### **Fase 1: Backend - Autenticación Base**
1. Instalar dependencias
2. Crear modelos de User y Auth
3. Implementar hash de contraseñas
4. Implementar JWT
5. Crear endpoints de login/logout/me
6. Crear middleware de autenticación

### **Fase 2: Backend - Sistema de Roles**
1. Agregar campo `role` a User
2. Crear dependencias de autorización
3. Implementar helpers de permisos
4. Crear modelo MemberPublic

### **Fase 3: Backend - Proteger Endpoints**
1. Modificar endpoints de miembros con permisos
2. Modificar endpoints de contactos
3. Modificar endpoints de ciudades
4. Agregar filtrado de datos según rol

### **Fase 4: Frontend - Autenticación**
1. Crear AuthContext
2. Crear página de Login
3. Configurar interceptor de axios
4. Implementar rutas protegidas

### **Fase 5: Frontend - UI con Permisos**
1. Mostrar/ocultar botones según rol
2. Crear vista pública vs. privada de perfiles
3. Manejar errores 403/401
4. Agregar logout

### **Fase 6: Testing y Refinamiento**
1. Probar todos los flujos
2. Validar seguridad
3. Ajustar permisos si es necesario
4. Documentar cambios

---

## 🔒 Consideraciones de Seguridad

1. **Contraseñas:**
   - Hash con bcrypt (salt rounds: 12)
   - Nunca devolver password_hash en respuestas
   - Validar fortaleza de contraseña (futuro)

2. **JWT:**
   - Expiración: 24 horas (configurable)
   - Secret key en variables de entorno
   - Validar firma en cada request

3. **Validaciones:**
   - Verificar que usuario esté activo
   - Verificar que token no esté expirado
   - Validar ObjectId antes de queries

4. **Rate Limiting:**
   - Limitar intentos de login (futuro)
   - Proteger endpoints sensibles (futuro)

---

## 📝 Notas Adicionales

1. **Migración de Datos:**
   - Los miembros existentes no tienen usuarios asociados
   - Necesitaremos crear usuarios para miembros existentes o permitir registro
   - Considerar script de migración

2. **Registro de Usuarios:**
   - Inicialmente, solo admin puede crear usuarios
   - Futuro: permitir auto-registro con aprobación

3. **Extensibilidad:**
   - El sistema de roles está diseñado para agregar más roles fácilmente
   - Ejemplos futuros: "moderator", "vip_member", etc.
   - Usar enum o lista configurable de roles

4. **Backward Compatibility:**
   - Algunos endpoints pueden necesitar funcionar sin auth (públicos)
   - Considerar modo "público" para ciertas vistas

---

## ✅ Checklist de Implementación

- [ ] Crear modelos de User y Auth
- [ ] Implementar hash de contraseñas
- [ ] Implementar JWT
- [ ] Crear endpoints de autenticación
- [ ] Crear middleware de autenticación
- [ ] Crear sistema de roles y permisos
- [ ] Modificar endpoints de miembros
- [ ] Modificar endpoints de contactos
- [ ] Modificar endpoints de ciudades
- [ ] Crear AuthContext en frontend
- [ ] Crear página de Login
- [ ] Implementar rutas protegidas
- [ ] Agregar filtrado de datos según rol
- [ ] Testing completo
- [ ] Documentación

---

**¿Listo para comenzar la implementación?** 🚀
