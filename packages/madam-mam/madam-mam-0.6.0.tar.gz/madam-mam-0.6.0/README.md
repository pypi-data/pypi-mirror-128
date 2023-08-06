# MADAM

MADAM is the Multi Agent Digital Asset Manager.

It provides a three-tier architecture platform to handle workflow processing in a distributed environment.

It uses Docker swarm to dispatch processes in a cluster of machines.

It is a free (as freedom) software written in Python.

## Documentation

[Link to the documentation](https://m5231.gitlab.io/documentation/)

## Support

If you find this project useful and want to contribute, please submit issues, merge requests. If you use it regularly,
you can help by the author by a financial support.

<script src="https://liberapay.com/vit/widgets/button.js"></script>
<noscript><a href="https://liberapay.com/vit/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript>

## Requirements

You will need [Camunda Modeler 4.11+](https://github.com/camunda/camunda-modeler/releases) to easily create
Zeebe BPMN XML workflows for MADAM.

## Licensing

MADAM is licensed under the [Gnu Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).

Camunda Modeler is licensed under [the MIT License (MIT)](https://mit-license.org/).

At its core, MADAM use [adhesive-zebe](https://github.com/vtexier/adhesive), a BPMN workflow python engine able to
execute Zeebe BPMN XML workflows. It is a fork of [adhesive](https://github.com/germaniumhq/adhesive) under
the original adhesive license that is [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)

## System environment setup

1. [Install Docker](https://docs.docker.com/engine/install/).

2. [Configure userns-remap](https://docs.docker.com/engine/security/userns-remap/) to map container user `root` to a
   host non-root user.

3. Configure the dev station as a [Docker Swarm Manager](https://docs.docker.com/engine/swarm/).

4. Install a [Postgresql](https://www.postgresql.org/download/) database server.
   
_You can use the Ansible playbook provided to install PostgreSQL locally with Docker,
after configuring `hosts.yaml`:_

    make environment

### Python environment setup

* It requires Python 3.8+.

* [Pyenv](https://github.com/pyenv/pyenv) should be used to choose the right version of Python, without breaking the
  default Python of the Operating System.

* A Python virtual environment should be created in a `.venv` folder.

```bash
    pyenv install 3.8.0
    pyenv shell 3.8.0
    python -m venv .venv 
    source .venv/bin/activate`
```

### Installation/Update

From PyPI:

In a Python virtualenv:

    pip install -U madam-mam

In your user install directory:

    pip install --user -U madam-mam

You should have a the `madam` cli command available:

    madam

or

    madam --help

will display command usage.

To have bash completion, you can type:

    _MADAM_COMPLETE=source_bash madam > madam-complete.sh
    sudo cp madam-complete.sh /etc/bash_completion.d/.

For another shell, replace `source_bash` by `source_zsh` or `source_fish`

### Development environment

Install [Poetry](https://python-poetry.org/) with the custom installer:

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

Install Python dependencies:

    poetry install --no-root

You can use the madam-cli dev command:

    ./bin/madam-cli

Get `bin/madam-cli` bash shell completion:

    _MADAM_CLI_COMPLETE=source_bash bin/madam-cli > madam-cli-complete.sh
    sudo cp madam-cli-complete.sh /etc/bash_completion.d/.

For another shell, replace `source_bash` by `source_zsh` or `source_fish`

### Configuration

Make a copy of the environment config example file:

    cp .env.example .env

Edit `.env` to suit your needs, then:

    export $(grep -v '^#' .env | xargs -d '\n')

Make a copy of the Ansible inventory example file:

    cp hosts.yaml.example hosts.yaml

Edit `hosts.yaml` to suit your needs.

Make a copy of the MADAM config example file:

    cp madam.yaml.example madam.yaml

Edit `madam.yaml` to suit your needs.

Make a copy of the MADAM config example file for the test environment:

    cp madam_tests.yaml.example madam_tests.yaml

Edit `madam_tests.yaml` to suit your needs.

Make a copy of the MADAM config example file for the local deploy:

    cp madam_deploy.yaml.example madam_deploy.yaml

Edit `madam_deploy.yaml` to suit your needs.

### Set and tag project version in Git

    ./bin/release.sh 1.0.0

### Build MADAM python package and Docker image

    make build

The wheel package will be build in the `dist` directory.

## Deploy MADAM as local docker container

To deploy MADAM container on localhost:

    make deploy

## Check static type and code quality

    make check

## Run tests

Run all [pytest](https://docs.pytest.org) tests with:

    make tests

Run only some tests by using `bin/tests.sh`:

    bin/tests.sh tests/domains/test_workflows.py::test_create

## Database setup

Set `DATABASE_URL` and `DATABASE_URL_TESTS` environment variable in `.env` file:

    DATABASE_URL=postgresql://postgres:xxxxx@hostname:5432/madam?sslmode=allow
    DATABASE_URL_TESTS=postgresql://postgres:xxxxx@hostname:5432/madam_tests?sslmode=allow

### Migrations scripts

Add/Edit scripts in `resources/migrations` directory:

    # version.name.[rollback].sql
    00001.init_tables.sql
    00001.init_tables.rollback.sql

### Migrate commands

    make databases
    make databases_rollback
    make databases_list
