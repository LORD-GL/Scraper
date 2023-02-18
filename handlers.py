from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from admin_panel import private

""" Ассинхронная функция старт, срабатывает при комманде /start """
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")

""" ФУНКЦИЯ ПОКУПКИ ПОДПИСКИ"""
async def subscribe(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Тут можно будет купить подписку")

""" ОБЪЕМЫ """
@private
async def amounts(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("ТУТ БУДУТ ДАННЫЕ ИЗ БИРЖ")

""" СВЯЗЬ С АДМИНОМ """
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("СВЯЗЬ С АДМИНОМ БУДЕТ ТУТ")

""" ТЕОРИЯ """
async def theory(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("ТЕОРЕТИЧЕСКАЯ ЧАСТЬ БУДЕТ ТУТ")

""" Ассинхронная функция для неизвестных сообщений """
async def unknown(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=context._chat_id, text=f"Прошу прощения, я не знаю что такое: {update.message.text}")
