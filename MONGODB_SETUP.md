# 🔌 Guía de Configuración de MongoDB Atlas

## Paso 1: Crear cuenta en MongoDB Atlas

1. Ve a https://www.mongodb.com/cloud/atlas/register
2. Crea una cuenta gratuita (o inicia sesión si ya tienes una)
3. Completa el formulario de registro

## Paso 2: Crear un Cluster Gratuito

1. Una vez dentro del dashboard, haz clic en **"Build a Database"**
2. Selecciona el plan **FREE (M0)** - es completamente gratuito
3. Elige un proveedor de nube (AWS, Google Cloud, o Azure) - cualquiera funciona
4. Selecciona una región cercana a Colombia (ej: `us-east-1` o `sa-east-1`)
5. Nombra tu cluster (ej: "Cluster0") o déjalo con el nombre por defecto
6. Haz clic en **"Create"** y espera 3-5 minutos mientras se crea

## Paso 3: Crear Usuario de Base de Datos

1. En la pantalla de "Security Quickstart", crea un usuario:
   - **Username**: Elige un nombre (ej: `jetta_club_admin`)
   - **Password**: Genera una contraseña segura o crea una propia
   - ⚠️ **IMPORTANTE**: Guarda estas credenciales, las necesitarás después
2. Haz clic en **"Create Database User"**

## Paso 4: Configurar Acceso de Red

1. En la sección "Network Access", haz clic en **"Add IP Address"**
2. Para desarrollo local, puedes usar:
   - **"Allow Access from Anywhere"** (0.0.0.0/0) - Más fácil pero menos seguro
   - O agrega tu IP específica para mayor seguridad
3. Haz clic en **"Confirm"**

## Paso 5: Obtener Connection String

1. Haz clic en **"Connect"** en tu cluster
2. Selecciona **"Connect your application"**
3. Elige **"Python"** como driver y **"3.6 or later"** como versión
4. Copia la connection string que aparece, se verá así:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Paso 6: Crear archivo .env en el Backend

1. Ve a la carpeta `backend/` de tu proyecto
2. Crea un archivo llamado `.env` (sin extensión, solo `.env`)
3. Abre el archivo y agrega:

```env
MONGODB_URI=mongodb+srv://TU_USUARIO:TU_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=jetta_club
```

**Ejemplo real:**
```env
MONGODB_URI=mongodb+srv://jetta_club_admin:MiPassword123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
DB_NAME=jetta_club
```

⚠️ **IMPORTANTE**: 
- Reemplaza `TU_USUARIO` con el username que creaste en el Paso 3
- Reemplaza `TU_PASSWORD` con la contraseña que creaste
- Si tu contraseña tiene caracteres especiales, debes codificarlos en URL:
  - `@` → `%40`
  - `#` → `%23`
  - `$` → `%24`
  - etc.

## Paso 7: Verificar la Conexión

1. Ejecuta el backend:
   ```bash
   cd backend
   python run.py
   ```

2. Deberías ver en la consola:
   ```
   ✅ Conectado a MongoDB: jetta_club
   ```

3. Si ves un error, verifica:
   - ✅ El archivo `.env` existe en `backend/`
   - ✅ La URI está correcta (sin espacios extra)
   - ✅ Tu IP está en la whitelist de MongoDB Atlas
   - ✅ El usuario y contraseña son correctos

## 🔍 Solución de Problemas Comunes

### Error: "ServerSelectionTimeoutError"
- **Causa**: Tu IP no está en la whitelist
- **Solución**: Ve a Network Access en MongoDB Atlas y agrega tu IP o usa 0.0.0.0/0

### Error: "Authentication failed"
- **Causa**: Usuario o contraseña incorrectos
- **Solución**: Verifica las credenciales en el archivo `.env`

### Error: "Connection string format is invalid"
- **Causa**: La URI tiene caracteres especiales sin codificar
- **Solución**: Codifica la contraseña en URL o cámbiala por una sin caracteres especiales

### El archivo .env no se lee
- **Causa**: El archivo está en la ubicación incorrecta
- **Solución**: Asegúrate de que `.env` esté en `backend/.env` (no en la raíz)

## 📝 Para Render.com

Cuando despliegues en Render.com, necesitarás agregar la variable de entorno `MONGODB_URI`:

1. Ve a tu servicio de backend en Render
2. Settings → Environment Variables
3. Agrega:
   - **Key**: `MONGODB_URI`
   - **Value**: Tu connection string completo (el mismo del archivo .env)
4. Agrega también:
   - **Key**: `DB_NAME`
   - **Value**: `jetta_club`

## ✅ Verificación Final

Una vez configurado, puedes probar la conexión visitando:
- http://localhost:8000/api/health

Deberías ver:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

¡Listo! Tu base de datos está configurada. 🎉

