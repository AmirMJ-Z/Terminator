import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from script import *
import cv2
import numpy as np

color = np.array([52, 159, 19], dtype = 'uint8')

auto_detect_position_boolean = False

position = (802, 753)
tab_count = 0

root = tk.Tk()
root.iconbitmap('./icon.ico')
ico = Image.open('TerminatorIcon.png')
photo = ImageTk.PhotoImage(ico)

time_offset = 0
prev_mill = 0

def auto_detect_position():
    global position
    global color
    global auto_detect_position_boolean
    auto_detect_position_boolean = True
    positions_x = []
    positions_y = []

    im  = pyautogui.screenshot()
    im.save('screenshot.jpg')

    im  = cv2.imread('./screenshot.jpg') 
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if int(im[i, j][0]) == int(color[0]) and int(im[i, j][1]) == int(color[1]) and int(im[i, j][2]) == int(color[2]):
                positions_x.append(i)
                positions_y.append(j)

    if positions_x == [] or positions_y == []:
        auto_detect_position_boolean = False
        return False
    
    pos_1 = (positions_x[0], positions_y[0])
    pos_2 = (positions_x[-1], positions_y[-1])

    position = (int((pos_1[0] + pos_2[0])/2), int((pos_1[1] + pos_2[1])/2))
    

def initialize_window():
    root.geometry("600x920")
    root.title('TERMINATOR BOT')

    root.wm_iconphoto(False, photo)
    root.iconphoto(False, photo)

initialize_window()

title_image = tk.Label(root, image=photo)
title_image.pack(pady=20)

clock_label = tk.Label(root, text = '', font=("Arial", 20, "bold"), fg='blue', bg = 'lightblue')
clock_label.pack(pady=10)

progress_bar = tk.ttk.Progressbar(length = 215)
progress_bar.pack()

def update_progress_bar():
    global progress_bar
    global prev_mill

    mill = get_time(time_offset).microsecond
    mill = mill/10000
    progress_bar.step(-1 * prev_mill)
    progress_bar.step(mill)

    prev_mill = mill
    root.after(1, update_progress_bar)

update_progress_bar()

def update_time():
    global time_offset
    time = get_time(time_offset)
    clock_label.config(text=time)
    root.after(1, update_time)

update_time()

cal_title = tk.Label(root, text = 'Calibration Options', font=("Arial", 15, "bold"), fg='blue', bg = 'lightblue')
cal_title.pack(pady=20)

cal_time_offset_text_input = tk.Text(root, width=25, height=1)
cal_time_offset_text_input.pack(pady=10)

def calibrate_time():
    global time_offset

    messagebox.showinfo("Time Calibration", "TERMINATOR uses time.ir to know the exact local time (Tehran, Iran).\nYou can visit the website yourself to make sure everything is right.\n\nSUPER IMPORTANT NOTE:\nTHE TERMINATION PROCESS BY ITSELF TAKES ABOYT 0.65s, SO AFTER CALIBRATING THE TIMER WITH THE SOURCE, PUT THIS DELAY INTO CONSIDERATION AS WELL.")
    text = cal_time_offset_text_input.get('1.0', tk.END).strip()
    if text == '':
        return
    time_offset = float(text)
    update_time()

cal_time = tk.Button(root, text = 'Calibrate Time', activebackground='lightblue', highlightbackground='blue', bg = 'lightblue', command=calibrate_time)
cal_time.pack(pady=10)

def screenshot():
    global position
    global screenshot_image_label

    im  = pyautogui.screenshot()
    im.save('screenshot.jpg')

    im  = cv2.imread('./screenshot.jpg')

    for i in range(im.shape[0]):
        im[i, position[1]] = np.array([0, 255, 0], dtype = 'uint8')

    for i in range(im.shape[1]):
        im[position[0], i] = np.array([0, 255, 0], dtype = 'uint8')

    cv2.imwrite('screenshot.jpg', im)

    screenshot_image = Image.open('screenshot.jpg')
    screenshot_image.show()

cal_pos_offset_text_input = tk.Text(root, width=25, height=1)
cal_pos_offset_text_input.pack(pady=10)

def calibrate_pos():
    global position
    global auto_detect_position_boolean
    auto_detect_position_boolean = False
    pos = cal_pos_offset_text_input.get('1.0', tk.END)
    pos = pos.strip()

    if pos == '':
        screenshot()
        messagebox.showinfo("Position Calibration", "This is the position set for the mouse.\nThe screenshot with the mouse coordinates will also be updated.")
        return
    
    pos = pos.split(',')
    position = (int(pos[1]), int(pos[0]))
    screenshot()
    messagebox.showinfo("Position Calibration", "Mouse position updated successfuly, here is the updated position.\nThe screenshot with the mouse coordinates will also be updated.")

cal_pos_button = tk.Button(root, text = 'Calibrate Position', activebackground='lightblue', highlightbackground='blue', bg = 'lightblue', command=calibrate_pos)
cal_pos_button.pack(pady=10)

def auto_calibrate_position():
    result = auto_detect_position()

    if result == False:
        messagebox.showwarning("Position Calibration", "Auto calibration process failed.")
        return

    messagebox.showinfo("Position Calibration", "This is the position automatically set for the mouse.\nThe screenshot with the mouse coordinates will also be updated.")

    im  = cv2.imread('./screenshot.jpg')

    for i in range(im.shape[0]):
        im[i, position[1]] = np.array([0, 255, 0], dtype = 'uint8')

    for i in range(im.shape[1]):
        im[position[0], i] = np.array([0, 255, 0], dtype = 'uint8')

    cv2.imwrite('screenshot.jpg', im)

    screenshot_image = Image.open('screenshot.jpg')
    screenshot_image.show()


auto_cal_pos_button = tk.Button(root, text = 'Auto Calibrate Position', activebackground='lightgreen', highlightbackground='green', bg = 'lightgreen', command=auto_calibrate_position)
auto_cal_pos_button.pack(pady=10)

exe_title = tk.Label(root, text = 'Execution', font=("Arial", 15, "bold"), fg='blue', bg = 'lightblue')
exe_title.pack(pady=20)

tab_count_input = tk.Text(root, width=25, height=1)
tab_count_input.pack(pady=10)

def set_tab_count():
    global tab_count
    tab_count = int(tab_count_input.get('1.0', tk.END))
    messagebox.showinfo("Course Count", f"The Course Count variable was set to {tab_count} successfuly.")

tab_count_button = tk.Button(root, text = 'Set Course Count', activebackground='lightblue', highlightbackground='blue', bg = 'lightblue', command=set_tab_count)
tab_count_button.pack(pady=10)

def terminate():
    for i in range(tab_count):
        if auto_detect_position_boolean:
            auto_detect_position()
        time.sleep(0.1)
        click(position)
        alt_tab()

exe_button = tk.Button(root, text = 'TERMINATE', activebackground='pink', highlightbackground='red', bg = 'pink', fg = 'red', command=terminate)
exe_button.pack(pady=10)

def auto_terminate():
    messagebox.showwarning("Auto Termination", "The auto termination loop started.\nThe program will be executed at 8:00 AM.\n\nCLOSE THE PROGRAM TO ABORT THE AUTO TERMINATION PROCESS")

    while True:
        time = datetime.datetime.now()
        if time.hour == 8:
            terminate()
            break

auto_exe_button = tk.Button(root, text = 'AUTO TERMINATE', activebackground='pink', highlightbackground='red', bg = 'pink', fg = 'red', command=auto_terminate)
auto_exe_button.pack(pady=10)

def show_credits():
    messagebox.showinfo("Credits", "Amirreza Mirjalily\nElectrical Engineering Student at Sharif University of Tcehnology\n\nSeptember 2024")

credits = tk.Button(root, text = 'CREDITS', activebackground='lightgreen', highlightbackground='green', bg = 'lightgreen', fg = 'green', command=show_credits)
credits.pack(pady=10)

frame = tk.Frame()
frame.pack()

root.mainloop()
