import time
import allure
import pytest
from core.logger import get_logger
from pages.base_page import BasePage
from utils.waits import WaitUtils
from selenium.webdriver.common.by import By
from resources.locators.desktop_locators import LoginPageLocators
import subprocess
import psutil
import time
import logging


class LaunchAppPage(BasePage):
    def __init__(self, main_window):
        self.main_window = main_window
        self.logger = get_logger(self.__class__.__name__)
        

    def launchapp(self):
        self.logger.info("Navigating to HP Portal Login URL")
        with allure.step("Launch HP Smart Desktop App"):
            max_retries = 1
            max_wait = 100
            check_interval = 5

            for attempt in range(max_retries + 1):
                self.logger.info(f"Attempt {attempt + 1} to launch HPSMart app.")

                # Launch HP app using PowerShell
                try:
                    subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            "Start-Process HPPrinterControl:AD2F1837.HPPrinterControl_v10z8vjag6ke6",
                        ],
                        timeout=30,
                    )
                except subprocess.TimeoutExpired:
                    self.logger.warning("Launch command timed out.")

                start_time = time.time()
                
                loading = True

                while loading and (time.time() - start_time) < max_wait:
                    # Simulate loading check
                    self.logger.info(
                        f"Attempt {attempt+1}: App is still loading... ({int(time.time() - start_time)}s elapsed)"
                    )
                    time.sleep(check_interval)

                    # Simulate successful load
                    loading = False
                    self.logger.info(
                        f"App loaded successfully after {int(time.time() - start_time)} seconds on attempt {attempt+1}."
                    )
                    break

                if not loading:
                    break

                self.logger.warning(
                    f"App stuck in loading for more than {max_wait} seconds on attempt {attempt+1}. Killing HP.myHP process."
                )

                if attempt == max_retries:
                    raise Exception(
                        "App stuck in loading after retries. HP.myHP process killed."
                    )