from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time


""" 
Открывает страницу, настраивает окно 
и возвращает объект класса webdriver.Chome 
:return - driver
"""
def set_driver():
    options = webdriver.ChromeOptions() # создание объекта класса настройки
    options.add_argument("--headless") # уставновка безголового режима (без показывания окна браузера)
    options.add_argument('--log-level=3')  # установка уровня логирования
    options.add_argument('--log-file=binancelogfile.log') # перенаправление вывода в файл

    # Открываем веб-драйвер Chrome и переходим на страницу Binance
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.binance.com/en/trade/BTC_USDT?theme=dark&type=spot")

    time.sleep(5) # ждём 5 секунд, чтобы дать время странице прогрутиться

    return driver


""" 
Принимает cookies, закрывает диалоговое окно
"""
def close_windows(driver):
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


"""
Находит выпадающий список и устанавливает уровень масштабирования
"""
def setscales(driver):
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
def _get_data(driver):
    # Находим кнопку Buy\Sell и кликаем на нее
    regime_button = driver.find_elements(By.CLASS_NAME, "css-1meiumy")
    driver.execute_script("arguments[0].click();", regime_button[1])
    
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
def _get_price_values(line, askBid):
    # Находим все дочерние элементы с классом "text" и выводим их содержимое
    text_elements = line.find_all('div', {'class' : 'text'})
    # Находим элемент с классом "ask-light" и выводим его содержимое
    price_element = line.find('div', {'class' : f"{askBid}-light"})

    return [str(price_element.text), str(text_elements[0].text), str(text_elements[1].text.replace(',', ''))]


""" Устанавливает тип данных на нейтарльный (ask + bid) """
def _set_default(driver):
    buy_button = driver.find_elements(By.CLASS_NAME, "css-1meiumy")
    driver.execute_script("arguments[0].click();", buy_button[0])


"""
Собирает данные, парсит их и возвращает message,
в котором храняться все собранные данные ask/bid
"""
def collect_data(driver):

    message = ""
    orderbook = _get_data(driver) # Sell
    for line in orderbook:
        line_data = _get_price_values(line, 'ask')
        message += " - ".join(line_data) + "\n"
    message += "----------------\n"
    orderbook = _get_data(driver) # Buy 
    for line in orderbook:
        line_data = _get_price_values(line, 'bid')
        message += " - ".join(line_data) + "\n"
    _set_default(driver)
    return message


""" Закрывает страницу и драйвер"""
def close_driver(driver):
    # Закрываем веб-драйвер
    driver.quit()