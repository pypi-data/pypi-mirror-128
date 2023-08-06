<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# progress portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_progress/master?logo=python)](
    https://gitlab.com/ae-group/ae_progress)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_progress)](
    https://pypi.org/project/ae-progress/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_progress/coverage.svg)](
    https://ae-group.gitlab.io/ae_progress/coverage/ae_progress_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_progress/mypy.svg)](
    https://ae-group.gitlab.io/ae_progress/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_progress/pylint.svg)](
    https://ae-group.gitlab.io/ae_progress/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_progress)](
    https://pypi.org/project/ae-progress/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_progress)](
    https://pypi.org/project/ae-progress/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_progress)](
    https://pypi.org/project/ae-progress/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_progress)](
    https://pypi.org/project/ae-progress/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_progress)](
    https://libraries.io/pypi/ae-progress)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_progress)](
    https://pypi.org/project/ae-progress/#files)


## installation


execute the following command to use the ae.progress module in your
application. it will install ae.progress into your python (virtual) environment:
 
```shell script
pip install ae-progress
```

if you instead want to contribute to this portion then first fork
[the ae_progress repository at GitLab](https://gitlab.com/ae-group/ae_progress "ae.progress code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_progress):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.progress.html#module-ae.progress
"ae_progress documentation").

<!-- common files version 0.2.77 deployed version 0.2.7 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_progress module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-progress as namespace portion ae-progress.
-->
