import pyautogui
import time
import multiprocessing
import random
import keyboard
from modules.variables import Config
from modules.functions import Hotkeys

def click_reset():
    pyautogui.click(Config.reset_btn[0], Config.reset_btn[1])


def move_and_click(x, y, speed):
    pyautogui.moveTo(x, y, speed)
    pyautogui.click(x, y)


def press_y(times):
    while times > 0:
        keyboard.press_and_release('y')
        time.sleep(0.002)
        times -= 1

# Функция для кликов по RESET
def click_constantly(stop_clicking, running):
    while running.value:
        if not stop_clicking.is_set():  # Если нет команды остановки кликов
            click_reset()
            time.sleep(Config.reset_click_delay)  # Задержка между кликами
        else:
            time.sleep(0.1)  # Проверяем каждый момент, но не кликаем


# Функция для выполнения анти-AFK
def anti_afk(stop_clicking, running):
    while running.value:
        time.sleep(Config.afk_timeout_min * 60) 

        stop_clicking.set()

        keyboard.press_and_release('esc')
        time.sleep(2)
        keyboard.press('w')
        time.sleep(random.uniform(0.1, 0.2))
        keyboard.release('w')
        move_and_click(Config.auction_house_btn[0], Config.auction_house_btn[1], 0.5)
        time.sleep(5)

        pyautogui.moveTo(Config.reset_btn[0], Config.reset_btn[1], 0.5)

        stop_clicking.clear()  # Возобновляем клики после завершения анти-AFK


# Функция подсчета количества символов в цене
# def count_digits():
#     digits = 0
#     no_applicable = False

#     x = Config.count_from_location[0]
#     pixels = [pyautogui.pixel(x - i, Config.count_from_location[1]) for i in range(Config.pixels_offset)]

#     for n in range(Config.pixels_offset):
#         current_pixel_color = pixels[n]
#         next_pixel_color = pixels[n - 1]

#         has_value_less_than_20 = any(value < 20 for value in current_pixel_color)
#         has_value_less_than_50 = any(value < 50 for value in current_pixel_color)
#         has_value_more_than_50 = any(value < 50 for value in next_pixel_color)

#         if has_value_less_than_50 and not has_value_more_than_50:
#             digits += 1

#         if has_value_less_than_20:
#             no_applicable = True

#     if digits == 2 and not no_applicable:
#         print(pixels)

#     return digits if not no_applicable else 0



def count_digits():
    is_needle = True

    pixels = [pyautogui.pixel(i[0], i[1]) for i in Config.ten_sign]

    for n in pixels:
        has_value_less_than_50 = any(value < 50 for value in n)
        # print(n)
        if has_value_less_than_50 is True:
            is_needle = False 

    return is_needle



# Основная логика аукциона
def monitor_auction(stop_clicking, running, is_buy_enabled):
    while running.value:
        # print('Checking....', running.value)
        # Проверка на совпадение цвета заголовка товара
        color_match = pyautogui.pixelMatchesColor(Config.item_header_text[0], Config.item_header_text[1], Config.item_header_color)

        if color_match:
            is_needle = count_digits()
            # print('----- digits -------', digits)
            if is_needle:  # Если цена состоит из двух символов
                stop_clicking.set()  # Останавливаем клики на время покупки
                buy_item(is_buy_enabled)
                
                time.sleep(2)
                is_buy_enabled.value = True  # Включаем покупку снова
                stop_clicking.clear()  # После завершения покупки возобновляем клики

        time.sleep(Config.monitor_delay)  # Интервал между проверками


# def monitor_auction(stop_clicking, running, is_buy_enabled):
#     while running.value:
#         # print('Checking....', running.value)
#         # Проверка на совпадение цвета заголовка товара
#         color_match = pyautogui.pixelMatchesColor(Config.item_header_text[0], Config.item_header_text[1], Config.item_header_color)

#         if color_match:
#             digits = count_digits()
#             # print('----- digits -------', digits)
#             if digits == 2:  # Если цена состоит из двух символов
#                 stop_clicking.set()  # Останавливаем клики на время покупки
#                 buy_item(is_buy_enabled)
                
#                 time.sleep(2)
#                 is_buy_enabled.value = True  # Включаем покупку снова
#                 stop_clicking.clear()  # После завершения покупки возобновляем клики

#         time.sleep(Config.monitor_delay)  # Интервал между проверками

def buy_item(is_buy_enabled):
    if not is_buy_enabled.value:
        return

    is_buy_enabled.value = False
    pyautogui.click(Config.first_item_btn[0], Config.first_item_btn[1])
    time.sleep(0.001)
    pyautogui.click(Config.first_item_btn[0], Config.first_item_btn[1])
    press_y(100)
    timestr = time.strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = timestr + '.png'
    pyautogui.screenshot('images/' + filename)
    time.sleep(5)
    press_y(100)
    time.sleep(1)

    Config.catched += 1
    print('Config.catched', Config.catched)

    for n in range(30):
        click_reset()
        time.sleep(Config.reset_click_delay)

    time.sleep(1)


if __name__ == '__main__':
    print('Get Ready')
    time.sleep(3)
    print('Starting...')

    Hotkeys.start_recording()
    stop_clicking = multiprocessing.Event()  # Остановка процесса кликов

    # Создаем процессы
    click_constantly_process = multiprocessing.Process(target=click_constantly, args=(stop_clicking, Config.running,))
    auction_monitor_process = multiprocessing.Process(target=monitor_auction, args=(stop_clicking, Config.running, Config.is_buy_enabled,))
    anti_afk_process = multiprocessing.Process(target=anti_afk, args=(stop_clicking, Config.running,))

    # Запускаем процессы
    click_constantly_process.start()
    auction_monitor_process.start()
    anti_afk_process.start()

    # Ожидаем завершения процессов
    click_constantly_process.join()
    auction_monitor_process.join()
    anti_afk_process.join()
