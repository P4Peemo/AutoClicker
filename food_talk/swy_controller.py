# coding=utf-8
import os
import time
from random import shuffle
from subprocess import call
import pyautogui

os.chdir(''.join([os.getcwd(), '\\food_talk\\assets']))

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
    'buffet_check_out_btn': (1720, 860)
}

class SwyController:
    '''
    SwyController is to automate boring clicking of dish cooking in the game named
    **the Tale of Food**. Currently it requires the game emulator to be a maximized
    window and NOT fullscreen.
    '''

    def __init__(self, windowTitle='Gameloop'):
        self.windowTitle = windowTitle
        self.swy_window = None

    def activate_window(self):
        if not self.swy_window:
            try:
                self.swy_window = pyautogui.getWindowsWithTitle(self.windowTitle)[0]
            except:
                print(f'No window with {self.windowTitle} is found, please check your\
                    window name.')
                return

        self.swy_window.activate()
        self.swy_window.maximize()
        print(f'Window size: {self.swy_window.size}')
        time.sleep(1)

    def get_batch_pos(self, img, confidence=1.0):
        if not img:
            return []
        boxes = list(pyautogui.locateAllOnScreen(img, confidence=confidence))
        boxes.sort(key=lambda x: (x.top, x.left))
        boxes = [box for i, box in enumerate(boxes)
                    if i == 0 or
                        (abs(box.left - boxes[i - 1].left) >= 50 or
                            abs(box.top - boxes[i - 1].top) >= 50)]
        return boxes

    def enter_kitchen_from_main(self):
        print('Entering kitchen from main menu')
        pyautogui.click(buttons['hamburger_btn'])
        time.sleep(1)
        pyautogui.click(buttons['kitchen_round_btn'])
        time.sleep(3)

    def enter_canteen_from_kitchen(self):
        print('Entering cateen from kitchen')
        pyautogui.click(buttons['canteen_btn_in_kitchen'])
        time.sleep(5)
    
    def enter_kitchen_from_canteen(self):
        print('Entering kitchen from canteen')
        pyautogui.click(buttons['kitchen_btn_in_canteen'])
        time.sleep(5)

    # primary job is to make way for buffet cooking
    def clear_cooking_dishes(self, n=3):
        stoves = self.get_batch_pos('cooking_stove.png', 0.9)
        cleared_stoves = []
        for stove in stoves[:n]:
            pyautogui.click(stove.left + 100, stove.top - 50)
            time.sleep(1)
            if cancel_btn := pyautogui.locateOnScreen('cancel_cooking_button.png', confidence=0.9):
                pyautogui.click(cancel_btn)
                time.sleep(1)
                if confirm_cancel_btn := pyautogui.locateOnScreen('confirm_cancel_cooking_button.png', confidence=0.9):
                    pyautogui.click(confirm_cancel_btn)
                    time.sleep(1)
                    # click blank area in case unlocked new dishes
                    pyautogui.click(100, 540)
                cleared_stoves.append(stove)
                print('Cleared a dish cooking stove')
            else:
                print('cancel button not found.')
        return cleared_stoves

    def scroll_dish_menu(self):
        pyautogui.moveTo(400, 900)
        pyautogui.dragTo(400, 320, duration=5)
        time.sleep(1)
    
    def scroll_dish_menu_to_bottom(self):
        pyautogui.moveTo(400, 400)
        for _ in range(10):
            pyautogui.scroll(-1)
            time.sleep(1)

    def cook_locked_dishes(self):
        # collect cooked dishes
        pyautogui.click(1630, 930)
        time.sleep(1)
        pyautogui.click(1730, 930)
        # TODO cofirm new dish unlock notification, check whether it needs confirmation.
        # get available stoves
        stoves = self.get_batch_pos('ready_to_cook_stove.png', 0.9)
        scroll_times = 0
        not_enough_ingredients = False
        for stove in stoves:
            # not enough ingredient to cook any dish
            if not_enough_ingredients:
                pyautogui.click('close_cooking_menu_button.png')
                print('Please wait for the farm to restock before cooking more dishes')
                break

            pyautogui.click(stove.left, stove.top)
            time.sleep(1)
            
            # previous dishes are short of ingredients to cook
            for _ in range(scroll_times):
                self.scroll_dish_menu()
            locked_dishes = self.get_batch_pos('dish_able_to_unlock.png', 0.9)
            shuffle(locked_dishes)

            for dish in locked_dishes:
                pyautogui.click(dish.left, dish.top)
                if cook_btn := pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    pyautogui.click(cook_btn.left, cook_btn.top)
                time.sleep(1)
                if not pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    print('successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')
            else:
                cook_succeeded = False
                while scroll_times < 2 and not cook_succeeded:
                    self.scroll_dish_menu()
                    scroll_times += 1
                    locked_dishes = self.get_batch_pos('dish_able_to_unlock.png', 0.9)
                    shuffle(locked_dishes)
                    for dish in locked_dishes:
                        pyautogui.click(dish.left, dish.top)
                        if cook_btn := pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                            pyautogui.click(cook_btn.left, cook_btn.top)
                        time.sleep(1)
                        if not pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                            cook_succeeded = True
                            print('successfully cooked')
                            break
                        print('Not enough to cook, checking for next available dish...')

                # if previous locked dishes are not able to cook, use last resort to cook eggplants
                if not cook_succeeded:
                    self.scroll_dish_menu_to_bottom()
                    if eggplant_icon := pyautogui.locateOnScreen('oil_stew_eggplant.png'):
                        pyautogui.click(eggplant_icon.left, eggplant_icon.top)
                        if cook_btn := pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                            pyautogui.click(cook_btn.left, cook_btn.top)
                        time.sleep(1)
                        if not pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                            cook_succeeded = True
                            print('successfully cooked')
                        else:
                            not_enough_ingredients = True
        else:
            if pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                pyautogui.click('close_cooking_menu_button.png')
                print('Please wait for the farm to restock before cooking more dishes')

    def cook_buffet_dishes(self, n=3):
        # collect cooked dishes
        pyautogui.click(1630, 930)
        time.sleep(1)
        pyautogui.click(1730, 930)

        n = min(n, 5)
        ready_to_cook_stoves = self.get_batch_pos('ready_to_cook_stove.png', 0.9)
        ready_to_cook_stoves += self.clear_cooking_dishes(max(0, n - len(ready_to_cook_stoves)))
        buffet_dishes = []

        print('ready to cook dishes: ', ready_to_cook_stoves)    
        for stove in ready_to_cook_stoves[:n]:
            pyautogui.click(stove.left, stove.top)
            time.sleep(1)
            if not buffet_dishes:
                buffet_dishes += self.get_batch_pos('burn_tail_buffet.png', 0.9)
                buffet_dishes += self.get_batch_pos('eagle_rise_buffet.png', 0.9)
                buffet_dishes += self.get_batch_pos('search_spring_buffet.png', 0.9)
                buffet_dishes += self.get_batch_pos('deer_beep_buffet.png', 0.9)
            for dish in buffet_dishes:
                pyautogui.click(dish.left, dish.top)
                time.sleep(1)
                # if already cooking in progress
                if pyautogui.locateOnScreen('not_pending_dish.png'):
                    continue
    
                if cook_btn := pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    pyautogui.click(cook_btn.left, cook_btn.top)
                time.sleep(1)
                if not pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    print('successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')
            else:
                if close_btn := pyautogui.locateOnScreen('close_cooking_menu_button.png', confidence=0.9):
                    pyautogui.click(close_btn.left, close_btn.top)
                    time.sleep(1)
            # TODO
            # locate all buffet items location and check if need cooking
            # if need then click cook
            # if not enough ingredient
            # go to next to check if need cook, if last, close tab

    def check_buffet_dishes(self):
        pyautogui.click(buttons['display_buffets_btn'])
        buffets = buttons['buffets_locations'][::-1]
        time.sleep(1)
        dishes_to_cook = 0
        for buffet in buffets:
            pyautogui.click(buffet)
            time.sleep(1)
            submit_dish_locations = self.get_batch_pos('submit_buffet_item_button.png', 0.9)
            cook_dish_locations = self.get_batch_pos('cook_buffet_item_button.png', 0.9)
            dishes_to_cook += len(cook_dish_locations)
            
            # there is no valid buffet or the buffet is not finished yet
            if not submit_dish_locations or cook_dish_locations:
                if close_btn := pyautogui.locateOnScreen('close_cooking_menu_button.png', confidence=0.9):
                    pyautogui.click(close_btn.left, close_btn.top)
                continue

            for submit_dish_btn in submit_dish_locations:
                pyautogui.click(submit_dish_btn)
                time.sleep(1)
            pyautogui.click(buttons['buffet_check_out_btn'])
            time.sleep(1)
            # remove the reward notification
            pyautogui.click(900, 900)
            time.sleep(1)
        # click the blank place to close buffets
        pyautogui.click(960, 540)
        time.sleep(1)
        return dishes_to_cook

    def start_customer_wave(self):
        pyautogui.click(buttons['display_customer_wave_btn'])
        time.sleep(1)
        pyautogui.click(buttons['start_customer_wave_btn'])
        time.sleep(3)
        counter = 26
        customer_wave_dishes = buttons['customer_wave_dishes']
        while counter > 0:
            for dish in customer_wave_dishes:
                pyautogui.click(dish)
            counter -= 1
        time.sleep(10)
        pyautogui.click(960, 960)

if __name__ == '__main__':
    print(pyautogui.__version__)

    controller = SwyController()
    controller.activate_window()
    time.sleep(1)
    # controller.enter_kitchen_from_main()
    # controller.enter_canteen_from_kitchen()
    
    # while True:
    #     pyautogui.moveTo(390, 900)
    #     time.sleep(1)
    #     pyautogui.dragTo(390, 350, duration=5)
    controller.start_customer_wave()
    # print(pyautogui.position()) #390 900 390 270
    # controller.check_buffet_dishes()
    # dishes_to_cook = controller.check_buffet_dishes()
    # print(f'dishes to cook: {dishes_to_cook}')
    # controller.enter_kitchen_from_canteen()
    # controller.cook_buffet_dishes(dishes_to_cook)
