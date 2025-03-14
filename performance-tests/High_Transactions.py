# Contains the tests for high transactions critical user flows for the application under test (AUT) 
# sign up, login, logout, account management, search, add to cart, checkout, etc.

from locust import HttpUser, TaskSet, task, tag, constant
import logging
from faker import Faker
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class MyTaskSet1(TaskSet):
    def on_start(self):
        """Set up headers for all requests."""
        self.headers = {"Content-Type": "application/json"}

    @task
    @tag('Signup')
    def signup(self):
        # Send a POST request to the signup endpoint
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
                timeout=60  # Increase timeout to 60 seconds
            )

            if response.status_code == 200:
                logging.info(f"Signup response: {response.status_code}")
                print("Signup successful")
                self.save_user(data)
            else:
                logging.error(f"Signup request failed: {response.status_code}")
                print(f"Signup failed with status code: {response.status_code}")
                print(f"Response content: {response.text}")  # Log the response content
        except Exception as e:
            logging.error(f"Signup request failed: {e}")
            print("Signup failed with exception")

    def save_user(self, data):
        """Save generated user data to a file."""
        data_to_save = {
            "email": data["email"],
            "password": data["password"]
        }

        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        users.append(data_to_save)

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)  # Add indentation for readability

    @task
    @tag('login')
    def login(self):
        # Send a POST request to the login endpoint
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.error("No users found")
            return

        # Get the last user data
        data = users[-1]

        # Use only email and password for login
        login_data = {
            "email": data["email"],
            "password": data["password"]
        }

        try:
            response = self.client.post(
                "/login/",
                data=json.dumps(login_data),
                headers=self.headers,
                name="Login",
                timeout=60  # Increase timeout to 60 seconds
            )

            if response.status_code == 200:
                logging.info(f"Login response: {response.status_code}")
                print("Login successful")
            else:
                logging.error(f"Login request failed: {response.status_code}")
                print(f"Login failed with status code: {response.status_code}")
                print(f"Response content: {response.text}")  # Log the response content
        except Exception as e:
            logging.error(f"Login request failed: {e}")
            print("Login failed with exception")

class UserBehaviour(HttpUser):
    host = "https://youbloom.com"  # Set the host URL here
    wait_time = constant(4)
    tasks = [MyTaskSet1]