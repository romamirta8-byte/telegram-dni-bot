# 🤖 Bot de Telegram - Consulta de DNI (Python)

Bot profesional de Telegram para consultar información de DNI usando la API de Perú. Desarrollado en Python con interfaz amigable mediante botones.

## 🚀 Características Principales

- ✅ Interfaz profesional con botones interactivos
- ✅ Botón "Conectar" con cuenta regresiva de 15 segundos
- ✅ Validación de entrada (8 dígitos)
- ✅ Consulta en tiempo real de la API de Perú
- ✅ Manejo robusto de errores
- ✅ Compatible con Render (plan free)
- ✅ Modo polling para desarrollo local
- ✅ Modo webhook para producción

## 📋 Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes de Python)
- Token de bot de Telegram (obtener de [@BotFather](https://t.me/botfather))
- Token de API Perú (obtener de [apiperu.dev](https://apiperu.dev))
- Cuenta en GitHub
- Cuenta en Render (plan free)

## 🛠️ Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/telegram-dni-bot.git
cd telegram-dni-bot
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env`

```bash
cp .env.example .env
```

### 5. Configurar variables en `.env`

Edita el archivo `.env` con tus datos:

```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
API_PERU_TOKEN=tu_token_api_aqui
NODE_ENV=development
PORT=3000
```

### 6. Ejecutar el bot localmente

```bash
python bot.py
```

Deberías ver en consola: `🤖 Bot iniciado - Esperando mensajes...`

## 📱 Cómo Usar el Bot

1. **Busca el bot en Telegram** por su nombre o usa el link que crees
2. **Presiona `/start`** para ver el menú principal
3. **Presiona el botón "✅ Conectar"**
4. **Espera 15 segundos** (el servidor se activa)
5. **Envía un número de DNI** (8 dígitos)
   - Ejemplo: `62048227`
6. **Recibe la información** del DNI consultado

## 🌐 Desplegar en GitHub y Render

### Paso 1: Preparar el repositorio local

```bash
git init
git add .
git commit -m "Initial commit: Telegram DNI Bot en Python"
```

### Paso 2: Crear repositorio en GitHub

1. Ve a [github.com](https://github.com)
2. Haz clic en "New repository"
3. Nombre: `telegram-dni-bot`
4. Descripción: `Bot de Telegram para consulta de DNI - API Perú`
5. Selecciona **Public**
6. **NO** inicialices con README
7. Clic en "Create repository"

### Paso 3: Subir código a GitHub

GitHub te mostrará comandos, cópialosy pégalos en PowerShell:

```bash
git remote add origin https://github.com/[tu-usuario]/telegram-dni-bot.git
git branch -M main
git push -u origin main
```

✅ Tu código está ahora en GitHub

### Paso 4: Configurar en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta (gratuita)
3. Clic en **"New +"** → **"Web Service"**
4. Selecciona **"Deploy an existing Git repository"**
5. Conecta tu cuenta de GitHub si es la primera vez
6. Busca y selecciona el repositorio: `telegram-dni-bot`

### Paso 5: Configurar el servicio en Render

En la página de creación del servicio, configura:

- **Name**: `telegram-dni-bot`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`
- **Region**: Elige el más cercano a ti
- **Plan**: Free

### Paso 6: Agregar variables de entorno en Render

1. En la misma página, desplázate a **"Environment"**
2. Agrega las siguientes variables:

| Key | Value |
|-----|-------|
| TELEGRAM_BOT_TOKEN | `8321928383:AAFWMRGKsN9A1jJ6yX062x99Je2tLrR51oA` |
| API_PERU_TOKEN | `1ea59516c0455c384bd5892c98e8cb270b3ef5a926f9458ff167fd15b3a9e38c` |
| NODE_ENV | `production` |
| WEBHOOK_URL | Déjalo vacío por ahora |
| PORT | `3000` |

3. Clic en **"Create Web Service"**

⏳ Render empezará a desplegar (tardará ~2-3 minutos)

### Paso 7: Obtener URL de Render

1. Espera a que el despliegue termine (verás "Live" en verde)
2. Copia la URL que aparece arriba (ej: `https://telegram-dni-bot-abc123.onrender.com`)
3. Ve a **"Environment"** y actualiza `WEBHOOK_URL`:
   - `WEBHOOK_URL=https://telegram-dni-bot-abc123.onrender.com`
4. Redeploy el servicio

### Paso 8: Registrar Webhook en Telegram

Una vez que Render esté corriendo, ejecuta en PowerShell:

```powershell
$token = "8321928383:AAFWMRGKsN9A1jJ6yX062x99Je2tLrR51oA"
$webhook_url = "https://telegram-dni-bot-abc123.onrender.com"

curl.exe -X POST "https://api.telegram.org/bot$token/setWebhook?url=$webhook_url"
```

Deberías recibir:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

### Paso 9: Verificar que está funcionando

```powershell
$token = "8321928383:AAFWMRGKsN9A1jJ6yX062x99Je2tLrR51oA"

curl.exe "https://api.telegram.org/bot$token/getWebhookInfo"
```

Deberías ver tu URL de webhook registrada.

### ✅ ¡Bot en Producción!

El bot ya está corriendo en Render. Abre Telegram y pruébalo: `/start`

## ⚙️ Variables de Entorno

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | ✅ Sí | `8321928383:AAF...` |
| `API_PERU_TOKEN` | Token de API Peru | ✅ Sí | `1ea59516c04...` |
| `NODE_ENV` | Entorno (development/production) | ❌ No | `production` |
| `PORT` | Puerto (solo desarrollo) | ❌ No | `3000` |
| `WEBHOOK_URL` | URL del webhook (solo producción) | ❌ No | `https://app.onrender.com` |

## 📝 Notas sobre Plan Free de Render

### Limitaciones
- ⏸️ Se suspende después de 15 minutos sin actividad
- ⏱️ Tarda ~50 segundos en "despertarse"
- 🔄 Esto es normal y esperado

### Soluciones

**Opción A: Usar UptimeRobot (Recomendado - Gratis)**

1. Ve a [uptimerobot.com](https://uptimerobot.com)
2. Crea una cuenta gratuita
3. "Add New Monitor"
4. Tipo: `HTTP(s)`
5. URL: `https://tu-app-name.onrender.com`
6. Intervalo: `14 minutos`
7. Monitor activo ✅

Esto pingueará tu bot cada 14 minutos para evitar que se suspenda.

**Opción B: Upgrade a Paid Plan** ($7/mes - Starter)
- Bot 24/7 sin pausas
- Mejor para usuarios frecuentes

## 🐛 Solución de Problemas

### El bot no responde

**Verificar logs en Render:**
1. Ve a tu servicio en Render
2. Haz clic en "Logs"
3. Busca mensajes de error

**Verificar webhook:**
```powershell
$token = "tu_token"
curl.exe "https://api.telegram.org/bot$token/getWebhookInfo"
```

### Error: "TELEGRAM_BOT_TOKEN no está configurado"
- Verifica que la variable esté correcta en Render
- Haz redeploy

### Error: "API_PERU_TOKEN no está configurado"
- Verifica el token en Render
- Comprueba que sea válido en [apiperu.dev](https://apiperu.dev)

### El DNI no se encontró
- Verifica que sea un DNI válido de 8 dígitos
- Comprueba que la API esté disponible en [apiperu.dev](https://apiperu.dev)

### Primera consulta es lenta
- Normal en plan free de Render
- Usa UptimeRobot para evitar suspensión

## 🔐 Seguridad

⚠️ **IMPORTANTE:**
- **Nunca** commitees el archivo `.env` a GitHub
- **Nunca** publiques tus tokens en el código
- Usa `.env.example` como plantilla
- Cambia periódicamente los tokens
- Haz el repositorio privado si es posible

## 📚 Documentación Útil

- [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [API Peru](https://apiperu.dev/)
- [Render Docs](https://render.com/docs)
- [BotFather - Crear Bot](https://t.me/botfather)

## 📊 Estructura del Proyecto

```
telegram-dni-bot/
├── bot.py                 # Bot principal
├── requirements.txt       # Dependencias de Python
├── .env.example          # Template de variables
├── .gitignore            # Archivos a ignorar en git
├── Procfile              # Configuración para Render
├── runtime.txt           # Versión de Python
└── README.md             # Esta documentación
```

## 📄 Licencia

MIT

## 👨‍💻 Autor

Creado con ❤️ para consultas de DNI en Perú

---

## 🚀 Resumen de Comandos Rápido

```bash
# Desarrollo local
python bot.py

# Git
git init
git add .
git commit -m "mensaje"
git push -u origin main

# Render webhook
curl.exe -X POST "https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
```

---

**¿Tienes dudas?** Crea un issue en GitHub o contacta al soporte de Render.
