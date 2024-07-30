import pytest
import subprocess
import pathlib
import json

from linkml.validator import validate

@pytest.fixture
def crate_path():
    return pathlib.Path("/work/crate/ro-crate-metadata.json")

@pytest.fixture
def schema_path():
    return pathlib.Path("/work/tests/schema.yaml")
    
def test_crate_valid(crate_path, schema_path):
    # Run doit to create the output
    result = subprocess.run(
        ['doit', '-f', '/work/dodo.py'],
        capture_output=True,
        text=True
    )

    # Fail early if the task failed
    assert result.returncode == 0

    # Load crate jsonld into json object
    with open(crate_path, 'r') as f:
        data = json.load(f)

        print("---------------------------------------------------")
        print(data)
        print("---------------------------------------------------")
        
        report = validate(data, schema_path)

        try:
            assert report.results == []
        except AssertionError as e:
            from pprint import pprint
            for r in report.results:
                print()
                pprint(r.message)
                print()
            raise e
