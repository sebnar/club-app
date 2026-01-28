# 📧 Configuración de Email con MailerSend

## 🚀 MailerSend - Servicio de Email Transaccional

MailerSend es un servicio moderno de email que permite enviar emails sin necesidad de verificar dominio propio (en algunos casos).

## 📋 Variables de Entorno Necesarias

Configura estas variables en Render.com:

```env
# API Key de MailerSend (obligatorio)
MAILERSEND_API_KEY=mlsn.1186bae72fb7e8b9d4988d1e8fcf243c427ba0ab7162c8ab034b4700fa740829

# Email remitente (debe estar verificado en MailerSend)
EMAIL_FROM=info@domain.com

# Nombre del remitente (opcional)
EMAIL_FROM_NAME=Club Volkswagen Jetta Colombia

# URL del frontend (para links en emails)
FRONTEND_URL=https://tu-frontend.onrender.com
```

## 🔧 Configuración Paso a Paso

### 1. Crear Cuenta en MailerSend

1. Ve a https://www.mailersend.com
2. Crea una cuenta (plan gratuito disponible)
3. Verifica tu email

### 2. Obtener API Key

1. Ve a https://app.mailersend.com/api-tokens
2. Haz clic en "Create Token"
3. Dale un nombre (ej: "Club Jetta Production")
4. Selecciona permisos: "Email Send"
5. Copia la API Key (empieza con `mlsn.`)

### 3. Verificar Dominio o Email

**Opción A: Verificar tu dominio (recomendado)**
1. Ve a https://app.mailersend.com/domains
2. Haz clic en "Add Domain"
3. Ingresa tu dominio
4. Agrega los registros DNS que MailerSend te proporciona
5. Espera verificación

**Opción B: Usar email verificado (puede funcionar sin dominio)**
- MailerSend puede permitir enviar desde emails verificados sin dominio propio
- Verifica tu email en la configuración de la cuenta
- Usa ese email como `EMAIL_FROM`

### 4. Configurar en Render

1. Ve a tu servicio backend en Render
2. Settings > Environment Variables
3. Agrega estas variables:

   **MAILERSEND_API_KEY:**
   ```
   mlsn.1186bae72fb7e8b9d4988d1e8fcf243c427ba0ab7162c8ab034b4700fa740829
   ```

   **EMAIL_FROM:**
   ```
   info@domain.com
   ```
   (o tu email verificado)

   **EMAIL_FROM_NAME:**
   ```
   Club Volkswagen Jetta Colombia
   ```

   **FRONTEND_URL:**
   ```
   https://tu-frontend.onrender.com
   ```

4. Guarda y redespliega

## ✅ Verificar que Funciona

1. Crea un miembro con usuario desde el frontend
2. Revisa los logs de Render
3. Deberías ver:
   ```
   ✅ [EMAIL] Email enviado exitosamente
      - Message ID: abc123...
   ```
4. Revisa tu bandeja de entrada (o spam)

## ⚠️ Límites del Plan Gratuito

- **12,000 emails/mes** (muy generoso)
- Puede requerir verificación de dominio dependiendo del plan
- Verifica los límites en tu cuenta de MailerSend

## 🔍 Troubleshooting

### Error: "API Key no configurada"
- Verifica que `MAILERSEND_API_KEY` esté configurada en Render
- Asegúrate de copiar la API Key completa (empieza con `mlsn.`)

### Error: "Domain not verified"
- Si usas tu dominio, verifica que esté completamente verificado en MailerSend
- Si usas email personal, verifica que esté verificado en tu cuenta

### Error: "Sender not verified"
- Verifica que el email en `EMAIL_FROM` esté verificado en MailerSend
- Puede requerir verificar dominio si usas un dominio personalizado

### No recibo emails
- Revisa la carpeta de spam
- Verifica que el email esté verificado en MailerSend
- Revisa los logs de Render para ver el Message ID

## 📝 Nota Importante

El sistema **NO falla** si el email no se puede enviar. El usuario se crea correctamente y las credenciales aparecen en los logs para que puedas enviarlas manualmente si es necesario.

## 🔗 Recursos

- Documentación de MailerSend: https://developers.mailersend.com
- Dashboard de MailerSend: https://app.mailersend.com
- API Tokens: https://app.mailersend.com/api-tokens
- Domains: https://app.mailersend.com/domains

## 💡 Ventajas de MailerSend

- ✅ Plan gratuito muy generoso (12,000 emails/mes)
- ✅ Puede funcionar sin dominio propio en algunos casos
- ✅ API REST moderna
- ✅ Funciona perfectamente desde Render
- ✅ Buena deliverability
