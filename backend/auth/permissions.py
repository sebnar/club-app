"""
Helpers simples para verificar permisos
Sistema sencillo y eficiente para control de acceso
"""
from typing import Optional


def is_admin(user: dict) -> bool:
    """Verificar si el usuario es administrador"""
    return user.get("role") == "admin"


def is_owner(user: dict, resource_owner_id: Optional[str]) -> bool:
    """
    Verificar si el usuario es el dueño del recurso
    
    Args:
        user: Diccionario del usuario actual
        resource_owner_id: ID del dueño del recurso (puede ser member_id u otro)
    
    Returns:
        True si el usuario es el dueño o es admin
    """
    if is_admin(user):
        return True
    
    user_member_id = user.get("member_id")
    if user_member_id and resource_owner_id:
        return str(user_member_id) == str(resource_owner_id)
    
    return False


def can_edit_member(user: dict, member_id: str) -> bool:
    """
    Verificar si el usuario puede editar un miembro específico
    
    Args:
        user: Diccionario del usuario actual
        member_id: ID del miembro a editar
    
    Returns:
        True si puede editar (es admin o es su propio perfil)
    """
    if is_admin(user):
        return True
    
    user_member_id = user.get("member_id")
    if user_member_id:
        return str(user_member_id) == str(member_id)
    
    return False


def require_owner_or_admin(user: dict, resource_owner_id: Optional[str]):
    """
    Helper para lanzar excepción si no es admin ni dueño
    
    Uso en endpoints:
        if not require_owner_or_admin(current_user, member_id):
            raise HTTPException(403, "No tienes permisos")
    """
    from fastapi import HTTPException, status
    
    if not is_owner(user, resource_owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    return True
