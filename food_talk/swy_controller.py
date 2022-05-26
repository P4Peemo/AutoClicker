# coding=utf-8
import os
import time
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
        stoves = self.get_batch_pos('cooking_stoves.png', 0.9)
        cleared_stoves = []
        for stove in stoves[:n]:
            pyautogui.click(stove.left, stove.top - 50)
            time.sleep(1)
            if cancel_btn := pyautogui.locateOnScreen('cancel_cooking_button.png', 0,9):
                pyautogui.click(cancel_btn)
                time.sleep(1)
                if confirm_cancel_btn := pyautogui.locateOnScreen('confirm_cancel_cooking_button.png', 0.9):
                    pyautogui.click(confirm_cancel_btn)
                    time.sleep(1)
                    # click blank area in case unlocked new dishes
                    pyautogui.click(100, 540)
                    cleared_stoves.append(stove)
                else:
                    print('confirm button not found')
            else:
                print('cancel button not found.')
        return cleared_stoves

    def cook_locked_dishes(self):
        # collect cooked dishes
        pyautogui.click(1630, 930)
        time.sleep(1)
        pyautogui.click(1730, 930)
        # TODO cofirm new dish unlock notification, check whether it needs confirmation.
        # get available stoves
        stoves = self.get_batch_pos('ready_to_cook_stove.png', 0.9)

        for stove in stoves:
            # not enough ingredient to cook any dish
            # TODO scroll the menu to continue search
            if pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                pyautogui.click('close_cooking_menu_button.png')
                break

            pyautogui.click(stove.left, stove.top)
            time.sleep(1)
            locked_dishes = self.get_batch_pos('dish_able_to_unlock.png', 0.9)

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
            if pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                pyautogui.click('close_cooking_menu_button.png')

    def cook_buffet_dishes(self, n=3):
        n = min(n, 5)
        ready_to_cook_stoves = self.get_batch_pos('ready_to_cook_stove.png', 0.9)
        ready_to_cook_stoves += self.clear_cooking_dishes(max(0, n - len(ready_to_cook_stoves)))
        buffet_dishes = []
        
        for stove in ready_to_cook_stoves:
            pyautogui.click(stove.left, stove.top)
            time.sleep(1)
            if not buffet_dishes:
                buffet_dishes += self.get_batch_pos('burn_tail_buffet.png', 0.9)
                buffet_dishes += self.get_batch_pos('eagle_rise_buffet.png', 0.9)
                buffet_dishes += self.get_batch_pos('search_spring_buffet.png', 0.9)
                # TODO add the last buffet pic
            
            for dish in buffet_dishes:
                pyautogui.click(dish.left, dish.top)
                time.sleep(1)
                # if already cooking in progress
                if pyautogui.locateOnScreen('not_pending_dish.png', confidence=0.9):
                    continue
    
                if cook_btn := pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    pyautogui.click(cook_btn.left, cook_btn.top)
                time.sleep(1)
                if not pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    print('successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')
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

if __name__ == '__main__':
    print(pyautogui.__version__)

    controller = SwyController()
    controller.activate_window()
    time.sleep(1)
    # controller.enter_kitchen_from_main()
    # controller.enter_canteen_from_kitchen()
    print(pyautogui.position())
    controller.cook_locked_dishes()
    # controller.cook_locked_dishes()