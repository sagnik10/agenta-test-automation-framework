from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
from core.logger import get_logger


class WaitUtils:
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)

    @allure.step("Wait until element is visible: {locator}")
    def wait_until_visible(self, by, locator, timeout=20, poll_frequency=0.5):
        """
        Wait until an element is visible on the page.

        :param by: locator strategy, e.g. By.XPATH
        :param locator: locator string
        :param timeout: maximum time to wait (seconds)
        :param poll_frequency: how often to check (seconds)
        :return: WebElement if found, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency)
            element = wait.until(EC.visibility_of_element_located((by, locator)))
            # allure.attach(
            #     self.driver.get_screenshot_as_png(),
            #     name="ElementVisible",
            #     attachment_type=allure.attachment_type.PNG
            # )
            return element
        except TimeoutException:
            # allure.attach(
            #     self.driver.get_screenshot_as_png(),
            #     name="WaitTimeout",
            #     attachment_type=allure.attachment_type.PNG
            # )
            allure.attach(
                f"Locator: ({by}, {locator}) waited {timeout}s without visibility.",
                name="Wait Timeout Details",
                attachment_type=allure.attachment_type.TEXT
            )
            return None
            
    @allure.step("Wait until element is clickable")
    def wait_until_clickable(self, by, locator, timeout=10):
        """Wait until the element becomes clickable."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
        except TimeoutException:
            allure.attach(
                f"Element not clickable: {locator} after {timeout}s",
                name="Wait Failure - Clickable",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Wait until text is present in element")
    def wait_until_text_present(self, by, locator, text, timeout=10):
        """Wait until a specific text appears in an element."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, locator), text)
            )
        except TimeoutException:
            allure.attach(
                f"Text '{text}' not found in element: {locator} after {timeout}s",
                name="Wait Failure - Text",
                attachment_type=allure.attachment_type.TEXT
            )
            raise
