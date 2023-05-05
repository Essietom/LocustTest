import json
from locust import HttpUser, between, task
from datetime import datetime, timedelta
import random

class MyUser(HttpUser):
    wait_time = between(0, 3) # add a random delay between requests

    @task
    def get_data(self):
        self.client.get("/transformAndValidateShipment")

    def on_start(self):
        self.schedule_task()


    def schedule_task(self):
        now = self.get_current_time()
        if self.is_weekend(now) or now.hour >= 19 or now.hour < 6:
            # Low traffic period
            self.schedule_task_in_seconds(5 + random.randint(10, 45))
        else:
            # High traffic period
            self.schedule_task_in_seconds(2 + random.randint(0, 3))

    def schedule_task_in_seconds(self, seconds):
        self._task_runner.add_task(self._task_runner.Task(self.my_task, args=[], kwargs={}), seconds)

    def get_current_time(self):
        return self.environment.runner.stats.get_current_human_time()
    
    def is_weekend(self, dt):
        return dt.weekday() >= 5


class ContinuousRun(HttpUser):
    wait_time = between(0, 5)

    def on_start(self):
        self.run_for_days(7)

    def run_for_days(self, days):
        stop_time = datetime.now() + timedelta(days=days)
        self.environment.runner.start(1, spawn_rate=1, stop_time=stop_time)
