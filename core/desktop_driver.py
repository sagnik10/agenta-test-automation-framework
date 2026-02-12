# core/desktop_driver.py
import os
import time
import subprocess
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError

class DesktopDriverManager:
    
    def __init__(self):
        self.app = None
        self.main_window = None

    def _get_hp_smart_appid(self):
        try:
            cmd = [
                "powershell",
                "-Command",
                "Get-StartApps | Where-Object { $_.Name -like '*HP Smart*' } | Select-Object -ExpandProperty AppID"
            ]
            appid = subprocess.check_output(cmd, text=True).strip()
            if not appid:
                raise FileNotFoundError("HP Smart AppID not found.")
            return appid
        except Exception as e:
            raise FileNotFoundError(f"Failed to get HP Smart AppID: {e}")

    def launch_app(self):
        appid = self._get_hp_smart_appid()
        print(f"Launching HP Smart via AppID: {appid}")

        os.system(f'start shell:appsFolder\\{appid}')
        time.sleep(5)

        from pywinauto import Application

        self.app = Application(backend="uia").connect(title_re=".*HP Smart.*")
        self.main_window = self.app.window(title_re=".*HP Smart.*")
        self.main_window.wait("visible", timeout=20)
        print("✅ Connected to HP Smart window successfully.")

        return self.main_window

    def get_driver(self):
        """Return the driver manager itself."""
        return self
    
    def wait_for_element(self, locator_dict, timeout=20):
        el = self.main_window.child_window(**locator_dict)
        el.wait("exists ready", timeout=timeout)
        return el

    def find_element(self, locator_dict):
        return self.main_window.child_window(**locator_dict)

    def click(self, locator_dict):
        el = self.find_element(locator_dict)
        el.wait("ready", timeout=10)
        el.click_input()

    def quit(self):
        if self.main_window:
            try:
                self.main_window.close()
                print("✅ HP Smart closed.")
            except Exception:
                pass
