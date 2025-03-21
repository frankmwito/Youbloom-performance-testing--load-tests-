""""This file contains youbloomconnect test cases for its user flows."""

from locust import HttpUser, TaskSet, task, tag, constant
import logging
import random


# set up logging
logging.basicConfig(level=logging.DEBUG)

class MyTaskSet1(TaskSet):
    def on_start(self):
        """Set up headers for all requests."""
        