# Contributing to StarTracker

:+1: First off, thanks for reading this contributing guide! :+1:

Welcome to the StarTracker! Here are the guidelines we'd like you to follow:

#### Table Of Contents
* [Code of Conduct](#coc)
* [Questions and Problems](#requests)
  * [Issues and Bugs](#issue)
  * [Feature Requests](#feature)
  * [Improving Documentation](#docs)
* [Issue Submission Guidelines](#submit)
* [Merge Request Submission Guidelines](#submit-mr)

## <a name="coc"></a> Code of Conduct

As main contributors are affiliated with the University of Geneva, we respect its [Code of Conduct][coc] and ask you to do the same.

## <a name="requests"></a> Questions, Bugs, Features

### <a name="issue"></a> Found an Issue or Bug?

If you find a bug in the source code, you can help us by submitting a Bug Report to our
[GitLab Repository][gitlab-issues]. Even better, you can submit a Merge Request with a fix.

**Please see the [Submission Guidelines](#submit) below.**

### <a name="feature"></a> Missing a Feature?

You can request a new feature by submitting an issue to our [GitLab Repository][gitlab-issues].

If you would like to implement a new feature, it should be discussed first in a
[GitLab issue][gitlab-issues] that clearly outlines the changes and benefits of the feature.

### <a name="docs"></a> Want a Doc Fix?

Should you have a suggestion for the documentation, you can open an issue and outline the problem
or improvement you have - however, creating the doc fix yourself is much better!

If you want to help improve the docs, it's a good idea to let others know what you're working on to
minimize duplication of effort. Create a new issue (or comment on a related existing one) to let
others know what you're working on.

For large fixes, please build and test the documentation before submitting the PR to be sure you
haven't accidentally introduced any layout or formatting issues. You should also make sure that your
commit message follows the **[Commit Message Guidelines][developers-commits]**.

## <a name="submit"></a> Issue Submission Guidelines
Before you submit your issue search the archive, maybe your question was already answered.

If your issue appears to be a bug, and hasn't been reported, open a new issue. Help us to maximize
the effort we can spend fixing issues and adding new features, by not reporting duplicate issues.

The "[new issue][gitlab-new-issue]" form contains a number of predefined templates under **Description**
drop-down. Please select the relevant issue template and fill it out to simplify the understanding
and proper treatment of the issue. Please add one of the following labels to your issue:
`bug`/`suggestion`/`enhancement`/`discussion`/`documentation`/`question`. Do not add other labels or assign
developers, this will be done by the project management. 

**If you get help, help others. Good karma rulez!**

## <a name="submit-mr"></a> Merge Request Submission Guidelines
Before you submit your merge request consider the following guidelines:

* Search [GitLab][gitlab-merge-requests] for an open or closed Merge Request
that relates to your submission. You don't want to duplicate effort.
* Create the [development environment][developers-setup]
* Make your changes in a new git branch:

    ```shell
    git checkout -b my-fix-branch master
    ```
    **Important**:
    - You do not need to fork the repository, instead you create a new branch in the central repository.
    - The branch name should follow the regular expression `(feature|bugfix|cleanup)/*`
    and be meaningful

* Create your patch commit, **including appropriate test cases**.
    - If it's your first commit in this repository, add yourself to the `CONTRIBUTORS` file
* Please follow our [Code Style Guideline][developers-rules].
* If the changes affect public APIs, change or add relevant documentation.
* Commit your changes using a descriptive commit message that follows our
  [commit message conventions][developers-commits]. 
    ```shell
    git add <list of files you have modified>
    git commit 
    ```
  Note: do not add to your commit binary files, libraries, build artefacts etc. 

* Push your branch to GitLab:

    ```shell
    git push origin my-fix-branch
    ```
* Test your code following the [testing instructions][developers-tests].
* In GitLab, open a merge request to `StarTracker:master`. 
* If we suggest changes, then:

  * Make the required updates.
  * Re-run all the applicable tests
  * Commit your changes to your branch (e.g. `my-fix-branch`).
  * Push the updated branch to the GitLab repository (this will update your Merge Request).

    You can also amend the initial commits and force push them to the branch.

    ```shell
    git rebase master -i
    git push origin my-fix-branch -f
    ```

    This is generally easier to follow, but separate commits are useful if the Merge Request contains
    iterations that might be interesting to see side-by-side.

That's it! Thank you for your contribution!

#### After your pull request is merged

After your pull request is merged, the branch you have created will be automatically
deleted from the central repository.

* Check out the master branch:

    ```shell
    git checkout master -f
    ```

* Delete the local branch:

    ```shell
    git branch -D my-fix-branch
    ```

* Update your master with the latest upstream version:

    ```shell
    git pull --ff origin master
    ```

[coc]:https://www.unige.ch/ethique/charter/
[gitlab]:https://gitlab.cern.ch/cta_unige/startracker
[gitlab-issues]:https://gitlab.cern.ch/cta_unige/startracker/issues
[gitlab-merge-requests]:https://gitlab.cern.ch/cta-unige/startracker/-/merge_requests
[developers-commits]:https://chris.beams.io/posts/git-commit/
[gitlab-new-issue]:https://gitlab.cern.ch/cta-unige/startracker/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D=
[developers-setup]:developers.md#setup
[developers-tests]:developers.md#tests
[developers-rules]:developers.md#rules
[developers-documentation]:developers.md#documentation
