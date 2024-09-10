
import pyautogui
import time
import datetime

position_sc = (753, 802)

def check_time(r, time):
    if time in r.text:
        return True
    return False

def click(pos):
    pyautogui.moveTo((pos[0], pos[1]))
    pyautogui.click(pos[0], pos[1])

def move(pos):
    pyautogui.moveTo((pos[0], pos[1]))

def alt_tab():
    pyautogui.hotkey('ctrl', 'tab')

def execution():
    for i in range(4):
        time.sleep(0.5)
        click(position)
        alt_tab()

def get_sign(num):
    if num > 0:
        return 1
    return -1

def get_time(time_offset):
    time_change = datetime.timedelta(seconds=time_offset)
    
    return (datetime.datetime.now() + time_change).time()

move((100, 100))

        
    



