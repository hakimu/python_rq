from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

from test import adder
result = q.enqueue(adder)
