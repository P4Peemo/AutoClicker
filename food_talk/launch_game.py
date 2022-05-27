from subprocess import Popen
import pyautogui
import os
import time
import pprint

pprint.pprint(pyautogui.getAllTitles())
'''
os.chdir(''.join([os.getcwd(), '\\food_talk\\assets\\game_launching']))

proc = Popen(["D:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe"])
time.sleep(10)
cw = pyautogui.getActiveWindow()
print(cw)
cw.maximize()
time.sleep(5)

if mine_btn := pyautogui.locateOnScreen('mine.png', 0.9):
    pyautogui.click(mine_btn.left, mine_btn.top)

while (logo_btn := pyautogui.locateOnScreen('the_tale_of_food_logo.png', 0.9)) is None:
    time.sleep(5)

pyautogui.click(logo_btn.left, logo_btn.top)
print('starting game')
time.sleep(30)
cw = pyautogui.getActiveWindow()
cw.maximize()
print(cw)
while (close_notif_btn := pyautogui.locateOnScreen('close_notif_button.png', 0.9)) is None:
    time.sleep(5)
pyautogui.click(close_notif_btn.left, close_notif_btn.top)
print('clicked close')
while (enter_game_btn := pyautogui.locateOnScreen('enter_game_button.png', 0.9)) is None:
    time.sleep(5)
pyautogui.click(enter_game_btn.left, enter_game_btn.top)
print('clicked enter')
time.sleep(10)

for _ in range(10):
    pyautogui.click(100, 900)
    time.sleep(2)
'''