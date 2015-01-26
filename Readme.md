I'm having trouble getting this test to report data.  I do see the PIDs when I look at agent runs so it appears things are working.  Just not seeing any data on the Overview graph, in Non-web or the Background jobs tab.

I've tried this with and without the decorator in the `test.py` file.  I've also tried adjusting the timeouts in the `newrelic_hooks_application_rq.py` file.

I'm running this using `python work.py`


Key things
----------

1. Calling `Queue.enqueue()` just puts a job in the Redis queue. It doesn't run the job.

2. I added a script called `rq_worker.py` which will listen for jobs put into the Redis queue, and then execute them. To try out the example, you should have 2 terminal windows open. In one, run `rq_worker.py` (make sure the NEW_RELIC_CONFIG_FILE environment variable is set in this terminal.) In the other, run `python work.py` to put a job in the Redis queue.

3. Make sure you have the following lines in your `newrelic.ini` file:

    [import-hook:rq.worker]
    enabled = true
    execute = newrelic_hooks_application_rq:instrument_rq_worker

    [import-hook:rq.job]
    enabled = true
    execute = newrelic_hooks_application_rq:instrument_rq_job

4. If you look in the `newrelic_hooks_application_rq.py` file, you can see the two key parts of instrumentation happening:

    * `perform_job` registers the application before executing the job, and forces harvest after execution.

    * `perform` calls the job with a BackgroundTask context manager, which records the metrics for that particular job.
