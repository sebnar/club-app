from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from auth.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependencia para obtener el usuario actual desde el token JWT
    """
    # Importar aquí para evitar importación circular
    from main import users_collection, user_helper
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    # Buscar usuario en la base de datos
    try:
        from bson import ObjectId
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise credentials_exception
        
        return user_helper(user)
    except Exception:
        raise credentials_exception


def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """
    Dependencia para obtener el usuario actual solo si está activo
    """
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


def require_role(allowed_roles: List[str]):
    """
    Factory function que retorna una dependencia para requerir uno de los roles especificados
    
    Uso:
        @app.get("/admin-only")
        async def admin_endpoint(user: dict = Depends(require_role(["admin"]))):
            ...
    """
    def role_checker(current_user: dict = Depends(get_current_active_user)):
        user_role = current_user.get("role", "user")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


def require_admin(current_user: dict = Depends(get_current_active_user)):
    """
    Dependencia simple para requerir rol admin
    
    Uso:
        @app.post("/members")
        async def create_member(user: dict = Depends(require_admin)):
            ...
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return current_user
