<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# literal portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_literal/master?logo=python)](
    https://gitlab.com/ae-group/ae_literal)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_literal)](
    https://pypi.org/project/ae-literal/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_literal/coverage.svg)](
    https://ae-group.gitlab.io/ae_literal/coverage/ae_literal_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_literal/mypy.svg)](
    https://ae-group.gitlab.io/ae_literal/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_literal/pylint.svg)](
    https://ae-group.gitlab.io/ae_literal/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_literal)](
    https://libraries.io/pypi/ae-literal)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_literal)](
    https://pypi.org/project/ae-literal/#files)


## installation


execute the following command to use the ae.literal module in your
application. it will install ae.literal into your python (virtual) environment:
 
```shell script
pip install ae-literal
```

if you instead want to contribute to this portion then first fork
[the ae_literal repository at GitLab](https://gitlab.com/ae-group/ae_literal "ae.literal code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_literal):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.literal.html#module-ae.literal
"ae_literal documentation").

<!-- common files version 0.2.77 deployed version 0.2.30 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_literal module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-literal as namespace portion ae-literal.
-->
