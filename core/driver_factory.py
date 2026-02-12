"""
driver_factory.py

Factory module responsible for creating platform-specific driver instances
(Web, Mobile, Desktop) in a unified and scalable manner.

This factory is the single entry point for driver creation in the Agentra
framework. It abstracts platform selection logic, instantiates the correct
driver manager implementation, and applies SingletonDriver so that each
pytest-xdist worker receives exactly one driver instance.

The factory ensures:
    - Platform-agnostic test execution.
    - Easy swapping of automation tools (e.g., Selenium → Playwright).
    - Centralized construction logic for all drivers.
    - Full compatibility with BaseDriver and Page Objects.

Typical usage in pytest:
    driver = DriverFactory.create_driver(
        platform="web",
        environment="qa",
        browser="chrome"
    )

    page = LoginPage(driver)

Architecture:
    BaseDriver (abstract)
        ↑
    [WebDriverManager | MobileDriverManager | DesktopDriverManager]
        ↑
    DriverFactory creates → SingletonDriver ensures thread/worker safety

Raises:
    ValueError: If unsupported platform or configuration is provided.
"""
from apps.hp_desktop_app import HPAppDesktop
from apps.hp_mobile_app import HPAppMobile
from apps.hp_web_app import HPAppWeb
from core.web_driver import WebDriverManager
from core.mobile_driver import MobileDriverManager
from core.desktop_driver import DesktopDriverManager

class DriverFactory:
    """Factory class for initializing platform-specific drivers.

    This class contains static methods to generate the appropriate driver
    implementation based on user-supplied runtime parameters. It ensures
    platform extensibility and single-responsibility by isolating all driver
    creation logic.

    Supported platforms:
        - "web"     → Selenium WebDriver (WebDriverManager)
        - "mobile"  → Appium Mobile Driver (MobileDriverManager)
        - "desktop" → pywinauto Desktop Driver (DesktopDriverManager)

    Methods:
        create_driver(platform, environment=None, **kwargs):
            Build and return the appropriate driver instance.

    Example:
        driver = DriverFactory.create_driver("web", browser="chrome")
        driver.get("https://example.com")
    """
    @staticmethod
    def get_driver(platform='web'):
        if platform == 'web':
            print("Creating Web Driver")
            return WebDriverManager().get_driver()
        elif platform == 'mobile':
            print("Creating Mobile Driver")
            return MobileDriverManager().get_driver()
        elif platform == 'desktop':
            print("Creating Desktop Driver")
            return DesktopDriverManager().get_driver()
        else:
            raise ValueError(f'Unsupported platform: {platform}')
        
    def __init__(self, platform):
            self.platform = platform.lower()
            self.driver = None

    def get_app(self):
        driver = self.get_driver()
        if self.platform == "web":
            return HPAppWeb(driver)
        elif self.platform == "mobile":
            return HPAppMobile(driver)
        elif self.platform == "desktop":
            return HPAppDesktop(driver)

    def quit_driver(self):
        if self.driver:
            self.driver.quit()            