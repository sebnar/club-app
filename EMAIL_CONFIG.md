# 📧 Configuración de Email

## 📋 Variables de Entorno Necesarias

Para que el sistema envíe emails con credenciales, configura estas variables en Render.com:

### Variables para Backend

```env
# Configuración SMTP
SMTP_HOST=smtp.gmail.com          # Servidor SMTP (Gmail, Outlook, etc.)
SMTP_PORT=587                      # Puerto SMTP (587 para TLS, 465 para SSL)
SMTP_USER=tu-email@gmail.com       # Email desde el que se enviarán los correos
SMTP_PASSWORD=tu-app-password      # Contraseña de aplicación (no la contraseña normal)
EMAIL_FROM=tu-email@gmail.com      # Email remitente (puede ser igual a SMTP_USER)
EMAIL_FROM_NAME=Club VW Jetta      # Nombre que aparecerá como remitente
FRONTEND_URL=https://tu-frontend.onrender.com  # URL del frontend (para links en emails)
```

## 🔧 Configuración por Proveedor

### Gmail

1. **Habilitar verificación en 2 pasos** en tu cuenta de Google
2. **Generar contraseña de aplicación:**
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Ingresa "Club Jetta App"
   - Copia la contraseña generada (16 caracteres)

3. **Configurar variables:**
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=tu-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # La contraseña de aplicación (sin espacios)
   ```

### Outlook/Hotmail

```
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=tu-email@outlook.com
SMTP_PASSWORD=tu-contraseña
```

### Otros Proveedores

Consulta la documentación de tu proveedor de email para obtener:
- SMTP_HOST
- SMTP_PORT
- Si requiere autenticación especial

## ⚠️ Modo de Desarrollo (Sin Email)

Si no configuras las variables de email, el sistema:
- ✅ **Seguirá funcionando** (no fallará)
- ✅ **Creará el usuario** correctamente
- ⚠️ **Mostrará las credenciales en los logs** del servidor
- ⚠️ **NO enviará email**

**Ejemplo de log cuando no hay email configurado:**
```
⚠️  Email no configurado. Credenciales para usuario@email.com:
   Username: usuario123
   Password: Abc123Xyz456
```

## 📝 Template del Email

El email enviado incluye:
- ✅ Username generado
- ✅ Contraseña temporal
- ✅ Instrucciones para cambiar contraseña
- ✅ Link al frontend
- ✅ Diseño HTML responsive

## 🔒 Seguridad

- ✅ Las contraseñas temporales son generadas de forma segura (12 caracteres)
- ✅ Las contraseñas se hashean antes de guardarse
- ✅ El usuario debe cambiar la contraseña al primer login
- ✅ El email se envía solo si está configurado

## 🧪 Probar el Envío de Email

1. Configura las variables de entorno en Render
2. Crea un miembro con `create_user: true`
3. Verifica que recibes el email
4. Si no recibes email, revisa los logs de Render para ver las credenciales

## 📋 Checklist de Configuración

- [ ] Variables SMTP configuradas en Render
- [ ] Contraseña de aplicación generada (si usas Gmail)
- [ ] FRONTEND_URL configurada
- [ ] Probar creación de miembro con usuario
- [ ] Verificar que se recibe el email
- [ ] Probar login con credenciales temporales
- [ ] Verificar que se fuerza cambio de contraseña
