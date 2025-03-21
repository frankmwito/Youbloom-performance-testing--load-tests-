# User class 

from locust import HttpUser, constant
import youbloomconnect
import High_user_tasks
import Low_user_tasks

class UserOnHost1(HttpUser):
    wait_time = constant(4)
    host = "https://youbloom.com"
    
    tasks = [High_user_tasks.MyTaskSet1, Low_user_tasks.MyTaskSet]
    

class UserOnHost2(HttpUser):
    wait_time = constant(4)
    host = "https://youbloomconnect.com"
    
    tasks = [youbloomconnect.MyTaskSet0]