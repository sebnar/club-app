# 🚀 Guía Rápida de Configuración

## Pasos Rápidos para Empezar

### 1. MongoDB Atlas (5 minutos)

1. Ve a https://www.mongodb.com/cloud/atlas/register
2. Crea una cuenta gratuita
3. Crea un nuevo cluster (elige la opción FREE M0)
4. Crea un usuario de base de datos:
   - Database Access → Add New Database User
   - Username y Password (guárdalos)
5. Configura Network Access:
   - Network Access → Add IP Address
   - Allow Access from Anywhere (0.0.0.0/0) para desarrollo
6. Obtén tu Connection String:
   - Clusters → Connect → Connect your application
   - Copia la URI (ej: `mongodb+srv://usuario:password@cluster.mongodb.net/`)

### 2. Configurar Variables de Entorno

**Backend:**
Crea `backend/.env`:
```env
MONGODB_URI=mongodb+srv://TU_USUARIO:TU_PASSWORD@TU_CLUSTER.mongodb.net/
DB_NAME=jetta_club
```

**Frontend:**
Crea `frontend/.env` (opcional para desarrollo local):
```env
VITE_API_URL=http://localhost:8000
```

### 3. Instalar Dependencias

**Backend:**
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4. Ejecutar

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
# O: uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Verificar

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🚢 Despliegue en Render.com

### Paso 1: Preparar el Repositorio

1. Sube tu código a GitHub/GitLab/Bitbucket
2. Asegúrate de tener el archivo `render.yaml` en la raíz

### Paso 2: Conectar con Render

1. Ve a https://dashboard.render.com/
2. Click en "New +" → "Blueprint"
3. Conecta tu repositorio
4. Render detectará automáticamente `render.yaml`

### Paso 3: Configurar Variables de Entorno

En cada servicio (backend y frontend), agrega:

**Backend:**
- `MONGODB_URI`: Tu connection string completo
- `DB_NAME`: `jetta_club`

**Frontend:**
- `VITE_API_URL`: La URL completa del backend (ej: `https://jetta-club-backend.onrender.com`)

### Paso 4: Desplegar

1. Click en "Apply" en Render
2. Espera a que ambos servicios se desplieguen
3. ¡Listo! Tu app estará en línea

## ⚠️ Notas Importantes

- **MongoDB Atlas Free Tier**: 512MB de almacenamiento (suficiente para empezar)
- **Render Free Tier**: 
  - Los servicios se "duermen" después de 15 min de inactividad
  - La primera petición después de dormir puede tardar ~30 segundos
  - Para producción, considera el plan Starter ($7/mes por servicio)

## 🐛 Solución de Problemas

### Error de conexión a MongoDB
- Verifica que tu IP esté en la whitelist de MongoDB Atlas
- Verifica que el usuario y contraseña sean correctos
- Asegúrate de que la URI tenga el formato correcto

### Error en Render
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs en Render Dashboard
- Asegúrate de que el `render.yaml` esté en la raíz del proyecto

### Frontend no conecta con Backend
- Verifica que `VITE_API_URL` esté configurado correctamente
- En producción, usa la URL completa con `https://`
- Verifica CORS en el backend (ya está configurado para permitir todos los orígenes)

