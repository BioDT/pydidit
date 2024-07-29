import pytest
import subprocess
import pathlib

from linkml.validator import validate_file

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

    # Verify that the output file exists
    assert crate_path.exists()

    # Verify the schema file exists
    assert schema_path.exists()

    # Validate the output against the schema
    report = validate_file(crate_path, schema_path, "Person")

    try:
        assert report.results == []
    except AssertionError as e:
        for r in report:
            print(r)
        raise e
