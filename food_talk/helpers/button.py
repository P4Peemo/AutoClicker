from os import getcwd

cwd = getcwd()

class Button():
    class BtnFactory():
        def __init__(self, pos=None, src=''):
            self.POS = pos
            if src:
                src = ''.join([cwd, '/food_talk/assets', src])
            self.SRC = src

    # General purposes
    BACK = BtnFactory((150, 80))
    HAMBURGER = BtnFactory((100, 400))

    # Cooking
    ROUND_KITCHEN = BtnFactory((150, 320))
    KITCHEN_CANTEEN_ENTRY = BtnFactory((960, 230))
    CANTEEN_KITCHEN_ENTRY = BtnFactory((960, 950))
    COOKING_POT_LOCS = BtnFactory([(360, 700), (660, 700), (960, 700), (1260, 700), (1560, 700)], '/dish_cooking/cooking_stove.png')
    CANCEL_COOKING_LOCS = BtnFactory([(620, 590), (920, 590), (1220, 590), (1520, 590), (1370, 590)], '/dish_cooking/cancel_cooking_button.png')
    STOVE_LOCS = BtnFactory([(360, 810), (660, 810), (960, 810), (1260, 810), (1560, 810)], '/dish_cooking/ready_to_cook_stove.png')
    COLLECT_DISHES = BtnFactory((1630, 930))
    CLOSE_MENU = BtnFactory((1650, 100), '/dish_cooking/close_cooking_menu_button.png')
    ALL_CATEGORIES = BtnFactory((256, 256))
    LOCKED_DISHES = BtnFactory(src='/dish_cooking/locked_dish.png')
    COOK_NOW = BtnFactory((1370, 920), '/dish_cooking/cook_button.png')
    NO_PENDING_DISH = BtnFactory(src='/dish_cooking/no_pending_dish.png')
    CONFIRM_UNLOCK_DISH = BtnFactory((960, 890))
    # dishes
    EGGPLANT = BtnFactory(src='/dish_cooking/oil_stew_eggplant.png')
    # Customer wave
    CUST_WAVE_ENTRY = BtnFactory((1730, 210))
    START_CUST_WAVE = BtnFactory((800, 840))
    CUST_WAVE_DISHES = BtnFactory([
        (965, 525), (1005, 545),
        (325, 200), (450, 215), (575, 200), (1350, 200), (1475, 215), (1600, 200),
        (995, 590), (885,530),
        (325, 465), (450, 480), (575, 465), (1375, 465), (1495, 480), (1610, 465),
        (1010, 625), (940, 615),
        (400, 630), (545, 645), (690, 630), (1225, 630), (1370, 645), (1515, 630),
    ])
    # Buffet
    BUFFET_LIST_ENTRY = BtnFactory((310, 940))
    BUFFET_LOCS = BtnFactory([(330, 300), (330, 470), (330, 640), (330, 810)])
    COOK_DISH = BtnFactory(src='/dish_cooking/cook_dish_button.png')
    SUBMIT_DISH = BtnFactory(src='/dish_cooking/submit_dish_button.png')
    CONFIRM_SUBMIT_DISH = BtnFactory(src='/dish_cooking/confirm_submit_dish_button.png')
    CHECK_OUT = BtnFactory((1720, 860))
    BUFFET_BURN_TAIL = BtnFactory(src='/dish_cooking/burn_tail_buffet.png')
    BUFFET_EAGLE_RISE = BtnFactory(src='/dish_cooking/eagle_rise_buffet.png')
    BUFFET_SEARCH_SPRING = BtnFactory(src='/dish_cooking/search_spring_buffet.png')
    BUFFET_DEER_BEEP = BtnFactory(src='/dish_cooking/deer_beep_buffet.png')
    BUFFET_THOUSAND_OLD_GAY = BtnFactory(src='/dish_cooking/thousand_old_gay_buffet.png')
    BUFFET_POOR_FOREST = BtnFactory(src='/dish_cooking/poor_forest_buffet.png')
    # Temple assembly
    TEMPLE_ASSEMBLY_ENTRY = BtnFactory((180, 940))
    TEMPLE_ASSEMBLY_ICON = BtnFactory(src='/dish_cooking/temple_assembly.png')
    INGREDIENT_SHARD_ICON = BtnFactory(src='/dish_cooking/ingredient_shard.png')
    # routinely
    FIRST_EXOTIC_SEARCH = BtnFactory((250, 490))
    ONLINE_REWARD = BtnFactory((1080, 170))
    CLAIM_ONLINE_REWARD = BtnFactory((1370, 650))
    MAIN_PAGE_CHAR_LOC = BtnFactory((580, 540))
    BUTLER_PAGE_ENTRY = BtnFactory((400, 835))
    FIRST_GIFT_LOC = BtnFactory((1280, 280))
    GIFT_NOW = BtnFactory((1620, 815))
    CHAR_LIST_ENTRY = BtnFactory((1600, 950))
    ADD_CHAR_EXP = BtnFactory((1570, 250))
    ADD_RABBIT = BtnFactory((1690, 415))
    LEVELING_UP = BtnFactory((1600, 800))

    # Game launching
    LOGIN_QR_CODE = BtnFactory(src='/game_launching/login_authorisation_code.png')

