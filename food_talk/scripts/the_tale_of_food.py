from schedule import run_pending, get_jobs
from time import sleep
from pyautogui import getWindowsWithTitle

import food_talk.schedulers.cooking_scheduler
from launch_game import launch_game, login

# TODO
# formalize methods to be protected or public
# add typing
# logging
# fail safe
# routine work
target_location = 'D:/Program Files/TxGameAssistant/AppMarket/AppMarket.exe'

if __name__ == '__main__':
    if not getWindowsWithTitle('Gameloop'):
        launch_game(target_location)
        login()
    all_jobs = get_jobs()
    print(f'{len(all_jobs)} tasks scheduled.')
    while True:
        run_pending()
        sleep(1)