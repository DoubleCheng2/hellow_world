# -*- coding: utf-8 -*-

# @Time : 2020-02-24 17:34

# @Author : Double 承（DC）

# @Site : 

# @File : redis传输.py

# @Software: PyCharm

from redis import StrictRedis

"""
redis是用于操作Redis的第三方库,StrictRedis是官方推荐的方法，而且Redis是它的子类，Redis能做到的StrictRedis基本都能做到
"""

#首先连接两个数据库
from redis import Redis
B = Redis(host='127.0.0.1', port=6379, db=0)
A = Redis(host='47.104.175.111', port=6379, db=0, password='0p^C2lGGZdZ*Fy#$dPEI8dxAke*!#pqX4W1JVIpWfrYt7o68qFvQ7rvhq6UUK!iF')
#测试连接是否成功
print(A,B)


def copydb():
    for key in A.keys():
        # 转成字符串形式
        key = str(key)[2:-1]
        key_type = str(A.type(key))[2:-1]
        print('*' * 30)
        print('A:', 'key=' + key, '---------type=' + key_type)
        # 对字符串类型的键值对执行操作------------------------------------------
        if key_type == 'string':
            print(A.get(key))
            B.set(key, str(A.get(key))[2:-1])
            print('写入到数据库B成功，{}'.format(B.get(key)))
        # 对哈希字典类型的键值对执行操作-----------------------------------------
        elif key_type == 'hash':
            print(A.hgetall(key))
            for son_key in A.hkeys(key):
                son_key = str(son_key)[2:-1]
                son_value = str(A.hget(key, son_key))[2:-1]
                B.hset(key, son_key, son_value)
            print('写入到数据库B成功，{}'.format(B.hgetall(key)))
        # 对列表类型的键值对执行操作---------------------------------------------
        elif key_type == 'list':
            print('A:', A.lrange(key, 0, A.llen(key)))
            for value in A.lrange(key, 0, A.llen(key)):
                v1 = str(value)[2:-1]
                B.rpush(key, v1)
            print('写入到数据库B成功，{}'.format(B.llen(key)))
        # 对集合类型的键值对执行操作---------------------------------------------
        elif key_type == 'set':
            print('A:', key, A.scard(key))
            for value in A.smembers(key):
                value = str(value)[2:-1]
                B.sadd(key, value)
            print('写入到数据库B成功，{}'.format(B.scard(key)))
        # 对有序集合类型的键值对执行操作------------------------------------------
        elif key_type == 'zset':
            print('A:', key, A.zcard(key))
            for value in A.zrangebyscore(key, 0, 100):
                value = str(value)[2:-1]
                score = A.zscore(key, value)
                print(value, score, end='----')
                B.zadd(key, value, score)
            print('\n写入到数据库B成功，{}'.format(B.zcard(key)))

copydb()
