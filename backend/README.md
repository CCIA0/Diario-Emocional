# 🎯 Guía Completa de Deploy - Diario Emocional

Deploy de aplicación **Angular + FastAPI + SQLite** en **Vercel + Render**

## 📋 Configuración Completada

### ✅ Backend (FastAPI + Render)
- **CORS configurado** para desarrollo y producción
- **Variables de entorno** para configuración dinámica
- **SQLite** con inicialización automática
- **render.yaml** configurado para deploy automático

### ✅ Frontend (Angular + Vercel)
- **Environments** configurados (development/production)
- **API Service** actualizado con manejo de errores
- **vercel.json** configurado para SPA routing
- **Build commands** optimizados

---

## 🚀 PASOS PARA DEPLOY

### 1. 📁 PREPARAR REPOSITORIO
```bash
# Asegúrate de que todos los archivos estén en tu repositorio Git
git add .
git commit -m "Configuración para deploy en Render y Vercel"
git push origin main
```

### 2. �️ DEPLOY BACKEND EN RENDER

#### 2.1 Crear cuenta en [Render.com](https://render.com)

#### 2.2 Crear nuevo Web Service
1. Clic en **"New +"** → **"Web Service"**
2. Conectar tu repositorio GitHub
3. **Root Directory:** `backend`
4. **Environment:** `Python`
5. **Build Command:** `pip install -r requirements.txt && python init_db.py`
6. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 2.3 Configurar Variables de Entorno
En el dashboard de Render, añadir:
```
ENVIRONMENT=production
GEMINI_API_KEY=tu_api_key_de_gemini
FRONTEND_URL=https://tu-app.vercel.app
```

#### 2.4 Deploy
- Clic en **"Create Web Service"**
- **Esperar 5-10 minutos** para el primer deploy
- **Copiar la URL** de tu backend: `https://tu-backend.onrender.com`

### 3. 🌐 DEPLOY FRONTEND EN VERCEL

#### 3.1 Actualizar URL del Backend
Editar `frontend/pruebaIA/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://TU-BACKEND-URL.onrender.com/api/v1', // ← Tu URL de Render
  appName: 'Diario Emocional'
};
```

#### 3.2 Commit y Push
```bash
cd frontend/pruebaIA
git add .
git commit -m "Actualizar URL del backend para producción"
git push origin main
```

#### 3.3 Crear cuenta en [Vercel.com](https://vercel.com)

#### 3.4 Importar Proyecto
1. Clic en **"New Project"**
2. Importar tu repositorio
3. **Root Directory:** `frontend/pruebaIA`
4. **Framework Preset:** `Angular`
5. **Build Command:** `npm run build:prod`
6. **Output Directory:** `dist/prueba-ia`

#### 3.5 Deploy
- Clic en **"Deploy"**
- **Esperar 2-5 minutos**
- **Copiar la URL** de tu frontend: `https://tu-app.vercel.app`

### 4. 🔄 ACTUALIZAR CORS EN BACKEND

#### 4.1 Actualizar Variables de Entorno en Render
Ir al dashboard de Render y actualizar:
```
FRONTEND_URL=https://tu-app.vercel.app
```

#### 4.2 Redeploy Backend
- En Render, clic en **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🧪 VERIFICACIÓN

### ✅ Backend Funcionando
Visita: `https://tu-backend.onrender.com/health`
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_service": "configured"
}
```

### ✅ Frontend Funcionando
Visita: `https://tu-app.vercel.app`
- Debería cargar la aplicación Angular
- Verificar que puede comunicarse con el backend

### ✅ Integración Completa
1. Crear una entrada en el diario
2. Verificar que se guarda en la base de datos
3. Comprobar análisis de sentimientos y feedback de IA

---

## 🛠️ COMANDOS ÚTILES

### Desarrollo Local
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend/pruebaIA
npm install
npm start
```

### Testing Local
```bash
# Probar backend
curl http://localhost:8000/health

# Probar frontend
curl http://localhost:4200
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ Error CORS
**Síntoma:** Frontend no puede conectar con backend
**Solución:**
1. Verificar `FRONTEND_URL` en variables de entorno de Render
2. Asegurar que la URL no tenga `/` al final
3. Redeploy del backend

### ❌ Base de Datos no Persiste
**Síntoma:** Los datos se pierden al reiniciar
**Solución:**
- En plan free de Render, la base de datos se reinicia
- Para persistencia, considera upgrade a plan pago o usar PostgreSQL

### ❌ Build Falla en Vercel
**Síntoma:** Error en build de Angular
**Solución:**
1. Verificar que `build:prod` existe en `package.json`
2. Comprobar que todas las dependencias están en `package.json`
3. Revisar logs de build en dashboard de Vercel

### ❌ API Key de Gemini no Funciona
**Síntoma:** Error 401/403 en endpoints de IA
**Solución:**
1. Verificar que `GEMINI_API_KEY` está configurada en Render
2. Comprobar que la API key es válida
3. Verificar logs del backend en Render

### ❌ App se "Duerme" en Render
**Síntoma:** Primera request tarda mucho
**Solución:**
- Normal en plan free (spins down after 15 min)
- Usar servicios como [UptimeRobot](https://uptimerobot.com) para ping periódico
- O upgrade a plan pago

---

## � MONITOREO

### Logs Backend (Render)
1. Dashboard de Render → Tu servicio → **"Logs"**
2. Ver errores y actividad en tiempo real

### Logs Frontend (Vercel)
1. Dashboard de Vercel → Tu proyecto → **"Functions"**
2. Ver métricas y errores de deployment

### Analytics (Opcional)
- Vercel Analytics para métricas de frontend
- Render Metrics para performance de backend

---

## 🔄 ACTUALIZACIONES FUTURAS

### Código
```bash
# Hacer cambios
git add .
git commit -m "Descripción del cambio"
git push origin main

# Deploy automático en ambas plataformas
```

### Variables de Entorno
- **Render:** Dashboard → Environment → Add Variable
- **Vercel:** Dashboard → Settings → Environment Variables

---

## 🎉 ¡DEPLOY COMPLETADO!

Tu aplicación ahora está funcionando en:
- **Frontend:** https://tu-app.vercel.app
- **Backend:** https://tu-backend.onrender.com

**¡Felicitaciones! 🎊 Tu Diario Emocional está en producción.**