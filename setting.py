#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
File Name: setting
Author: shangxc
Created Time: 2018/5/9 上午12:55
"""
ip = '192.168.204.131'
port = 27017
db_name = 'test'
table_name = 'test'
source_dir = '/Users/shangxc/Workspace/data'

concurrent_num = 10
exec_times = 10
delay = 1
style = 'concurrent'  # sequence 顺序执行 concurrent 并发执行 scheduler 定时执行

if __name__ == '__main__':
    pass
