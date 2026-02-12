from abc import ABC, abstractmethod

class BaseDriver(ABC):
    """Abstract base class for all platform drivers.

    This class defines the common driver interface that all concrete
    platform-specific drivers (Web, Mobile, Desktop) must implement.

    Responsibilities:
        - Provide consistent interaction API for pages.
        - Hide platform/tool-specific execution differences.
        - Standardize driver lifecycle.

    Methods to implement:
        get_driver(): Initialize and return driver instance.
        get(url): Navigate to a URL (where applicable).
        find_element(locator_type, locator_value): Locate element.
        click(locator_type, locator_value): Click on element.
        send_keys(locator_type, locator_value, text): Type text.
        wait_for_element(locator_type, locator_value, timeout): Explicit wait.
        quit(): Terminate driver session.
    """
    @abstractmethod
    def get(self, url: str):
        pass

    @abstractmethod
    def find_element(self, locator_type: str, locator_value: str):
        pass

    @abstractmethod
    def click(self, locator_type: str, locator_value: str):
        pass

    @abstractmethod
    def send_keys(self, locator_type: str, locator_value: str, text: str):
        pass

    @abstractmethod
    def wait_for_element(self, locator_type: str, locator_value: str, timeout: int = 10):
        pass

    @abstractmethod
    def quit(self):
        pass
