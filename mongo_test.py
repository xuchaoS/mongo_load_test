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

from sxc_test_tools import LoadTest


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


class Handle(LoadTest):
    def __init__(self):
        super().__init__()
        self.mongo = Mongo()

    def run(self):
        file_id = self.mongo.insert_file()
        self.mongo.get_file_by_id(file_id)


if __name__ == '__main__':
    Handle().start()
    pass
