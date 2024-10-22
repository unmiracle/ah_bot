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

def is_win():
    from sys import platform
    if platform == "win32":
        return True
    else:
        return False
    

def is_focused():
    """
    Check if the application is in focus
    Returns True/False

    is_focused()
    """
    if is_win():
        import win32gui,win32process
        focus_window_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
        current_process_pid = os.getppid()

        return focus_window_pid == current_process_pid
    else:
        return True




class Hotkeys:
    def start_recording():
        """
        Start listening for keyboard hotkeys
        
        X = Exit Program | S = Save Remaining Lines
        """
        from keyboard import add_hotkey
        def stop_checking_func():
            """
            Terminate the thread pool
            """
            if is_focused():
                Config.stopping = True
        add_hotkey('x',stop_checking_func)
    def stop_recording():
        """Stop listening for hotkeys"""
        from keyboard import clear_all_hotkeys
        clear_all_hotkeys()