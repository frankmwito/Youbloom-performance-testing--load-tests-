# Contains the tests for high transactions critical user flows for the application under test (AUT) 
# sign up, login, logout, account management, search, add to cart, checkout, etc.

from locust import HttpUser, TaskSet, task, tag, constant
import logging
from faker import Faker
import json

# set up logging
logging.basicConfig(level=logging.DEBUG)

class MyTaskSet1(TaskSet):
    
    @task
    @tag('Signup')
    def signup(self):
        # send a post request to the signup endpoint
        faker = Faker()
        data = {
            "first_name" : faker.first_name(),
            "last_name" : faker.last_name(),
            "email" : faker.email(),
            "password" : "Test@1111",
            "confirm_password" : "Test@1111"
        }
        
        response = self.client.post("/become-a-show-creator/", data=json.dumps(data), name="Signup")
        
        if response.status_code == 200:
            logging.info(f"Signup response: {response.status_code}")
            print(f"Signup successful")
            print(f"Signup successful with status code: {response.status_code}")
            self.save_user(data)
        else:
            logging.error(f"Signup request failed: {response.status_code}")
            print(f"Signup failed")
            print(f"Signup failed with status code: {response.status_code}")
            
    def save_user(self, data):
        """save generated user data to a file"""
        # Save only email and password
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
            json.dump(users, file)
            
    @task
    @tag('Login')
    def login(self):
        # send a post request to the login endpoint
        
        # get the user data from the file
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.error("No users found")
            return
        
        # get the last user data
        data = users[-1]
        
        # Use only email and password for login
        login_data = {
            "email": data["email"],
            "password": data["password"]
        }
        
        response = self.client.post("/login/", data=json.dumps(login_data), name="login")
        
        if response.status_code == 200:
            logging.info(f"Login response: {response.status_code}")
            print(f"Login successful")
            print(f"Login successful with status code: {response.status_code}")
        else:
            logging.error(f"Login request failed: {response.status_code}")
            print(f"Login failed")
            print(f"Login failed with status code: {response.status_code}")

