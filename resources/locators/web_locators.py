"""
Locator definitions for the <PAGE NAME> of the Web application.

This module contains all Selenium-compatible web element locators for the
corresponding page. Each locator is defined as a constant tuple using a
Selenium `By` strategy and its associated value.

Purpose:
    - Centralize all web selectors for maintainability.
    - Provide clean separation between structure (locators) and behavior (Page Objects).
    - Avoid hard-coded selectors inside page logic.
    - Simplify UI updates — changes occur here, not in tests or page classes.

Locator Format:
    LOCATOR_NAME = (By.<STRATEGY>, "locator_value")

Common Strategies:
    - By.ID
    - By.NAME
    - By.XPATH
    - By.CSS_SELECTOR
    - By.CLASS_NAME
    - By.LINK_TEXT
    - By.TAG_NAME

Example:
    USERNAME_INPUT = (By.ID, "username")
    LOGIN_BUTTON   = (By.XPATH, "//button[@id='submit']")

Usage:
    Page objects import these constants and use them with WebDriver's
    find_element(), click(), send_keys(), and wait utilities.

Naming Convention:
    - CONSTANTS in UPPER_SNAKE_CASE
    - Group locators logically by page sections if needed
"""
from selenium.webdriver.common.by import By

class LoginPageLocators:
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@id='submit1']")
    SUCCESS_MESSAGE = (By.XPATH, "//*[text()='Logged In Successfully']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")


class EnrollmentPageLocators:
    START_BUTTON = (By.XPATH, "//button[text()='Start Enrollment']")
    CONTINUE_BUTTON = (By.XPATH, "//button[text()='Continue']")
    SHIPPING_ADDRESS_INPUT = (By.NAME, "shippingAddress")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Submit']")


class SpecialOfferModalLocators:
    EK_CODE_INPUT = (By.ID, "ek-code")
    APPLY_BUTTON = (By.XPATH, "//button[text()='Apply']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-success")
    NOTIFICATION_MESSAGE = (By.XPATH, "//*[contains(text(),'payment method is needed')]")
    CREDITS_BREAKDOWN_SECTION = (By.CSS_SELECTOR, ".credits-breakdown")
    CODE_NAME_TEXT = (By.XPATH, "//div[contains(@class, 'code-name')]")
    TRIAL_MONTHS_TEXT = (By.XPATH, "//div[contains(@class, 'trial-months')]")
