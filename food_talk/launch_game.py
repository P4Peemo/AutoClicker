from subprocess import Popen
import pyautogui
import os
import time

from helpers.email_sender import send_email

os.chdir(''.join([os.getcwd(), '\\food_talk\\assets\\game_launching']))

def launch_game():
    proc = Popen(["D:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe"])
    # wait for the program to start up
    time.sleep(10)
    app_market = pyautogui.getActiveWindow()
    app_market.maximize()
    time.sleep(2)

    # switch to "我的" tab
    pyautogui.click(800, 70)
    time.sleep(5)

    # search for the logo and start the emulator
    while (logo_btn := pyautogui.locateOnScreen('the_tale_of_food_logo.png', 0.9)) is None:
        time.sleep(5)
    pyautogui.click(logo_btn.left, logo_btn.top)
    print('Attempting to start the game')
    while pyautogui.getActiveWindow() == app_market:
        time.sleep(5)
    print('Starting up the game emulator')
    app_market.close()
    time.sleep(5)

    # wait and grab the game window, note that the emulator itself has an empty title.
    time.sleep(30)
    game_window = pyautogui.getWindowsWithTitle('Gameloop')[0]
    game_window.maximize()
    while (close_notif_btn := pyautogui.locateOnScreen('close_notif_button.png', 0.9)) is None:
        time.sleep(10)
    pyautogui.click(close_notif_btn.left, close_notif_btn.top)
    print('closed notification board')
    time.sleep(2)

def login():
    # check whether needs logging in
    if android_btn := pyautogui.locateOnScreen('play_with_android_button.png', 0.9):
        print('Requiring WeChat login authorization...')
        # agree to T&Cs
        pyautogui.click(313, 928)
        time.sleep(1)
        pyautogui.click(android_btn.left, android_btn.top)

        # wait for authorization.
        time.sleep(5)
        login_authorisation_path = ''.join([os.getcwd(), '\\login_authorisation.png'])
        pyautogui.screenshot(login_authorisation_path)
        time.sleep(2)
        send_email(login_authorisation_path)

    while (enter_game_btn := pyautogui.locateOnScreen('enter_game_button.png', 0.9)) is None:
        time.sleep(5)
    pyautogui.click(enter_game_btn.left, enter_game_btn.top)
    print('entering game...')
    time.sleep(15)

    # skip any posters popped up
    for _ in range(10):
        pyautogui.click(100, 800)
        time.sleep(1)

launch_game()
login()