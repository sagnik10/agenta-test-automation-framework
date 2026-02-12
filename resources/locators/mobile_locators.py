"""
Locator definitions for the <PAGE NAME> of the Mobile application.

This module contains all Appium-compatible element locators for Android
and/or iOS screens. Each locator is defined as a constant tuple describing
the locator strategy and its selector value.

Purpose:
    - Provide a single source of truth for mobile UI selectors.
    - Abstract locator differences between Android and iOS.
    - Prevent hard-coded Appium selectors in Page Objects.
    - Improve reusability across device types and OS versions.

Locator Format:
    LOCATOR_NAME = ("strategy", "locator_value")

Supported Appium Strategies:
    Android:
        - "id"
        - "xpath"
        - "accessibility id"
        - "class name"
        - "uiautomator"
    
    iOS:
        - "id"
        - "xpath"
        - "accessibility id"
        - "class name"
        - "predicate"
        - "class chain"

Example:
    USERNAME_FIELD = ("id", "com.app.example:id/username")
    LOGIN_BTN      = ("xpath", "//android.widget.Button[@text='Login']")

Usage:
    Page objects import these locators and pass them into the driver’s
    find_element(), click(), send_keys(), and wait utilities.

Naming Convention:
    - CONSTANTS in UPPER_SNAKE_CASE
    - Distinguish OS-specific locators if required, e.g.:
        USERNAME_FIELD_ANDROID
        USERNAME_FIELD_IOS
"""
