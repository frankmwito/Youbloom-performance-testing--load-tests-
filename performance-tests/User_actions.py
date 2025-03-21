# User class 

from locust import HttpUser, task, constant

class UserBehaviour(HttpUser):
    wait_time = constant(4)
    host = "https://youbloom.com"
    
    
    