# coding=utf-8
import os
import time
import pyautogui

os.chdir(''.join([os.getcwd(), '\\food_talk\\assets']))

buttons = {
    'hamburger_btn': (100, 400),
    'kitchen_round_btn': (150, 320),
    'canteen_btn_in_kitchen': (960, 230),
    'retrieve_dish_btn': (1620, 915),
    'stove_locations': [(), (), (), (1265, 810), ()],
    'buffets_btn': (310, 940),
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

    def enter_kitchen_from_ms(self):
        pyautogui.click(buttons['hamburger_btn'])
        time.sleep(1)
        pyautogui.click(buttons['kitchen_round_btn'])
        time.sleep(3)

    def cook_locked_dishes(self):
        # get available stoves
        stoves = self.get_batch_pos('ready_to_cook.png', 0.9)

        for stove in stoves:
            pyautogui.click(stove.left, stove.top)
            time.sleep(1)
            dishes_locked = self.get_batch_pos('dish_able_to_unlock.png', 0.9)

            for dish in dishes_locked:
                pyautogui.click(dish.left, dish.top)
                if cook_btn := pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    pyautogui.click(cook_btn.left, cook_btn.top)
                time.sleep(1)
                if not pyautogui.locateOnScreen('cook_button.png', confidence=0.9):
                    print('successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')

    def enter_canteen_from_kitchen(self):
        pyautogui.click(buttons['canteen_btn_in_kitchen'])
        time.sleep(5)
    
print(pyautogui.__version__)

controller = SwyController()
controller.activate_window()
time.sleep(1)
# controller.enter_kitchen_from_ms()
# controller.enter_canteen_from_kitchen()
print(pyautogui.position())
# controller.cook_locked_dishes()