from didit.reporter import WorkflowRunROCrateReporter

DOIT_CONFIG = {'reporter': WorkflowRunROCrateReporter}

def task_modify():
    return {'actions': ["echo bar > foo.txt"],
            'file_dep': ["foo.txt"],
            }

def task_create():
    return {'actions': ["touch foo.txt"],
            'targets': ["foo.txt"]
            }

def task_say_hello():
    return {'actions': ["echo hello"],
            }
