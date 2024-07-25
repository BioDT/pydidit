import pytest
import subprocess

def test_doit_callable():
    result = subprocess.run(
        ['doit', 'list'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    
def test_doit_success():
    result = subprocess.run(
        ['doit', '-f', '/work/tests/task-success.py'],
        capture_output=True,
        text=True
    )
        
    assert result.returncode == 0

def test_doit_failure():
    result = subprocess.run(
        ['doit', '-f', '/work/tests/task-failure.py'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode != 0
