from schedule import repeat, every, run_all

from food_talk.controllers.routine_controller import RoutineController
from food_talk.controllers.cooking_controller import CookingController
controller = RoutineController()

@repeat(every().day.at("06:30"))
def claim_rewards():
    controller.claim_rewards()

@repeat(every().day.at("11:30"))
@repeat(every().day.at("17:30"))
@repeat(every().day.at("20:00"))
def claim_rice():
    controller.claim_rice()

@repeat(every().day.at("06:20"))
def single_customer_wave():
    CookingController().customer_wave_creation(1)

@repeat(every().day.at("05:10"))
@repeat(every().day.at("17:10"))
def exotic_expeditions():
    controller.exotic_expeditions()

@repeat(every().day.at("01:00"))
@repeat(every().day.at("13:00"))
@repeat(every().day.at("19:00"))
def make_dirt_purchase():
    controller.make_dirt_purchase()

if __name__ == '__main__':
    pass