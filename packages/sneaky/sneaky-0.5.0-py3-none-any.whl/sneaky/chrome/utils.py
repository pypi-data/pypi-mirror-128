from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys as _Keys
import random
import time


class Keys(_Keys):
    class chord:
        def __init__(self, *args):
            self.keys = args

        def actions(self, driver):
            actions = ActionChains(driver)
            for _ in self.keys[:-1]:
                actions.key_down(_)
            actions.send_keys(self.keys[-1])
            for _ in reversed(self.keys[:-1]):
                actions.key_up(_)
            return actions

        def perform(self, driver):
            return self.actions(driver).perform()

    class pause:
        def __init__(self, second):
            self.sec = second

        def pause(self):
            time.sleep(self.sec)

    class pause_random(pause):
        def __init__(self):
            super().__init__(random.SystemRandom().randint(150, 250)/1000)