import logging
import warnings
from conf import Conf
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import ApplicationBuilder, filters, CallbackQueryHandler
from handlers import *

# Отключение предупреждений tracemalloc
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    # Создает обьект приложения по токену
    app = ApplicationBuilder().token("5926902754:AAGmRe9XBGaFkDX1q1aRq7S74OhFSWeM7ZQ").build()

    Conf.set_keyboards() # Создаёт всё кнопки

    Conf.configPage() # Настраиваем скрапер

    ##### Добавляем и инициализируем хэндреры #####
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(subscribe, pattern="subscribe"))  # Купить подписку
    app.add_handler(CallbackQueryHandler(amounts, pattern="amounts")) # Посмотреть объемы
    app.add_handler(CallbackQueryHandler(update, pattern="update")) # Обновить
    app.add_handler(CallbackQueryHandler(help, pattern="help")) # Помощь админа 
    app.add_handler(CallbackQueryHandler(theory, pattern="theory")) # Теория
    app.add_handler(MessageHandler(filters.TEXT, unknown))

    app.run_polling()

    Conf.closePage() # закрываем скрапер