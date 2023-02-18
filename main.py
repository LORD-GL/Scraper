import logging
import warnings
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import ApplicationBuilder, filters
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

    ##### Добавляем и инициализируем хэндреры #####
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text("Купить подписку"), subscribe))
    app.add_handler(MessageHandler(filters.Text("Объемы"), amounts))
    app.add_handler(MessageHandler(filters.Text("Помощь админа"), help))
    app.add_handler(MessageHandler(filters.Text("Теория"), theory))
    app.add_handler(MessageHandler(filters.TEXT, unknown))

    app.run_polling()