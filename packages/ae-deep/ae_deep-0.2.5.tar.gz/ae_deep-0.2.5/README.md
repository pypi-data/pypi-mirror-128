<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# deep portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_deep/master?logo=python)](
    https://gitlab.com/ae-group/ae_deep)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_deep)](
    https://pypi.org/project/ae-deep/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_deep/coverage.svg)](
    https://ae-group.gitlab.io/ae_deep/coverage/ae_deep_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_deep/mypy.svg)](
    https://ae-group.gitlab.io/ae_deep/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_deep/pylint.svg)](
    https://ae-group.gitlab.io/ae_deep/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_deep)](
    https://pypi.org/project/ae-deep/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_deep)](
    https://pypi.org/project/ae-deep/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_deep)](
    https://pypi.org/project/ae-deep/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_deep)](
    https://pypi.org/project/ae-deep/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_deep)](
    https://libraries.io/pypi/ae-deep)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_deep)](
    https://pypi.org/project/ae-deep/#files)


## installation


execute the following command to use the ae.deep module in your
application. it will install ae.deep into your python (virtual) environment:
 
```shell script
pip install ae-deep
```

if you instead want to contribute to this portion then first fork
[the ae_deep repository at GitLab](https://gitlab.com/ae-group/ae_deep "ae.deep code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_deep):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.deep.html#module-ae.deep
"ae_deep documentation").

<!-- common files version 0.2.77 deployed version 0.2.3 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_deep module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-deep as namespace portion ae-deep.
-->
