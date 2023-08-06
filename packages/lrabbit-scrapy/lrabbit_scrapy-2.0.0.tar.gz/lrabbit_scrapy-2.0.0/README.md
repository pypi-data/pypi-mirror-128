lrabbit_scrapy
=====

this is a small spider,you can easy running. When you often need to crawl a single site, you don't have to redo some
repeated code every time, using this small framework you can quickly crawl data into a file or database.


Installing
----------

    $ pip3 install lrabbit_scrapy

A Simple Example
----------------

```python
class Spider(LrabbitSpider):
    """
     # spider_name 
     redis_key:
        list:spider_name 任务队列
        success:count:spider_name 记录成功数
        list:error:excepiton404
    """
    spider_name = "test"
    # 最大线程数
    max_thread_num = 10
    # 重置任务队列
    reset_task_config = False
    # 开启循环模式
    loop_task_config = False
    # 去除确认信息
    remove_confirm_config = False

    def __init__(self):
        super().__init__()
        self.session = RequestSession()
        self.proxy_session = RequestSession(proxies=None)

    def worker(self, task):
        LogUtils.log_info(task)
        self.session.send_request(method='GET', url="https://www.lrabbit.life/233333333333333333/")
        # when you keyboraderror you can't lost you task
        self.task_list.remove(task)
        # update stat
        self.update_stat_redis()
        LogUtils.log_finish(task)

    def init_task_list(self):
        res = self.mysql_client.query("select id from rookie limit 100 ")
        return [item['id'] for item in res]

    
if __name__ == '__main__':
    spider = Spider()
    spider.run()

```

Links
-----

- author: https://www.lrabbit.life/

