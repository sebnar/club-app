"""
Servicio de envío de emails
Usa SMTP para enviar credenciales a los usuarios
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Configuración de email desde variables de entorno
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Club Volkswagen Jetta Colombia")


def send_credentials_email(to_email: str, username: str, temporary_password: str) -> bool:
    """
    Enviar email con credenciales de acceso
    
    Args:
        to_email: Email del destinatario
        username: Nombre de usuario
        temporary_password: Contraseña temporal
    
    Returns:
        True si se envió correctamente, False en caso contrario
    """
    print(f"📧 [EMAIL] Iniciando proceso de envío de email")
    print(f"   - Destinatario: {to_email}")
    print(f"   - Username: {username}")
    print(f"   - SMTP_HOST: {SMTP_HOST}")
    print(f"   - SMTP_PORT: {SMTP_PORT}")
    print(f"   - SMTP_USER configurado: {'Sí' if SMTP_USER else 'No'}")
    print(f"   - SMTP_PASSWORD configurado: {'Sí' if SMTP_PASSWORD else 'No'}")
    
    # Si no hay configuración de email, solo loguear (no fallar)
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"⚠️  [EMAIL] Email no configurado. Variables faltantes:")
        if not SMTP_USER:
            print(f"   - SMTP_USER no está configurado")
        if not SMTP_PASSWORD:
            print(f"   - SMTP_PASSWORD no está configurado")
        print(f"   Credenciales para {to_email}:")
        print(f"   - Username: {username}")
        print(f"   - Password: {temporary_password}")
        return False
    
    try:
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Bienvenido al Club Volkswagen Jetta Colombia - Tus Credenciales'
        msg['From'] = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"
        msg['To'] = to_email
        
        # Contenido del email
        text_content = f"""
Bienvenido al Club Volkswagen Jetta Colombia

Tus credenciales de acceso son:

Usuario: {username}
Contraseña temporal: {temporary_password}

⚠️ IMPORTANTE: Debes cambiar esta contraseña al iniciar sesión por primera vez.

Para acceder, visita: {os.getenv("FRONTEND_URL", "https://tu-frontend.onrender.com")}

Saludos,
Club Volkswagen Jetta Colombia
"""
        
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
            
            <p>Para acceder, visita: <a href="{os.getenv("FRONTEND_URL", "https://tu-frontend.onrender.com")}">{os.getenv("FRONTEND_URL", "https://tu-frontend.onrender.com")}</a></p>
        </div>
        <div class="footer">
            <p>Club Volkswagen Jetta Colombia</p>
            <p>Este es un email automático, por favor no respondas.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Agregar contenido
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Enviar email
        print(f"🔌 [EMAIL] Conectando a servidor SMTP {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            print(f"✅ [EMAIL] Conexión establecida")
            print(f"🔐 [EMAIL] Iniciando TLS...")
            server.starttls()
            print(f"✅ [EMAIL] TLS iniciado")
            print(f"🔑 [EMAIL] Autenticando con usuario {SMTP_USER}...")
            server.login(SMTP_USER, SMTP_PASSWORD)
            print(f"✅ [EMAIL] Autenticación exitosa")
            print(f"📤 [EMAIL] Enviando mensaje...")
            server.send_message(msg)
            print(f"✅ [EMAIL] Mensaje enviado exitosamente")
        
        print(f"✅ [EMAIL] Email enviado correctamente a {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ [EMAIL] Error de autenticación SMTP: {e}")
        print(f"   Verifica que SMTP_USER y SMTP_PASSWORD sean correctos")
        print(f"   Credenciales para {to_email}:")
        print(f"   - Username: {username}")
        print(f"   - Password: {temporary_password}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ [EMAIL] Error de conexión SMTP: {e}")
        print(f"   Verifica que SMTP_HOST y SMTP_PORT sean correctos")
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
