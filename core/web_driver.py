from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base_driver import BaseDriver
from core.singleton_driver import SingletonDriver

from core.logger import get_logger

logger = get_logger(__name__)

class WebDriverManager(BaseDriver):
    """Web platform driver implementation using Selenium.

    Provides Selenium ChromeDriver setup and exposes a consistent API
    defined by the BaseDriver interface.

    Args:
        browser (str): Browser type ("chrome" supported).

    Attributes:
        driver: The underlying Selenium WebDriver instance.

    Methods:
        get_driver(): Initialize and return WebDriver instance.
        get(url): Navigate to a webpage.
        find_element(...): Locate element using Selenium By strategies.
        click(...): Perform click action.
        send_keys(...): Type into input field.
        wait_for_element(...): Explicit wait using WebDriverWait.
        quit(): Quit browser session.
    """
    def __init__(self, browser='chrome'):
        self.driver = None
        self.browser = browser

    def get_driver(self):
        def create():
            logger.info("Launching Chrome browser...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            #options.add_argument('--headless')  # remove headless for visual run
            return webdriver.Chrome(options=options)
        self.driver = SingletonDriver.get_instance('web', create)
        return self

    def get(self, url):
        self.driver.get(url)

    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(getattr(By, locator_type.upper()), locator_value)

    def click(self, locator_type, locator_value):
        self.find_element(locator_type, locator_value).click()

    def send_keys(self, locator_type, locator_value, text):
        el = self.find_element(locator_type, locator_value)
        el.clear()
        el.send_keys(text)

    def wait_for_element(self, locator_type, locator_value, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((getattr(By, locator_type.upper()), locator_value))
        )

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            finally:
                SingletonDriver.reset()
