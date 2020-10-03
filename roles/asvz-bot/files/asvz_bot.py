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
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def waiting_fct(lesson_time):
    currentTime = datetime.today()
    enrollmentTime = datetime.strptime(lesson_time, "%H:%M")

    logging.info(
        "\ncurrent time: {}\nlesson time: {}".format(currentTime, enrollmentTime)
    )
    while currentTime.hour < enrollmentTime.hour:
        logging.info("Wait for enrollment to open")
        time.sleep(60)
        currentTime = datetime.today()

    if currentTime.hour == enrollmentTime.hour:
        while currentTime.minute < enrollmentTime.minute - 3:
            logging.info("Wait for enrollment to open")
            time.sleep(30)
            currentTime = datetime.today()

    if currentTime.hour > enrollmentTime.hour:
        logging.info("Enrollment time is over. Exiting...")
        exit(1)

    return


def asvz_enroll(username, password, weekday, facility, start_time, sportfahrplan_link):
    logging.info("Enrollment started")

    if weekday == "0":
        weekday = "Sonntag"
    elif weekday == "1":
        weekday = "Montag"
    elif weekday == "2":
        weekday = "Dienstag"
    elif weekday == "3":
        weekday = "Mittwoch"
    elif weekday == "4":
        weekday = "Donnerstag"
    elif weekday == "5":
        weekday = "Freitag"
    elif weekday == "6":
        weekday = "Samstag"
    else:
        logging.error("invalid weekday specified")
        exit(0)

    logging.info(
        "\nweekday: {}\n facility: {}\n start time: {}\n sportfahrplan: {}".format(
            weekday, facility, start_time, sportfahrplan_link
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
        driver.implicitly_wait(10)  # wait 10 seconds if not defined differently
        logging.info("Headless Chrome Initialized")
        # find corresponding day div:
        day_ele = driver.find_element_by_xpath(
            "//div[@class='teaser-list-calendar__day'][contains(., '" + weekday + "')]"
        )
        # search in day div after corresponding location and time
        day_ele.find_element_by_xpath(
            ".//li[@class='btn-hover-parent'][contains(., '"
            + facility
            + "')][contains(., '"
            + start_time
            + "')]"
        ).click()

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[@class='btn btn--block btn--icon relative btn--primary']",
                )
            )
        ).send_keys(Keys.ENTER)
        # switch to new window:
        time.sleep(2)  # necessary because tab needs to be open to get window handles
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
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
        organization.send_keys(Keys.CONTROL + "a")
        organization.send_keys("ETH Zurich")
        organization.send_keys(Keys.ENTER)

        driver.find_element_by_xpath("//input[@id='username']").send_keys(username)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        logging.info("Submitted Login Credentials")

        # wait for button to be clickable for 5 minutes, which is more than enough
        # still needs to be tested what happens if we are on the page before button is enabled
        WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@id='btnRegister' and @class='btn-primary btn enrollmentPlacePadding ng-star-inserted']",
                )
            )
        ).click()
        logging.info("Successfully enrolled. Train hard and have fun!")
    except:  # using non-specific exceptions, since there are different exceptions possible: timeout, element not found because not loaded, etc.
        driver.quit()
        raise  # re-raise previous exception

    driver.quit  # close all tabs and window
    return True


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="ETHZ username i.e. nethz")
parser.add_argument("-p", "--password", help="ETHZ password")
parser.add_argument(
    "-w",
    "--weekday",
    help="Day of the week of the lesson (0-6 for Sunday-Saturday, etc )",
)
parser.add_argument("-t", "--time", help="Time when the lesson starts e.g. 19:15")
parser.add_argument(
    "-f",
    "--facility",
    help="Facility where the lesson takes place e.g. Sport Center Polyterrasse",
)
parser.add_argument(
    "sportfahrplan",
    help="link to particular sport on ASVZ Sportfahrplan, e.g. volleyball",
)
args = parser.parse_args()

# run enrollment script:
i = 0  # count
success = False

logging.info("Script started")
waiting_fct(args.time)

# if there is an exception (no registration possible), enrollment is tried again and then stopped to avoid a lock-out
while not success:
    try:
        success = asvz_enroll(
            args.username,
            args.password,
            args.weekday,
            args.facility,
            args.time,
            args.sportfahrplan,
        )
        logging.info("Script successfully finished")
    except:
        if i < 3:
            i += 1
            logging.info("Enrollment failed. Start try number {}".format(i + 1))
            pass
        else:
            raise
