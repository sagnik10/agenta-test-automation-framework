import pytest
import apps
from core.configManager import ConfigManager


# =========================================================
# SESSION INITIALIZATION
# =========================================================
@pytest.fixture(scope="session", autouse=True)
def initialize_config():
    """
    Loads config.yaml once per test session.
    Makes configuration globally available via ConfigManager.
    """
    ConfigManager.load()


# =========================================================
# PYTEST CLI ARGUMENTS
# =========================================================
def pytest_addoption(parser):
    """
    Registers custom CLI arguments.

    Supported args:
        --platform: web | mobile | desktop
        --env: dev | qa | staging | prod
        --browser: chrome | firefox
    """
    parser.addoption("--platform", action="store", default="web",
                     help="Platform: web | mobile | desktop")
    parser.addoption("--env", action="store", default="qa",
                     help="Environment: dev | qa | staging | prod")
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser: chrome | firefox")


# =========================================================
# DRIVER FIXTURE
# =========================================================
@pytest.fixture(scope="function")
def driver(request):
    """
    Creates and yields a platform driver based on CLI arguments.

    Behavior:
        - Instantiates WebDriverManager / MobileDriverManager /
          DesktopDriverManager.
        - Applies SingletonDriver internally.
        - Ensures proper teardown.
    """
    platform = request.config.getoption("--platform")

    if platform == "web":
        from core.web_driver import WebDriverManager
        drv = WebDriverManager().get_driver()

    elif platform == "mobile":
        from core.mobile_driver import MobileDriverManager
        drv = MobileDriverManager().get_driver()

    elif platform == "desktop":
        from core.desktop_driver import DesktopDriverManager
        drv = DesktopDriverManager().get_driver()

    else:
        raise ValueError(f"Unknown platform: {platform}")

    yield drv

    # Teardown (ensures browser/app is closed)
    try:
        drv.quit()
    except Exception:
        pass


# =========================================================
# HP APP FIXTURE (PLATFORM AGNOSTIC APP CONTROLLER)
# =========================================================
@pytest.fixture(scope="function")
def hpApp(request, driver):
    """
    Returns the appropriate HPApp implementation
    based on platform CLI option.
    """
    platform = request.config.getoption("--platform")

    if platform == "web":
        from apps.hp_web_app import HPAppWeb
        return HPAppWeb(driver)

    elif platform == "mobile":
        from apps.hp_mobile_app import HPAppMobile
        return HPAppMobile(driver)

    elif platform == "desktop":
        from core.desktop_driver import DesktopDriverManager
        from apps.hp_desktop_app import HPAppDesktop

        driver_manager = DesktopDriverManager()
        return HPAppDesktop(driver_manager)


    else:
        raise ValueError(f"Unknown platform: {platform}")
