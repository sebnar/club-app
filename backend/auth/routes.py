from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserLogin, UserResponse, ChangePasswordRequest
from auth.security import verify_password, create_access_token, get_password_hash
from auth.dependencies import get_current_user, get_current_active_user, oauth2_scheme
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login - Recibe username y password, devuelve token JWT
    """
    # Importar aquí para evitar importación circular
    from main import users_collection
    
    try:
        # Buscar usuario por username
        user = users_collection.find_one({"username": form_data.username})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar si el usuario está activo
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Verificar contraseña
        if not verify_password(form_data.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Actualizar último login
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Verificar si debe cambiar contraseña
        must_change_password = user.get("must_change_password", False)
        
        # Crear token
        access_token = create_access_token(
            data={
                "user_id": str(user["_id"]),
                "username": user["username"],
                "role": user.get("role", "user"),
                "member_id": str(user["member_id"]) if user.get("member_id") else None
            }
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "must_change_password": must_change_password
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar login: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Obtener información del usuario actual autenticado
    """
    return current_user


@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Cambiar contraseña del usuario actual
    Requiere la contraseña actual y la nueva contraseña
    """
    from main import users_collection
    from bson import ObjectId
    
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario no válido"
            )
        
        # Buscar usuario en la base de datos
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(password_data.current_password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta"
            )
        
        # Verificar que la nueva contraseña sea diferente
        if verify_password(password_data.new_password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña debe ser diferente a la actual"
            )
        
        # Actualizar contraseña
        new_password_hash = get_password_hash(password_data.new_password)
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "password_hash": new_password_hash,
                    "must_change_password": False,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "message": "Contraseña actualizada exitosamente",
            "must_change_password": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar contraseña: {str(e)}"
        )
