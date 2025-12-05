# 🚀 Guía de Despliegue en Render.com

## Opción 1: Usar Blueprint (Recomendado - Más Fácil)

### Paso 1: Preparar el Repositorio

1. Asegúrate de que tu código esté en GitHub, GitLab o Bitbucket
2. Verifica que el archivo `render.yaml` esté en la raíz del repositorio

### Paso 2: Crear Blueprint en Render

1. Ve a https://dashboard.render.com/
2. Inicia sesión o crea una cuenta (es gratis)
3. Haz clic en **"New +"** en la parte superior
4. Selecciona **"Blueprint"**
5. Conecta tu repositorio:
   - Si es la primera vez, autoriza Render para acceder a tu cuenta de GitHub/GitLab
   - Selecciona el repositorio `club-app`
6. Render detectará automáticamente el archivo `render.yaml`
7. Haz clic en **"Apply"**

### Paso 3: Configurar Variables de Entorno

Render creará dos servicios automáticamente. Necesitas configurar las variables de entorno:

#### Para el Backend (jetta-club-backend):

1. Ve al servicio `jetta-club-backend`
2. Ve a **Settings** → **Environment Variables**
3. Agrega o edita:
   - **Key**: `MONGODB_URI`
   - **Value**: `mongodb+srv://alyamatosan_db_user:1wdwxviSjRGYZDJ9@cluster0.53fkwew.mongodb.net/?retryWrites=true&w=majority`
   - Haz clic en **"Save Changes"**

#### Para el Frontend (jetta-club-frontend):

1. **IMPORTANTE**: Primero espera a que el backend se despliegue completamente
2. Ve al servicio `jetta-club-backend` y copia su URL (ej: `https://jetta-club-backend.onrender.com`)
3. Ve al servicio `jetta-club-frontend`
4. Ve a **Settings** → **Environment Variables**
5. Edita `VITE_API_URL`:
   - **Key**: `VITE_API_URL`
   - **Value**: La URL completa de tu backend (ej: `https://jetta-club-backend.onrender.com`)
   - Haz clic en **"Save Changes"**
6. Haz clic en **"Manual Deploy"** → **"Deploy latest commit"** para reconstruir con la nueva variable

### Paso 4: Esperar el Despliegue

- El backend se desplegará primero (5-10 minutos)
- Luego el frontend (5-10 minutos)
- Ambos servicios estarán disponibles en URLs como:
  - Backend: `https://jetta-club-backend.onrender.com`
  - Frontend: `https://jetta-club-frontend.onrender.com`

---

## Opción 2: Crear Servicios Manualmente

Si prefieres más control, puedes crear los servicios uno por uno:

### Crear Backend

1. Ve a https://dashboard.render.com/
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio
4. Configuración:
   - **Name**: `jetta-club-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. En **Environment Variables**, agrega:
   - `MONGODB_URI`: `mongodb+srv://alyamatosan_db_user:1wdwxviSjRGYZDJ9@cluster0.53fkwew.mongodb.net/?retryWrites=true&w=majority`
   - `DB_NAME`: `jetta_club`
6. Haz clic en **"Create Web Service"**

### Crear Frontend

1. Espera a que el backend termine de desplegarse
2. Copia la URL del backend (ej: `https://jetta-club-backend.onrender.com`)
3. Haz clic en **"New +"** → **"Web Service"**
4. Conecta el mismo repositorio
5. Configuración:
   - **Name**: `jetta-club-frontend`
   - **Environment**: `Node`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `cd frontend && npm run preview -- --port $PORT --host 0.0.0.0`
6. En **Environment Variables**, agrega:
   - `VITE_API_URL`: `https://jetta-club-backend.onrender.com` (usa la URL real de tu backend)
7. Haz clic en **"Create Web Service"**

---

## ⚠️ Notas Importantes

### Plan Free Tier de Render

- Los servicios se "duermen" después de 15 minutos de inactividad
- La primera petición después de dormir puede tardar ~30 segundos
- Para producción, considera el plan Starter ($7/mes por servicio)

### MongoDB Atlas

- Asegúrate de que tu IP de Render esté permitida en MongoDB Atlas
- O mejor aún, permite acceso desde cualquier IP (0.0.0.0/0) para desarrollo

### Variables de Entorno

- **NUNCA** subas el archivo `.env` a GitHub (ya está en `.gitignore`)
- Las variables de entorno se configuran directamente en Render

### URLs

- Render genera URLs automáticamente: `https://tu-servicio.onrender.com`
- Puedes personalizar el nombre en la configuración del servicio

---

## 🔍 Verificar el Despliegue

### Backend

1. Ve a la URL de tu backend: `https://jetta-club-backend.onrender.com`
2. Deberías ver: `{"message": "Bienvenido a la API del Club Volkswagen Jetta Colombia", "version": "1.0.0"}`
3. Ve a: `https://jetta-club-backend.onrender.com/docs` para ver la documentación de la API

### Frontend

1. Ve a la URL de tu frontend: `https://jetta-club-frontend.onrender.com`
2. Deberías ver la página de inicio del club
3. Prueba navegar a "Miembros" y "Directorio"

### Health Check

- Backend: `https://jetta-club-backend.onrender.com/api/health`
- Debería retornar: `{"status": "healthy", "database": "connected"}`

---

## 🐛 Solución de Problemas

### El backend no conecta a MongoDB

- Verifica que `MONGODB_URI` esté correctamente configurado en Render
- Asegúrate de que MongoDB Atlas permita conexiones desde cualquier IP (0.0.0.0/0)

### El frontend no puede conectar al backend

- Verifica que `VITE_API_URL` tenga la URL completa con `https://`
- Asegúrate de que el backend esté desplegado y funcionando
- Reconstruye el frontend después de cambiar `VITE_API_URL`

### Error de build

- Revisa los logs en Render Dashboard
- Verifica que todas las dependencias estén en `requirements.txt` y `package.json`

### El servicio está "sleeping"

- Es normal en el plan gratuito
- La primera petición después de dormir será lenta
- Considera usar un servicio de "ping" para mantenerlo activo

---

## ✅ Checklist de Despliegue

- [ ] Código subido a GitHub/GitLab/Bitbucket
- [ ] Archivo `render.yaml` en la raíz del repositorio
- [ ] Blueprint creado en Render (o servicios manuales)
- [ ] `MONGODB_URI` configurado en el backend
- [ ] `DB_NAME` configurado en el backend
- [ ] Backend desplegado y funcionando
- [ ] URL del backend copiada
- [ ] `VITE_API_URL` configurado en el frontend con la URL del backend
- [ ] Frontend reconstruido después de configurar `VITE_API_URL`
- [ ] Ambos servicios funcionando correctamente

¡Listo! Tu aplicación estará en línea. 🎉

