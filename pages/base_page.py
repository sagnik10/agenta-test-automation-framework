"""
BasePage Module
===============

This module defines the BasePage class, acting as the foundation for all
Page Object classes in the Agentra automation framework.

It provides:
- Tool-agnostic interaction APIs
- Centralized retry & failure handling
- Heuristic self-healing at step level
- Unified logging and Allure reporting

Core Responsibilities
---------------------
1. Driver abstraction (Web / Mobile / Desktop)
2. Safe UI interactions (click, enter_text, get_text)
3. Retry + self-healing mechanism
4. Failure capture with diagnostics
5. Reporting & logging consistency

Design Principles
-----------------
- Single interaction authority
- Runtime resilience via self-healing
- Predictable error behavior
- Extensible for platform specialization
"""

import time
import traceback
import allure

from utils.self_healing import SelfHealingEngine

# Selenium exceptions
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    WebDriverException
)

# Appium exceptions fallback
try:
    from appium.webdriver.common.exceptions import WebDriverException as AppiumDriverException
except Exception:
    AppiumDriverException = WebDriverException

# Desktop exceptions (pywinauto)
try:
    from pywinauto.findwindows import ElementNotFoundError
except Exception:
    ElementNotFoundError = Exception

from core.configManager import ConfigManager
from core.logger import get_logger, log_allure


class BasePage:
    """Base class for all Page Objects providing safe & intelligent UI interactions."""

    RETRY_EXCEPTIONS = (
        # StaleElementReferenceException,
        # NoSuchElementException,
        # TimeoutException,
        # ElementNotInteractableException
    )

    def __init__(self, driver):
        self.driver = driver
        self.RETRIES = ConfigManager.get_retry_count("step_retry")
        self.logger = get_logger(self.__class__.__name__)
        self.healer = SelfHealingEngine(driver)

    # ------------------------------------------------------------------
    # SAFE ACTION EXECUTOR WITH SELF-HEALING + DEBUG TRACE
    # ------------------------------------------------------------------
    def _safe_action(self, action_name, func, locator, *args):
        """
        Executes an action safely with:
        - Retry logic
        - Screenshot capture
        - Self-healing on locator failure
        - Allure step tracking
        """

        healed_locator = None
        healing_applied = False

        for attempt in range(1, self.RETRIES + 2):

            try:
                with allure.step(f"{action_name} (Attempt {attempt})"):
                    self.logger.info(f"{action_name} - Attempt {attempt}")

                    active_locator = healed_locator if healed_locator else locator
                    return func(active_locator, *args)

            except Exception as e:

                self.logger.error(
                    f"[Attempt {attempt}] {action_name} failed with {type(e).__name__}: {str(e)}"
                )

                # 📸 Screenshot on every failed attempt
                self._attach_screenshot(f"{action_name}_Attempt_{attempt}_Failure")

                # 🧠 Self-healing trigger (once per action)
                if not healing_applied and self._is_locator_failure(e):

                    self.logger.warning(f"Triggering self-healing for {locator}")
                    healed_locator = self.healer.self_heal_locator(locator)

                    if healed_locator:
                        healing_applied = True
                        self.logger.info(
                            f"✅ Self-healed locator applied: {locator} → {healed_locator}"
                        )

                        allure.attach(
                            f"Healed from {locator} to {healed_locator}",
                            name="Self-Healing Triggered",
                            attachment_type=allure.attachment_type.TEXT
                        )

                        continue  # retry using healed locator

                # Retry logic
                if attempt <= self.RETRIES:
                    self.logger.warning(
                        f"Retrying {attempt}/{self.RETRIES} after failure..."
                    )
                    time.sleep(0.3)
                    continue

                # ❌ Final failure
                return self._fail(
                    action_name,
                    f"Failed after {self.RETRIES} retries ({type(e).__name__})",
                    e
                )

    def _is_locator_failure(self, exception):
        # primary: by type
        if isinstance(exception, self.RETRY_EXCEPTIONS):
            return True

        # fallback: by class name (handles selenium/appium/wrapper TimeoutException etc.)
        return exception.__class__.__name__ in (
            "TimeoutException",
            "NoSuchElementException",
            "StaleElementReferenceException",
            "ElementNotInteractableException"
        )


    # ------------------------------------------------------------------
    # SCREENSHOT HELPER
    # ------------------------------------------------------------------
    def _attach_screenshot(self, name):
        """Attach screenshot safely to Allure report."""
        try:
            if hasattr(self.driver, "driver"):
                real_driver = self.driver.driver
            else:
                real_driver = self.driver

            if hasattr(real_driver, "get_screenshot_as_png"):
                allure.attach(
                    real_driver.get_screenshot_as_png(),
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            self.logger.warning(f"Screenshot capture failed: {e}")

    # ------------------------------------------------------------------
    # FAILURE HANDLER
    # ------------------------------------------------------------------
    def _fail(self, action_name, title, exception_obj):
        """Logs detailed failure and raises a clean assertion."""

        error_msg = f"{title} during: {action_name}\n{str(exception_obj)}"
        self.logger.error(error_msg)
        self.logger.debug(traceback.format_exc())

        allure.attach(
            f"{type(exception_obj).__name__}: {str(exception_obj)}",
            name="Failure Reason",
            attachment_type=allure.attachment_type.TEXT
        )

        raise AssertionError(f"{title} during: {action_name}")

    # ------------------------------------------------------------------
    # PUBLIC INTERACTION WRAPPERS
    # ------------------------------------------------------------------

    def click(self, locator_type, locator_value):
        locator = (locator_type, locator_value)
        action_name = f"Clicking element {locator}"

        return self._safe_action(
            action_name,
            self._click,
            locator
        )

    def _click(self, locator):
        self.driver.wait_for_element(*locator)
        self.driver.click(*locator)


    def enter_text(self, locator_type, locator_value, text):
        locator = (locator_type, locator_value)
        action_name = f"Entering text into {locator}"

        return self._safe_action(
            action_name,
            self._enter_text,
            locator,
            text
        )

    def _enter_text(self, locator, text):
        self.driver.wait_for_element(*locator)
        self.driver.send_keys(*locator, text)

    def get_text(self, locator_type, locator_value):
        locator = (locator_type, locator_value)
        action_name = f"Fetching text from {locator}"

        return self._safe_action(
            action_name,
            self._get_text,
            locator
        )

    def _get_text(self, locator):
        el = self.driver.find_element(*locator)
        return el.text if el else None
    

    def desktop_click(self, locator_dict):
        """
        Safe click for Desktop UI elements (pywinauto).
        locator_dict is a dictionary of UIA properties:
            {"title": "OK", "control_type": "Button"}
        """
        action_name = f"Desktop click {locator_dict}"
        return self._safe_action(
            action_name,
            self._desktop_click,
            locator_dict
        )


    def _desktop_click(self, locator_dict):
        """
        Actual click logic for Desktop.
        """
        # get main window from driver (DesktopDriverManager exposes main_window)
        window = self.driver.main_window

        # locate child element
        element = window.child_window(**locator_dict)

        # wait for element to exist & be ready
        element.wait("exists ready", timeout=4)

        # perform click
        element.click_input()    