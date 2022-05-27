from schedule import repeat, every
import os
from swy_controller import SwyController

os.chdir(''.join([os.getcwd(), '\\food_talk\\assets\\dish_cooking']))
controller = SwyController()

@repeat(every().sunday.at("00:01"))
@repeat(every().tuesday.at("08:01"))
@repeat(every().thursday.at("16:01"))
def temple_assembly_selection():
    controller.temple_assembly_selection()

@repeat(every().day.at("00:05"))
@repeat(every().day.at("04:05"))
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
@repeat(every().day.at("08:10"))
@repeat(every().day.at("16:10"))
def temple_assembly_dish_cooking():
    controller.temple_assembly_dish_cooking()

@repeat(every().day.at("00:15"))
@repeat(every().day.at("06:15"))
@repeat(every().day.at("12:15"))
@repeat(every().day.at("18:15"))
def customer_wave_creation():
    controller.customer_wave_creation()

@repeat(every().hour.at(":20"))
@repeat(every().hour.at(":30"))
@repeat(every().hour.at(":40"))
@repeat(every().hour.at(":50"))
def locked_dish_cooking():
    controller.locked_dish_cooking()
