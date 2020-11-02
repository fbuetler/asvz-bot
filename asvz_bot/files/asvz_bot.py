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
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from validators import ValidationFailure, url as url_validator

TIMEFORMAT = "%H:%M"

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def waiting_fct(enrollment_time):
    current_time = datetime.today()

    logging.info(
        "\n\tcurrent time: {}\n\tenrollment time: {}".format(
            current_time.strftime("%H:%M:%S"), enrollment_time.strftime("%H:%M:%S")
        )
    )

    login_before_enrollment_seconds = 1 * 60
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


def asvz_enroll(
    username, password, weekday, facility, enrollment_time, sportfahrplan_link
):
    logging.info("Enrollment started")

    logging.info(
        "\n\tweekday: {}\n\tenrollment time: {}\n\tfacility: {}\n\tsportfahrplan: {}".format(
            weekday, enrollment_time, facility, sportfahrplan_link
        )
    )

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
                facility, enrollment_time.strftime(TIMEFORMAT)
            )
        ).click()

        if (enrollment_time - datetime.today()).days >= 0:
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

        # choose organization:
        organization = driver.find_element_by_xpath(
            "//input[@id='userIdPSelection_iddtext']"
        )
        organization.send_keys("{}a".format(Keys.CONTROL))
        organization.send_keys("ETH Zurich")
        organization.send_keys(Keys.ENTER)

        driver.find_element_by_xpath("//input[@id='username']").send_keys(username)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        logging.info("Submitted Login Credentials")

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
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="ETHZ username i.e. nethz")
    parser.add_argument("-p", "--password", help="ETHZ password")
    parser.add_argument(
        "-w",
        "--weekday",
        help="Day of the week of the lesson i.e. 0-6 for Sunday-Saturday",
    )
    parser.add_argument("-t", "--time", help="Time when the lesson starts e.g. '19:15'")
    parser.add_argument(
        "-f",
        "--facility",
        help="Facility where the lesson takes place e.g. 'Sport Center Polyterrasse'",
    )
    parser.add_argument(
        "sportfahrplan",
        help="link to particular sport on ASVZ Sportfahrplan, e.g. https://asvz.ch/426-sportfahrplan?f[0]=sport:45743 for volleyball. Make sure there starts only one lesson for that particular time at that particular location (i.e. use ASVZ filters).",
    )
    args = parser.parse_args()
    logging.debug("Parsed arguments")

    # validate args
    if args.weekday == "0":
        weekday = "Sonntag"
    elif args.weekday == "1":
        weekday = "Montag"
    elif args.weekday == "2":
        weekday = "Dienstag"
    elif args.weekday == "3":
        weekday = "Mittwoch"
    elif args.weekday == "4":
        weekday = "Donnerstag"
    elif args.weekday == "5":
        weekday = "Freitag"
    elif args.weekday == "6":
        weekday = "Samstag"
    else:
        logging.error("invalid weekday specified")
        exit(1)

    try:
        time = datetime.strptime(args.time, TIMEFORMAT)
    except ValueError:
        logging.error("invalid time specified")
        exit(1)

    if not url_validator(args.sportfahrplan):
        logging.error("invalid url specified")
        exit(1)

    current_time = datetime.today()
    enrollment_time = datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        time.hour,
        time.minute,
    )

    # special case if one starts the script max 24h before the enrollement
    # e.g enrollment at Monday 20:00, script started on Sunday 21:00
    if current_time > enrollment_time:
        enrollment_time += timedelta(days=1)
        logging.info(
            "The enrollement for today is already over. Assuming you wanted to enroll tomorrow."
        )

    logging.info("Script started")
    waiting_fct(time)

    asvz_enroll(
        args.username,
        args.password,
        weekday,
        args.facility,
        enrollment_time,
        args.sportfahrplan,
    )
    logging.info("Script successfully finished")


if __name__ == "__main__":
    main()