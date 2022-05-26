from subprocess import call
import schedule
import time

from swy_controller import SwyController

if __name__ == '__main__':
    controller = SwyController()
    schedule.every(15).minutes.do(controller.locked_dish_cooking)

    while True:
        schedule.run_pending()
        time.sleep(1)