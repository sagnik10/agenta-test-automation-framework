import allure
import pytest
from core.testdataManager import TestDataManager
from pages.web import login_page
from core.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.flaky(reruns=2, reruns_delay=3)
@pytest.mark.parametrize('user,pwd', [('student','Password123')])
@allure.title("Test Login Functionality on Web Platform")
@allure.description("""
This test validates the login functionality on the web platform using valid user credentials.
It ensures that:
1. The login page opens correctly.
2. Username and password are entered.
3. Login action succeeds.
4. Success message or post-login page is visible.
""")

def test_login_web(hpApp, user, pwd):

    # user = TestDataManager.get("login", "valid", "username")
    # pwd = TestDataManager.get("login", "valid", "password")

    """
    <Short Test Title>
    <1–2 line summary of what this test validates.>

    Description:
        <High-level description of the business flow under test.>
        <Explain why this test exists and what user scenario it simulates.>

    Test Type:
        <Functional / Regression / Integration / E2E / Smoke / Sanity>

    Preconditions:
        - <List all required pre-state conditions>
        - <User account, device state, environment, network, etc.>
        - <If none, write: None>

    Platforms:
        - Supported: Web / Mobile / Desktop
        - Driven by CLI flag: --platform

    Steps:
        1. <Step 1 description>
        2. <Step 2 description>
        3. <Step 3 description>
        ...
        N. <Final step>

    Expected Result:
        <The exact outcome that must occur for the test to pass>
        <May include UI behavior, API response, state updates, etc.>

    Parameters:
        driver (BaseDriver):
            Platform-agnostic driver instance injected by pytest.
        test_data (dict or tuple):
            Data-driven inputs supplied by JSON/Excel or @pytest.mark.parametrize.

    Tags:
        pytest.mark.<suite>
        pytest.mark.<business_module>
        pytest.mark.<platform>
        pytest.mark.dependency()

    Notes:
        - This test uses the Agentra abstraction layer, so page objects
          automatically adjust based on selected platform.
        - Avoid platform-specific conditions inside the test; those belong
          in Page Objects.

    """    
    logger.info(f"Starting test_login_web with user={user}")
    hpApp.launch_app()
    hpApp.login()
    # hpApp.start_enrollment()
    # hpApp.enter_shipping_details()
    # hpApp.confirm_enrollment()
    # hpApp.validateOnboarding(codeType="EK", codeValue="EK12345")
    
    
