from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver.v2 import Chrome as _Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome as __Chrome
from selenium.webdriver.common.by import By
from .utils import Keys, ActionChains
from html import escape, unescape
from scipy import interpolate
from lxml import html, etree
from typing import List
import numpy as np
import random
import string
import math
import time


class Chrome(_Chrome):
    cursor_pos = [0, 0]

    @staticmethod
    def is_xpath(s):
        return s[0] in [".", "/"]

    def exist(self, path_or_selector):
        try:
            if self.is_xpath(path_or_selector):
                self.find_element(By.XPATH, path_or_selector)
            else:
                self.find_element(By.CSS_SELECTOR, path_or_selector)
            return True
        except:
            return False

    def remove(self, path_or_selector_or_webelement):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        return self.execute_script('''
            var element = arguments[0];
            element.parentNode.removeChild(element);
        ''', path_or_selector_or_webelement)

    def expand_shadow_dom(self, element: WebElement) -> WebElement:
        return self.execute_script("return arguments[0].shadowRoot", element)

    def xpath(self, xpath) -> List[WebElement]:
        return WebDriverWait(self, 5).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def querySelectorAll(self, selector) -> List[WebElement]:
        return WebDriverWait(self, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

    def get_client_viewport_size(self) -> List[int]:
        return self.execute_script('''
            return [
                document.documentElement.clientWidth,
                document.documentElement.clientHeight
            ];
        ''')

    def move_by_offset(self, x, y, delay: int = 250):
        x = int(x)
        y = int(y)
        self.cursor_pos[0] += x
        self.cursor_pos[1] += y
        actions = ActionChains(self, delay)
        actions.move_by_offset(x, y)
        return actions.perform()

    def move_to_xy(self, x, y, delay: int = 250):
        _x, _y = self.get_client_viewport_size()
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > _x:
            x = _x
        if y > _y:
            y = _y
        actions = ActionChains(self, delay)
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        self.cursor_pos[0] = x
        self.cursor_pos[1] = y
        return actions.perform()

    def _bezier_curve_coords_from_xy(
            self,
            x2, y2,
            control_points: int = random.SystemRandom().randint(3, 5),
            steps = None
    ):
        x2 = int(x2)
        y2 = int(y2)
        x1, y1 = self.cursor_pos
        if x1 == x2 and y1 == y2:
            return None
        degree = 3 if control_points > 3 else control_points - 1
        x = np.linspace(x1, x2, num=control_points, dtype="int")
        y = np.linspace(y1, y2, num=control_points, dtype="int")
        offsetx = int(abs(x1-x2)/(control_points+1))
        offsety = int(abs(y1-y2)/(control_points+1))
        def rand(a):
            while True:
                b = random.SystemRandom().randint(-a, a)
                if abs(b/a) > 0.2:
                    return b
        xr = [0 if i == 0 or i == control_points-1 or offsetx == 0 else rand(offsetx) for i in range(control_points)]
        yr = [0 if i == 0 or i == control_points-1 or offsety == 0 else rand(offsety) for i in range(control_points)]
        xr[0] = yr[0] = xr[-1] = yr[-1] = 0
        x += xr
        y += yr
        tck, u = interpolate.splprep([x, y], k=degree)
        u = np.linspace(0, 1, num=steps)
        return interpolate.splev(u, tck)

    def mimic_move_to_random_xy(self, x_range: list = None, y_range: list = None, duration: float = None, steps: int = None):
        _x, _y = self.get_client_viewport_size()
        if not x_range:
            x_range = [_x//2, _x]
        if not y_range:
            y_range = [_y//2, _y]
        x = random.SystemRandom().randint(*x_range)
        y = random.SystemRandom().randint(*y_range)
        return self.mimic_move_to_xy(x, y, duration, steps)

    def mimic_move_to_xy(self, x: int, y: int, duration: float = None, steps: int = None):
        if not steps or not duration:
            steps = math.sqrt(abs(x-self.cursor_pos[0])**2+abs(y-self.cursor_pos[1])**2)/4
            duration = steps/283*2
            steps = int(steps)
        coords = self._bezier_curve_coords_from_xy(x, y, steps=steps)
        if not coords:
            return
        for coord in zip(*(i.astype(int) for i in coords)):
            self.move_to_xy(*coord, 0)
            self.wait(duration/steps)
        return True

    def mimic_move_to_element(self, path_or_selector_or_webelement, duration: float = None, steps: int = None):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        x = path_or_selector_or_webelement.location["x"]+(path_or_selector_or_webelement.rect["width"])/2
        y = path_or_selector_or_webelement.location["y"]+(path_or_selector_or_webelement.rect["height"])/2
        return self.mimic_move_to_xy(
            x,
            y,
            duration=duration,
            steps=steps,
        )

    def _mimic_click(self):
        actions = ActionChains(self, Keys.pause_random().sec*1000)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pointer_up()
        return actions.perform()

    def mimic_click_xy(self, x, y, duration: float = None, steps: int = None):
        self.mimic_move_to_xy(x, y, duration, steps)
        return self._mimic_click()

    def mimic_click(self, path_or_selector_or_webelement = None, duration: float = None, steps: int = None):
        if path_or_selector_or_webelement:
            self.mimic_move_to_element(path_or_selector_or_webelement, duration, steps)
        return self._mimic_click()

    def _mimic_send_input(self, input, delay: int = Keys.pause_random().sec*1000):
        actions = ActionChains(self, delay)
        if input in string.ascii_uppercase+'''~!@#$%^&*()_+{}|:"<>?''':
            actions.key_down(Keys.SHIFT)
            actions.pause(Keys.pause_random().sec)
            actions.send_keys(input)
            actions.key_up(Keys.SHIFT)
        else:
            actions.send_keys(input)
        return actions.perform()

    def mimic_send_chord(self, chord: Keys.chord):
        actions = ActionChains(self, Keys.pause_random().sec*1000)
        for _ in chord.keys[:-1]:
            actions.key_down(_)
        actions.pause(Keys.pause_random().sec)
        actions.send_keys(chord.keys[-1])
        for _ in reversed(chord.keys[:-1]):
            actions.key_up(_)
        return actions.perform()

    def mimic_send_input(self, path_or_selector_or_webelement, inputs, clear: bool = False):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        self.mimic_click(path_or_selector_or_webelement)
        self.mimic_move_to_random_xy()
        if clear:
            self.mimic_send_chord(Keys.chord(Keys.CONTROL, "a"))
            self.wait(Keys.pause_random().sec)
            self._mimic_send_input(Keys.BACKSPACE)
            self.wait(Keys.pause_random().sec)
        if isinstance(inputs, (str, Keys.chord, Keys.pause, Keys.pause_random)):
            inputs = [inputs]
        elif not isinstance(inputs, (list, tuple)):
            raise ValueError("send input does not support type '{}'".format(type(inputs)))
        for input in inputs:
            if isinstance(input, Keys.chord):
                self.mimic_send_chord(input)
                self.wait(Keys.pause_random().sec)
            elif isinstance(input, (Keys.pause, Keys.pause_random)):
                self.wait(input.sec)
            else:
                for _ in input:
                    delay = Keys.pause_random().sec
                    self._mimic_send_input(_, delay*1000)
                    self.wait(delay)
        return True

    def move_to_element(self, path_or_selector_or_webelement, delay: int = 250):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        actions = ActionChains(self, delay)
        actions.move_to_element(path_or_selector_or_webelement)
        self.cursor_pos = [
            path_or_selector_or_webelement.location["x"],
            path_or_selector_or_webelement.location["y"],
        ]
        return actions.perform()

    def click(self, path_or_selector_or_webelement = None, delay: int = 250):
        if path_or_selector_or_webelement:
            if not isinstance(path_or_selector_or_webelement, WebElement):
                if self.is_xpath(path_or_selector_or_webelement):
                    path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
                else:
                    path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
            self.move_to_element(path_or_selector_or_webelement)
        actions = ActionChains(self, delay)
        actions.click()
        return actions.perform()

    def send_input(self, path_or_selector_or_webelement, input, delay: int = 250):
        if path_or_selector_or_webelement:
            if not isinstance(path_or_selector_or_webelement, WebElement):
                if self.is_xpath(path_or_selector_or_webelement):
                    path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
                else:
                    path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
            self.click(path_or_selector_or_webelement)
        actions = ActionChains(self, delay)
        actions.send_keys(input)
        return actions.perform()

    @staticmethod
    def wait(s):
        time.sleep(s)

    @staticmethod
    def sleep_random():
        time.sleep(random.SystemRandom().uniform(0.5, 1))

    def format_element(self, e: WebElement):
        if not isinstance(e, WebElement):
            raise ValueError("'{}' is not WebElement".format(e))
        attributes = self.execute_script("var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value } return items;", e)
        attributes = " ".join("{}='{}'".format(k, escape(v)) for k, v in attributes.items())
        if attributes:
            attributes = " "+attributes
        return "<{tag}{}>...</{tag}>".format(attributes, tag=e.tag_name)

    def print_element(self, e: WebElement):
        print(self.format_element(e), flush=True)

    def pretty_format_element(self, e: WebElement):
        if not isinstance(e, WebElement):
            raise ValueError("'{}' is not WebElement".format(e))
        return etree.tostring(html.fromstring(e.get_attribute("outerHTML")), method="html", pretty_print=True).decode()

    def pretty_print_element(self, e: WebElement):
        print(self.pretty_format_element(e), flush=True)

    def get_console_log(self, level: str = None):
        log = self.get_log("browser")
        if not level:
            return log
        else:
            return [_ for _ in log if _["level"].lower() == level.lower()]
