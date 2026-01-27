from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
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
