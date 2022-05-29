from time import sleep
from pyautogui import click, locateOnScreen, scroll

from swy_controller import SwyController

class RoutineController(SwyController):
    # TODO complete exotic search functionality
    def __init__(self):
        super().__init__()
        self.cwd = ''.join([self.cwd, '/food_talk/assets/routine_fulfilling/'])

    def perform_exotic_search(self):
        click(buttons['hamburger_btn'])
        sleep(1)
        click(buttons['exotic_search_btn'])
    
    def claim_online_rewards(self):
        click(buttons['online_reward_btn'])
        sleep(1)
        click(buttons['claim_online_reward_btn'])
        sleep(1)
        self.click_bottom_blank()
    
    def interact_with_character(self):
        sleep(5)
        for _ in range(5):
            click(buttons['main_page_character_location'])
        sleep(1)
        click(buttons['butler_page_entry'])
        sleep(5)
        click(buttons['first_gift_location'])
        sleep(1)
        click(buttons['back_btn'])
        sleep(5)
    
    def upgrade_character(self):
        click(buttons['character_list_entry'])
        sleep(2)
        scroll(-1)
        sleep(1)
        if character_level_icons := self.__get_batch_pos('..\\daily_quest\character_level_icon.png', 0.9):
            click(character_level_icons[0])
            sleep(2)
            click(buttons['character_add_btn'])
            sleep(1)
            click(buttons['add_rabbit_btn'])
            sleep(1)
            click(buttons['upgrade_btn'])
            sleep(1)
            click(buttons['back_btn'])
            sleep(2)
        else:
            print('No level icon is found')
        click(buttons['back_btn'])
        sleep(2)