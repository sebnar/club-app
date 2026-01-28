# 🌐 Configurar Dominio en Resend

## ⚠️ Problema Actual

Estás viendo este error:
```
Solo puedes enviar correos de prueba a tu propia dirección (alyamatosan@gmail.com). 
Para enviar correos a otros destinatarios, verifica un dominio en resend.com/domains
```

Esto significa que estás usando el dominio de prueba `onboarding@resend.dev`, que solo permite enviar a tu email verificado.

## ✅ Solución: Verificar tu Dominio

### Paso 1: Agregar Dominio en Resend

1. Ve a https://resend.com/domains
2. Haz clic en **"Add Domain"**
3. Ingresa tu dominio (ej: `tu-dominio.com`)
   - Puedes usar el dominio principal o un subdominio (ej: `mail.tu-dominio.com`)
4. Haz clic en **"Add"**

### Paso 2: Configurar Registros DNS

Resend te mostrará registros DNS que debes agregar. Ejemplo:

**Registro TXT (verificación):**
```
Tipo: TXT
Nombre: @ (o el subdominio)
Valor: resend-domain-verification=abc123...
TTL: 3600
```

**Registro MX (opcional, para recibir respuestas):**
```
Tipo: MX
Nombre: @
Valor: feedback-smtp.resend.com
Prioridad: 10
TTL: 3600
```

**Registro SPF (opcional, para autenticación):**
```
Tipo: TXT
Nombre: @
Valor: v=spf1 include:resend.com ~all
TTL: 3600
```

### Paso 3: Agregar Registros en tu Proveedor DNS

1. Ve a tu proveedor de DNS (donde compraste el dominio):
   - GoDaddy
   - Namecheap
   - Cloudflare
   - Google Domains
   - etc.

2. Ve a la sección de "DNS Management" o "Zone Records"

3. Agrega los registros que Resend te proporcionó

4. Guarda los cambios

### Paso 4: Esperar Verificación

1. Vuelve a https://resend.com/domains
2. El dominio aparecerá como **"Pending"** (pendiente)
3. La verificación puede tardar:
   - **5-30 minutos** si agregaste los registros correctamente
   - **Hasta 24 horas** en algunos casos
4. Cuando esté verificado, aparecerá como **"Verified"** ✅

### Paso 5: Actualizar Variables en Render

Una vez verificado, actualiza en Render:

**EMAIL_FROM:**
```
noreply@tu-dominio.com
```
(o cualquier email de tu dominio verificado)

**Ejemplo completo:**
```env
RESEND_API_KEY=re_Dn1kTc3y_EYnY77omvhfBN3hmEz2sqBcF
EMAIL_FROM=noreply@tu-dominio.com
EMAIL_FROM_NAME=Club Volkswagen Jetta Colombia
FRONTEND_URL=https://tu-frontend.onrender.com
```

## 🔍 Verificar Estado

1. Ve a https://resend.com/domains
2. Busca tu dominio
3. Debe aparecer como **"Verified"** (no "Pending")
4. Si aparece un error, haz clic para ver los detalles

## ⚠️ Problemas Comunes

### "Domain verification failed"
- Verifica que los registros DNS estén correctos
- Asegúrate de que el TTL haya pasado (puede tardar)
- Revisa que no haya errores de tipeo en los valores

### "DNS records not found"
- Espera más tiempo (hasta 24 horas)
- Verifica que guardaste los cambios en tu proveedor DNS
- Algunos proveedores tardan en propagar cambios

### No tengo un dominio
**Opción 1:** Compra un dominio barato:
- Namecheap: ~$10/año
- GoDaddy: ~$12/año
- Google Domains: ~$12/año

**Opción 2:** Usa un subdominio de un dominio que ya tengas

**Opción 3:** Temporalmente, solo envía a tu email verificado para pruebas

## 📝 Nota

Una vez que tu dominio esté verificado, podrás enviar emails a **cualquier destinatario** usando cualquier email de tu dominio como remitente.
