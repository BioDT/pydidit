from didit.reporter import WorkflowRunROCrateReporter

reporter_options = {
    "crate_profile": "process-run",
    "agent":
    {
        "name": "John Doe",
        "affiliation": "University of Nowhere",
        "orcid_url": "https://orcid.org/0000-0002-1825-0097"
    },
    "script_path": f"{__file__}"
}

DOIT_CONFIG = {
    'reporter': WorkflowRunROCrateReporter(options=reporter_options)
}


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
