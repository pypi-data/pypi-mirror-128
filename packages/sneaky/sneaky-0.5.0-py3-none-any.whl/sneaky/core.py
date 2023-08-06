from .chrome.devtools.protocol.network import requestWillBeSent, responseReceived
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from eavesdropper import EAVESDROPPER, Dropper, HTTPFlow, Request, Response
from undetected_chromedriver.v2 import ChromeOptions
from subprocess import run, PIPE, DEVNULL
import undetected_chromedriver.patcher
from .chrome.driver import Chrome
from typing import Union, List
from threading import Thread
from munch import munchify
from copy import deepcopy
import vpncmd


class SNEAKY:
    request_traffic: List[Union[Request, requestWillBeSent]] = []
    response_traffic: List[Union[Response, responseReceived]] = []
    _capture_request_traffic: bool = False
    _capture_response_traffic: bool = False

    def __init__(
            self,
            *args,
            user_agent: str = None,
            open_developer_tools: bool = False,
            vpncmd_enable: bool = True,
            vpncmd_init: dict = None,
            vpncmd_setup_cmd_args: list = None,
            vpncmd_connect_known_vpn_kwargs: dict = None,
            eavesdropper_enable: bool = True,
            eavesdropper_init_kwargs: dict = None,
            eavesdropper_dropper: Dropper = None,
            debug: bool = False,
            **kwargs
    ):
        _self = self
        if eavesdropper_dropper and issubclass(eavesdropper_dropper, Dropper):
            class _Dropper(eavesdropper_dropper):
                pass
        else:
            class _Dropper(Dropper):
                pass
        class SneakyDropper(_Dropper):
            def request(self, flow: HTTPFlow):
                if _self._capture_request_traffic:
                    _self.request_traffic.append(deepcopy(flow.request))
                super().request(flow)

            def response(self, flow: HTTPFlow):
                if _self._capture_response_traffic:
                    _self.request_traffic.append(deepcopy(flow.response))
                super().response(flow)
        args = list(args)
        self.debug = debug
        self.open_developer_tools = open_developer_tools
        self.vpncmd_enable = vpncmd_enable
        self.eavesdropper_enable = eavesdropper_enable
        if self.vpncmd_enable:
            self.vpncmd = vpncmd.VPNCMD(**(vpncmd_init or {}))
            self.vpncmd.setup_cmd(*(vpncmd_setup_cmd_args or []))
            self.vpncmd.connect_known_vpn(**(vpncmd_connect_known_vpn_kwargs or {}))
            while not self.vpncmd.is_connected_to_vpn():
                Chrome.wait(0.5)
            if self.debug:
                print("started vpncmd")
        else:
            self.vpncmd = None
        if self.eavesdropper_enable:
            self.eavesdropper = EAVESDROPPER(**(eavesdropper_init_kwargs or {}))
            self.eavesdropper.Dropper = SneakyDropper
            self.eavesdropper.configure()
            self.eavesdropper_thread = Thread(target=self.eavesdropper.start)
            self.eavesdropper_thread.daemon = True
            self.eavesdropper_thread.start()
        else:
            self.eavesdropper = None
        self.chrome_options = self.tweak_chrome_options(args, kwargs)
        self.chrome_capabilities = self.tweak_chrome_capabilities(args, kwargs)
        self.driver = Chrome(*args, enable_cdp_events=True, **kwargs)
        if self.debug:
            print("chrome_options", self.chrome_options)
            print("chrome_capabilities", self.chrome_capabilities)
            print("Chrome(args, kwargs)", args, kwargs)
        self.driver.wait(1)
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": user_agent or "Mozilla/5.0 (Windows NT 8.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
            },
        )

    def tweak_chrome_capabilities(self, args, kwargs):
        chrome_capabilities = None
        chrome_capabilities_in_args = any(
            isinstance(_, dict) and "browserName" in _ and _["browserName"] == "chrome" for _ in args)
        chrome_capabilities_i = -1
        if "desired_capabilities" in kwargs:
            chrome_capabilities = kwargs["desired_capabilities"]
        elif chrome_capabilities_in_args:
            for i, _ in enumerate(args):
                if isinstance(_, dict) and "browserName" in _ and _["browserName"] == "chrome":
                    chrome_capabilities = _
                    chrome_capabilities_i = i
                    break
        if not chrome_capabilities:
            chrome_capabilities = self.chrome_options.to_capabilities()
        else:
            chrome_capabilities.update(self.chrome_options.to_capabilities())
        chrome_capabilities["goog:loggingPrefs"] = {
            "browser": "ALL"
        }
        if chrome_capabilities_i != -1:
            args[chrome_capabilities_i] = chrome_capabilities
        else:
            kwargs["desired_capabilities"] = chrome_capabilities
        return chrome_capabilities

    def tweak_chrome_options(self, args, kwargs):
        chrome_options = None
        chrome_options_in_args = any(isinstance(_, ChromeOptions) for _ in args)
        chrome_options_i = -1
        if "options" in kwargs:
            chrome_options = kwargs["options"]
        elif chrome_options_in_args:
            for i, _ in enumerate(args):
                if isinstance(_, ChromeOptions):
                    chrome_options = _
                    chrome_options_i = i
                    break
        if not chrome_options:
            chrome_options = ChromeOptions()
        if self.open_developer_tools:
            chrome_options.add_argument("--auto-open-devtools-for-tabs")
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        if self.eavesdropper_enable:
            chrome_options.add_argument("--proxy-server={}".format(self.eavesdropper.proxy))
        if chrome_options_i != -1:
            args[chrome_options_i] = chrome_options
        else:
            kwargs["options"] = chrome_options
        return chrome_options

    def capture_request_callback(self, data):
        self.request_traffic.append(munchify(deepcopy(data["params"])))

    def capture_response_callback(self, data):
        self.response_traffic.append(munchify(deepcopy(data["params"])))

    def capture_traffic(self):
        self.capture_request_traffic()
        self.capture_response_traffic()

    def capture_request_traffic(self):
        self._capture_request_traffic = True
        if self.eavesdropper_enable:
            return
        self.driver.add_cdp_listener("Network.requestWillBeSent", self.capture_request_callback)

    def capture_response_traffic(self):
        self._capture_response_traffic = True
        if self.eavesdropper_enable:
            return
        self.driver.add_cdp_listener("Network.responseReceived", self.capture_response_callback)

    def stop_capture_traffic(self):
        self.stop_capture_request_traffic()
        self.stop_capture_response_traffic()

    def stop_capture_request_traffic(self):
        self._capture_request_traffic = False
        if self.eavesdropper_enable:
            return
        try:
            self.driver.reactor.handlers.pop("Network.requestWillBeSent".lower())
        except KeyError:
            pass

    def stop_capture_response_traffic(self):
        self._capture_response_traffic = False
        if self.eavesdropper_enable:
            return
        try:
            self.driver.reactor.handlers.pop("Network.responseReceived".lower())
        except KeyError:
            pass

    def clear_traffic(self):
        self.clear_request_traffic()
        self.clear_response_traffic()

    def clear_request_traffic(self):
        self.request_traffic.clear()

    def clear_response_traffic(self):
        self.response_traffic.clear()

    @property
    def traffic(self):
        return {
            "request": self.request_traffic,
            "response": self.response_traffic,
        }

    def __del__(self):
        self.quit()

    def quit(self):
        self.driver.quit()
        if self.vpncmd_enable:
            self.vpncmd.disconnect_vpn()
        if undetected_chromedriver.patcher.IS_POSIX:
            kill_cmd = '''kill $(ps aux | grep 'browsermob-proxy' | awk '{print $2}')'''
        else:
            kill_cmd = '''wmic process where "CommandLine Like '%browsermob-proxy%'" delete'''
        run(kill_cmd, shell=True, stdin=DEVNULL, stdout=PIPE, stderr=PIPE)


def test(init, job):
    web = SNEAKY(**init)
    driver = web.driver
    vpncmd = web.vpncmd

    driver.get("chrome://extensions")
    driver.wait(1)

    try:
        job(web, driver, vpncmd)
    except:
        import traceback
        traceback.print_exc()

    driver.wait(5 * 1)
    web.quit()

    print("__main__ is finished.")
    print("Console is safe to close.")







