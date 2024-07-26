# Description: This file contains the schema for the selected level of workflow run RO-Crate
# Please note - these are not schemas for validating the entire RO-Crate, but only that the user space input in the task file is correct

from schema import Schema, And, Use, Optional, SchemaError

process_run = Schema({
    'crate_profile': And(Use(str)),
    'agent': {
        'name': And(Use(str)),
        'affiliation': And(Use(str)),
        'orcid_url': And(Use(str)),
    },
    'script_path': And(Use(str))
})

workflow_run = Schema({
    'crate_profile': And(Use(str)),
    'agent': {
        'name': And(Use(str)),
        'affiliation': And(Use(str)),
        'orcid_url': And(Use(str)),
    },
    'script_path': And(Use(str))
})

provenance_run = Schema({
    'crate_profile': And(Use(str)),
    'agent': {
        'name': And(Use(str)),
        'affiliation': And(Use(str)),
        'orcid_url': And(Use(str)),
    },
    'script_path': And(Use(str))
})


profiles = {
    'process-run': process_run,
    'workflow-run': workflow_run,
    'provenance-run': provenance_run
}
