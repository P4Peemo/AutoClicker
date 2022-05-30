from time import sleep
from pyautogui import click, locateOnScreen, scroll, position, moveTo, scroll

from food_talk.helpers.button import Button
from food_talk.controllers.swy_controller import SwyController

class RoutineController(SwyController):
    # TODO complete exotic search functionality
    # N.B. for issue with 8 sharp hours, we need to perform this every 12 hour
    def perform_exotic_searches(self):
        click(Button.HAMBURGER.POS)
        sleep(1)
        click(Button.FIRST_EXOTIC_SEARCH_PANEL_LOC.POS)
        sleep(2)
        for _ in range(4):
            click(Button.FIRST_EXOTIC_SEARCH_FULL_LOC.POS)
            sleep(1)
            click(Button.WELCOME_HOME.POS)
            sleep(1)
            self.click_bottom_blank()
            click(Button.WELCOME_HOME.POS)
            sleep(1)
        click(Button.CLAIM_EXOTIC_SKYWORK_STONE.POS)
        sleep(1)
        self.click_top_blank()
        click(Button.BACK.POS)
        sleep(2)
    
    def claim_online_rewards(self):
        click(Button.ONLINE_REWARD.POS)
        sleep(1)
        click(Button.CLAIM_ONLINE_REWARD.POS)
        sleep(1)
        self.click_bottom_blank()
    
    def interact_with_character(self):
        sleep(5)
        for _ in range(5):
            click(Button.MAIN_PAGE_CHAR_LOC.POS)
        sleep(1)
        click(Button.BUTLER_PAGE_ENTRY.POS)
        sleep(5)
        click(Button.FIRST_GIFT_LOC.POS)
        sleep(1)
        click(Button.BACK.POS)
        sleep(5)
    
    def upgrade_character(self):
        click(Button.CHAR_LIST_ENTRY.POS)
        sleep(2)
        scroll(-1)
        sleep(1)
        if character_level_icons := self.__get_batch_pos(Button.LEVEL_ICON.SRC, confidence=0.9):
            print(character_level_icons)
            click(character_level_icons[0])
            sleep(2)
            click(Button.ADD_CHAR_EXP.POS)
            sleep(1)
            click(Button.ADD_RABBIT.POS)
            sleep(1)
            click(Button.LEVELING_UP.POS)
            sleep(1)
            click(Button.BACK.POS)
            sleep(2)
        else:
            print('No level icon is found')
        click(Button.BACK.POS)
        sleep(2)
    
    def check_in(self):
        click(Button.SIGN_IN.POS)
        sleep(5)
        self.click_bottom_blank()
        self.click_bottom_left_blank()
    
    def make_wish(self):
        click(Button.CLAN_ENTRY.POS)
        sleep(1)
        click(Button.CLAN_ACTIVITIES_ENTRY.POS)
        sleep(1)
        click(Button.MAKE_WISH_PAGE_ENTRY.POS)
        sleep(1)
        # TODO add thanks functionality
        click(Button.MAKE_WISH_LIST_ENTRY.POS)
        sleep(1)
        if locateOnScreen(Button.CHAR_FULFILLED.SRC, confidence=0.9):
            print('character fulfilled, please select a new character.')
            click(Button.CLOSE_MAKE_WISH)
        else:
            click(Button.SELECT_WISHED_CHAR.POS)
            click(Button.CONFIRM_MAKE_WISH.POS)
        sleep(1)
        click(Button.BACK.POS)
        sleep(1)
        click(Button.BACK.POS)
        sleep(1)
        click(Button.BACK.POS)
        sleep(1)
    
    def claim_home_rewards(self):
        click(Button.HAMBURGER.POS)
        sleep(1)
        click(Button.HOME_ROUND.POS)
        sleep(5)
        # skywork rock
        click(Button.CLAIM_SKYWORK_STONE_ENTRY.POS)
        sleep(1)
        click(Button.CLAIM_SKYWORK_STONE_ENTRY.POS)
        sleep(1)
        click(Button.FREE_SKYWORK_STONE_DRAW.POS)
        sleep(5)
        self.click_bottom_blank()
        click(Button.CLOSE_SKYWORK_STONE_MENU.POS)
        sleep(1)
        # rabbit bun
        click(Button.STEAM_RABBIT_ENTRY.POS)
        sleep(1)
        click(Button.STEAM_NOW.POS)
        sleep(1)
        click(Button.CLOSE_STEAM_RABBIT_MENU.POS)
        sleep(1)
        # click like button
        click(Button.VISIT_LIST_ENTRY.POS)
        sleep(1)
        click(Button.VISIT_NOW.POS)
        sleep(3)
        click(Button.LIKE_NOW.POS)
        sleep(1)
        click(Button.BACK.POS)
        sleep(3)
        click(Button.CLOSE_VISIT_LIST.POS)
        sleep(1)
        click(Button.BACK.POS)
        sleep(5)

    def claim_shop_rewards(self):
        click(Button.SHOP_ENTRY.POS)
        sleep(2)
        click(Button.STRAIGHT_SALE.POS)
        sleep(1)
        click(Button.LIMITED_TIME.POS)
        sleep(1)
        click(Button.DAILY_FREE_GIFT.POS)
        sleep(1)
        self.click_bottom_blank()
        click(Button.MONTHLY_SALARY.POS)
        sleep(1)
        click(Button.CLAIM_GOLD_YU.POS)
        sleep(1)
        self.click_bottom_blank()
        click(Button.BACK.POS)
        sleep(2)
    
    def _claim_shop_babee_reward(self):
        click(Button.SHOP_ENTRY.POS)
        sleep(2)
        click(Button.MISCELLANEOUS.POS)
        sleep(1)
        click(Button.UTENSILS.POS)
        sleep(1)
        moveTo(960, 540)
        sleep(1)
        scroll(-1)
        sleep(1)
        babee_items = self._get_batch_pos(Button.BABEE.SRC, confidence=0.9)
        sleep(1)
        for item in babee_items:
            click(item)
            sleep(1)
            click(Button.CONFIRM_BABEE_PURCHASE.POS)
            sleep(1)
            self.click_bottom_blank()
        click(Button.BACK.POS)
        sleep(2)

    def _claim_free_rice(self):
        click(Button.ACTIVITY_PAGE_ENTRY.POS)
        sleep(1)
        if love_btn := locateOnScreen(Button.LUNCHBOX_WITH_LOVE.SRC, confidence=0.9):
            click(love_btn)
            sleep(1)
            for btn in Button.CLAIM_FREE_RICE_LOCS.POS:
                click(btn)
                sleep(1)
                self.click_bottom_blank()
        else:
            print('No lunch box found')
        click(Button.CLOSE_ACTIVITY_PAGE.POS)
        sleep(1)
    
    def claim_rewards(self):
        self.activate_window()
        self.claim_online_rewards()
        self.claim_shop_rewards()
        self.claim_home_rewards()
        self.minimize_window()
    
    def claim_rice(self):
        self.activate_window()
        self._claim_free_rice()
        self.minimize_window()

    def exotic_expeditions(self):
        self.activate_window()
        self.perform_exotic_searches()
        self.minimize_window()
    
    def make_dirt_purchase(self):
        self.activate_window()
        self._claim_shop_babee_reward()
        self.minimize_window()

if __name__ == '__main__':
    sleep(2)
    controller = RoutineController()
    # controller.make_wish()
    # controller.perform_exotic_searches()
    # controller._claim_free_rice()
    # print(position())