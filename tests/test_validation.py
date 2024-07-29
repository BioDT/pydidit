import pytest
import subprocess
import pathlib

from linkml.validator import validate_file

@pytest.fixture
def test_pass_file_path():
    return pathlib.Path("/work/tests/fixtures/validation/pass.json")

@pytest.fixture
def test_fail_file_path():
    return pathlib.Path("/work/tests/fixtures/validation/fail.json")

@pytest.fixture
def test_schema_file_path():
    return pathlib.Path("/work/tests/fixtures/validation/schema.yaml")

def test_validation_pass(test_pass_file_path, test_schema_file_path):
    report = validate_file(test_pass_file_path,
                           test_schema_file_path,
                           "Person")

    try:
        assert report.results == []
    except AssertionError as e:
        for r in report:
            print(r)
        raise e

def test_validation_fail(test_fail_file_path, test_schema_file_path):
    report = validate_file(test_fail_file_path,
                           test_schema_file_path,
                           "Person")

    assert report.results != []
