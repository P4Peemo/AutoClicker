from schedule import run_pending, get_jobs
from time import sleep
from cooking_scheduler import *

if __name__ == '__main__':
    while True:
        run_pending()
        sleep(1)