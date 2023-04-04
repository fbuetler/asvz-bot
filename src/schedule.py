import sched
import time

from collections import namedtuple
from typing import Optional

Event = namedtuple("Event", ["sport", "weekday", "start_time", "facility"])


class ScheduledEvent:
    def __init__(
        self,
        schedule_manager: "ScheduleManager",
        event: Event,
        start_time_seconds: float,
        repeat_interval_seconds: float = 0,
        next_time_seconds: float = 0,
    ):
        self.schedule_manager = schedule_manager
        self.event = event
        self.start_time_seconds = start_time_seconds
        self.repeat_interval_seconds = repeat_interval_seconds

        if next_time_seconds == 0:
            self.next_time_seconds = start_time_seconds
        else:
            self.next_time_seconds = next_time_seconds

    def execute(self):
        self.sign_up()
        self.update_schedule()
        print(self.event)

    def sign_up(self):
        pass

    def get_next(self) -> Optional["ScheduledEvent"]:
        if self.repeat_interval_seconds > 0:
            next_time_seconds = self.next_time_seconds + self.repeat_interval_seconds
            new_event = ScheduledEvent(
                self.schedule_manager,
                self.event,
                self.start_time_seconds,
                self.repeat_interval_seconds,
                next_time_seconds,
            )
            return new_event
        else:
            return None

    def update_schedule(self):
        new_event = self.get_next()
        if new_event:
            self.schedule_manager.schedule_event(new_event)


class ScheduleManager:
    def __init__(self):
        self.schedule = sched.scheduler(time.time)

    def run(self):
        self.schedule.run()

    def schedule_event(self, scheduled_event: ScheduledEvent):
        self.schedule.enterabs(scheduled_event.next_time_seconds, 1, scheduled_event.execute)

    def add(self, sport, weekday, start_time, facility, repeat_interval_seconds: float = 0):
        event = Event(sport, weekday, start_time, facility)
        scheduled_event = ScheduledEvent(self, event, time.time(), repeat_interval_seconds)
        self.schedule_event(scheduled_event)

    def __str__(self):
        return str(self.schedule.queue)
