# Scripts Útiles para Deploy

## 🔧 Scripts de Desarrollo

### Backend - Test Local
```bash
# Navegar al backend
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python init_db.py

# Ejecutar servidor
uvicorn app.main:app --reload --port 8000

# Test health endpoint
curl http://localhost:8000/health
```

### Frontend - Test Local
```bash
# Navegar al frontend
cd frontend/pruebaIA

# Instalar dependencias
npm install

# Ejecutar en desarrollo (con proxy)
npm start

# Build para producción
npm run build:prod

# Test build local
npx http-server dist/prueba-ia
```

## 🚀 Scripts de Deploy

### Deploy Rápido
```bash
# Backend + Frontend
git add .
git commit -m "Deploy update"
git push origin main

# Los deploys son automáticos en Render y Vercel
```

### Verificación Post-Deploy
```bash
# Test backend
curl https://tu-backend.onrender.com/health

# Test frontend
curl -I https://tu-app.vercel.app
```

## 🐛 Debug Scripts

### Logs Backend
```bash
# Ver logs en tiempo real (usar dashboard de Render)
# O localmente:
tail -f logs/app.log
```

### Test Database Local
```bash
cd backend
python -c "
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT name FROM sqlite_master WHERE type=\"table\";'))
    print('Tablas:', [row[0] for row in result])
"
```

### Test API Endpoints
```bash
# Health check
curl https://tu-backend.onrender.com/health

# Test journal endpoint
curl -X POST https://tu-backend.onrender.com/api/v1/journal/entries \
  -H "Content-Type: application/json" \
  -d '{"text": "Test entry", "user_id": "test-user"}'
```

## 📊 Monitoreo

### Uptime Check
```bash
# Script para verificar que la app esté funcionando
#!/bin/bash
BACKEND_URL="https://tu-backend.onrender.com"
FRONTEND_URL="https://tu-app.vercel.app"

echo "Checking backend..."
curl -f $BACKEND_URL/health && echo "✅ Backend OK" || echo "❌ Backend Error"

echo "Checking frontend..."
curl -f $FRONTEND_URL && echo "✅ Frontend OK" || echo "❌ Frontend Error"
```

### Performance Test
```bash
# Test de carga básico
curl -w "@curl-format.txt" -o /dev/null -s https://tu-backend.onrender.com/health

# Donde curl-format.txt contiene:
#     time_namelookup:  %{time_namelookup}\n
#      time_connect:  %{time_connect}\n
#   time_appconnect:  %{time_appconnect}\n
#  time_pretransfer:  %{time_pretransfer}\n
#     time_redirect:  %{time_redirect}\n
#        time_total:  %{time_total}\n
```