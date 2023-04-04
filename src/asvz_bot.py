import logging
from login import LoginManager
from schedule import ScheduleManager

logging.basicConfig(format="[%(name)s] %(levelname)s: %(message)s", level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)


def main():
    # driver = LoginManager().get_driver()

    schedule = ScheduleManager()

    schedule.add(0, 0, 0, 0, 2)
    schedule.add(1, 0, 0, 0, 1)

    schedule.run()


if __name__ == "__main__":
    main()
