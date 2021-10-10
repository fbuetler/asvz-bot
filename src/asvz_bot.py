#!/usr/bin/python3
# coding=UTF-8

import argparse
import getpass
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

TIMEFORMAT = "%H:%M"

LESSON_BASE_URL = "https://schalter.asvz.ch"

SPORTFAHRPLAN_BASE_URL = "https://asvz.ch/426-sportfahrplan"

CREDENTIALS_FILENAME = ".asvz-bot.json"
CREDENTIALS_ORG = "organisation"
CREDENTIALS_UNAME = "username"
CREDENTIALS_PW = "password"

# organisation name as displayed by SwitchAAI
ORGANISATIONS = {
    "ETH": "ETH Zürich",
    "UZH": "Universität Zürich",
    "ZHAW": "ZHAW - Zürcher Hochschule für Angewandte Wissenschaften",
}

WEEKDAYS = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday",
    "Su": "Sunday",
}

FACILITIES = {
    "Sport Center Polyterrasse": 45594,
    "Sport Center Irchel": 45577,
    "Sport Center Hönggerberg": 45598,
    "Sport Center Fluntern": 45575,
    "Sport Center Winterthur": 45610,
    "Wädenswil Kraft-/Cardio-Center": 45613,
    "Online": 294542,
}

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class AsvzBotException(Exception):
    pass


class CredentialsManager:
    def __init__(self, org, uname, password, save_credentials):
        self.credentials = self.__load()
        if self.credentials is None:
            if org is None or uname is None:
                raise AsvzBotException("Not all required credentials are supplied")

            logging.info("Loading credentials from arguments")
            if password is None:
                password = getpass.getpass("Organisation password:")

            self.credentials = {
                CREDENTIALS_ORG: ORGANISATIONS[org],
                CREDENTIALS_UNAME: uname,
                CREDENTIALS_PW: password,
            }
        elif org is not None or uname is not None:
            logging.info(
                "Overwriting credentials loaded from local store with arguments"
            )
            if org is not None:
                self.credentials[CREDENTIALS_ORG] = ORGANISATIONS[org]
            if uname is not None:
                self.credentials[CREDENTIALS_UNAME] = uname

            password = getpass.getpass("Organisation password:")
            if password is not None and len(password) > 0:
                self.credentials[CREDENTIALS_PW] = password
        else:
            logging.info("Loaded credentials from local store")

        if save_credentials:
            logging.info("Storing credentials in local store")
            self.__store()

    def get(self):
        return self.credentials

    def __store(self):
        with open(CREDENTIALS_FILENAME, "w") as f:
            json.dump(
                self.credentials,
                f,
            )

    def __load(self):
        creds = Path(CREDENTIALS_FILENAME)
        if not creds.is_file():
            return None

        with open(CREDENTIALS_FILENAME, "r") as f:
            data = json.load(f)
            if (
                CREDENTIALS_ORG not in data
                or CREDENTIALS_UNAME not in data
                or CREDENTIALS_PW not in data
            ):
                return None
            return data


class AsvzEnroller:
    @classmethod
    def from_lesson_attributes(
        cls, chromedriver, weekday, start_time, trainer, facility, sport_id, creds
    ):
        today = datetime.today()
        weekday_int = time.strptime(WEEKDAYS[weekday], "%A").tm_wday
        weekday_date = today + timedelta((weekday_int - today.weekday()) % 7)

        sport_url = (
            "{}?f[0]=sport:{}&f[1]=facility:{}&date={}-{:02d}-{:02d}%20{}:{}".format(
                SPORTFAHRPLAN_BASE_URL,
                sport_id,
                FACILITIES[facility],
                weekday_date.year,
                weekday_date.month,
                weekday_date.day,
                start_time.hour,
                start_time.minute,
            )
        )
        logging.info("Searching lesson on '{}'".format(sport_url))

        lesson_url = None
        driver = None
        try:
            driver = AsvzEnroller.get_driver(chromedriver)
            driver.get(sport_url)
            driver.implicitly_wait(3)

            day_ele = driver.find_element_by_xpath(
                "//div[@class='teaser-list-calendar__day']"
            )

            lesson = day_ele.find_element_by_xpath(
                ".//li[@class='btn-hover-parent'][contains(., '{}')]".format(
                    trainer,
                )
            )

            lesson_url = lesson.find_element_by_xpath(
                ".//a[starts-with(@href, '{}')]".format(LESSON_BASE_URL)
            ).get_attribute("href")
        finally:
            if driver is not None:
                driver.quit()

        return cls(chromedriver, lesson_url, creds)

    @staticmethod
    def get_driver(chromedriver):
        options = Options()
        options.add_argument("--private")
        options.add_argument("--headless")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'de,de_CH'})
        return webdriver.Chrome(
            chromedriver,
            options=options,
        )

    @staticmethod
    def wait_until(enrollment_start):
        current_time = datetime.today()

        logging.info(
            "\n\tcurrent time: {}\n\tenrollment time: {}".format(
                current_time.strftime("%H:%M:%S"), enrollment_start.strftime("%H:%M:%S")
            )
        )

        login_before_enrollment_seconds = 1 * 59
        if (enrollment_start - current_time).seconds > login_before_enrollment_seconds:
            sleep_time = (
                enrollment_start - current_time
            ).seconds - login_before_enrollment_seconds
            logging.info(
                "Sleep for {} seconds until {}".format(
                    sleep_time,
                    (current_time + timedelta(seconds=sleep_time)).strftime("%H:%M:%S"),
                )
            )
            time.sleep(sleep_time)

    def __init__(self, chromedriver, lesson_url, creds):
        self.chromedriver = chromedriver
        self.lesson_url = lesson_url
        self.creds = creds

        self.__get_enrollment_and_start_time()

        logging.info(
            "Summary:\n\tOrganisation: {}\n\tUsername: {}\n\tPassword: {}\n\tLesson: {}".format(
                self.creds[CREDENTIALS_ORG],
                self.creds[CREDENTIALS_UNAME],
                "*" * len(self.creds[CREDENTIALS_PW]),
                self.lesson_url,
            )
        )

    def enroll(self):
        logging.info("Checking login credentials")
        try:
            driver = AsvzEnroller.get_driver(self.chromedriver)
            driver.get(self.lesson_url)
            driver.implicitly_wait(3)
            self.__organisation_login(driver)
        finally:
            driver.quit()

        if datetime.today() < self.enrollment_start:
            AsvzEnroller.wait_until(self.enrollment_start)

        try:
            driver = AsvzEnroller.get_driver(self.chromedriver)
            driver.get(self.lesson_url)
            driver.implicitly_wait(3)

            logging.info("Starting enrollment")

            if self.enrollment_start < datetime.today():
                logging.info(
                    "Enrollment is already open. Checking for available places."
                )
                self.__wait_for_free_places(driver)

            logging.info("Lesson has free places")

            self.__organisation_login(driver)

            logging.info("Waiting for enrollment")
            WebDriverWait(driver, 5 * 60).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[@id='btnRegister' and @class='btn-primary btn enrollmentPlacePadding ng-star-inserted']",
                    )
                )
            ).click()
            time.sleep(5)

            logging.info("Successfully enrolled. Train hard and have fun!")
        finally:
            driver.quit()

    def __get_enrollment_and_start_time(self):
        driver = None
        try:
            driver = AsvzEnroller.get_driver(self.chromedriver)
            driver.get(self.lesson_url)
            driver.implicitly_wait(3)

            enrollment_interval_raw = driver.find_element_by_xpath(
                "//dl[contains(., 'Anmeldezeitraum')]/dd"
            )
            # enrollment_interval_raw is like 'So, 09.05.2021 06:35 - Mo, 10.05.2021 07:05'
            enrollment_start_raw = (
                enrollment_interval_raw.get_attribute("innerHTML")
                .split("-")[0]
                .split(",")[1]
                .strip()
            )
            try:
                self.enrollment_start = datetime.strptime(
                    enrollment_start_raw, "%d.%m.%Y %H:%M"
                )
            except ValueError as e:
                logging.error(e)
                raise AsvzBotException(
                    "Failed to parse enrollment start time: '{}'".format(
                        enrollment_start_raw
                    )
                )

            lesson_interval_raw = driver.find_element_by_xpath(
                "//dl[contains(., 'Datum/Zeit')]/dd"
            )
            # lesson_interval_raw is like 'Mo, 10.05.2021 06:55 - 08:05'
            lesson_start_raw = (
                lesson_interval_raw.get_attribute("innerHTML")
                .split("-")[0]
                .split(",")[1]
                .strip()
            )
            try:
                self.lesson_start = datetime.strptime(
                    lesson_start_raw, "%d.%m.%Y %H:%M"
                )
            except ValueError as e:
                logging.error(e)
                raise AsvzBotException(
                    "Failed to parse lesson start time: '{}'".format(lesson_start_raw)
                )

        finally:
            if driver is not None:
                driver.quit()

    def __organisation_login(self, driver):
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@class='btn btn-default ng-star-inserted' and @title='Login']",
                )
            )
        ).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@class='btn btn-warning btn-block' and @title='SwitchAai Account Login']",
                )
            )
        ).click()

        logging.info("Login to '{}'".format(self.creds[CREDENTIALS_ORG]))

        organization = driver.find_element_by_xpath(
            "//input[@id='userIdPSelection_iddtext']"
        )
        organization.send_keys("{}a".format(Keys.CONTROL))
        organization.send_keys(self.creds[CREDENTIALS_ORG])
        organization.send_keys(Keys.ENTER)

        # apparently all organisations have the same xpath
        driver.find_element_by_xpath("//input[@id='username']").send_keys(
            self.creds[CREDENTIALS_UNAME]
        )
        driver.find_element_by_xpath("//input[@id='password']").send_keys(
            self.creds[CREDENTIALS_PW]
        )
        driver.find_element_by_xpath("//button[@type='submit']").click()

        logging.info("Submitted login credentials")
        time.sleep(3)  # wait until redirect is completed

        if not driver.current_url.startswith(LESSON_BASE_URL):
            logging.warning(
                "Authentication might have failed. Current URL is '{}'".format(
                    driver.current_url
                )
            )
        else:
            logging.info("Valid login credentials")

    def __wait_for_free_places(self, driver):
        while True:
            try:
                driver.find_element_by_xpath(
                    "//alert[@class='ng-star-inserted'][contains(., 'ausgebucht')]"
                )
            except NoSuchElementException:
                # has free places
                return

            if datetime.today() > self.lesson_start:
                raise AsvzBotException(
                    "Stopping enrollment because lesson has started."
                )

            retry_interval_sec = 1 * 60
            logging.info(
                "Lesson is booked out. Rechecking in {} secs..".format(
                    retry_interval_sec
                )
            )
            time.sleep(retry_interval_sec)
            driver.refresh()


def validate_start_time(start_time):
    try:
        return datetime.strptime(start_time, TIMEFORMAT)
    except ValueError:
        msg = "Invalid start time specified. Supported format is {}".format(TIMEFORMAT)
        raise argparse.ArgumentTypeError(msg)


def get_chromedriver():
    webdriver_manager = None
    try:
        webdriver_manager = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM)
    except:
        webdriver_manager = None

    if webdriver_manager is None:
        try:
            webdriver_manager = ChromeDriverManager(chrome_type=ChromeType.GOOGLE)
        except:
            webdriver_manager = None

    if webdriver_manager is None:
        logging.error("Failed to find chrome/chromium")
        exit(1)

    return webdriver_manager.install()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-org",
        "--organisation",
        choices=list(ORGANISATIONS.keys()),
        help="Name of your organisation.",
    )
    parser.add_argument("-u", "--username", type=str, help="Organisation username")
    parser.add_argument("-p", "--password", type=str, help="Organisation password")
    parser.add_argument(
        "--save-credentials",
        default=False,
        action="store_true",
        help="Store your login credentials locally and reused them on the next run",
    )

    subparsers = parser.add_subparsers(dest="type")
    parser_lesson = subparsers.add_parser("lesson", help="For lessons visited once")
    parser_lesson.add_argument(
        "lesson_id",
        type=int,
        help="ID of a particular lesson e.g. 200949 in https://schalter.asvz.ch/tn/lessons/200949",
    )

    parser_training = subparsers.add_parser(
        "training", help="For lessons visited periodically"
    )
    parser_training.add_argument(
        "-w",
        "--weekday",
        required=True,
        choices=list(WEEKDAYS.keys()),
        help="Day of the week of the lesson",
    )
    parser_training.add_argument(
        "-s",
        "--start-time",
        required=True,
        type=validate_start_time,
        help="Time when the lesson starts e.g. '19:15'",
    )
    parser_training.add_argument(
        "-t", "--trainer", required=True, type=str, help="Trainer giving this lesson"
    )
    parser_training.add_argument(
        "-f",
        "--facility",
        required=True,
        choices=list(FACILITIES.keys()),
        help="Facility where the lesson takes place e.g. 'Sport Center Polyterrasse'",
    )
    parser_training.add_argument(
        "sport_id",
        type=int,
        help="Number at the end of link to a particular sport on ASVZ Sportfahrplan, e.g. 45743 in https://asvz.ch/426-sportfahrplan?f[0]=sport:45743 for volleyball",
    )

    args = parser.parse_args()

    creds = None
    try:
        creds = CredentialsManager(
            args.organisation, args.username, args.password, args.save_credentials
        ).get()
    except AsvzBotException as e:
        logging.error(e)
        exit(1)

    chromedriver = get_chromedriver()

    enroller = None
    if args.type == "lesson":
        lesson_url = "{}/tn/lessons/{}".format(LESSON_BASE_URL, args.lesson_id)
        enroller = AsvzEnroller(chromedriver, lesson_url, creds)
    elif args.type == "training":
        enroller = AsvzEnroller.from_lesson_attributes(
            chromedriver,
            args.weekday,
            args.start_time,
            args.trainer,
            args.facility,
            args.sport_id,
            creds,
        )
    else:
        raise AsvzBotException("Unknown enrollment type: '{}".format(args.type))

    enroller.enroll()


if __name__ == "__main__":
    main()
