import redis
from rq import Worker, Queue, Connection
import os
os.chdir('../')
listen = ['default']

redis_url = 'redis://10.180.250.26:6379'

conn = redis.from_url(redis_url)

with Connection(conn):
    worker = Worker(map(Queue,listen))
    worker.work()