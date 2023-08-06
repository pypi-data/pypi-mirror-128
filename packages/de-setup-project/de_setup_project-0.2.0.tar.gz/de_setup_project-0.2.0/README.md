<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED 
-->
# project setup portion of the de namespace

[![GitLab develop](https://img.shields.io/gitlab/pipeline/degroup/de_setup_project/develop?logo=python)](
    https://gitlab.com/degroup/de_setup_project)
[![GitLab release](https://img.shields.io/gitlab/pipeline/degroup/de_setup_project/release?logo=python)](
    https://gitlab.com/degroup/de_setup_project/-/tree/release)
[![PyPIVersion](https://img.shields.io/pypi/v/de_setup_project)](
    https://pypi.org/project/de-setup-project/#history)

>the portions (modules and sub-packages) of the Development Environment for Python are within
the `de` namespace and are providing helper methods and classes for your Python projects.

[![Coverage](https://degroup.gitlab.io/de_setup_project/coverage.svg)](
    https://degroup.gitlab.io/de_setup_project/coverage/de_setup_project_py.html)
[![MyPyPrecision](https://degroup.gitlab.io/de_setup_project/mypy.svg)](
    https://degroup.gitlab.io/de_setup_project/lineprecision.txt)
[![PyLintScore](https://degroup.gitlab.io/de_setup_project/pylint.svg)](
    https://degroup.gitlab.io/de_setup_project/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/de_setup_project)](
    https://pypi.org/project/de-setup-project/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/de_setup_project)](
    https://pypi.org/project/de-setup-project/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/de_setup_project)](
    https://pypi.org/project/de-setup-project/)
[![PyPIFormat](https://img.shields.io/pypi/format/de_setup_project)](
    https://pypi.org/project/de-setup-project/)
[![PyPIStatus](https://img.shields.io/pypi/status/de_setup_project)](
    https://libraries.io/pypi/de-setup-project)
[![PyPIDownloads](https://img.shields.io/pypi/dm/de_setup_project)](
    https://pypi.org/project/de-setup-project/#files)


## installation

execute the following command to use the `de.setup_project` module in your Python project. it will install
`de.setup_project` into your Python (virtual) environment:
 
```shell script
pip install de-setup-project
```

to contribute to this portion, fork the
[`de-setup-project` repository at GitLab](https://gitlab.com/degroup/de_setup_project
"de.setup_project code repository"), pull it to your machine and finally execute the following command in the root
folder of this repository (`de_setup_project`):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with the tools you need to
develop and run tests or to extend the portion documentation. to contribute only to the unit tests, or the documentation
of this portion replace the setup extras key `dev` in the above command with `tests` or `docs` respectively.

the repository of this portion is using the `git-flow workflow` with the branch names `develop` and `release`. more
details on this workflow you find [here](https://nvie.com/posts/a-successful-git-branching-model/) and 
[here](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).


## namespace portion documentation

more info on the features and usage of this portion is available at
[ReadTheDocs](https://de.readthedocs.io/en/latest/_autosummary/de.setup_project.html#module-de.setup_project
"de_setup_project documentation").
