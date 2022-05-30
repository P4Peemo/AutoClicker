from schedule import repeat, every
from food_talk.controllers.cooking_controller import CookingController

controller = CookingController()

@repeat(every().sunday.at("00:01"))
@repeat(every().tuesday.at("08:01"))
@repeat(every().thursday.at("16:01"))
def temple_assembly_selection():
    controller.temple_assembly_selection()

@repeat(every().day.at("00:05"))
@repeat(every().day.at("08:05"))
@repeat(every().day.at("10:05"))
@repeat(every().day.at("12:05"))
@repeat(every().day.at("14:05"))
@repeat(every().day.at("16:05"))
@repeat(every().day.at("18:05"))
@repeat(every().day.at("20:05"))
@repeat(every().day.at("22:05"))
def buffet_dish_cooking():
    controller.buffet_dish_cooking()

@repeat(every().day.at("00:10"))
@repeat(every().day.at("06:10"))
@repeat(every().day.at("12:10"))
@repeat(every().day.at("18:10"))
def temple_assembly_dish_cooking():
    controller.temple_assembly_dish_cooking()

@repeat(every().day.at("00:30"))
def customer_wave_creation():
    controller.customer_wave_creation(3)

@repeat(every().day.at("00:15"))
@repeat(every().day.at("08:15"))
@repeat(every().day.at("10:15"))
@repeat(every().day.at("12:15"))
@repeat(every().day.at("14:15"))
@repeat(every().day.at("16:15"))
@repeat(every().day.at("18:15"))
@repeat(every().day.at("20:15"))
@repeat(every().day.at("22:15"))
def locked_dish_cooking():
    controller.locked_dish_cooking()

@repeat(every().day.at("23:15"))
@repeat(every().day.at("23:30"))
@repeat(every().day.at("23:45"))
def eggplant_meal_cooking():
    controller.eggplant_meal_cooking()


if __name__ == '__main__':
    controller.customer_wave_creation(1)