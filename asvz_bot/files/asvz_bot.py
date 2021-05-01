#!/usr/bin/python3

"""
Based on initial script of Julian Stiefel
Initally Created on: Mar 20, 2019
Author: Julian Stiefel
License: BSD 3-Clause
Description: Script for automatic enrollment in ASVZ classes

Updated Version on: September 25, 2020
Author: Florian Bütler
"""

import time
import argparse
import logging
import getpass
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from validators import ValidationFailure, url as url_validator

TIMEFORMAT = "%H:%M"

BASE_URL = "https://asvz.ch/426-sportfahrplan?f[0]=sport:"

# organisation name as dispay by SwitchAAI
ORGANISATIONS = {
    "ETH": "ETH Zürich",
    "Uni Zürich": "University of Zurich",
    "ZHAW": "ZHAW - Zürcher Hochschule für Angewandte Wissenschaften",
}

WEEKDAYS = {
    "Mo": "Montag",
    "Di": "Dienstag",
    "Mi": "Mittwoch",
    "Do": "Donnerstag",
    "Fr": "Freitag",
    "Sa": "Samstag",
    "So": "Sonntag",
}

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def validate_starttime(start_time):
    try:
        return datetime.strptime(start_time, TIMEFORMAT)
    except ValueError:
        msg = "Invalid start time specified. Supported format is {}".format(TIMEFORMAT)
        raise argparse.ArgumentTypeError(msg)


def wait_until(enrollment_time):
    current_time = datetime.today()

    logging.info(
        "\n\tcurrent time: {}\n\tenrollment time: {}".format(
            current_time.strftime("%H:%M:%S"), enrollment_time.strftime("%H:%M:%S")
        )
    )

    login_before_enrollment_seconds = 1 * 59
    if (enrollment_time - current_time).seconds > login_before_enrollment_seconds:
        sleep_time = (
            enrollment_time - current_time
        ).seconds - login_before_enrollment_seconds
        logging.info(
            "Sleep for {} seconds until {}".format(
                sleep_time,
                (current_time + timedelta(seconds=sleep_time)).strftime("%H:%M:%S"),
            )
        )
        time.sleep(sleep_time)
        currentTime = datetime.today()

    return


def organisation_login(driver, organisation, username, password):
    logging.info("Login to '{}'".format(organisation))

    organization = driver.find_element_by_xpath(
        "//input[@id='userIdPSelection_iddtext']"
    )
    organization.send_keys("{}a".format(Keys.CONTROL))
    organization.send_keys(organisation)
    organization.send_keys(Keys.ENTER)

    # apparently all organisations have the same xpath
    driver.find_element_by_xpath("//input[@id='username']").send_keys(username)
    driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
    driver.find_element_by_xpath("//button[@type='submit']").click()

    logging.info("Submitted Login Credentials")


def asvz_enroll(
    organisation,
    username,
    password,
    weekday,
    start_time,
    facility,
    sportfahrplan_link,
):
    logging.info("Enrollment started")

    options = Options()
    options.add_argument(
        "--private"
    )  # open in private mode to avoid different login scenario
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(sportfahrplan_link)
        driver.implicitly_wait(10)
        logging.info("Headless Chrome started")

        day_ele = driver.find_element_by_xpath(
            "//div[@class='teaser-list-calendar__day'][contains(., '{}')]".format(
                weekday
            )
        )
        day_ele.find_element_by_xpath(
            ".//li[@class='btn-hover-parent'][contains(., '{}')][contains(., '{}')]".format(
                facility,
                start_time.strftime(TIMEFORMAT),
            )
        ).click()

        if (start_time - datetime.today()).days >= 0:
            xpath = (
                "//a[@class='btn btn--block btn--icon relative btn--primary-border']"
            )
        else:
            xpath = "//a[@class='btn btn--block btn--icon relative btn--primary']"

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    xpath,
                )
            )
        ).send_keys(Keys.ENTER)

        time.sleep(2)  # necessary because tab needs to be open to get window handles
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        logging.info("Lesson found")

        full = None
        try:
            full = driver.find_element_by_xpath(
                "//alert[@class='ng-star-inserted'][contains(., 'ausgebucht')]"
            )
        except:
            pass
        if full is not None:
            logging.info("Lesson is booked out.")
            return

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

        organisation_login(driver, organisation, username, password)

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


def main():
    logging.debug("Parsing arguments")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-org",
        "--organisation",
        required=True,
        choices=list(ORGANISATIONS.keys()),
        help="Name of your organisation.",
    )
    parser.add_argument(
        "-u", "--username", required=True, type=str, help="Organisation username"
    )
    parser.add_argument(
        "-w",
        "--weekday",
        required=True,
        choices=list(WEEKDAYS.keys()),
        help="Day of the week of the lesson",
    )
    parser.add_argument(
        "-s",
        "--starttime",
        required=True,
        type=validate_starttime,
        help="Time when the lesson starts e.g. '19:15'",
    )
    parser.add_argument(
        "-f",
        "--facility",
        required=True,
        type=str,
        help="Facility where the lesson takes place e.g. 'Sport Center Polyterrasse'",
    )
    parser.add_argument(
        "sportfahrplan_nr",
        type=int,
        help="number at the end of link to particular sport on ASVZ Sportfahrplan, e.g. 45743 in https://asvz.ch/426-sportfahrplan?f[0]=sport:45743 for volleyball.",
    )
    args = parser.parse_args()
    logging.debug("Parsed arguments")

    current_time = datetime.today()
    start_time = datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        args.starttime.hour,
        args.starttime.minute,
    )

    # special case if one starts the script max 24h before the enrollement
    # e.g enrollment at Monday 20:00, script started on Sunday 21:00
    if current_time > start_time:
        start_time += timedelta(days=1)
        logging.info(
            "The enrollement for today is already over. Assuming you wanted to enroll tomorrow."
        )

    url = "{}{}&date={}-{:02d}-{:02d}%20{}:{}".format(
        BASE_URL,
        args.sportfahrplan_nr,
        start_time.year,
        start_time.month,
        start_time.day + 1,
        args.starttime.hour,
        args.starttime.minute,
    )
    if not url_validator(url):
        logging.error("Invalid url specified: '{}'".format(url))
        exit(1)

    password = getpass.getpass("Organisation password:")

    logging.info(
        "Summary:\n\tOrganisation: {}\n\tUsername: {}\n\tPassword: {}\n\tWeekday: {}\n\tEnrollment time: {}\n\tFacility: {}\n\tSportfahrplan: {}".format(
            args.organisation,
            args.username,
            "*" * len(password),
            args.weekday,
            start_time,
            args.facility,
            url,
        )
    )

    logging.info("Script started")
    wait_until(start_time)

    asvz_enroll(
        args.organisation,
        args.username,
        password,
        args.weekday,
        start_time,
        args.facility,
        url,
    )
    logging.info("Script successfully finished")


if __name__ == "__main__":
    main()
