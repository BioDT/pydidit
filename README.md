# PyDidIt

PyDidIt is a Python library for creating and running reproducible computational workflows. It is built on top of the [DoIt](https://pydoit.org/) task management library and provides additional functionality for creating Research Object Crates (RO-Crates) for workflows.

## Detailed documentation

### Tutorial

#### Introduction

This tutorial will guide you through the process of creating a simple computational workflow using PyDidIt and packaging the results in an RO-Crate.

#### Prerequisites

Before you begin, you will need to have the following installed on your system:
- Docker ([installation instructions](https://docs.docker.com/get-docker/))

#### Step 1: Building the project

To build the project, you can run the following command in the root directory of the project:

```bash
docker build -t doit ./
```

This will build the project and create a Docker image with the name `doit`.

#### Step 2: Creating the work directory

Before running the project, you need to create a `work` directory in the root directory of the project. This directory will be used to store the input and output files for the project. You can create the directory with the following command:

```bash
mkdir work
```

The work directory needs to container a dodo.py file. This file contains the tasks that need to be run by the project. You can create a dodo.py file with the following content:

```python
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
```

This file contains three tasks:
- `create`: This task creates a file called `foo.txt`.
- `modify`: This task modifies the `foo.txt` file by writing `bar` to it.
- `say_hello`: This task prints `hello` to the console.

The `DOIT_CONFIG` variable is used to configure the project. In this case, we are using the `WorkflowRunROCrateReporter` reporter to generate a Research Object Crate (RO-Crate) for the project.

#### Step 3: Running the project

To run the project, you can run the following command:

```bash
docker run -v ./work:/work -v ./didit/:/work/didit -w /work doit
```

Where:
- `-v ./work:/work` mounts the `work` directory in the current directory to the `/work` directory in the container.
- `-v ./didit/:/work/didit` mounts the `didit` directory in the current directory to the `/work/didit` directory in the container.
- `-w /work` sets the working directory in the container to `/work`.

This command will run the tasks defined in the `dodo.py` file and generate an RO-Crate in the `didit` directory.

#### Step 4: Viewing the RO-Crate

You can view the contents of the RO-Crate by opening the generated zip file in a file explorer or by extracting the contents to a directory. 

### Explanation

#### RO-Crates

RO-Crates are a method for packaging research data and metadata in a Findable, Accessible, Interoperable, and Reusable (FAIR) way. They are based on the [Research Object Crate (RO-Crate)](https://www.researchobject.org/ro-crate/) specification.

RO-Crates are often organized as a zip file containing a metadata manifest along with files and directories.

A typical RO-Crate may look like:

```
my-research-object.crate.zip
├── ro-crate-metadata.json
├── data/
│   ├── file1.txt
│   ├── file2.csv
├── code/
│   ├── script.py
├── LICENSE
```

#### Workflow Run RO-Crates

Workflow run RO-Crates are a way to package and share the results of a computational workflow. They contain the input and output files of the workflow, as well as metadata about the workflow itself. 

This metadata includes information about the tasks that were run, the software that was used, and the environment in which the workflow was executed. For more detials you can view the profiles for creating workflow run RO-Crates [here](https://www.researchobject.org/workflow-run-crate/profiles/).

### How to

#### Building the project

To build the project, you need to have Docker installed. You can install Docker from [here](https://docs.docker.com/get-docker/).

To build the project, run the following command in the root directory of the project:

```bash
docker build -t doit ./
```

This will build the project and create a Docker image with the name `doit`.

#### Running the project

##### Creating the work directory

Before running the project, you need to create a `work` directory in the root directory of the project. This directory will be used to store the input and output files for the project and must container a dodo.py file. For details on an exapmle dodo.py file you can view the tutorial.

##### Running the project

To run the project, you can run the following command:

```bash
docker run  -v ./work:/work -v ./didit/:/work/didit -w /workdoit
```

Where:
- `-v ./work:/work` mounts the `work` directory in the current directory to the `/work` directory in the container.
- `-v ./didit/:/work/didit` mounts the `didit` directory in the current directory to the `/work/didit` directory in the container.
- `-w /work` sets the working directory in the container to `/work`.

### Reference
