from newrelic.agent import (shutdown_agent, application,
    register_application, BackgroundTask)
 
# [import-hook:rq.worker]
# enabled = true
# execute = newrelic_hooks_application_rq:instrument_rq_worker
 
def instrument_rq_worker(module):
    _perform_job = module.Worker.perform_job
 
    def perform_job(self, job):
        # This gets called in the forked process to trigger
        # execution of the actual job. We first need to force
        # register the application we are going to report data
        # against. Allow up to 5.0 seconds for this to complete.
        # Normally should take less than 2.0 seconds. If
        # registration hasn't occurred after 5.0 seconds, the
        # job will be run anyway.
 
        register_application(timeout=10.0)
 
        # Execute the actual task.
 
        result = _perform_job(self, job)
 
        # Now shutdown the agent, which will force a data
        # harvest. We do this explicitly because RQ calls
        # os._exit() to force exit the process and that bypasses
        # atexit callbacks, which is how we normally harvest on
        # shutdown. Again wait for up to 5.0 seconds to allow
        # data to be posted to the data collector.
 
        shutdown_agent(timeout=10.0)
 
        return result
 
    module.Worker.perform_job = perform_job
 
# [import-hook:rq.job]
# enabled = true
# execute = newrelic_hooks_application_rq:instrument_rq_job
 
def instrument_rq_job(module):
    _perform = module.Job.perform
 
    def perform(self):
        # This is the jobs own method to execute the task. Time
        # this as a background task where name is the name of
        # the queued task. This should also capture any record
        # any unhandled exceptions that occurred when running
        # the task.
 
        with BackgroundTask(application(), self.func_name):
            return _perform(self)
 
    module.Job.perform = perform