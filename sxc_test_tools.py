#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
File Name: sxc_test_tools
Author: shangxc
Created Time: 2018/5/10 上午11:56
"""
import sched
import threading
import logging
import time
import sys
from logging.handlers import RotatingFileHandler

from setting import *


class LoadTest(object):
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s %(levelname)-6s: %(process)d %(threadName)s %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    file_handler = RotatingFileHandler('sxc_test_tools.log', maxBytes=1024*1024*10, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(file_handler)

    time_list = []

    def __init__(self):
        self.event = threading.Condition()

    def run(self):
        print(time.time())
        pass

    def start(self, current_num=concurrent_num, exec_times=exec_times, delay=delay, style=style):
        start_time = time.time()
        th = []
        for i in range(current_num):
            th.append(threading.Thread(target=self._run, args=(exec_times, style)))
        for j in th:
            j.start()

        if style == 'concurrent':
            for i in range(exec_times):
                while len(self.event._waiters) != current_num:
                    time.sleep(0.1)
                self.event.acquire()
                self.event.notify_all()
                self.event.release()
                if i + 1 != exec_times:
                    while len(self.event._waiters) != current_num:
                        time.sleep(0.1)
                    time.sleep(delay)

        for k in th:
            k.join()
        run_times = len(self.time_list)
        total_time = sum(self.time_list)
        avg_time = total_time / run_times
        max_time = max(self.time_list)
        end_time = time.time()
        during = end_time - start_time
        self.logger.info('load test finished, use time %fs, see results below' % during)
        self.logger.info('result: total time %fs, run times %d, average time %fs, max time %fs' % (total_time, run_times, avg_time, max_time))

    def _run(self, exec_times, style):
        self.logger.info('start')
        if style == 'sequence':
            for _ in range(exec_times):
                self.run()
                time.sleep(delay)
        elif style == 'concurrent':
            for _ in range(exec_times):
                self.event.acquire()
                self.event.wait()
                self.event.release()
                self.logged_run()
        elif style == 'scheduler':
            s = sched.scheduler()
            for i in range(exec_times):
                s.enter(i * delay, 1, self.run)
            s.run()
        else:
            raise Exception('style not support: ' + style)
        self.logger.info('finish')

    def logged_run(self):
        self.logger.debug('start run')
        start_time = time.time()
        try:
            self.run()
        except Exception as e:
            self.logger.exception('an error occur at run method')
        end_time = time.time()
        during = end_time-start_time
        self.time_list.append(during)
        self.logger.info('run take time %fs' % during)
        self.logger.debug('finish run')


if __name__ == '__main__':
    pass
