from subprocess import Popen
from time import sleep
from pyautogui import click, getActiveWindow, getWindowsWithTitle, locateOnScreen, screenshot

from food_talk.helpers.email_sender import send_email
from food_talk.helpers.button import Button

def launch_game(target_location):
    proc = Popen([target_location])
    # wait for the program to start up
    sleep(10)
    app_market = getActiveWindow()
    app_market.maximize()
    sleep(2)

    # switch to "我的" tab
    click(800, 70)
    sleep(5)

    # search for the logo and start the emulator
    while (logo_btn := locateOnScreen(Button.GAME_LOGO.SRC, confidence=0.9)) is None:
        sleep(5)
    click(logo_btn)
    print('Attempting to start the game')
    while getActiveWindow() == app_market:
        sleep(5)
    print('Starting up the game emulator')
    app_market.close()
    proc.kill()
    sleep(5)

    # wait and grab the game window, note that the emulator itself has an empty title.
    sleep(30)
    game_window = getWindowsWithTitle('Gameloop')[0]
    game_window.maximize()
    while (close_notif_btn := locateOnScreen(Button.CLOSE_NOTIF.SRC, confidence=0.9)) is None:
        sleep(10)
    click(close_notif_btn)
    print('closed notification board')
    sleep(2)

def login():
    # check whether needs logging in
    if android_btn := locateOnScreen(Button.PLAY_WITH_ANDROID.SRC, confidence=0.9):
        print('Requiring WeChat login authorization...')
        # agree to T&Cs
        click(Button.TERMS_N_CONDITIONS.POS)
        sleep(1)
        click(android_btn)

        # wait for authorization.
        sleep(5)
        screenshot(Button.LOGIN_QR_CODE.SRC)
        sleep(2)
        send_email(Button.LOGIN_QR_CODE.SRC)

    while (enter_game_btn := locateOnScreen(Button.ENTER_GAME.SRC, confidence=0.9)) is None:
        sleep(5)
    click(enter_game_btn)
    print('entering game...')
    sleep(15)

    # skip any posters popped up
    for _ in range(10):
        click(100, 800)
        sleep(1)

if __name__ == '__main__':
    launch_game()
    login()