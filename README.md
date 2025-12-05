# 🚗 Club Volkswagen Jetta Colombia

Aplicación web para el club de carros Volkswagen Jetta en Colombia. Permite gestionar miembros del club, perfiles de usuarios y un directorio de contactos por categorías.

## 🎯 Características

- **Perfiles de Miembros**: Cada integrante puede tener su perfil con información no sensible
- **Directorio de Contactos**: Contactos organizados por categorías (latonería, lujos, etc.)
- **Información General**: Sección informativa sobre el club
- **Interfaz Moderna**: Diseño responsive y atractivo

## 🛠️ Stack Tecnológico

- **Backend**: Python + FastAPI
- **Frontend**: React + Vite
- **Base de Datos**: MongoDB Atlas (Free Tier)
- **Despliegue**: Render.com

## 📋 Requisitos Previos

- Python 3.11+
- Node.js 18+
- Cuenta en MongoDB Atlas (gratuita)
- Cuenta en Render.com (gratuita)

## 🚀 Instalación Local

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd club-app
```

### 2. Configurar Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar MongoDB Atlas

📖 **Guía completa**: Consulta [MONGODB_SETUP.md](MONGODB_SETUP.md) para instrucciones detalladas paso a paso.

**Resumen rápido:**
1. Crea una cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crea un cluster gratuito (M0)
3. Crea un usuario de base de datos
4. Configura Network Access (permite tu IP o 0.0.0.0/0)
5. Obtén tu connection string (URI)
6. Crea un archivo `.env` en la carpeta `backend`:

```env
MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=jetta_club
```

**Probar conexión:**
```bash
cd backend
python test_connection.py
```

### 4. Configurar Frontend

```bash
cd frontend
npm install
```

### 5. Ejecutar la aplicación

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
# O: uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📦 Despliegue en Render.com

### Opción 1: Usando render.yaml (Recomendado)

1. Conecta tu repositorio a Render.com
2. Render detectará automáticamente el archivo `render.yaml`
3. Configura las variables de entorno:
   - `MONGODB_URI`: Tu connection string de MongoDB Atlas
   - `DB_NAME`: `jetta_club`
   - `VITE_API_URL`: URL del backend desplegado (se configurará automáticamente)

### Opción 2: Configuración Manual

#### Backend Service:
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `MONGODB_URI`: Tu connection string
  - `DB_NAME`: `jetta_club`

#### Frontend Service:
- **Build Command**: `cd frontend && npm install && npm run build`
- **Start Command**: `cd frontend && npm run preview -- --port $PORT --host 0.0.0.0`
- **Environment Variables**:
  - `VITE_API_URL`: URL completa del backend (ej: `https://jetta-club-backend.onrender.com`)

## 📁 Estructura del Proyecto

```
club-app/
├── backend/
│   ├── main.py              # API principal con FastAPI
│   ├── models.py            # Modelos Pydantic
│   ├── requirements.txt     # Dependencias Python
│   └── .env                 # Variables de entorno (no commitear)
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/          # Páginas principales
│   │   ├── services/       # Servicios API
│   │   ├── App.jsx         # Componente principal
│   │   └── main.jsx        # Punto de entrada
│   ├── package.json
│   └── vite.config.js
├── render.yaml              # Configuración Render.com
└── README.md
```

## 🔌 API Endpoints

### Miembros
- `GET /api/members` - Listar todos los miembros
- `GET /api/members/{id}` - Obtener un miembro
- `POST /api/members` - Crear un miembro
- `PUT /api/members/{id}` - Actualizar un miembro
- `DELETE /api/members/{id}` - Eliminar un miembro

### Contactos
- `GET /api/contacts` - Listar contactos (opcional: `?category=latonería`)
- `GET /api/contacts/categories` - Listar categorías
- `POST /api/contacts` - Crear un contacto

### Health Check
- `GET /api/health` - Estado de la API y conexión a BD

## 🔒 Seguridad y Privacidad

- ✅ Solo se almacenan datos **no sensibles**
- ✅ No se almacenan contraseñas ni información financiera
- ✅ Email y teléfono son opcionales
- ✅ Cumple con buenas prácticas de privacidad

## 🎨 Próximas Funcionalidades

- [ ] Sección "Ver Coche" con vista 360
- [ ] Sistema de autenticación (opcional)
- [ ] Panel de administración
- [ ] Subida de imágenes de perfil
- [ ] Sistema de eventos del club
- [ ] Chat o foro interno

## 📝 Notas Importantes

- La aplicación está diseñada para uso interno del club
- MongoDB Atlas Free Tier tiene límites (512MB de almacenamiento)
- Render.com Free Tier puede tener "cold starts" (primera petición lenta)
- Para producción, considera actualizar a planes pagos

## 🤝 Contribuciones

Este es un proyecto para el club. Las contribuciones son bienvenidas.

## 📄 Licencia

Uso interno del club.

---

**Desarrollado con ❤️ para el Club Volkswagen Jetta Colombia**
