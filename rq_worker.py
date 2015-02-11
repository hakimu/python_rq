#!/usr/bin/env python

import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from newrelic_hooks_application_rq import instrument_rq_worker, instrument_rq_job

from redis import Redis
from rq import Queue, Connection, Worker

q = Queue(connection=Redis())

with Connection():
    w = Worker(q)
    w.work()
