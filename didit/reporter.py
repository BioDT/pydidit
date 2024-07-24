"""Reports doit execution status/results
   Extended for reporting a Workflow Run RO-Crate
"""

import sys
import time
import datetime
import json
from io import StringIO

from rocrate.rocrate import ROCrate

from doit.exceptions import BaseFail

class TaskResult():
    """ Task result data object i.e. the result of a single task

    - result (str): fail, success, up-to-date, ignore
    - out (str): stdout from task
    - err (str): stderr from task
    - error (str): error from doit (exception traceback)
    - started (str): datetime when task execution started
    - elapsed (float): time (in secs) taken to execute task
    """

    # FIXME what about returned value from python-actions ?
    def __init__(self, task):
        self.task = task
        self.result = None  # fail, success, up-to-date, ignore
        self.out = None  # stdout from task
        self.err = None  # stderr from task
        self.error = None  # error from doit (exception traceback)
        self.started = None  # datetime when task execution started
        self.elapsed = None  # time (in secs) taken to execute task
        self._started_on = None  # timestamp
        self._finished_on = None  # timestamp

    def start(self):
        """called when task starts its execution"""
        self._started_on = time.time()

    def set_result(self, result, error=None):
        """called when task finishes its execution"""
        self._finished_on = time.time()
        self.result = result
        line_sep = "\n<------------------------------------------------>\n"
        self.out = line_sep.join([a.out for a in self.task.actions if a.out])
        self.err = line_sep.join([a.err for a in self.task.actions if a.err])
        self.error = error

    def to_dict(self):
        """convert result data to dictionary"""
        if self._started_on is not None:
            started = datetime.datetime.utcfromtimestamp(self._started_on)
            self.started = str(started.strftime('%Y-%m-%d %H:%M:%S.%f'))
            self.elapsed = self._finished_on - self._started_on
        return {'name': self.task.name,
                'result': self.result,
                'out': self.out,
                'err': self.err,
                'error': self.error,
                'started': self.started,
                'elapsed': self.elapsed}


class WorkflowRunROCrateReporter():
    """ Report overall doit execution status/results 

    
    """

    desc = 'output as Workflow Run RO-Crate'

    def __init__(self, outstream, options=None):  # pylint: disable=W0613

        # Create ROCrate object
        self.crate = ROCrate()
        
        # options parameter is not used
        # json result is sent to stdout when doit finishes running
        self.t_results = {}
        # when using json reporter output can not contain any other output
        # than the json data. so anything that is sent to stdout/err needs to
        # be captured.
        self._old_out = sys.stdout
        sys.stdout = StringIO()
        self._old_err = sys.stderr
        sys.stderr = StringIO()
        self.outstream = outstream
        # runtime and cleanup errors
        self.errors = []

    def get_status(self, task):
        """called when task is selected (check if up-to-date)"""
        self.t_results[task.name] = TaskResult(task)

    def execute_task(self, task):
        """called when execution starts"""
        self.t_results[task.name].start()

    def add_failure(self, task, exception):
        """called when execution finishes with a failure"""
        self.t_results[task.name].set_result('fail', exception.get_msg())

    def add_success(self, task):
        """called when execution finishes successfully"""
        self.t_results[task.name].set_result('success')

    def skip_uptodate(self, task):
        """skipped up-to-date task"""
        self.t_results[task.name].set_result('up-to-date')

    def skip_ignore(self, task):
        """skipped ignored task"""
        self.t_results[task.name].set_result('ignore')

    def cleanup_error(self, exception):
        """error during cleanup"""
        self.errors.append(exception.get_msg())

    def runtime_error(self, msg):
        """error from doit (not from a task execution)"""
        self.errors.append(msg)

    def teardown_task(self, task):
        """called when starts the execution of teardown action"""
        pass

    def complete_run(self):
        """called when finished running all tasks"""

        # Serialize the ROCrate object to disk
        self.crate.write("crate.zip")
        
        # restore stdout
        log_out = sys.stdout.getvalue()
        sys.stdout = self._old_out
        log_err = sys.stderr.getvalue()
        sys.stderr = self._old_err

        # add errors together with stderr output
        if self.errors:
            log_err += "\n".join(self.errors)

        task_result_list = [
            tr.to_dict() for tr in self.t_results.values()]
        json_data = {'tasks': task_result_list,
                     'out': log_out,
                     'err': log_err}
        # indent not available on simplejson 1.3 (debian etch)
        # json.dump(json_data, sys.stdout, indent=4)
        json.dump(json_data, self.outstream)
