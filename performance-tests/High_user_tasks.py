# Contains the tests for high transactions critical user flows for the application under test (AUT) 
# sign up, login, logout, account management, search, add to cart, checkout, etc.

from locust import HttpUser, TaskSet, task, tag, constant
import logging
from faker import Faker
import json
import random
from shared import shared_file # Import save_user function properly

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class MyTaskSet1(TaskSet):
    def on_start(self):
        """Set up headers for all requests."""
        self.headers = {"Content-Type": "application/json"}
        self.shared_file = shared_file()  # Create an instance of SharedFile

    @task(2)
    @tag('Signup')
    def signup(self):
        """Send a POST request to the signup endpoint."""
        faker = Faker()
        data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "password": "Test@1111",
            "confirm_password": "Test@1111"
        }

        try:
            response = self.client.post(
                "/become-a-show-creator/",
                data=json.dumps(data),
                headers=self.headers,
                name="Signup",
                timeout=120  # Increased timeout
            )

            if response.status_code == 200:
                logging.info(f"Signup response: {response.status_code}")
                self.shared_file.save_user(data)  # Call the method on the instance
            else:
                logging.error(f"Signup request failed: {response.status_code}")
                logging.error(f"Response content: {response.text}")
        except Exception as e:
            logging.error(f"Signup request failed: {e}")

    @task(1)
    def enter_nested_task_set2(self):
        logging.info("Switching to MyTaskset2 (Login TaskSet)")
        self.schedule_task(self.MyTaskset2)  # Call the class, not a method

    class MyTaskset2(TaskSet):
        def on_start(self):
            self.headers = {"Content-Type": "application/json"}
            logging.info("Starting MyTaskset2 (Login TaskSet)")

        @task(2)
        @tag('login')
        def login(self):
            """Send a POST request to the login endpoint."""
            try:
                with open("users.json", "r") as file:
                    users = json.load(file)

                if not users:
                    logging.error("No users found in the file")
                    return

            except (FileNotFoundError, json.JSONDecodeError):
                logging.error("No users found")
                return

            # Select one random user
            user = random.choice(users)
            login_data = {
                "email": user["email"],
                "password": user["password"]
            }
            try:
                response = self.client.post(
                    "/login/",
                    data=json.dumps(login_data),
                    headers=self.headers,
                    name="Login",
                    timeout=120  # Increased timeout
                )
                if response.status_code == 200:
                    logging.info("Login successful")
                else:
                    logging.error(f"Login request failed: {response.status_code}")
                    logging.error(f"Response content: {response.text}")
            except Exception as e:
                logging.error(f"Login request failed: {e}")

        @task(1)
        def stop_nested_1(self):
            logging.info("Stopping MyTaskset2 (Login TaskSet)")
            self.interrupt()  # Exit back to parent TaskSet

    def on_stop(self):
        logging.info("Stopping MyTaskSet1 (Signup TaskSet)")


class UserBehaviour(HttpUser):
    host = "https://youbloom.com"  # Set the host URL here
    wait_time = constant(4)
    tasks = [MyTaskSet1]  # Use a list for tasks