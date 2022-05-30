# coding=utf-8
from time import sleep
from random import shuffle
from pyautogui import click, getWindowsWithTitle, locateAllOnScreen, position, __version__

from food_talk.helpers.button import Button

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
        sleep(1)

    def minimize_window(self):
        self.__swy_window.minimize()
        sleep(1)

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
        click(Button.BACK.POS)
        sleep(5)
    
    def click_bottom_blank(self):
        click(960, 900)
        sleep(1)

    def click_bottom_left_blank(self):
        click(120, 900)
        sleep(1)
    
    def click_top_blank(self):
        click(960, 135)
        sleep(1)

    
if __name__ == '__main__':
    print(__version__)
    controller = SwyController()
    controller.activate_window()
    sleep(2)
    print(position()) 
    controller.minimize_window()
