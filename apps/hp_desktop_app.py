# apps/hp_app_desktop.py
from pages.desktop.login_page import LoginPage
from core.configManager import ConfigManager


class HPAppDesktop:
    def __init__(self, driver):
        self.driver = driver
        self.main_window = driver.main_window
        self.login_page = LoginPage(self.driver, self.main_window)
        # self.enroll_page = WebEnrollPage(driver)

    def launchApp(self):
        self.main_window = self.driver.launch_app()

        # give main_window to pages
        from pages.desktop.login_page import LoginPage
        self.login_page = LoginPage(self.driver, self.main_window)

        return self   

    def login(self):
        self.login_page.open()
        # self.login_page.login()
    
    def start_enrollment(self):
        self.login_page.open()
        # self.login_page.login()
    
    def enter_shipping_details(self):
        self.enroll_page.fill_shipping()
    
    def confirm_enrollment(self):
        self.enroll_page.confirm()
    
    def verify_confirmation_screen(self):
        self.enroll_page.verify_success_message()
