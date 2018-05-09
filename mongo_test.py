#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
File Name: mongo_test
Author: shangxc
Created Time: 2018/5/9 上午12:54
"""
from setting import *
from pymongo import MongoClient
from gridfs import GridFS
import random
import os
import threading
import time
import sched


class Mongo(object):
    def __init__(self):
        self.client = MongoClient(ip, port)
        self.db = self.client.get_database(db_name)
        self.fs = GridFS(self.db, table_name)

    def insert_file(self):
        file_name = random.choice(os.listdir(source_dir))
        file_path = os.path.join(source_dir, file_name)
        with open(file_path, 'rb') as f:
            data = f.read()
            file_id = self.fs.put(data, filename=file_name)
        return file_id

    def get_file_by_name(self, file_name):
        file = self.fs.get_version(file_name)
        data = file.read()

    def get_file_by_id(self, object_id):
        data = self.fs.get(object_id)

    def del_file_by_id(self, object_id):
        self.fs.delete(object_id)

    def run(self):
        self.insert_file()


class LoadTest(object):
    def __init__(self):
        self.event = threading.Condition()

    def run(self):
        print(time.time())
        pass

    def start(self, current_num=concurrent_num, exec_times=exec_times, delay=delay, style=style):
        th = []
        for i in range(current_num):
            th.append(threading.Thread(target=self._run, args=(exec_times, style)))
        for j in th:
            j.start()
        if style == 'concurrent':
            for _ in range(exec_times):
                self.event.acquire()
                self.event.notify_all()
                self.event.release()
                while len(self.event._waiters) != current_num:
                    time.sleep(0.1)
                time.sleep(delay)

    def _run(self, exec_times, style):
        if style == 'sequence':
            for _ in range(exec_times):
                self.run()
                time.sleep(delay)
        elif style == 'concurrent':
            for _ in range(exec_times):
                self.event.acquire()
                self.event.wait()
                self.event.release()
                self.run()
        elif style == 'scheduler':
            s = sched.scheduler()
            for i in range(exec_times):
                s.enter(i * delay, 1, self.run)
            s.run()
        else:
            raise Exception('style not support: ' + style)


if __name__ == '__main__':
    LoadTest().start()
    pass
