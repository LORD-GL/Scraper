import funcs
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
class Conf:
    ACCESSORS_LIST = [549745613, 852489448]
    driver = None
    main_keyboard = None
    update_keyboard = None

    @classmethod
    def configPage(cls):
        cls.driver = funcs.set_driver()
        funcs.close_windows(cls.driver)
        funcs.setscales(cls.driver)

    @classmethod
    def closePage(cls):
        funcs.close_driver(cls.driver)

    @classmethod
    def set_keyboards(cls):
        # Создаем массив кнопок
        keyboard1 = [[InlineKeyboardButton("Купить подписку", callback_data="subscribe"),
                    InlineKeyboardButton("Объемы", callback_data="amounts")],
                    [InlineKeyboardButton("Помощь админа", callback_data="help"), 
                    InlineKeyboardButton("Теория", callback_data="theory")]
                    ]

        keyboard2 = [[InlineKeyboardButton("Обновить данные", callback_data="update")]]

        # Создаем объекты InlineKeyboardMarkup
        cls.main_keyboard = InlineKeyboardMarkup(keyboard1)
        cls.update_keyboard = InlineKeyboardMarkup(keyboard2)