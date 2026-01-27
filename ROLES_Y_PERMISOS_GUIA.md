# 🔐 Guía de Uso: Sistema de Roles y Permisos

## 📋 Resumen

Sistema **sencillo y eficiente** para control de acceso basado en roles. Solo 3 dependencias principales y helpers simples.

---

## 🎯 Dependencias Principales

### 1. `get_current_user`
Obtiene el usuario actual (cualquier usuario autenticado)

```python
from auth.dependencies import get_current_user

@app.get("/mi-endpoint")
async def mi_endpoint(user: dict = Depends(get_current_user)):
    return {"message": f"Hola {user['username']}"}
```

### 2. `get_current_active_user`
Obtiene el usuario actual solo si está activo

```python
from auth.dependencies import get_current_active_user

@app.get("/mi-endpoint")
async def mi_endpoint(user: dict = Depends(get_current_active_user)):
    # Solo usuarios activos pueden acceder
    return {"message": f"Hola {user['username']}"}
```

### 3. `require_admin`
Solo permite acceso a administradores

```python
from auth.dependencies import require_admin

@app.post("/members")
async def create_member(member: MemberCreate, user: dict = Depends(require_admin)):
    # Solo admin puede crear miembros
    ...
```

### 4. `require_role`
Permite acceso a uno o varios roles específicos

```python
from auth.dependencies import require_role

@app.get("/admin-panel")
async def admin_panel(user: dict = Depends(require_role(["admin"]))):
    # Solo admin
    ...

@app.get("/moderator-panel")
async def moderator_panel(user: dict = Depends(require_role(["admin", "moderator"]))):
    # Admin o moderator
    ...
```

---

## 🛠️ Helpers de Permisos

### `is_admin(user)`
Verificar si es admin

```python
from auth.permissions import is_admin

if is_admin(current_user):
    # Hacer algo solo para admin
    pass
```

### `is_owner(user, resource_owner_id)`
Verificar si es el dueño del recurso (o admin)

```python
from auth.permissions import is_owner

if is_owner(current_user, member_id):
    # Puede editar
    pass
```

### `can_edit_member(user, member_id)`
Verificar si puede editar un miembro específico

```python
from auth.permissions import can_edit_member

if can_edit_member(current_user, member_id):
    # Puede editar este miembro
    pass
```

### `require_owner_or_admin(user, resource_owner_id)`
Lanza excepción si no es admin ni dueño

```python
from auth.permissions import require_owner_or_admin

@app.put("/members/{member_id}")
async def update_member(member_id: str, current_user: dict = Depends(get_current_active_user)):
    require_owner_or_admin(current_user, member_id)
    # Si llegamos aquí, tiene permisos
    ...
```

---

## 📝 Ejemplos Prácticos

### Ejemplo 1: Endpoint solo para admin

```python
from auth.dependencies import require_admin

@app.post("/api/members")
async def create_member(member: MemberCreate, user: dict = Depends(require_admin)):
    # Solo admin puede crear
    ...
```

### Ejemplo 2: Endpoint para admin o user

```python
from auth.dependencies import get_current_active_user

@app.get("/api/members")
async def get_members(user: dict = Depends(get_current_active_user)):
    # Cualquier usuario autenticado puede ver
    ...
```

### Ejemplo 3: Endpoint donde user solo puede editar su perfil

```python
from auth.dependencies import get_current_active_user
from auth.permissions import can_edit_member
from fastapi import HTTPException, status

@app.put("/api/members/{member_id}")
async def update_member(
    member_id: str,
    member_update: MemberUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    # Verificar permisos
    if not can_edit_member(current_user, member_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes editar tu propio perfil"
        )
    
    # Actualizar miembro
    ...
```

### Ejemplo 4: Endpoint con lógica condicional según rol

```python
from auth.dependencies import get_current_active_user
from auth.permissions import is_admin

@app.get("/api/members/{member_id}")
async def get_member(
    member_id: str,
    current_user: Optional[dict] = Depends(get_current_active_user)
):
    member = get_member_from_db(member_id)
    
    # Si es admin, mostrar todo
    if current_user and is_admin(current_user):
        return member
    
    # Si es el dueño, mostrar todo
    if current_user and can_edit_member(current_user, member_id):
        return member
    
    # Si no, mostrar solo datos públicos
    return filter_member_public(member)
```

---

## 🎨 Patrones de Uso Comunes

### Patrón 1: Solo Admin
```python
user: dict = Depends(require_admin)
```

### Patrón 2: Admin o User (cualquier autenticado)
```python
user: dict = Depends(get_current_active_user)
```

### Patrón 3: Admin o Dueño del Recurso
```python
user: dict = Depends(get_current_active_user)
# Luego verificar con can_edit_member() o require_owner_or_admin()
```

### Patrón 4: Opcional (público o autenticado)
```python
from typing import Optional

current_user: Optional[dict] = Depends(get_current_user)
# Si es None, es público. Si tiene valor, está autenticado.
```

---

## ✅ Ventajas de este Sistema

1. **Simple**: Solo 3 dependencias principales
2. **Eficiente**: Validaciones rápidas
3. **Legible**: Código claro y fácil de entender
4. **Extensible**: Fácil agregar nuevos roles o permisos
5. **Type-safe**: Funciona bien con FastAPI y Pydantic

---

## 🚀 Próximos Pasos

Ahora que tienes el sistema de roles, puedes:

1. Proteger endpoints existentes usando estas dependencias
2. Filtrar datos según el rol del usuario
3. Implementar lógica de permisos personalizada

**¿Listo para proteger los endpoints?** 🎯
