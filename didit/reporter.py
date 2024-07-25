"""Reports doit execution status/results
   Extended for reporting a Workflow Run RO-Crate
"""

import sys
import time
import datetime
import json
from io import StringIO
import didit.profiles as profiles
import logging

from rocrate.rocrate import ROCrate
from rocrate.model.person import Person

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TaskResult():
    """ Task result data object i.e. the result of a single task

    - result (str): fail, success, up-to-date, ignore
    - out (str): stdout from task
    - err (str): stderr from task
    - error (str): error from doit (exception traceback)
    - started (str): datetime when task execution started
    - elapsed (float): time (in secs) taken to execute task
    """

    def __init__(self, task):
        """initialize task result"""
        logger.debug("TASK: Initializing TaskResult")
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
        logger.debug("TASK: TaskResult.start")

        self._started_on = time.time()

    def set_result(self, result, error=None):
        """called when task finishes its execution"""
        logger.debug("TASK: TaskResult.set_result")

        self._finished_on = time.time()
        self.result = result
        line_sep = "\n<------------------------------------------------>\n"
        self.out = line_sep.join([a.out for a in self.task.actions if a.out])
        self.err = line_sep.join([a.err for a in self.task.actions if a.err])
        self.error = error

    def to_dict(self):
        """convert result data to dictionary"""
        logger.debug("TASK: TaskResult.to_dict")

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

    def __init__(self, outstream=sys.stdout, options=None):
        """initialize reporter"""
        logger.debug("Initializing WorkflowRunROCrateReporter")

        # ----------------------------------------------------------------------
        # Initialize the reporter options
        
        self.options = options
        if self.options['crate_profile'] not in profiles.profiles:
            raise Exception("Invalid crate profile")
        else:
            self.options_schema = profiles.profiles[self.options['crate_profile']]

        # ----------------------------------------------------------------------
        # Validate the reporter options

        valid = self.options_schema.validate(self.options)
        if not valid:
            raise Exception("Invalid reporter options")

        # ----------------------------------------------------------------------
        # Create the RO-Crate object for reporting provenance

        self.crate = ROCrate()

        # ----------------------------------------------------------------------
        # Parse metadata from the reporter options and add to the RO-Crate

        author_input = Person(self.crate,
                              self.options['agent']['orcid_url'],
                              properties={
                                  "name": self.options['agent']['name'],
                                  "affiliation": self.options['agent']['affiliation']
                              })                        
        author = self.crate.add(author_input)

        # ----------------------------------------------------------------------
        # Onward!

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
        logger.debug("get_status")
        
        print("get_status")
        self.t_results[task.name] = TaskResult(task)

    def execute_task(self, task):
        """called when execution starts"""
        logger.debug("execute_task")
        self.t_results[task.name].start()

    def add_failure(self, task, exception):
        """called when execution finishes with a failure"""
        logger.debug("add_failure")
        self.t_results[task.name].set_result('fail', exception.get_msg())

    def add_success(self, task):
        """called when execution finishes successfully"""
        logger.debug("add_success")
        self.t_results[task.name].set_result('success')

    def skip_uptodate(self, task):
        """skipped up-to-date task"""
        logger.debug("skip_uptodate")
        self.t_results[task.name].set_result('up-to-date')

    def skip_ignore(self, task):
        """skipped ignored task"""
        logger.debug("skip_ignore")
        self.t_results[task.name].set_result('ignore')

    def cleanup_error(self, exception):
        """error during cleanup"""
        logger.debug("cleanup_error")
        self.errors.append(exception.get_msg())

    def runtime_error(self, msg):
        """error from doit (not from a task execution)"""
        logger.debug("runtime_error")
        self.errors.append(msg)

    def teardown_task(self, task):
        """called when starts the execution of teardown action"""
        logger.debug("teardown_task")
        pass

    def complete_run(self):
        """called when finished running all tasks"""
        logger.debug("complete_run")

        # Serialize the ROCrate object to disk (and make a debugging print)
        self.crate.write("crate")
        
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
