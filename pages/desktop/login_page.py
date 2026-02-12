import time
import allure
import pytest
from core.logger import get_logger
from pages.base_page import BasePage
from utils.waits import WaitUtils
from selenium.webdriver.common.by import By
from resources.locators.desktop_locators import LoginPageLocators


class LoginPage(BasePage):
    def __init__(self, driver, main_window):
        super().__init__(driver)
        self.main_window = main_window
        self.logger = get_logger(self.__class__.__name__)
        self.wait = WaitUtils(driver)

    def open(self):
        self.logger.info("Navigating to HP Portal Login URL")
        with allure.step("Launch HP Smart Desktop App"):
            self.main_window.set_focus()
            self.main_window.wait("exists ready visible", timeout=30)      
            self.desktop_click(LoginPageLocators.MANAGE_HP_ACCOUNT_BTN)
            self.desktop_click(LoginPageLocators.LOGIN_BUTTON)


    def enter_username(self, username):
        self.logger.info("Entering username into input field")        
        with allure.step("Enter username"):
            self.driver.find_element(*LoginPageLocators.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.logger.info("Entering password into input field")
        with allure.step("Enter username"):
            self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.logger.info("Clicking Login button")
        with allure.step("Click Login button"):
            self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def is_login_successful(self):
        self.logger.info("Checking if login was successful")
        with allure.step("Check if login was successful"):
            return self.driver.find_element(*LoginPageLocators.SUCCESS_MESSAGE).is_displayed()

