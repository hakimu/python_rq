import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from newrelic_hooks_application_rq import instrument_rq_worker, instrument_rq_job

from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

from test import adder
result = q.enqueue(adder)


