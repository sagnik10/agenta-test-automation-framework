# apps/hp_app_web.py
from core.configManager import ConfigManager
from pages.web import *
from pages.web.login_page import LoginPage


class HPAppWeb:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        #self.enroll_page = WebEnrollPage(driver)

    def login(self, username, password):
        self.login_page.open()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        assert self.login_page.is_login_successful(), "Login unsuccessful"
    
    def start_enrollment(self):
        self.login_page.open()
        self.login_page.login()
    
    def enter_shipping_details(self):
        self.enroll_page.fill_shipping()
    
    def confirm_enrollment(self):
        self.enroll_page.confirm()
    
    def verify_confirmation_screen(self):
        self.enroll_page.verify_success_message()

    def validateOnboarding(self):
        self.enroll_page.verify_success_message()