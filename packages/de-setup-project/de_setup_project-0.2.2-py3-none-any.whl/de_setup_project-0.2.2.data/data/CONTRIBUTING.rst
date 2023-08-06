
..
    THIS FILE IS EXCLUSIVELY MAINTAINED by the project de_tpl_project V0.2.0 

contributing
============

we want to make it as easy and fun as possible for you to contribute to this project.


reporting bugs
--------------

before you create a new issue, please check to see if you are using the latest version of this project; the bug may
already be resolved.

also search for similar problems in the issue tracker; it may already be an identified problem.

include as much information as possible into the issue description, at least:

1. version numbers (of Python and any involved packages)
2. small self-contained code example that reproduces the bug
3. steps to reproduce the error
4. any traceback/error/log messages shown


requesting new features
-----------------------

1. provide a clear and detailed explanation of the feature you want and why it's important to add.
2. if you are able to implement the feature yourself (refer to the `contribution steps`_ section below).


contribution steps
------------------

thanks for your contribution -- we'll get your merge request reviewed. you should also review other merge requests, just
like other developers will review yours and comment on them. based on the comments, you should address them. once the
reviewers approve, the maintainers will merge.

before you start make sure you have a `GitLab account <https://gitlab.com/users/sign_in>`__.

contribution can be done either with the `git-repo-manager tool <https://gitlab.com/degroup/de_git_repo_manager>`__ or
directly by using `git` and the `Gitlab` site.


using the git repository manager `grm`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. fork and clone the repository of this project to your computer

   in your console change the working directory to your project's parent folder. then run the following command with
   the <new_feature_or_fix> part replaced by an appropriate branch name, describing shortly your contribution::

      grm fork degroup/de_setup_project --branch <new_feature_or_fix>

   .. note::
      this grm action will also add the forked repository as the remote ``upstream`` to your local repository.
      additionally the branch specified by the --branch/-b option will be created and pushed to your remote repository.

2. code

   implement the new feature or the bug fix; include tests, and ensure they pass.

3. push your changes

   before you initiate a push/merge request against the Gitlab server, create a ``commit.txt`` file in the root folder
   of this project, containing a short summary (max. 69 characters) in the first line followed with a blank line and
   then more detailed descriptions of the change.

   provide a detailed, clear, and complete description of your commit! for changes, initiated by a bug fix or change
   request issue, please include the issue number (in the format ``fixes #<issue-number>``) in your commit summary. use
   Markdown syntax for simple styling.

   finally in the root folder of your project run the following command::

      grm merge-request

   .. note::
      this `grm` command includes a pull and rebase from the ``upstream`` remote repository as well as a push to the
      ``origin`` remote repository to keep your fork up-to-date.


using `git` and `Gitlab`
^^^^^^^^^^^^^^^^^^^^^^^^

1. fork this repository `at Gitlab <https://docs.gitlab.com/ce/workflow/forking_workflow.html>`__ on the Gitlab site.

2. clone your forked repo as ``origin`` remote to your computer, and add an ``upstream`` remote for the destination
   repo::

      git clone https://gitlab.com/<YourGitLabUserName>/de_setup_project.git
      git remote add upstream https://gitlab.com/degroup/de_setup_project.git

3. checkout out a new local feature branch and update it to the latest version of the ``develop`` branch::

      git checkout -b feature-xxx develop
      git pull --rebase upstream develop

   please keep your code clean by staying current with the ``develop`` branch, where code will be merged. if you
   find another bug, please fix it in a separated branch instead.

4. push the branch to your fork. treat it as a backup::

      git push origin feature-xxx

5. code

   implement the new feature or the bug fix; include tests, and ensure they pass.

6. check

   run the basic code style and typing checks locally (pylint, mypy and flake8) before you commit.

7. commit

   for every commit please write a short (max 72 characters) summary in the first line followed with a blank line and
   then more detailed descriptions of the change. use Markdown syntax for simple styling.

   please include any issue number (in the format #nnn) in your summary::

      git commit -m "issue #123: put change summary here (can be a issue title)"

   **never leave the commit message blank!** provide a detailed, clear, and complete description of your commit!

8. prepare a Merge Request

   before submitting a `merge request <https://docs.gitlab.com/ce/workflow/forking_workflow.html#merging-upstream>`__,
   update your branch to the latest code::

      git pull --rebase upstream develop

   if you have made many commits, we ask you to squash them into atomic units of work. most issues should have one
   commit only, especially bug fixes, which makes them easier to back port::

      git checkout develop
      git pull --rebase upstream develop
      git checkout feature-xxx
      git rebase -i develop

   push changes to your fork::

      git push -f

9. issue/make a GitLab Merge Request:

   * navigate to your fork where you just pushed to
   * click `Merge Request`
   * in the branch field write your feature branch name (this is filled with your default branch name)
   * click `Update Commit Range`
   * ensure the changes you implemented are included in the `Commits` tab
   * ensure that the `Files Changed` tab incorporate all of your changes
   * fill in some details about your potential patch including a meaningful title
   * click `New merge request`.


deployment to PYPI
------------------

the deployment of a new/changed project will automatically be initiated by the GitLab CI, using the two
protected vars PYPI_USERNAME and PYPI_PASSWORD (marked as masked) from the users group of this namespace, in order
to provide the user name and password of the maintainers PYPI account (on Gitlab.com at Settings/CI_CD/Variables).


other resources
---------------

-  `General GitLab documentation <https://docs.gitlab.com/ce/>`__
-  `GitLab workflow
   documentation <https://docs.gitlab.com/ce/workflow/README.html>`__
