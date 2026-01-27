from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserLogin, UserResponse
from auth.security import verify_password, create_access_token
from auth.dependencies import get_current_user, oauth2_scheme
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
            "token_type": "bearer"
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
