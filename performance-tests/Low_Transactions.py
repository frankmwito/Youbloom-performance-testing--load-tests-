from locust import HttpUser,TaskSet, task, tag, between
import logging
from High_Transactions import MyTaskSet1

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class MyTaskSet(TaskSet):
    @task(3)
    @tag('Homepage')
    def homepage(self):
        try:
            response = self.client.get("/")
            logging.info(f"Homepage response: {response.status_code}")
        except Exception as e:
            logging.error(f"Homepage request failed: {e}")
    
    @task(2)
    @tag('About')
    def about(self):
        try:
            response = self.client.get("/about/")
            logging.info(f"About response: {response.status_code}")
        except Exception as e:
            logging.error(f"About request failed: {e}")
    
    @task(1)
    @tag('Contact')
    def contact(self):
        try:
            response = self.client.get("/contact/")
            logging.info(f"Contact response: {response.status_code}")
        except Exception as e:
            logging.error(f"Contact request failed: {e}")
    
    @task(2)
    @tag('Intern')
    def intern(self):
        try:
            response = self.client.get("/intern/")
            logging.info(f"Intern response: {response.status_code}")
        except Exception as e:
            logging.error(f"Intern request failed: {e}")
    
    @task(3)
    @tag('Blog')
    def blog(self):
        try:
            response = self.client.get("/blog/")
            logging.info(f"Blog response: {response.status_code}")
        except Exception as e:
            logging.error(f"Blog request failed: {e}")
    
    @task(2)
    @tag('Privacy')
    def privacy(self):
        try:
            response = self.client.get("/privacy/")
            logging.info(f"Privacy response: {response.status_code}")
        except Exception as e:
            logging.error(f"Privacy request failed: {e}")
    
    @task(1)
    @tag('Help_Center')
    def help(self):
        try:
            response = self.client.get("/knowledge-base/")
            logging.info(f"Help Center response: {response.status_code}")
        except Exception as e:
            logging.error(f"Help Center request failed: {e}")
    
    @task(2)
    @tag('Terms')
    def terms(self):
        try:
            response = self.client.get("/youbloom-at-bloom-2025/")
            logging.info(f"Terms response: {response.status_code}")
        except Exception as e:
            logging.error(f"Terms request failed: {e}")

class UserBehaviour(HttpUser):
    host = "https://youbloom.com"  # Set the host URL here
    wait_time = between(0.5, 4)
    tasks = [MyTaskSet , MyTaskSet1]