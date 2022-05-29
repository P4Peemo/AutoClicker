from time import sleep
from pyautogui import click, dragTo, locateOnScreen, moveTo, scroll

# from swy_controller import SwyController
from food_talk.controllers.swy_controller import SwyController
from food_talk.helpers.button import Button

class CookingController(SwyController):
    def scroll_dish_menu(self):
        moveTo(400, 900)
        dragTo(400, 350, duration=5)
        sleep(1)
    
    def scroll_dish_menu_to_bottom(self):
        moveTo(400, 400)
        for _ in range(10):
            scroll(-1)
            sleep(1)

    def enter_kitchen_from_main(self):
        print('Entering kitchen from main menu')
        click(Button.HAMBURGER.POS)
        sleep(1)
        click(Button.ROUND_KITCHEN.POS)
        sleep(5)

    def enter_canteen_from_kitchen(self):
        print('Entering cateen from kitchen')
        click(Button.KITCHEN_CANTEEN_ENTRY.POS)
        sleep(5)
    
    def enter_kitchen_from_canteen(self):
        print('Entering kitchen from canteen')
        click(Button.CANTEEN_KITCHEN_ENTRY)
        sleep(5)

    def collect_dishes(self):
        # collect cooked dishes
        click(Button.COLLECT_DISHES.POS)
        sleep(1)
        # Clear reward notif
        click(Button.COLLECT_DISHES.POS)
        sleep(1)
        click(Button.CONFIRM_UNLOCK_DISH.POS)
        sleep(1)
        # TODO consider unlocked dish
    
    # primary job is to make way for important cooking tasks
    def clear_cooking_dishes(self, cooking_indices):
        pots = Button.COOKING_POT_LOCS.POS
        cancel_cooking_locs = Button.CANCEL_COOKING_LOCS.POS
        stoves = Button.STOVE_LOCS.POS
        cleared_stoves = []

        for i in cooking_indices:
            self.collect_dishes()
            click(pots[i])
            sleep(1)
            click(cancel_cooking_locs[i])
            sleep(1)
            print(f'Cleared No.{i + 1} stove')
            cleared_stoves.append(stoves[i])
        return cleared_stoves

    def cook_locked_dishes(self):
        self.collect_dishes()

        # get available stoves
        stoves = self._get_batch_pos(Button.STOVE_LOCS.SRC, confidence=0.9)
        scroll_times = 0
        not_enough_ingredients = False

        for stove in stoves:
            # not enough ingredient to cook any dish
            if not_enough_ingredients:
                click(Button.CLOSE_MENU.POS)
                print('Please wait for the farm to restock before cooking more dishes')
                break

            click(stove)
            sleep(2)
            
            # make sure we are on the right panel of dish selections
            click(Button.ALL_CATEGORIES.POS)

            # previous dishes are short of ingredients to cook
            for _ in range(scroll_times):
                print('scrolling...')
                self.scroll_dish_menu()
            
            locked_dishes = self._get_batch_pos(Button.LOCKED_DISHES.SRC, 0.9, True)


            for dish_loc in locked_dishes:
                click(dish_loc)
                click(Button.COOK_NOW.POS)
                sleep(1)
                if not locateOnScreen(Button.COOK_NOW.SRC, confidence=0.9):
                    print('Successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')
            else:
                cook_succeeded = False
                # check for only first three screens of dishes
                while scroll_times < 2 and not cook_succeeded:
                    self.scroll_dish_menu()
                    scroll_times += 1
                    locked_dishes = self._get_batch_pos(Button.LOCKED_DISHES.SRC, 0.9, True)

                    for dish_loc in locked_dishes:
                        click(dish_loc)
                        click(Button.COOK_NOW.POS)
                        sleep(1)
                        if not locateOnScreen(Button.COOK_NOW.SRC, confidence=0.9):
                            print('Successfully cooked')
                            cook_succeeded = True
                            break
                        print('Not enough to cook, checking for next available dish...')

                # If previous locked dishes are not able to cook, use last resort to cook eggplants
                if not cook_succeeded:
                    cook_succeeded = self.cook_eggplant()
                not_enough_ingredients = not cook_succeeded
        else:
            if locateOnScreen('cook_button.png', confidence=0.9):
                click('close_cooking_menu_button.png')
                print('Please wait for the farm to restock before cooking more dishes')

    def cook_eggplant(self):
        self.scroll_dish_menu_to_bottom()
        if eggplant_dish := locateOnScreen(Button.EGGPLANT.SRC, confidence=0.9):
            click(eggplant_dish)
            click(Button.COOK_NOW.POS)
            sleep(1)
            if not locateOnScreen(Button.COOK_NOW.SRC, confidence=0.9):
                print('successfully cooked')
                return True
        else:
            print('No eggplant dish found')
        return False
    
    def prepare_stoves_for_cooking(self, n, reversed=False):
        def map_to_nearest_stoves(stove_locs):
            stove_indices = []
            for i, stove_loc in enumerate(stove_locs):
                x1, y1 = stove_loc
                for j, std_stove_loc in enumerate(Button.STOVE_LOCS.POS):
                    x2, y2 = std_stove_loc
                    if abs(x1 - x2) <= 50 and abs(y1 - y2) <= 50:
                        stove_locs[i] = std_stove_loc
                        stove_indices.append(j)
                        break
            return stove_indices

        n = min(n, 5)
        self.collect_dishes()
        ready_to_cook_stoves = self._get_batch_pos(Button.STOVE_LOCS.SRC, 0.9)
        ready_indices = map_to_nearest_stoves(ready_to_cook_stoves)
        stove_range = range(5 - n, 5) if reversed else range(n)
        cooking_indices = set(stove_range).difference(set(ready_indices))
        ready_to_cook_stoves += self.clear_cooking_dishes(cooking_indices)
        return list(stove_range)

    def cook_buffet_dishes(self, n):
        ready_to_cook_stoves = self.prepare_stoves_for_cooking(n)
        buffet_dishes = []

        for stove in ready_to_cook_stoves:
            click(stove)
            sleep(1)
            if not buffet_dishes:
                buffet_dishes += self._get_batch_pos(Button.BUFFET_BURN_TAIL.SRC, 0.9)
                buffet_dishes += self._get_batch_pos(Button.BUFFET_EAGLE_RISE.SRC, 0.9)
                buffet_dishes += self._get_batch_pos(Button.BUFFET_SEARCH_SPRING, 0.9)
                buffet_dishes += self._get_batch_pos(Button.BUFFET_DEER_BEEP, 0.9)
                buffet_dishes += self._get_batch_pos(Button.BUFFET_THOUSAND_OLD_GAY, 0.9)
                buffet_dishes += self._get_batch_pos(Button.BUFFET_POOR_FOREST, 0.9)

            for dish in buffet_dishes:
                click(dish)
                sleep(1)
                # if already cooking in progress
                if locateOnScreen(Button.NO_PENDING_DISH.SRC, confidence=0.9):
                    continue
    
                click(Button.COOK_NOW.POS)
                sleep(1)
                if not locateOnScreen(Button.COOK_NOW.SRC, confidence=0.9):
                    print('Successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')
            else:
                if close_btn := locateOnScreen(Button.CLOSE_MENU.SRC, confidence=0.9):
                    click(close_btn)
                    sleep(1)

    def check_buffet_dishes(self):
        click(Button.BUFFET_LIST_ENTRY)
        sleep(1)
        dishes_to_cook = 0
        for buffet in Button.BUFFET_LOCS[::-1]:
            click(buffet)
            sleep(1)
            submit_dish_locations = self._get_batch_pos(Button.SUBMIT_DISH.SRC, confidence=0.9)
            cook_dish_locations = self._get_batch_pos(Button.COOK_DISH.SRC, confidence=0.9)
            dishes_to_cook += len(cook_dish_locations)
            
            # there is no valid buffet or the buffet is not finished yet
            if not submit_dish_locations or cook_dish_locations:
                if close_btn := locateOnScreen(Button.CLOSE_MENU.SRC, confidence=0.9):
                    click(close_btn)
                    sleep(1)
                continue

            for submit_dish_btn in submit_dish_locations:
                click(submit_dish_btn)
                sleep(1)
            click(Button.CHECK_OUT.POS)
            sleep(1)
            # remove the reward notification
            self.click_bottom_blank()
        # click the blank place to close buffets
        self.click_bottom_blank()
        return dishes_to_cook

    def start_customer_wave(self):
        click(Button.CUST_WAVE_ENTRY.POS)
        sleep(1)
        click(Button.START_CUST_WAVE.POS)
        sleep(3)
        counter = 26
        customer_wave_dishes = Button.CUST_WAVE_DISHES
        while counter > 0:
            for dish in customer_wave_dishes:
                click(dish)
            counter -= 1
        sleep(10)
        self.click_bottom_blank()

    def select_temple_assembly(self):
        click(Button.TEMPLE_ASSEMBLY_ENTRY.POS)
        sleep(1)
        # TODO add five-coloured dirt image
        if shard_icon := locateOnScreen('ingredient_shard.png'):
            x, y = shard_icon
            click(x, y + 160)
        else:
            print('Unable to select temple assembly')

        sleep(1)
        click(Button.CLOSE_MENU.POS)
        sleep(1)

    def check_temple_assembly_dishes(self):
        click(Button.TEMPLE_ASSEMBLY_ENTRY.POS)
        sleep(1)
        submit_dish_locations = self._get_batch_pos(Button.SUBMIT_DISH.SRC, confidence=0.9)

        for submit_dish_btn in submit_dish_locations:
            click(submit_dish_btn)
            sleep(1)
            if submit_btn := locateOnScreen(Button.CONFIRM_SUBMIT_DISH.SRC, confidence=0.9):
                click(submit_btn)
                sleep(1)
            else:
                print('temple assembly dish submit button not found')

        cook_dish_locations = self._get_batch_pos(Button.COOK_DISH.SRC, confidence=0.9)
        if not cook_dish_locations:
            click(Button.CHECK_OUT.POS)
            sleep(1)
            self.click_bottom_blank()
        else:
            if close_btn := locateOnScreen(Button.CLOSE_MENU.SRC, confidence=0.9):
                click(close_btn)

        sleep(1)
        return len(cook_dish_locations)

    def cook_temple_assembly_dishes(self, n):
        ready_to_cook_stoves = self.prepare_stoves_for_cooking(n, True)
        temple_assembly_dishes = []

        for stove in ready_to_cook_stoves:
            click(stove)
            sleep(1)
            if not temple_assembly_dishes:
                temple_assembly_dishes = self._get_batch_pos(Button.TEMPLE_ASSEMBLY_ICON.SRC, confidence=0.9)
            for dish in temple_assembly_dishes:
                click(dish)
                sleep(1)
                # if already cooking in progress
                if locateOnScreen(Button.NO_PENDING_DISH.SRC):
                    continue
    
                click(Button.COOK_NOW.POS)
                sleep(1)
                if not locateOnScreen(Button.COOK_NOW.SRC, confidence=0.9):
                    print('Successfully cooked')
                    break
                print('Not enough to cook, checking for next available dish...')
            else:
                if close_btn := locateOnScreen(Button.CLOSE_MENU.SRC, confidence=0.9):
                    click(close_btn)
                    sleep(1)

    def locked_dish_cooking(self):
        self.activate_window()
        self.enter_kitchen_from_main()
        self.cook_locked_dishes()
        self.go_back_to_main()
        self.minimize_window()
    
    def buffet_dish_cooking(self):
        self.activate_window()
        self.enter_kitchen_from_main()
        self.enter_canteen_from_kitchen()
        n_dishes_to_cook = self.check_buffet_dishes()
        print(f'{n_dishes_to_cook} dishes of buffet pending...')
        self.enter_kitchen_from_canteen()
        self.cook_buffet_dishes(n_dishes_to_cook)
        self.go_back_to_main()
        self.minimize_window()
    
    def temple_assembly_selection(self):
        self.activate_window()
        self.enter_kitchen_from_main()
        self.enter_canteen_from_kitchen()
        self.select_temple_assembly()
        self.go_back_to_main()
        self.minimize_window()
    
    def temple_assembly_dish_cooking(self):
        self.activate_window()
        self.enter_kitchen_from_main()
        self.enter_canteen_from_kitchen()
        n_dishes_to_cook = self.check_temple_assembly_dishes()
        print(f'{n_dishes_to_cook} dishes of temple assembly pending...')
        self.enter_kitchen_from_canteen()
        self.cook_temple_assembly_dishes(n_dishes_to_cook)
        self.go_back_to_main()
        self.minimize_window()

    def customer_wave_creation(self):    
        self.activate_window()
        self.enter_kitchen_from_main()
        self.enter_canteen_from_kitchen()
        self.start_customer_wave()
        self.go_back_to_main()
        self.minimize_window()

if __name__ == '__main__':
    ct = CookingController()
    ct.activate_window()
    ct.cook_buffet_dishes(3)