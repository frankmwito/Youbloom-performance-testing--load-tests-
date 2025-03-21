""""This file contains youbloomconnect test cases for its user flows."""

from locust import HttpUser, TaskSet,SequentialTaskSet, task, tag, constant
import logging
import random
from shared import shared_file
import json


# set up logging
logging.basicConfig(level=logging.DEBUG)

class MyTaskSet0(TaskSet):
    def on_start(self):
        """Set up headers for all requests."""
        self.headers = {"Content-Type": "application/json"}
        self.shared_file = shared_file()        
        
    @task
    @tag('login')
    def login(self):
        """send a POST request to the login endpoint"""
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
                user = random.choice(users)
                
                login_data = {
                    "email": user["email"],
                    "password": user["password"]
                }
                response = self.client.post(
                    "/login/",
                    headers = self.headers,
                    data = json.dumps(login_data),
                    name = "youbloom connect login",
                    timeout = 120 
                )
                
                if response.status_code == 200:
                    logging.info(f"Login response: {response.status_code}")
                    logging.info(f"Cookies after login: {self.client.cookies}")
                else:
                    logging.error(f"Login request failed: {response.status_code}")
                    logging.error(f"Response content: {response.text}")
        except Exception as response:
            logging.error(f"Login request failed: {response}")
            
    @task
    def enter_nested_task_set2(self):
        logging.info(f"Switching to MyTaskset2 (Artists TaskSet)")
        self.schedule_task(MyTaskset2)
        
        
@tag('Artists')
class MyTaskset2(SequentialTaskSet):
    @task
    @tag('bands')
    def artist_bands(self):
        try:
            response = self.client.get("/band/", name = "artist_bands", timeout = 120)
            logging.info(f"Artist bands response: {response.status_code}")
        except Exception as response:
            logging.error(f"Artist bands request failed: {response}")
            
    @task
    @tag('region')
    def artist_region(self):
        try:
            response = self.client.get("/regions/cityrep/", name = "artist_region", timeout = 120)
            logging.info(f"Artist region response: {response.status_code}")
        except Exception as response:
            logging.error(f"Artist region request failed: {response}")
    
    @task
    @tag('band-local')
    def artist_band_local(self):
        try:
            response = self.client.get("/band-local/", name = "artist_band_local", timeout = 120)
            logging.info(f"Artist band local response: {response.status_code}")
        except Exception as response:
            logging.error(f"Artist band local request failed: {response}")
            
    @task
    @tag('band-remote')
    def artist_band_remote(self):
        try:
            response = self.client.get("/band-remote/", name = "artist_band_remote", timeout = 120)
            logging.info(f"Artist band remote response: {response.status_code}")
        except Exception as response:
            logging.error(f"Artist band remote request failed: {response}")
    @task
    def enter_nested_task_set3(self):
        logging.info(f"Switching to MyTaskSet3 (Shows TaskSet)")
        self.schedule_task(MyTaskSet3)
        
    
      
@tag('Shows')      
class MyTaskSet3(SequentialTaskSet):      
    @task
    @tag('confirmedgig')
    def show_setup(self):
        try:
            response = self.client.get("/confirmedgig/", name = 'Show setup', timeout = 120)
            logging.info(f"show setup response: {response.status_code}")
        except Exception as response:
            logging.error(f"show setup request failed: {response}")
            
    @task
    @tag('My shows')
    def show_myshows(self):
        try:
            response = self.client.get("/myshows/", name = 'My Shows', timeout = 120)
            logging.info(f"My shows response: {response.satus_code}")
        except Exception as response:
            logging.error(f"My shows request failed: {response}")
    
    @task
    @tag('checkin')
    def checkin(self):
        try:
            response = self.client.get("/checkin/", name = 'show checkin', timeout = 120)
            logging.info(f"My show checkin response: {response.satus_code}")
        except Exception as response:
            logging.error(f"My show checkin request failed: {response}")
            
    @task
    @tag('discountcodes')
    def show_discountcodes(self):
        try:
            response = self.client.get("/discountcodes/", name = 'My Show discountcodes', timeout = 120)
            logging.info(f"My show discountcodes response: {response.satus_code}")
        except Exception as response:
            logging.error(f"My show discountcodes request failed: {response}")
        
    @task
    def enter_nested_task_set3(self):
        logging.info(f"Switching to MyTaskSet4 (Ratings TaskSet)")
        self.schedule_task(MyTaskSet4)
@tag('Ratings')        
class MyTaskSet4(SequentialTaskSet):    
    @task
    @tag('My show ratings')
    def myshow_ratings(self):
        try:
            response = self.client.get("/myshowratings/", name = 'My show ratings', timeout = 120)
            logging.info(f"My show ratings' response: {response.satus_code}")
        except Exception as response:
            logging.error(f"My show ratings request failed: {response}")
    
    @task
    @tag('Artist ratings')
    def artists_Ratings(self):
        try:
            response = self.client.get("/artistsSCRatings/", name = 'Artist Ratings', timeout = 120)
            logging.info(f"Artist Ratings response: {response.satus_code}")
        except Exception as response:
            logging.error(f"Artist Ratings request failed: {response}")
            
    @task
    @tag('Artists FanRating')
    def artists_FanRating(self):
        try:
            response = self.client.get("/artistsFanRating/", name = 'Artists FanRating', timeout = 120)
            logging.info(f"Artists FanRating response: {response.satus_code}")
        except Exception as response:
            logging.error(f"Artists FanRating request failed: {response}")
            
    @task
    def enter_nested_task_set1(self):
        logging.info(f"Switching to MyTaskSet0")
        self.interrupt()
        
    def on_stop(self):
        logging.info("Stopping the tasks")
        
        
class UserBehaviour(HttpUser):
    wait_time = constant(4)
    
    tasks = [MyTaskSet0]