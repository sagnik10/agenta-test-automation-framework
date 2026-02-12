from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base_driver import BaseDriver
from core.singleton_driver import SingletonDriver

class MobileDriverManager(BaseDriver):
    """Mobile platform driver implementation using Appium.

    Handles initialization of Appium driver for Android/iOS and provides
    the standard BaseDriver interface for page interactions.

    Args:
        device_name (str): Name of target mobile device.
        app_path (str): Path to APK/IPA for installation.
        platform (str): "android" or "ios".

    Methods:
        get_driver(): Start Appium session with capabilities.
        find_element(...): Locate mobile elements.
        click(...): Tap on element.
        send_keys(...): Input text using virtual keyboard.
        wait_for_element(...): Mobile explicit waits.
        quit(): End Appium session.
    """
    def __init__(self):
        self.driver = None

    def get_driver(self):
        def create():
            desired_caps = {
                "platformName": "Android",
                "deviceName": "AndroidDevice",
                "automationName": "UiAutomator2",
                "noReset": True
            }
            return webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        self.driver = SingletonDriver.get_instance('mobile', create)
        return self

    def get(self, url):
        pass

    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(getattr(AppiumBy, locator_type.upper()), locator_value)

    def click(self, locator_type, locator_value):
        self.find_element(locator_type, locator_value).click()

    def send_keys(self, locator_type, locator_value, text):
        el = self.find_element(locator_type, locator_value)
        el.clear()
        el.send_keys(text)

    def wait_for_element(self, locator_type, locator_value, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((getattr(AppiumBy, locator_type.upper()), locator_value))
        )

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            finally:
                SingletonDriver.reset()
