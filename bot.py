import logging
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de configuración
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_TOKEN = os.getenv('API_PERU_TOKEN')
API_BASE_URL = 'https://apiperu.dev/api/dni'

# Estados de conversación
MENU, CONNECTING, WAITING, CONSULTING, RESULT = range(5)

# Almacenar estado de usuarios
user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Comando /start - menú principal"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Inicializar estado del usuario
    user_states[user_id] = {
        'connected': False,
        'connect_time': None
    }
    
    welcome_text = (
        f"👋 ¡Hola {user_name}!\n\n"
        f"Bienvenido al 🤖 *Bot de Consulta de DNI*\n\n"
        f"📋 Este bot te permite consultar información de DNI usando la API de Perú.\n\n"
        f"⚠️ Antes de empezar, debes presionar el botón *'Conectar'* y esperar 15 segundos.\n"
        f"Esto permite que el servidor se active correctamente.\n\n"
        f"¿Listo para comenzar?"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Conectar", callback_data='connect')],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    return MENU


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja los clics de botones"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == 'connect':
        return await handle_connect(query, context, user_id)
    elif query.data == 'help':
        return await handle_help(query)
    elif query.data == 'consult':
        return await handle_consult_button(query, user_id)
    elif query.data == 'restart':
        return await handle_restart(query, user_id, context)
    
    return MENU


async def handle_connect(query, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> int:
    """Maneja el botón de conectar con cuenta regresiva"""
    user_states[user_id]['connected'] = False
    
    # Mensaje inicial
    await query.edit_message_text(
        text="⏳ *Conectando con el servidor...*\n\n"
             "⏱️ Espera 15 segundos para que el servidor se active.\n\n"
             "_(Por favor NO envíes mensajes aún)_",
        parse_mode='Markdown'
    )
    
    # Cuenta regresiva
    for countdown in range(15, 0, -1):
        await asyncio.sleep(1)
        
        # Actualizar cada 3 segundos para no sobrecargar
        if countdown % 3 == 0 or countdown <= 3:
            try:
                await query.edit_message_text(
                    text=f"⏳ *Conectando con el servidor...*\n\n"
                         f"⏱️ Espera {countdown} segundos para que el servidor se active.\n\n"
                         f"_(Por favor NO envíes mensajes aún)_",
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.warning(f"Error al actualizar: {e}")
    
    # Conexión exitosa
    user_states[user_id]['connected'] = True
    user_states[user_id]['connect_time'] = datetime.now()
    
    keyboard = [
        [InlineKeyboardButton("🔍 Consultar DNI", callback_data='consult')],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data='help')],
        [InlineKeyboardButton("🔄 Reconectar", callback_data='connect')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="✅ *¡Conectado exitosamente!*\n\n"
             "🎉 El servidor está listo.\n\n"
             "📝 Ahora puedes consultar un DNI.\n\n"
             "Presiona el botón *'Consultar DNI'* o envía un número de DNI (8 dígitos).",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return MENU


async def handle_help(query) -> int:
    """Muestra la ayuda"""
    help_text = (
        "📚 *AYUDA - Bot de Consulta de DNI*\n\n"
        "🎯 *Cómo usar:*\n"
        "1️⃣ Presiona *'Conectar'* desde el menú\n"
        "2️⃣ Espera 15 segundos (es importante)\n"
        "3️⃣ Envía un número de DNI (8 dígitos)\n"
        "4️⃣ Recibirás la información registrada\n\n"
        "📋 *Datos que obtendrás:*\n"
        "• 🆔 Número de DNI\n"
        "• 👤 Nombre completo\n"
        "• 📝 Nombres y Apellidos\n"
        "• 🔐 Código de verificación\n\n"
        "⚠️ *Nota importante:*\n"
        "El servidor está en plan free, la primera consulta puede tardar hasta 50 segundos.\n\n"
        "❓ *¿Dudas?*\n"
        "Presiona /start para volver al menú."
    )
    
    keyboard = [
        [InlineKeyboardButton("↩️ Volver al Menú", callback_data='restart')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=help_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    return MENU


async def handle_consult_button(query, user_id: int) -> int:
    """Maneja el botón de consultar DNI"""
    if not user_states.get(user_id, {}).get('connected'):
        await query.edit_message_text(
            text="⚠️ *Error*\n\n"
                 "Primero debes presionar 'Conectar' y esperar 15 segundos."
        )
        return MENU
    
    await query.edit_message_text(
        text="📝 *Ingresa un DNI*\n\n"
             "Por favor, envía un número de DNI (8 dígitos).\n\n"
             "Ejemplo: 62048227"
    )
    
    return CONSULTING


async def handle_restart(query, user_id: int, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Vuelve al menú principal"""
    keyboard = [
        [InlineKeyboardButton("✅ Conectar", callback_data='connect')],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🤖 *Menú Principal*\n\n"
             "¿Qué deseas hacer?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return MENU


async def handle_dni_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja la entrada de DNI del usuario"""
    user_id = update.effective_user.id
    dni = update.message.text.strip()
    
    # Verificar si está conectado
    if not user_states.get(user_id, {}).get('connected'):
        await update.message.reply_text(
            "⚠️ *Debes conectar primero*\n\n"
            "Usa /start para ir al menú.",
            parse_mode='Markdown'
        )
        return MENU
    
    # Validar que sea 8 dígitos
    if not dni.isdigit() or len(dni) != 8:
        await update.message.reply_text(
            "❌ *DNI inválido*\n\n"
            "El DNI debe tener exactamente 8 dígitos numéricos.\n\n"
            "Intenta de nuevo:",
            parse_mode='Markdown'
        )
        return CONSULTING
    
    # Consultar API
    await update.message.reply_text("⏳ *Consultando información...*\n\nEspera por favor.", parse_mode='Markdown')
    
    result = await query_dni_api(dni)
    
    if result['error']:
        await update.message.reply_text(
            f"❌ *Error*\n\n{result['message']}",
            parse_mode='Markdown'
        )
    else:
        data = result['data']
        response_text = (
            f"✅ *INFORMACIÓN DEL DNI*\n\n"
            f"🆔 *DNI:* `{data['numero']}`\n"
            f"👤 *Nombre Completo:* {data['nombre_completo']}\n"
            f"📝 *Nombres:* {data['nombres']}\n"
            f"👨 *Apellido Paterno:* {data['apellido_paterno']}\n"
            f"👩 *Apellido Materno:* {data['apellido_materno']}\n"
            f"🔐 *Código de Verificación:* {data['codigo_verificacion']}\n\n"
            f"⏱️ *Tiempo de respuesta:* {result.get('time', 'N/A')}s"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔍 Otra búsqueda", callback_data='consult')],
            [InlineKeyboardButton("📋 Menú Principal", callback_data='restart')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            response_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    return MENU


async def query_dni_api(dni: str) -> dict:
    """Consulta la API de Perú"""
    try:
        url = f"{API_BASE_URL}/{dni}?api_token={API_TOKEN}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                return {
                    'error': False,
                    'data': data['data'],
                    'time': round(data.get('time', 0), 2)
                }
            else:
                return {
                    'error': True,
                    'message': '❌ DNI no encontrado en la base de datos.\n\nVerifica el número e intenta nuevamente.'
                }
        else:
            return {
                'error': True,
                'message': '❌ Error al conectar con la API.\n\nIntenta de nuevo más tarde.'
            }
    except requests.exceptions.Timeout:
        return {
            'error': True,
            'message': '❌ Tiempo de espera agotado.\n\nIntenta de nuevo.'
        }
    except Exception as e:
        logger.error(f"Error en query_dni_api: {e}")
        return {
            'error': True,
            'message': f'❌ Error: {str(e)}'
        }


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela la consulta actual"""
    await update.message.reply_text(
        "❌ Operación cancelada.\n\nUsa /start para volver al menú.",
        parse_mode='Markdown'
    )
    return MENU


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help"""
    help_text = (
        "📚 *AYUDA - Bot de Consulta de DNI*\n\n"
        "🎯 *Comandos disponibles:*\n"
        "/start - Menú principal\n"
        "/help - Esta ayuda\n"
        "/cancel - Cancelar operación\n\n"
        "📋 *Cómo usar el bot:*\n"
        "1. Usa /start\n"
        "2. Presiona 'Conectar' y espera 15 segundos\n"
        "3. Envía un DNI (8 dígitos)\n"
        "4. Recibe la información\n\n"
        "⚠️ El servidor está en plan free, puede tardar en responder."
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


def main():
    """Función principal"""
    if not TOKEN or not API_TOKEN:
        logger.error("Error: TOKEN o API_TOKEN no configurados")
        return
    
    # Crear aplicación
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dni_input))
    
    # Iniciar bot
    logger.info("🤖 Bot iniciado - Esperando mensajes...")
    
    if os.getenv('NODE_ENV') == 'production':
        # Modo webhook para Render
        webhook_url = os.getenv('WEBHOOK_URL')
        port = int(os.getenv('PORT', 3000))
        
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"{webhook_url}/{TOKEN}"
        )
    else:
        # Modo polling para desarrollo
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
