# 📧 Configuración de Email con Resend

## 🚀 Resend - Servicio Moderno de Email

Resend es un servicio diseñado específicamente para aplicaciones en la nube. Es más confiable que SMTP tradicional y funciona perfectamente desde Render.

## 📋 Variables de Entorno Necesarias

Configura estas variables en Render.com:

```env
# API Key de Resend (obligatorio)
RESEND_API_KEY=re_Dn1kTc3y_EYnY77omvhfBN3hmEz2sqBcF

# Email remitente (debe estar verificado en Resend)
EMAIL_FROM=onboarding@resend.dev

# Nombre del remitente (opcional)
EMAIL_FROM_NAME=Club Volkswagen Jetta Colombia

# URL del frontend (para links en emails)
FRONTEND_URL=https://tu-frontend.onrender.com
```

## 🔧 Configuración Paso a Paso

### 1. Crear Cuenta en Resend

1. Ve a https://resend.com
2. Crea una cuenta (gratis)
3. Verifica tu email

### 2. Obtener API Key

1. Ve a https://resend.com/api-keys
2. Haz clic en "Create API Key"
3. Dale un nombre (ej: "Club Jetta Production")
4. Copia la API Key (empieza con `re_`)

### 3. Verificar Dominio o Usar Dominio de Prueba

**⚠️ IMPORTANTE:** El dominio de prueba `onboarding@resend.dev` solo permite enviar a tu email verificado. Para enviar a otros destinatarios, debes verificar un dominio.

**Opción A: Usar dominio de prueba (solo para pruebas)**
- Resend proporciona `onboarding@resend.dev` por defecto
- ⚠️ **LIMITACIÓN:** Solo puedes enviar a tu email verificado (el que usaste para crear la cuenta)
- No puedes enviar a otros destinatarios
- Perfecto solo para pruebas iniciales

**Opción B: Verificar tu dominio (OBLIGATORIO para producción)**
1. Ve a https://resend.com/domains
2. Haz clic en "Add Domain"
3. Ingresa tu dominio (ej: `tu-dominio.com` o un subdominio como `mail.tu-dominio.com`)
4. Resend te mostrará registros DNS que debes agregar:
   - Registro TXT para verificación
   - Registro MX (opcional, para recibir respuestas)
   - Registro SPF (opcional)
5. Agrega estos registros en tu proveedor de DNS (donde compraste el dominio)
6. Espera a que se verifique (puede tardar unos minutos a horas)
7. Una vez verificado (aparece como "Verified"), puedes usar cualquier email de ese dominio:
   - `noreply@tu-dominio.com`
   - `club@tu-dominio.com`
   - `info@tu-dominio.com`
   - etc.

### 4. Configurar en Render

1. Ve a tu servicio backend en Render
2. Settings > Environment Variables
3. Agrega estas variables:

   **RESEND_API_KEY:**
   ```
   re_Dn1kTc3y_EYnY77omvhfBN3hmEz2sqBcF
   ```

   **EMAIL_FROM:**
   ```
   onboarding@resend.dev
   ```
   (o tu email verificado si usas dominio propio)

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
      - ID del email: abc123...
   ```
4. Revisa tu bandeja de entrada (o spam)

## ⚠️ Límites del Plan Gratuito

- **100 emails/día** (suficiente para desarrollo y pruebas)
- Solo puedes enviar a emails verificados si usas dominio de prueba
- Para producción, considera el plan de pago

## 🔍 Troubleshooting

### Error: "API Key no configurada"
- Verifica que `RESEND_API_KEY` esté configurada en Render
- Asegúrate de copiar la API Key completa (empieza con `re_`)

### Error: "Solo puedes enviar correos de prueba a tu propia dirección"
**Causa:** Estás usando `onboarding@resend.dev` (dominio de prueba) y tratando de enviar a un email diferente al verificado.

**Solución:**
1. **Opción rápida:** Cambia `EMAIL_FROM` a tu email verificado temporalmente:
   ```
   EMAIL_FROM=alyamatosan@gmail.com
   ```
   (Pero esto puede no funcionar si Resend requiere dominio verificado)

2. **Opción correcta:** Verifica un dominio en Resend:
   - Ve a https://resend.com/domains
   - Agrega tu dominio
   - Configura los registros DNS
   - Espera verificación
   - Usa un email de tu dominio: `noreply@tu-dominio.com`

### Error: "Domain not verified"
- Si usas tu dominio, verifica que esté completamente verificado en Resend
- El estado debe aparecer como "Verified" (no "Pending")
- Si usas `onboarding@resend.dev`, solo puedes enviar a tu email verificado

### No recibo emails
- Revisa la carpeta de spam
- Verifica que el email esté en la lista de emails permitidos (si usas dominio de prueba)
- Revisa los logs de Render para ver el ID del email

## 📝 Nota Importante

El sistema **NO falla** si el email no se puede enviar. El usuario se crea correctamente y las credenciales aparecen en los logs para que puedas enviarlas manualmente si es necesario.

## 🔗 Recursos

- Documentación de Resend: https://resend.com/docs
- Dashboard de Resend: https://resend.com/emails
- API Keys: https://resend.com/api-keys
