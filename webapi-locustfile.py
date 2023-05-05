import json
from locust import HttpUser, between, task
from datetime import datetime, timedelta
import random

class MyUser(HttpUser):
    wait_time = between(5, 100) # add a random delay between requests

    @task(9)  
    def get_data(self):
        # GET endpoint are used more often
        self.client.get("/users")
    
    def get_data_list(self):
        response = self.client.get("/users")
        if response.ok:
            return json.loads(response.text)
        else:
            return []

    @task(1) # POST requests are used less frequently than GET
    def create_data(self):
        # replace with your POST endpoint and payload
        payload = {"name": "fola", "email": "fola@gmail"}
        self.client.post("/users", json=payload)

    @task(2) # PUT requests are used even less frequently but a bit more than POST
    def update_data(self):
        data = self.get_data_list()
        if data:
            item_id = random.choice(data)["id"]
        # replace with your PUT endpoint and payload
        payload = {"name": "Toba", "email": "toba@gmail"}
        self.client.put(f"/users/{item_id}", json=payload)

    @task(1) # DELETE requests are used the least frequently
    def delete_data(self):
        data = self.get_data_list()
        if data:
            item_id = random.choice(data)["id"]
        self.client.delete(f"/users/{item_id}")

   
class ContinuousRun(HttpUser):
    wait_time = between(0, 5)

    def on_start(self):
        self.run_for_days(7)

    def run_for_days(self, days):
        stop_time = datetime.now() + timedelta(days=days)
        self.environment.runner.start(1, spawn_rate=1, stop_time=stop_time)
