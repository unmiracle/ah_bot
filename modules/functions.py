import os
from console.utils import set_title
from datetime import datetime
from modules.variables import Config

def clear():
    os.system('cls')



def exit_program(_=None):
    """Close the application"""
    os._exit(0)

def get_time():
    """
    Gets the time and date in the format:
    Year-Month-Day Hour-Minute-Second
    """
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# def is_win():
#     from sys import platform
#     if platform == "win32":
#         return True
#     else:
#         return False
    

class Hotkeys:
    def start_recording():
        from keyboard import add_hotkey
        def stop_checking_func():
            print('Trying to stop....')
            Config.running.value = False
            exit_program()
        
        print('Record started')
        add_hotkey('space',stop_checking_func)

    def stop_recording():
        from keyboard import clear_all_hotkeys
        clear_all_hotkeys()