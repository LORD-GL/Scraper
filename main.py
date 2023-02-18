import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import ApplicationBuilder, ContextTypes, filters

# Логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

""" 
Ассинхронная функция старт, срабатывает при комманде /start
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")
    
"""
Ассинхронная функция "эхо"
"""
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=context._chat_id, text=f"Вы отправили: {update.message.text}")

if __name__ == '__main__':
    # Создает обьект приложения по токену
    app = ApplicationBuilder().token("5926902754:AAGmRe9XBGaFkDX1q1aRq7S74OhFSWeM7ZQ").build()

    ##### Добавляем и инициализируем хэндреры #####
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, echo))

    app.run_polling()