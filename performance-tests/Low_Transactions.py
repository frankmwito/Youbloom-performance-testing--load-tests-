from locust import HttpUser, SequentialTaskSet, task, between


"""
This is a Locust test script to test low transaction endpoints in the host: https://youbloom.com

Classes:
    UserBehavior: Defines the behavior of the simulated user.

Methods:
    on_start(self): Method that runs when a simulated user starts.
    index(self): Simulates a user visiting the index page.
    about(self): Simulates a user visiting the about page.

Usage:
    Run this script with Locust to simulate user behavior and test the performance of low transaction endpoints on https://youbloom.com.
"""
# test class for low transactions endpoints in sequential order

class MyTaskSet(SequentialTaskSet):
    @task(3)
    @task('Homepage')
    def homepage(self):
        self.client.get("/")
    
    @task(3)
    @task('About')
    def about(self):
        self.client.get("/about/")
    
    @task(1)
    @task('Contact')
    def contact(self):
        self.client.get("/contact/")
        
    @task(2)
    @task('Intern')
    def intern(self):
        self.client.get("/intern/")
    
    @task(2)
    @task('Blog')
    def blog(self):
        self.client.get("/blog/")
    
    @task(1)
    @task('Privacy')
    def privacy(self):
        self.client.get("/privacy/")
    
    @task(1)
    @task('Help_Center')
    def privacy(self):
        self.client.get("/knowledge-base/")
        
    @task(2)
    @task('Terms')
    def privacy(self):
        self.client.get("/youbloom-at-bloom-2025/")

# test class for low transactions endpoints

class UserBehaviour(HttpUser):
    wait_time = between(1, 10)
    
    tasks = [MyTaskSet]