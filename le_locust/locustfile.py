# -*- coding: utf-8 -*-
'''
@summary:***
@since:2017/10/19 13:39
@author: Hu Liang
'''
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        self.client.post("/login", {"username":"ellen_key", "password":"education"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/profile")

class websiteUser(HttpLocust):
    task_set = UserBehavior
    host = "http://debugtalk.com"
    min_wait = 5000
    max_wait = 9000