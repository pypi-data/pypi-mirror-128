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
from lrabbit_scrapy.common_utils.print_log_helper import LogUtils


class LrabbitSpider:

    def __init__(self):
        try:
            config_env_name = self.__getattribute__("config_env_name")
        except Exception as e:
            config_env_name = 'config_path'
        try:
            redis_db = int(self.__getattribute__("redis_db_config"))
        except Exception as e:
            redis_db = 0
        self.mysql_client = MysqlClient(config_path_env=config_env_name)
        self.redis_client = RedisClient(config_path_env=config_env_name, db=redis_db)
        spider_task_key = f'list:{self.__getattribute__("spider_name")}'
        self.spider_name = self.__getattribute__("spider_name")
        self.task_list_redis_key = spider_task_key
        self.success_count_all_key = f"success:count:{self.spider_name}"
        self.success_count_day_key = f"success:count:{self.spider_name}:{get_time_format_now()}"
        self.fail_count_all_key = f"fail:count:{self.spider_name}"
        self.fail_count_day_key = f"fail:count:{self.spider_name}:{get_time_format_now()}"
        self.thread_task_list = []
        self.task_list = []

    def _send_task_redis(self, task_list):
        for task in task_list:
            LogUtils.log_info("new task", task)
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
            LogUtils.log_info("is reset_task_config ? default to False")
            reset_task_config = False
        if reset_task_config or not self.redis_client.redis_executor.exists(self.task_list_redis_key):

            LogUtils.log_info("init task list")
            generate_task_list_callback = self.__getattribute__("init_task_list")
            if self.redis_client.redis_executor.exists(self.task_list_redis_key):

                LogUtils.log_info("already exists", self.task_list_redis_key, "task list", "count",
                                  self.redis_client.redis_executor.scard(self.task_list_redis_key))
                try:
                    remove_confirm_config = self.__getattribute__("remove_confirm_config")
                    if not remove_confirm_config:
                        option = input("please input y to delete task list and add new task")
                        if option != 'y':
                            exit(-1)
                except AttributeError as e:
                    option = input("please input y to delete task list and add new task")
                    if option != 'y':
                        exit(-1)
                except Exception as e:
                    pass
                self.redis_client.redis_executor.delete(self.task_list_redis_key)

            generate_task_all = generate_task_list_callback()
            if len(generate_task_all) < 10:
                for item in generate_task_all:
                    LogUtils.log_info("new task", item)
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
            LogUtils.log_finish("init task list success")

        task_count = self.redis_client.redis_executor.scard(self.task_list_redis_key)
        LogUtils.log_info("current task count", task_count)
        try:
            remove_confirm_config = self.__getattribute__("remove_confirm_config")
            if not remove_confirm_config:
                option = input("please input y to continue")
                if option != 'y':
                    exit(-1)
        except AttributeError as e:
            option = input("please input y to continue")
            if option != 'y':
                exit(-1)
        except Exception as e:
            pass

    def _run(self):
        self._init_task_list()
        try:
            max_thread = self.__getattribute__("max_thread_num")
        except Exception as e:
            LogUtils.log_info("not config max_thread_num,default to 10")
            max_thread = 10
        worker_callback = self.__getattribute__("worker")

        def self_work_call_back(*args):
            try:
                worker_callback(*args)
            except Exception as e:
                name_exception = type(e).__name__.lower()
                LogUtils.log_error("".join(args), e.__getattribute__("args"))
                self.redis_client.redis_executor.sadd(
                    f"list:error:count:{self.spider_name}:{name_exception}:{get_time_format_now()}",
                    args[0])
                self.redis_client.redis_executor.incr(self.fail_count_day_key)
                self.redis_client.redis_executor.incr(self.fail_count_all_key)

        while True:
            self.thread_task_list = []
            self.task_list = []
            for _ in range(max_thread):
                task = self.redis_client.redis_executor.spop(self.task_list_redis_key)
                if not task:
                    break
                self.task_list.append(task)
                t = Thread(target=self_work_call_back, args=(task,))
                t.start()
                self.thread_task_list.append(t)
            for t in self.thread_task_list:
                t.join()
            time.sleep(2)
            last_task_count = self.redis_client.redis_executor.scard(self.task_list_redis_key)
            if last_task_count == 0:
                try:
                    loop_task_config = self.__getattribute__("loop_task_config")
                    if loop_task_config and last_task_count == 0:
                        self._init_task_list()
                except Exception as e:
                    pass
            LogUtils.log_now_time_str()
            LogUtils.log_running("next task_list loop", "remain task count", last_task_count)

    def _menu(self):
        import sys
        options = sys.argv[1:]
        if len(options) > 0:
            if options[0] == 'stat':

                LogUtils.log_info("remain task list", self.redis_client.redis_executor.scard(self.task_list_redis_key))
                print("\n")
                LogUtils.log_finish("today success count",
                                    self.redis_client.redis_executor.get(self.success_count_day_key))
                LogUtils.log_error("today fail count", self.redis_client.redis_executor.get(self.fail_count_day_key))
                LogUtils.log_finish("all success count",
                                    self.redis_client.redis_executor.get(self.success_count_all_key))
                LogUtils.log_error("all fail count", self.redis_client.redis_executor.get(self.fail_count_all_key))
                print("\n")
                LogUtils.log_error("404 status_code count",
                                   self.redis_client.redis_executor.scard(
                                       f"list:error:count:{self.spider_name}:exception404:{get_time_format_now()}"))
                LogUtils.log_error("403 status_code count",
                                   self.redis_client.redis_executor.scard(
                                       f"list:error:count:{self.spider_name}:exception403:{get_time_format_now()}"))
                LogUtils.log_error("500 status_code count",
                                   self.redis_client.redis_executor.scard(
                                       f"list:error:count:{self.spider_name}:exception500:{get_time_format_now()}"))
            else:
                LogUtils.log_error(" you can add stat option ,check scrapy stat")
            exit(-1)

    def run(self):
        self._menu()
        try:
            self._run()
        except KeyboardInterrupt as e:
            # when you keyboard break,need give this task back
            print(self.task_list)
            for item in self.task_list:
                self.redis_client.redis_executor.sadd(self.task_list_redis_key, item)


if __name__ == '__main__':
    spider = LrabbitSpider()
