from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from admin_panel import private
from conf import Conf
import funcs

""" Ассинхронная функция старт, срабатывает при комманде /start """
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Добрый день {update.effective_user.first_name}!\n"+
        "Для того, чтобы начать работу нажмите на кнопку: Объем\n"+
        "Чтобы купить подписку нажмите: Купить подписку", 
        reply_markup=Conf.main_keyboard
        )

""" ФУНКЦИЯ ПОКУПКИ ПОДПИСКИ"""
async def subscribe(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    await context.bot.send_message(chat_id=query.message.chat_id,
        text = "Тут можно будет купить подписку"
        )

""" ОБЪЕМЫ """
@private
async def amounts(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    message = ""
    message = funcs.collect_data(Conf.driver)
    await context.bot.send_message(chat_id=query.message.chat_id, text = message, reply_markup=Conf.update_keyboard)

""" ОБНОВИТЬ ОБЪЕМЫ """
@private
async def update(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    message = ""
    message = funcs.collect_data(Conf.driver)
    await query.edit_message_text(text = message, reply_markup=Conf.update_keyboard)

""" СВЯЗЬ С АДМИНОМ """
async def help(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    await context.bot.send_message(chat_id=query.message.chat_id, text =
        "Если у вас возникли проблемы во-время использования ботом\n"+
        "Свяжитесь с Админом: @LORD_GL" )

""" ТЕОРИЯ """
async def theory(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    await context.bot.send_message(chat_id=query.message.chat_id, text = "ТЕОРЕТИЧЕСКАЯ ЧАСТЬ БУДЕТ ТУТ")

""" Ассинхронная функция для неизвестных сообщений """
async def unknown(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=context._chat_id, 
        text=f"Прошу прощения, я не знаю что такое: {update.message.text}"
        )