# coding=utf-8
import time
from random import shuffle
from pyautogui import click, getWindowsWithTitle, locateAllOnScreen, position, __version__

buttons = {
    'hamburger_btn': (100, 400),
    'kitchen_round_btn': (150, 320),
    'canteen_btn_in_kitchen': (960, 230),
    'kitchen_btn_in_canteen': (950, 950),
    'retrieve_dish_btn': (1620, 915),
    'pot_locations': [(360, 700), (660, 700), (960, 700), (1260, 700), (1560, 700)],
    'stove_locations': [(360, 810), (660, 810), (960, 810), (1260, 810), (1560, 810)],
    'display_customer_wave_btn': (1730, 210),
    'start_customer_wave_btn': (800, 840),
    'customer_wave_dishes': [
        (965, 525), (1005, 545),
        (325, 200), (450, 215), (575, 200), (1350, 200), (1475, 215), (1600, 200),
        (995, 590), (885,530),
        (325, 465), (450, 480), (575, 465), (1375, 465), (1495, 480), (1610, 465),
        (1010, 625), (940, 615),
        (400, 630), (545, 645), (690, 630), (1225, 630), (1370, 645), (1515, 630),
    ],
    'display_buffets_btn': (310, 940),
    'buffets_locations': [(330, 300), (330, 470), (330, 640), (330, 810)],
    'buffet_check_out_btn': (1720, 860),
    'display_temple_assemblies_btn': (180, 940),
    'first_exotic_search_btn': (250, 490),
    'online_reward_btn': (1080, 170),
    'claim_online_reward_btn': (1370, 650),
    'main_page_character_location': (580, 540),
    'butler_page_entry': (400, 835),
    'first_gift_location': (1280, 280),
    'gift_btn': (1620, 815),
    'back_btn': (150, 80),
    'character_list_entry': (1600, 950),
    'character_add_btn': (1570, 250),
    'add_rabbit_btn': (1690, 415),
    'upgrade_btn': (1600, 800)
}

class SwyController:
    '''
    SwyController is to automate boring clicking of dish cooking in the game named
    **the Tale of Food**. Currently it requires the game emulator to be a maximized
    window and NOT fullscreen.
    '''

    def __init__(self, windowTitle='Gameloop'):
        self.windowTitle = windowTitle
        self.__swy_window = None

    def activate_window(self):
        try:
            self.__swy_window = getWindowsWithTitle(self.windowTitle)[0]
        except:
            print(f'No window with {self.windowTitle} is found, please check your\
                window name.')
            return
        try:
            self.__swy_window.activate()
            self.__swy_window.maximize()
        except:
            # some time it throws pyGetWindowException, this fixes the problem.
            self.__swy_window.minimize()
            self.__swy_window.maximize()
            self.__swy_window.activate()
        print(f'Window size: {self.__swy_window.size}')
        time.sleep(1)

    def minimize_window(self):
        self.__swy_window.minimize()
        time.sleep(1)

    def _get_batch_pos(self, img, confidence=1.0, isShuffling=False):
        if not img:
            return []
        boxes = list(locateAllOnScreen(img, confidence=confidence))
        boxes.sort(key=lambda x: (x.top, x.left))
        boxes = [box for i, box in enumerate(boxes)
                    if i == 0 or
                        (abs(box.left - boxes[i - 1].left) >= 50 or
                            abs(box.top - boxes[i - 1].top) >= 50)]
        boxes = list(map(lambda x: (x.left, x.top), boxes))

        if isShuffling:
            shuffle(boxes)
        return boxes

    def go_back_to_main(self):
        click(buttons['back_btn'])
        time.sleep(5)
    
    def click_bottom_blank(self):
        click(960, 900)
        time.sleep(1)

    

    
if __name__ == '__main__':
    print(__version__)
    controller = SwyController()
    controller.activate_window()
    time.sleep(2)
    print(position()) 
    controller.minimize_window()
