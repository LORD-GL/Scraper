import logging
import os
from telegram import LabeledPrice
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder
from telegram.ext import CallbackQueryHandler, filters, PreCheckoutQueryHandler
import stripe

stripe.api_key = "sk_test_51MdcIXFPN4tXRAOnV2UxgeOUoaMns4pRTHQw1tgMBd9xuIvyMcKdwfuJwtdWklaOFDURl18NCLsS0uSgaFPyMx6S006pXF4DIP"

# Создание объекта бота
bot = ApplicationBuilder().token("5926902754:AAGmRe9XBGaFkDX1q1aRq7S74OhFSWeM7ZQ").build()

# Определение логгера
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Обработка команды "start"
async def start(update, context):
    await update.message.reply_text('Добро пожаловать в магазин!')

# Обработка команды "invoice"
async def send_invoice(update, context):
    chat_id = update.effective_chat.id # update.message.chat_id

    # Установка настроек оплаты
    price = [LabeledPrice('Product', 100)]
    
    await context.bot.send_invoice(  # Отправка инвойса
        chat_id=chat_id,
        title='Bot',
        description='Купить и получить доступ к боту!',
        payload='payload',
        provider_token='284685063:TEST:YTllMWZjMmUwNWMz',
        start_parameter='payment',
        currency='eur',
        prices=price,
        need_shipping_address=False,
    )

# Обработка ответа на запрос на платеж
def precheckout_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text('Processing payment...')
    payment_intent_client_secret = query.invoice_payload
    try:
        # Подтверждение платежа
        payment_intent = stripe.PaymentIntent.confirm(payment_intent_client_secret)
        query.edit_message_text('Payment successful!')
    except Exception as e:
        print(e)
        query.edit_message_text('Payment failed!')

bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT, send_invoice))
#precheckout_handler = PreCheckoutQueryHandler(precheckout_callback)
bot.add_handler(CallbackQueryHandler(precheckout_callback, pattern='.*'))
bot.run_polling()
