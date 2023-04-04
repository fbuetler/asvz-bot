import json
import os
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from typing import List, Optional

DRIVER_SERVICE = FirefoxService(GeckoDriverManager().install())

ASVZ_SCHALTER_URL = "https://schalter.asvz.ch"
ASVZ_AUTH_URL = "https://auth.asvz.ch"

COOKIES_FILE = ".cookies.json"


class LoginManager:
    def __init__(self, store_cookies=True):
        if store_cookies:
            self.cookies = self._load_cookies()

        self.driver = self._new_driver(cookies=self.cookies)

        if not self._is_logged_in():
            self.cookies = self._login()
            self.driver = self._new_driver(cookies=self.cookies)

            if store_cookies:
                self._store_cookies()

    def _new_driver(
        self, headless: bool = True, cookies: Optional[List[dict]] = None
    ) -> webdriver.Firefox:
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=DRIVER_SERVICE, options=options
        )

        # go to this url so that we can store the cookies
        driver.get(ASVZ_AUTH_URL)

        if cookies:
            for cookie in cookies:
                driver.add_cookie(cookie)

        return driver

    def _is_logged_in(self) -> bool:
        logging.debug("Checking if the user is logged in")
        self.driver.get(ASVZ_SCHALTER_URL)
        try:
            WebDriverWait(self.driver, 2).until(EC.url_contains("auth"))
            logging.debug("User is not logged in.")
            return False
        except TimeoutException:
            logging.debug("User is logged in!")
            return True

    def _login(self) -> List[dict]:
        logging.info("Logging in...")
        driver = self._new_driver(headless=False)
        driver.get(ASVZ_AUTH_URL)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.ID, "LoggedInUser"))
        )
        cookies = driver.get_cookies()
        driver.close()

        return cookies

    def _load_cookies(self) -> Optional[List[dict]]:
        logging.debug("Loading cookies")
        if os.path.isfile(COOKIES_FILE):
            logging.debug("Found cookies!")
            with open(COOKIES_FILE, "r") as f:
                return json.load(f)
        else:
            logging.debug("No cookies found :(")
            return None

    def _store_cookies(self):
        logging.debug("Storing cookies")
        with open(COOKIES_FILE, "w") as f:
            json.dump(self.cookies, f)

    def get_driver(self) -> webdriver.Firefox:
        return self.driver
