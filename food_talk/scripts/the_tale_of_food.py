from schedule import run_pending, get_jobs
from time import sleep
from pyautogui import getWindowsWithTitle
from dotenv import dotenv_values

import food_talk.schedulers.cooking_scheduler
import food_talk.schedulers.routine_scheduler
from launch_game import launch_game, login

config = dotenv_values()
# TODO
# formalize methods to be protected or public
# add typing
# logging
# fail safe
# routine work

if __name__ == '__main__':
    if not getWindowsWithTitle('Gameloop'):
        launch_game(config['APP_MARKET_PATH'])
        login()
    all_jobs = get_jobs()
    print(f'{len(all_jobs)} tasks scheduled.')
    while True:
        run_pending()
        sleep(1)