"""
Generador de contraseñas temporales seguras
"""
import secrets
import string


def generate_temporary_password(length: int = 12) -> str:
    """
    Generar una contraseña temporal segura
    
    Args:
        length: Longitud de la contraseña (default: 12)
    
    Returns:
        Contraseña temporal generada
    """
    # Caracteres permitidos: letras (mayúsculas y minúsculas), números
    alphabet = string.ascii_letters + string.digits
    # Asegurar que tenga al menos una mayúscula, una minúscula y un número
    password = (
        secrets.choice(string.ascii_uppercase) +  # Al menos una mayúscula
        secrets.choice(string.ascii_lowercase) +  # Al menos una minúscula
        secrets.choice(string.digits) +            # Al menos un número
        ''.join(secrets.choice(alphabet) for _ in range(length - 3))  # Resto aleatorio
    )
    # Mezclar los caracteres
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    generated_password = ''.join(password_list)
    return generated_password
