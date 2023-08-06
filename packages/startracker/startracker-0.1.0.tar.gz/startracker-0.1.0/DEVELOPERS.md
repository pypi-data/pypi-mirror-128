# Developing StarTracker

* [Development Setup](#setup)
* [Running Tests](#tests)
* [Code Style Guidelines](#rules)
* [Writing Documentation](#documentation)

## <a name="setup"> Development Setup
### Development requirements

Recommended way of development is under virtual environment. Same instructions are applicable
to non-virtual environment too, but it is not advised. Use at your own risk.
First of all, you need to have `python` of version `>=3.6` available on your development PC.
Ensuring this is your own responsibility, as different operation systems are supplied with
different python interpreters and different methods are used to install modern python interpreter
alongside with the system one. On CERN's CC7 based machines the recommended way is to [source
an appropriate software collection](https://cern.service-now.com/service-portal?id=kb_article&n=KB0000730).

```shell
python3 -m venv /path/to/venv/ # create your python3 virtual environment, to be done only once
source /path/to/venv/bin/activate # activate your virtual environment, to be done every time you want to develop/test
python3 -m pip install --upgrade pip # optional, if you want to upgrade pip to the most recent version, to be done only once
python3 -m pip install flit # required for project building and installation, to be done only once
deactivate # return from virtual environment to the regular one
```

### Installation instructions

* Clone the repository `git clone https://gitlab.cern.ch/cta-unige/StarTracker.git && cd StarTracker`

* Activate your virtual environment `source /path/to/venv/bin/activate`
* Install the `StarTracker` package in your virtual environment `flit install --symlink` 

## <a name="tests"> Running Tests

Always test your developments before making a merge request. 
Unit-tests are not provided due to simplicity of the project. 
Integration tests are found in `test.py` and should be launched with

```shell
python -m unittest discover -v
```
Test `test_local_run` is expected to fail (it is configured to run a dummy production in CI).

Project's CI pipeline runs linting with `pylint`. Do not commit the code which decreases linter's rating,
unless strictly required (in this case you will have to explain the reasons). 
Also an automated doc building is launched serving as well as a package consistency test 
and low statistics local job with `sim_telarray` is launched on dummy example corsika data. 
All log files, job output and histograms are uploaded as artifacts. 

## <a name="rules"> Code Style Guidelines
We are following [PEP8][pep8] standard for python code.

## <a name="documentation"> Writing Documentation
We use the [sphinx][sphinx] with read-the-docs theme for `python` code documentation.
Additional dependencies to install:
- `sphinx`
- `sphinx_rtd_theme`
- `recommonmark`
- `sphinx-argparse`

The documentation can be generated using the following command:

```bash
sphinx-build -b html doc doc/_build
```

Generated files are placed in `doc/_build`.

This section will be completed later with precise documentation style guide, for the moment follow the examples from the code itself.

[pep8]:https://www.python.org/dev/peps/pep-0008/
[sphinx]:https://www.sphinx-doc.org/en/master/usage/quickstart.html
