"""
Servicio de envío de emails usando MailerSend
API REST directa para evitar conflictos de dependencias
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuración de MailerSend desde variables de entorno
MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "info@domain.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Club Volkswagen Jetta Colombia")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://tu-frontend.onrender.com")


def send_credentials_email(to_email: str, username: str, temporary_password: str) -> bool:
    """
    Enviar email con credenciales de acceso usando MailerSend API REST
    
    Args:
        to_email: Email del destinatario
        username: Nombre de usuario
        temporary_password: Contraseña temporal
    
    Returns:
        True si se envió correctamente, False en caso contrario
    """
    print(f"📧 [EMAIL] Iniciando proceso de envío de email con MailerSend")
    print(f"   - Destinatario: {to_email}")
    print(f"   - Username: {username}")
    print(f"   - MAILERSEND_API_KEY configurado: {'Sí' if MAILERSEND_API_KEY else 'No'}")
    print(f"   - EMAIL_FROM: {EMAIL_FROM}")
    
    # Si no hay API key configurada, solo loguear (no fallar)
    if not MAILERSEND_API_KEY:
        print(f"⚠️  [EMAIL] MailerSend API Key no configurada")
        print(f"   Configura la variable MAILERSEND_API_KEY en Render")
        print(f"   Credenciales para {to_email}:")
        print(f"   - Username: {username}")
        print(f"   - Password: {temporary_password}")
        return False
    
    try:
        # Contenido HTML del email
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #24373E; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .credentials {{ background-color: white; padding: 15px; margin: 20px 0; border-left: 4px solid #007bff; }}
        .warning {{ background-color: #fff3cd; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 Club Volkswagen Jetta Colombia</h1>
        </div>
        <div class="content">
            <h2>Bienvenido al Club</h2>
            <p>Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales de acceso:</p>
            
            <div class="credentials">
                <p><strong>Usuario:</strong> {username}</p>
                <p><strong>Contraseña temporal:</strong> {temporary_password}</p>
            </div>
            
            <div class="warning">
                <p><strong>⚠️ IMPORTANTE:</strong> Debes cambiar esta contraseña al iniciar sesión por primera vez.</p>
            </div>
            
            <p>Para acceder, visita: <a href="{FRONTEND_URL}">{FRONTEND_URL}</a></p>
        </div>
        <div class="footer">
            <p>Club Volkswagen Jetta Colombia</p>
            <p>Este es un email automático, por favor no respondas.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Contenido de texto plano (fallback)
        text_content = f"""
Bienvenido al Club Volkswagen Jetta Colombia

Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales de acceso:

Usuario: {username}
Contraseña temporal: {temporary_password}

⚠️ IMPORTANTE: Debes cambiar esta contraseña al iniciar sesión por primera vez.

Para acceder, visita: {FRONTEND_URL}

Saludos,
Club Volkswagen Jetta Colombia
"""
        
        print(f"📤 [EMAIL] Enviando email a través de MailerSend API...")
        print(f"   - From: {EMAIL_FROM_NAME} <{EMAIL_FROM}>")
        print(f"   - To: {to_email}")
        
        # Preparar payload para MailerSend API
        payload = {
            "from": {
                "email": EMAIL_FROM,
                "name": EMAIL_FROM_NAME
            },
            "to": [
                {
                    "email": to_email,
                    "name": username
                }
            ],
            "subject": "Bienvenido al Club Volkswagen Jetta Colombia - Tus Credenciales",
            "html": html_content,
            "text": text_content
        }
        
        # Headers para la API de MailerSend
        headers = {
            "Authorization": f"Bearer {MAILERSEND_API_KEY}",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # Enviar email usando MailerSend API REST
        response = requests.post(
            "https://api.mailersend.com/v1/email",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 202:
            print(f"✅ [EMAIL] Email enviado exitosamente")
            print(f"   - Status: {response.status_code}")
            print(f"   - Response: {response.text}")
            return True
        else:
            print(f"❌ [EMAIL] Error al enviar email: Status {response.status_code}")
            print(f"   - Response: {response.text}")
            print(f"   Credenciales para {to_email}:")
            print(f"   - Username: {username}")
            print(f"   - Password: {temporary_password}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ [EMAIL] Error de conexión al enviar email a {to_email}: {e}")
        print(f"   Credenciales para {to_email}:")
        print(f"   - Username: {username}")
        print(f"   - Password: {temporary_password}")
        return False
    except Exception as e:
        print(f"❌ [EMAIL] Error inesperado al enviar email a {to_email}: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        print(f"   Traceback completo:")
        traceback.print_exc()
        # No fallar si el email no se puede enviar, solo loguear
        print(f"   Credenciales para {to_email}:")
        print(f"   - Username: {username}")
        print(f"   - Password: {temporary_password}")
        return False
