# 🚀 Configuración Manual en Render.com

## Paso 1: Crear el Backend (Servicio Web)

### 1.1 Crear el Servicio

1. Ve a https://dashboard.render.com/
2. Haz clic en **"New +"** (arriba a la derecha)
3. Selecciona **"Servicio web"** (Web Service)
4. Si te pide conectar un repositorio:
   - Conecta tu cuenta de GitHub/GitLab/Bitbucket
   - Autoriza Render para acceder a tus repositorios
   - Selecciona el repositorio `club-app`

### 1.2 Configurar el Backend

Completa el formulario con estos valores:

**Información Básica:**
- **Name**: `jetta-club-backend`
- **Region**: Elige la más cercana (ej: `Oregon (US West)`)

**Configuración del Entorno:**
- **Environment**: Selecciona **"Python 3"**
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Selecciona **"Free"** (gratis)

### 1.3 Configurar Variables de Entorno

Antes de hacer clic en "Create Web Service":

1. Haz clic en **"Advanced"** o busca la sección **"Environment Variables"**
2. Haz clic en **"Add Environment Variable"**
3. Agrega estas variables:

   **Variable 1:**
   - **Key**: `MONGODB_URI`
   - **Value**: `mongodb+srv://alyamatosan_db_user:1wdwxviSjRGYZDJ9@cluster0.53fkwew.mongodb.net/?retryWrites=true&w=majority`

   **Variable 2:**
   - **Key**: `DB_NAME`
   - **Value**: `jetta_club`

   **Variable 3 (opcional pero recomendado):**
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.0`

4. Haz clic en **"Create Web Service"**

### 1.4 Esperar el Despliegue

- El backend comenzará a construirse (5-10 minutos)
- Cuando termine, copia la URL que Render te da (ej: `https://jetta-club-backend.onrender.com`)
- **IMPORTANTE**: Guarda esta URL, la necesitarás para el frontend

---

## Paso 2: Crear el Frontend (Servicio Web)

### 2.1 Crear el Servicio

1. Haz clic en **"New +"** nuevamente
2. Selecciona **"Servicio web"** (Web Service)
3. Selecciona el mismo repositorio `club-app`

### 2.2 Configurar el Frontend

Completa el formulario con estos valores:

**Información Básica:**
- **Name**: `jetta-club-frontend`
- **Region**: La misma que elegiste para el backend

**Configuración del Entorno:**
- **Environment**: Selecciona **"Node"**
- **Build Command**: `cd frontend && npm install && npm run build`
- **Start Command**: `cd frontend && npm run preview -- --port $PORT --host 0.0.0.0`

**Plan:**
- Selecciona **"Free"** (gratis)

### 2.3 Configurar Variables de Entorno

**IMPORTANTE**: Necesitas la URL del backend que copiaste en el Paso 1.4

1. En la sección **"Environment Variables"**
2. Haz clic en **"Add Environment Variable"**
3. Agrega:

   **Variable:**
   - **Key**: `VITE_API_URL`
   - **Value**: `https://jetta-club-backend.onrender.com` 
     ⚠️ **Reemplaza esto con la URL REAL de tu backend que copiaste antes**

4. Haz clic en **"Create Web Service"**

### 2.4 Esperar el Despliegue

- El frontend comenzará a construirse (5-10 minutos)
- Cuando termine, tendrás la URL del frontend (ej: `https://jetta-club-frontend.onrender.com`)

---

## Paso 3: Verificar que Todo Funciona

### Verificar Backend

1. Ve a la URL de tu backend: `https://jetta-club-backend.onrender.com`
2. Deberías ver:
   ```json
   {
     "message": "Bienvenido a la API del Club Volkswagen Jetta Colombia",
     "version": "1.0.0"
   }
   ```
3. Ve a: `https://jetta-club-backend.onrender.com/docs`
   - Deberías ver la documentación interactiva de la API (Swagger UI)

4. Prueba el health check: `https://jetta-club-backend.onrender.com/api/health`
   - Debería retornar: `{"status": "healthy", "database": "connected"}`

### Verificar Frontend

1. Ve a la URL de tu frontend: `https://jetta-club-frontend.onrender.com`
2. Deberías ver la página de inicio del club
3. Prueba navegar a "Miembros" y "Directorio"
4. Si hay errores, abre la consola del navegador (F12) para ver los detalles

---

## ⚠️ Problemas Comunes y Soluciones

### El backend no conecta a MongoDB

**Solución:**
1. Ve a Settings → Environment Variables del backend
2. Verifica que `MONGODB_URI` esté correctamente configurado
3. Asegúrate de que MongoDB Atlas permita conexiones desde cualquier IP:
   - Ve a MongoDB Atlas → Network Access
   - Agrega `0.0.0.0/0` (Allow Access from Anywhere)

### El frontend muestra errores de conexión

**Solución:**
1. Verifica que el backend esté funcionando (ve a su URL)
2. Ve a Settings → Environment Variables del frontend
3. Verifica que `VITE_API_URL` tenga la URL completa con `https://`
4. **IMPORTANTE**: Después de cambiar `VITE_API_URL`, haz clic en:
   - **"Manual Deploy"** → **"Deploy latest commit"**
   - Esto reconstruye el frontend con la nueva variable

### Error de build en el backend

**Solución:**
1. Ve a los logs del servicio en Render
2. Verifica que el Build Command sea: `pip install -r backend/requirements.txt`
3. Verifica que el Start Command sea: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Error de build en el frontend

**Solución:**
1. Ve a los logs del servicio en Render
2. Verifica que el Build Command sea: `cd frontend && npm install && npm run build`
3. Verifica que el Start Command sea: `cd frontend && npm run preview -- --port $PORT --host 0.0.0.0`

### El servicio está "sleeping" (durmiendo)

**Explicación:**
- En el plan gratuito, los servicios se "duermen" después de 15 minutos de inactividad
- La primera petición después de dormir puede tardar ~30 segundos
- Esto es normal y no es un error

**Solución (opcional):**
- Considera usar un servicio de "ping" para mantenerlo activo
- O actualiza al plan Starter ($7/mes) que no se duerme

---

## 📋 Checklist de Configuración

### Backend
- [ ] Servicio web creado con nombre `jetta-club-backend`
- [ ] Environment: Python 3
- [ ] Build Command: `pip install -r backend/requirements.txt`
- [ ] Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Variable `MONGODB_URI` configurada
- [ ] Variable `DB_NAME` configurada
- [ ] Backend desplegado y funcionando
- [ ] URL del backend copiada y guardada

### Frontend
- [ ] Servicio web creado con nombre `jetta-club-frontend`
- [ ] Environment: Node
- [ ] Build Command: `cd frontend && npm install && npm run build`
- [ ] Start Command: `cd frontend && npm run preview -- --port $PORT --host 0.0.0.0`
- [ ] Variable `VITE_API_URL` configurada con la URL del backend
- [ ] Frontend reconstruido después de configurar `VITE_API_URL`
- [ ] Frontend desplegado y funcionando

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tu aplicación estará en línea y accesible desde cualquier lugar.

**URLs de ejemplo:**
- Backend: `https://jetta-club-backend.onrender.com`
- Frontend: `https://jetta-club-frontend.onrender.com`
- API Docs: `https://jetta-club-backend.onrender.com/docs`

