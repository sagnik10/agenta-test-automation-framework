import time
import allure
import pytest
from pages.base_page import BasePage
from utils.waits import WaitUtils
from selenium.webdriver.common.by import By
from resources.locators.web_locators import LoginPageLocators
from core.logger import get_logger
from core.configManager import ConfigManager


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)
        self.wait = WaitUtils(driver)

    def open(self):
        self.logger.info("Navigating to HP Portal Login URL")
        with allure.step("Launch HP Portal"):
            url = ConfigManager.get_url("login")
            self.driver.get(url)  # Replace with actual login URL

    def enter_username(self, username):
        self.logger.info("Entering username into input field")        
        with allure.step("Enter username"):
            self.enter_text(*LoginPageLocators.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.logger.info("Entering password into input field")
        with allure.step("Enter password"):
            self.enter_text(*LoginPageLocators.PASSWORD_INPUT, password)

    def click_login(self):
        self.logger.info("Clicking Login button")
        with allure.step("Click Login button"):
            self.click(*LoginPageLocators.LOGIN_BUTTON)

    def is_login_successful(self):
        self.logger.info("Checking if login was successful")
        with allure.step("Check if login was successful"):
            return self.driver.find_element(*LoginPageLocators.SUCCESS_MESSAGE).is_displayed()

