# <center>Locust学习总结</center>
-------

## 学习网址
[Locust中文](http://www.testclass.net/locust/)  
[Locust Documentation英文](https://docs.locust.io/en/latest/index.html)

## locust是什么
locust是一个开源性能测试工具，它使用 Python 代码来定义用户行为。用它可以模拟百万计的并发用户访问你的系统。  
locust 的并发机制采用协程（gevent）的机制，协程避免了系统级资源调度，可以大幅提高单机的并发能力
## locust执行命令
*locust -f .\脚本名称 --host=测试网址*  
-f 指定性能测试脚本文件。  
–host 指定被测试应用的URL的地址，注意访问百度使用的HTTPS协议。
## locust访问地址：
http://localhost:8089 （Locust启动网络监控器，默认为端口号为: 8089）

## locust no-web模式
*locust -f load_test.py --host=https://www.baidu.com --no-web -c 10 -r 2 -t 1m*  
**启动参数：**  
–no-web 表示不使用Web界面运行测试。  
-c 设置虚拟用户数。  
-r 设置每秒启动虚拟用户数。  
-t 设置设置运行时间。  

## Locust 分布式运行
在 master 模式下启动 Locust:  
*locust -f my_loucstfile.py --master*  
在每个 slave 中执行(192.168.0.14 替换为你 msater 的IP):  
*locust -f my_locustfile.py --slave --master-host=192.168.0.14*  


**参数说明:**  
–master  
设置 Locust 为 master 模式。网页交互会在这台节点机器中运行。  
–slave  
设置 Locust 为 slave 模式。  
–master-host=X.X.X.X  
可选项，与 --slave 一起结合使用，用于设置 master 模式下的 master 机器的IP/hostname(默认设置为127.0.0.1)  
–master-port=5557  
可选项，与 --slave 一起结合使用，用于设置 master 模式下的 master 机器中 Locust 的端口(默认为5557)。注意，locust 将会使用这个指定的
端口号，同时指定端口+1的号也会被占用。因此，5557 会被使用，Locust将会使用 5557 和 5558。  
–master-bind-host=X.X.X.X  
可选项，与 --master 一起结合使用。决定在 master 模式下将会绑定什么网络接口。默认设置为*(所有可用的接口)。  
–master-bind-port=5557  
可选项，与 --master 一起结合使用。决定哪个网络端口 master 模式将会监听。默认设置为 5557。注意 Locust 会使用指定的端口号，同时指定
端口+1的号也会被占用。因此，5557 会被使用，Locust 将会使用 5557 和 5558。  
–expect-slaves=X  
在 no-web 模式下启动 master 时使用。master 将等待X连接节点在测试开始之前连接  

## Locust 的类和方法
 

**HttpLocust 类:**

``` python
from locust import HttpLocust, TaskSet, task

class UserTask(TaskSet):

    @task
    def tc_index(self):
        self.client.get("/")

class UserOne(HttpLocust):
    task_set = UserTask
    weight = 1
    min_wait = 1000
    max_wait = 3000
    stop_timeout = 5
    host = "https://www.baidu.com"

class UserTwo(HttpLocust):
    weight = 2
    task_set = UserTask
    host = "https://www.baidu.com"
``` 
    
    
* task_set
指向一个 TaskSet 类，TaskSet 类定义了每个用户的行为。
* min_wait
用户执行任务之间等待时间的下界，单位：毫秒。如果TaskSet类中有覆盖，以TaskSet 中的定义为准。
* max_wait
用户执行任务之间等待时间的上界，单位：毫秒。如果TaskSet类中有覆盖，以TaskSet中的定义为准。
* host
如果是 Web 服务的测试，host 相当于是提供 URL 前缀的默认值，但是如果在命令行中指定了 --host 选项，则以命令行中指定的为准。如果不是
Web 服务测试，使用默认的 None 就好。
* stop_timeout
设置 Locust 多少秒后超时，如果为 None ,则不会超时。
* weight
一个Locust实例被挑选执行的权重，数值越大，执行频率越高。



**TaskSet 类:**
```python
from locust import HttpLocust, TaskSet, task


class stay(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("start test")

    @task(3)
    def readBook(self):
        print('I am reading a book.')

    @task(7)
    def listenMusic(self):
        print('I am listening to music.')

    @task(1)
    def logOut(self):
        self.interrupt()


class UserTask(TaskSet):
    tasks = {stay:2}

    @task(1)
    def leave(self):
        print('I don not like this page.')


class User(HttpLocust):
    task_set = UserTask
    host = "https://www.baidu.com"
```

TaskSet类定义了每个用户的任务集合，测试任务开始后，每个 Locust 用户会从 TaskSet 中随机挑选一个任务执行，然后随机等待 HttpLocust 类中
定义的 min_wait和 max_wait 之间的一段时间，执行下一个任务。
 
* on_start()
定义每个 Locust 用户开始做的第一件事。
* @task
通过@task()装饰的方法为一个事务。方法的参数用于指定该行为的执行权重。参数越大每次被虚拟用户执行的概率越高。如果不设置默认为1。
* interrupt(reschedule=True)
顶层的TaskSet（即被绑定到某个Locust类的task_set的第一层TaskSet）不能调用这个方法。reschedule置为True时，从被嵌套任务出来马上选择新
任务执行，如果置为False，从被嵌套任务出来后，随机等待min_wait和max_wait之间的一段时间，再选择新任务执行。
* tasks 属性
tasks = {stay:2} 表示每个用户执行 stay 的频率是2，也就的 UserTask 的两倍。
