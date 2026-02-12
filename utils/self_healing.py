# utils/self_healing.py
import re
import json
import os
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


class SelfHealingEngine:

    def __init__(self, driver, log_path="reports/healing_log.json"):
        # Unwrap WebDriverManager / MobileDriverManager etc.
        if hasattr(driver, "driver"):
            self.driver = driver.driver       # raw selenium/appium driver
        else:
            self.driver = driver

        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def similarity(self, a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def self_heal_locator(self, locator):
        """
        Heuristic self-healing based on DOM attributes and similarity.

        Supports:
        - id-based locators
        - xpath locators using @id, @name, @placeholder, @aria-label
        """
        by, original_value = locator

        # 🔥 IMPORTANT: use real selenium driver's page_source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # --- Case 1: pure ID locator -------------------------------------
        if by.lower() == "id":
            healed = self._heal_by_similarity("id", original_value, soup)
            if healed:
                self._log(locator, healed)
                return healed

        # --- Case 2: XPATH with @id / @name / @placeholder / @aria-label --
        if by.lower() == "xpath":
            # Try to extract @id='<value>' from xpath
            id_match = re.search(r"@id=['\"]([^'\"]+)['\"]", original_value)
            if id_match:
                id_value = id_match.group(1)
                healed = self._heal_by_similarity("id", id_value, soup)
                if healed:
                    self._log(locator, healed)
                    return healed

            name_match = re.search(r"@name=['\"]([^'\"]+)['\"]", original_value)
            if name_match:
                name_value = name_match.group(1)
                healed = self._heal_by_similarity("name", name_value, soup)
                if healed:
                    self._log(locator, healed)
                    return healed

            placeholder_match = re.search(r"@placeholder=['\"]([^'\"]+)['\"]", original_value)
            if placeholder_match:
                placeholder_value = placeholder_match.group(1)
                healed = self._heal_by_similarity("placeholder", placeholder_value, soup)
                if healed:
                    self._log(locator, healed)
                    return healed

            aria_match = re.search(r"@aria-label=['\"]([^'\"]+)['\"]", original_value)
            if aria_match:
                aria_value = aria_match.group(1)
                healed = self._heal_by_similarity("aria-label", aria_value, soup)
                if healed:
                    self._log(locator, healed)
                    return healed

        # --- Fallback: try raw value against other attributes ------------
        for attr in ["name", "placeholder", "aria-label"]:
            healed = self._heal_by_similarity(attr, original_value, soup)
            if healed:
                self._log(locator, healed)
                return healed

        return None

    def _heal_by_similarity(self, attr, original_value, soup):
        best_match = None
        best_score = 0.0

        for tag in soup.find_all(attrs={attr: True}):
            current = tag.get(attr)
            score = self.similarity(original_value, current)

            if score > best_score and score > 0.7:
                best_score = score
                best_match = current

        if best_match:
            if attr == "id":
                return ("id", best_match)
            return ("xpath", f"//*[@{attr}='{best_match}']")

        return None

    def _log(self, old, new):
        data = {}
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = {}

        data[str(old)] = {"old": old, "new": new}

        with open(self.log_path, "w") as f:
            json.dump(data, f, indent=4)
