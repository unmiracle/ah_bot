import pyautogui
import time
import multiprocessing
import random
import keyboard

# locations
RESET_LOCATION = (2340, 323)
FIRST_ITEM_LOCATION = (2025, 485)
AUCTION_HOUSE_LOCATION = (2290, 380)
DYNAMIC_COUNT_FROM_LOCATION = (2334, 509)
ITEM_HEADER_LOCATION = (810, 494)

# colors
ITEM_HEADER_COLOR = (169, 121, 203)

# misc
PIXELS_OFFSET = 70

# глобальные флаги
is_buy_enabled = multiprocessing.Value('b', True)  # Покупка разрешена
running = multiprocessing.Value('b', True)  # Выполнение процессов


# Функция для кликов по RESET
def click_reset(stop_clicking):
    while running.value:
        if not stop_clicking.is_set():  # Если нет команды остановки кликов
            pyautogui.click(RESET_LOCATION[0], RESET_LOCATION[1])
            # print('click')
            time.sleep(0.01)  # Задержка между кликами
        else:
            time.sleep(0.1)  # Проверяем каждый момент, но не кликаем


# Функция для выполнения анти-AFK
def anti_afk(stop_clicking):
    while running.value:
        time.sleep(10 * 60)  # Таймер анти-AFK (20 минут)

        stop_clicking.set()  # Останавливаем клики на время анти-AFK

        # time.sleep(5)
        # print('anti-afk executed')
        keyboard.press_and_release('esc')
        time.sleep(2)
        keyboard.press('w')
        time.sleep(random.uniform(0.1, 0.2))
        keyboard.release('w')
        move_and_click(AUCTION_HOUSE_LOCATION[0], AUCTION_HOUSE_LOCATION[1], 0.5)
        time.sleep(5)

        pyautogui.moveTo(RESET_LOCATION[0], RESET_LOCATION[1], 0.5)

        stop_clicking.clear()  # Возобновляем клики после завершения анти-AFK


# Функция подсчета количества символов в цене
def count_digits():
    x = DYNAMIC_COUNT_FROM_LOCATION[0]
    digits = 0
    no_applicable = False

    pixels = [pyautogui.pixel(x - i, DYNAMIC_COUNT_FROM_LOCATION[1]) for i in range(PIXELS_OFFSET)]

    for n in range(PIXELS_OFFSET):
        current_pixel_color = pixels[n]
        next_pixel_color = pixels[n - 1]

        # Проверка условия на наличие значений меньше 50
        has_value_less_than_20 = any(value < 20 for value in current_pixel_color)
        has_value_less_than_50 = any(value < 50 for value in current_pixel_color)
        has_value_more_than_50 = any(value < 50 for value in next_pixel_color)

        if has_value_less_than_50 and not has_value_more_than_50:
            digits += 1

        if has_value_less_than_20:
            no_applicable = True

    if digits == 2 and not no_applicable:
        print(pixels)

    return digits if not no_applicable else 0


# Функция покупки
def buy_item():
    global is_buy_enabled
    if not is_buy_enabled.value:
        return

    is_buy_enabled.value = False
    pyautogui.click(FIRST_ITEM_LOCATION[0], FIRST_ITEM_LOCATION[1])
    time.sleep(0.001)
    pyautogui.click(FIRST_ITEM_LOCATION[0], FIRST_ITEM_LOCATION[1])
    press_y(100)
    time.sleep(5)
    press_y(100)
    time.sleep(1)

    for n in range(30):
        pyautogui.click(RESET_LOCATION[0], RESET_LOCATION[1])
        # print('click')
        time.sleep(0.005)  # Задержка между кликами

    time.sleep(1)

    # is_buy_enabled.value = False  # Покупка выполнена, остановим


# Функция нажатия клавиши Y
def press_y(times):
    while times > 0:
        # keyboard.press_and_release('y')
        time.sleep(0.002)
        times -= 1


# Основная логика аукциона
def monitor_auction(stop_clicking):
    while running.value:
        # print('Checking....')
        # Проверка на совпадение цвета заголовка товара
        color_match = pyautogui.pixelMatchesColor(ITEM_HEADER_LOCATION[0], ITEM_HEADER_LOCATION[1], ITEM_HEADER_COLOR)

        if color_match:
            digits = count_digits()
            print('----- digits -------', digits)
            if digits == 2:  # Если цена состоит из двух символов
                stop_clicking.set()  # Останавливаем клики на время покупки
                buy_item()
                
                time.sleep(2)
                is_buy_enabled.value = True  # Включаем покупку снова
                stop_clicking.clear()  # После завершения покупки возобновляем клики

        time.sleep(0.02)  # Интервал между проверками


# Функция для отслеживания клавиши пробел
def check_keyboard(stop_clicking):
    while running.value:
        if keyboard.is_pressed('space'):
            print("Space pressed, stopping execution.")
            running.value = True  # Остановка всех процессов
            stop_clicking.set()  # Остановка кликов



            # time.sleep(5)
            # stop_clicking.clear()
            # break
        else:
            time.sleep(0.1)
        time.sleep(0.1)


# Функция перемещения и клика
def move_and_click(x, y, speed):
    pyautogui.moveTo(x, y, speed)
    pyautogui.click(x, y)


if __name__ == '__main__':
    print('Get Ready')
    time.sleep(3)
    print('Starting...')


    stop_clicking = multiprocessing.Event()  # Остановка процесса кликов

    # Создаем процессы
    # click_reset_process = multiprocessing.Process(target=click_reset, args=(stop_clicking,))
    auction_monitor_process = multiprocessing.Process(target=monitor_auction, args=(stop_clicking,))
    anti_afk_process = multiprocessing.Process(target=anti_afk, args=(stop_clicking,))
    keyboard_process = multiprocessing.Process(target=check_keyboard, args=(stop_clicking,))

    # Запускаем процессы
    # click_reset_process.start()
    auction_monitor_process.start()
    anti_afk_process.start()
    keyboard_process.start()

    # Ожидаем завершения процессов
    # click_reset_process.join()
    auction_monitor_process.join()
    anti_afk_process.join()
    keyboard_process.join()
