# -*- coding: utf-8 -*-
"""
@Time    : 2021/11/18 11:41
@Author  : lrabbit
@FileName: spider.py
@Software: PyCharm
@Blog    : https://www.lrabbit.life
"""
import time
from lrabbit_scrapy.common_utils.mysql_helper import MysqlClient
from lrabbit_scrapy.common_utils.redis_helper import RedisClient
from threading import Thread
from lrabbit_scrapy.common_utils.all_in_one import get_time_format_now
from lrabbit_scrapy.all_excepiton import Excepiton404


class LrabbitSpider:

    def __init__(self):
        self.mysql_client = MysqlClient()
        self.redis_client = RedisClient()
        spider_task_key = f'list:{self.__getattribute__("spider_name")}'
        self.exception_count_task_key = "list:error"
        self.spider_name = self.__getattribute__("spider_name")
        print("spider_redis_key", spider_task_key)
        self.task_list_redis_key = spider_task_key
        self.success_count_all_key = f"success:count:{self.spider_name}"
        self.success_count_day_key = f"success:count:{self.spider_name}:{get_time_format_now()}"
        self.thread_task_list = []
        self.task_list = []

    def _send_task_redis(self, task_list):
        for task in task_list:
            print("新增任务", task)
            self.redis_client.redis_executor.sadd(self.task_list_redis_key, task)

    def update_stat_redis(self):
        """
         success:count_all   success:count:spider_name
         success:count:day   success:count:spider_name:2021-11-11
        :return:
        """

        self.redis_client.redis_executor.incr(self.success_count_all_key)
        self.redis_client.redis_executor.incr(self.success_count_day_key)

    def _init_task_list(self):

        try:
            reset_task_config = self.__getattribute__("reset_task_config")
        except Exception as e:
            print("是否重置任务队列reset_task_config，默认为False")
            reset_task_config = False
        if reset_task_config or not self.redis_client.redis_executor.exists(self.task_list_redis_key):
            print("生产队列数据")
            generate_task_list_callback = self.__getattribute__("init_task_list")
            if self.redis_client.redis_executor.exists(self.task_list_redis_key):
                print("已存在", self.task_list_redis_key, "任务队列", "数量",
                      self.redis_client.redis_executor.scard(self.task_list_redis_key))
                try:
                    remove_confirm_config = self.__getattribute__("remove_confirm_config")
                    if not remove_confirm_config:
                        option = input("请输入y确认删除重新添加数据")
                        if option != 'y':
                            exit(-1)
                except AttributeError as e:
                    option = input("请输入y确认删除重新添加数据")
                    if option != 'y':
                        exit(-1)
                except Exception as e:
                    pass
                self.redis_client.redis_executor.delete(self.task_list_redis_key)

            generate_task_all = generate_task_list_callback()
            if len(generate_task_all) < 10:
                for item in generate_task_all:
                    print(item)

                    self.redis_client.redis_executor.sadd(self.task_list_redis_key, item)
            else:
                thread_num = 10
                step = len(generate_task_all) // thread_num
                send_thread_list = []
                for i in range(thread_num):
                    if i == thread_num - 1:
                        t = Thread(target=self._send_task_redis, args=(generate_task_all[i * step:],))
                    else:
                        t = Thread(target=self._send_task_redis, args=(generate_task_all[(i * step):(i + 1) * step],))
                    t.start()
                    send_thread_list.append(t)
                for t in send_thread_list:
                    t.join()
            print("生产初始队列成功")
        task_count = self.redis_client.redis_executor.scard(self.task_list_redis_key)
        print("当前队列数", task_count)
        try:
            remove_confirm_config = self.__getattribute__("remove_confirm_config")
            if not remove_confirm_config:
                option = input("请输入y开始")
                if option != 'y':
                    exit(-1)
        except AttributeError as e:
            option = input("请输入y开始")
            if option != 'y':
                exit(-1)
        except Exception as e:
            pass

    def _run(self):
        self._init_task_list()
        try:
            max_thread = self.__getattribute__("max_thread_num")
        except Exception as e:
            print("为提供线程数参数max_thread_num,默认为10")
            max_thread = 10
        worker_callback = self.__getattribute__("worker")

        def self_work_call_back(*args):
            try:
                worker_callback(*args)
            except Exception as e:
                name_exception = type(e).__name__.lower()
                print(args, name_exception)
                self.redis_client.redis_executor.sadd(f"list:error:count:{name_exception}", args[0])

        while True:
            self.thread_task_list = []
            self.task_list = []
            for _ in range(max_thread):
                task = self.redis_client.redis_executor.spop(self.task_list_redis_key)
                if not task:
                    continue
                self.task_list.append(task)
                t = Thread(target=self_work_call_back, args=(task,))
                t.start()
                self.thread_task_list.append(t)
            for t in self.thread_task_list:
                t.join()
            time.sleep(3)
            last_task_count = self.redis_client.redis_executor.scard(self.task_list_redis_key)
            if last_task_count == 0:
                try:
                    loop_task_config = self.__getattribute__("loop_task_config")
                    if loop_task_config and last_task_count == 0:
                        self._init_task_list()
                except Exception as e:
                    pass
            print("开始一下轮", "剩余任务数量", last_task_count)

    def run(self):
        import sys
        options = sys.argv[1:]
        if len(options) > 0:
            if options[0] == 'stat':
                print("今日下载情况", self.redis_client.redis_executor.scard(self.success_count_day_key))
                print("总共下载情况", self.redis_client.redis_executor.scard(self.success_count_all_key))
                print("错误情况")
                print("404", self.redis_client.redis_executor.scard("list:error:count:exception404"))
                print("403", self.redis_client.redis_executor.scard("list:error:count:exception403"))
                print("500", self.redis_client.redis_executor.scard("list:error:count:exception500"))
        try:
            self._run()
        except KeyboardInterrupt as e:
            # 人为中断程序需要把未完成的队列重新放入
            print(self.task_list)
            for item in self.task_list:
                self.redis_client.redis_executor.sadd(self.task_list_redis_key, item)


if __name__ == '__main__':
    spider = LrabbitSpider()
