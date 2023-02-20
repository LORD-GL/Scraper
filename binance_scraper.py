from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

# Импорт виртуального дисплея
from pyvirtualdisplay import Display
# from xvfbwrapper import Xvfb  ### для UNIX систем

# Импорт библиотки и модулей для цветного текста в консоли #
from colorama import init
from colorama import Fore, Style
init()
########

options = webdriver.ChromeOptions() # создание объекта класса настройки
#options.add_argument("--headless") # уставновка безголового режима (без показывания окна браузера)
options.add_argument('--log-level=3')  # установка уровня логирования
options.add_argument('--log-file=binancelogfile.log') # перенаправление вывода в файл

# Создания виртуального дисплея
# Xvfb() # ДЛЯ UNIX
#display = Display(visible=0, size=(800, 600))
#display.start()

# Открываем веб-драйвер Chrome и переходим на страницу Binance
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(5) # ждём 5 секунд, чтобы дать время странице прогрутиться 
driver.get("https://www.binance.com/en/trade/BTC_USDT?theme=dark&type=spot")

# Если нужно соглашаемся с cookies
try:
    # Автоматическое согласение со всеми cookies
    cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookie_button.click()
except:
    print("Here is no cookies to accept")
# Если есть приветственное диалоговое окно - убираем его
try:
    dialog_w = driver.find_element(By.CLASS_NAME, "css-4rbxuz")
    driver.execute_script("arguments[0].click();", dialog_w)
except:
    print("Here is no welcoming dialog window")

# находим выпадающий список и кликаем на него
scale = driver.find_element(By.CLASS_NAME, "tick-content")
# driver.execute_script("arguments[0].setAttribute('style', 'display: block;')", scale)
driver.execute_script("arguments[0].click();", scale)

# выбираем масштабирование в выпадающем списке
scale_options = driver.find_elements(By.CLASS_NAME, "css-o950o9")
if int(scale_options[3].text) == 50: # Проверяем. чтобы мы выбрали уровень масштабирования именно 50
    scale_options[3].click() 
else: # Выдаём ошибку, что уровень масштабирования не тот
    print(f"ERROR ERROR ERROR\nERROR LIST SCALE INDEX ERROR (INDEX {scale_options[3].text})!\nERROR ERROR ERROR")

""" 
Функция примимает на вход два аргумента:
    driver - объект класса Chrome модуля webdriver (Selenium)
    askBid - принимает на вход либо 'bid' либо 'ask' (настройка режима сбора данных) 

Функция кликает на кнопку в зависимости от режима, 
получает список данных (Цена, Объем(BTC), USDT)
и возвращает данные объектом класса BeautifulSoup

"""
def get_data(driver, askBid = 'bid'):
    # Находим кнопку Buy\Sell и кликаем на нее
    regime_button = driver.find_elements(By.CLASS_NAME, "css-1meiumy")
    driver.execute_script("arguments[0].click();", regime_button[1])

    time.sleep(2)

    # Получаем HTML-код страницы после нажатия на кнопку
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Находим тег div с классом "orderbook-progress" и выводим его содержимое
    orderbook = soup.find_all('div', {'class': 'orderbook-progress'})
    
    return orderbook

""" 
Функция парсит страку с данными о цене и объемах
Принимает: объект класса BeautifulSoup - line 
Возвращает данные в формате: Price, Amount(BTC), Amount(USDT)
"""
def get_price_values(line, askBid):
    # Находим все дочерние элементы с классом "text" и выводим их содержимое
    text_elements = line.find_all('div', {'class' : 'text'})
    # Находим элемент с классом "ask-light" и выводим его содержимое
    price_element = line.find('div', {'class' : f"{askBid}-light"})

    return int(price_element.text), float(text_elements[0].text), float(text_elements[1].text.replace(',', ''))

""" 
Функция принимает: 
    orderbook - список данных (Цена, Объем(BTC), USDT) объектом класса BeautifulSoup
    bidAsk - тип получаемых данных

Ничего не возвращает, но принтит данные в цвета=
"""
def print_data(orderbook, askBid):
    if askBid == "ask":
        print(Fore.RED+"", end="")
    elif askBid == "bid":
        print(Fore.GREEN+"", end="")

    # выводим в консоль полученные данные
    for line in orderbook:
        print(get_price_values(line, askBid))

# Устанавливает тип данных на нейтарльный (ask + bid)
def set_default(driver):
    buy_button = driver.find_elements(By.CLASS_NAME, "css-1meiumy")
    driver.execute_script("arguments[0].click();", buy_button[0])

### ПОЛУЧАЕМ ДАННЫЕ ###
for i in range(1):
    print(Fore.BLUE+"=========== ITERATION ===========")
    orderbook = get_data(driver, 'ask') # Sell
    print_data(orderbook, 'ask')
    print(Style.RESET_ALL+"", end="")
    print("----------------")
    orderbook = get_data(driver, 'bid') # Buy 
    print_data(orderbook, 'bid')
    set_default(driver)


# Закрываем веб-драйвер
driver.quit()
# Закрываем веб-дисплей
#display.stop()
