import pytest

from didit.reporter import WorkflowRunROCrateReporter

# Fixture for basic reporter options
@pytest.fixture
def reporter_options():
    return {
        "crate_profile": "process-run",
        "agent":
        {
            "name": "John Doe",
            "affiliation": "University of Nowhere",
            "orcid_url": "https://orcid.org/0000-0002-1825-0097"
        },
        "script_path": f"{__file__}"
    }


def test_reporter_options(reporter_options):
    reporter = WorkflowRunROCrateReporter(options=reporter_options)
    assert True == True # Test has passed if no exception is raised

def test_reporter_invalid_agent(reporter_options):
    reporter_options["agent"] = {} 
        
    with pytest.raises(Exception) as e: 
        reporter = WorkflowRunROCrateReporter(options=reporter_options)

def test_reporter_missing_agent(reporter_options):
    del reporter_options["agent"]
    
    with pytest.raises(Exception) as e: 
        reporter = WorkflowRunROCrateReporter(options=reporter_options)
        
def test_reporter_invalid_profile(reporter_options):
    reporter_options["crate_profile"] = "invalid-profile"
    
    with pytest.raises(Exception) as e: 
        reporter = WorkflowRunROCrateReporter(options=reporter_options)
