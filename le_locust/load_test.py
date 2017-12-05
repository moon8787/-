# -*- coding: utf-8 -*-
'''
@summary:***
@since:2017/10/19 11:23
@author: Hu Liang
'''
from locust import HttpLocust, TaskSet, task

class UserTask(TaskSet):

    @task
    def job(self):
        with self.client.get('/', catch_response = True) as response:
            if response.status_code == 200:
                response.failure('Failed')
            else:
                response.success()

class User(HttpLocust):
    task_set = UserTask
    min_wait = 1000
    max_wait = 3000
    host = "http://www.baidu.com"