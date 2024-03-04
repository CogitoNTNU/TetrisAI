# Git Guidelines

**ℹ️ [git-conventional-commits](https://github.com/qoomon/git-conventional-commits)**  A CLI util to ensure this conventions and generate changelogs

## Commit Message Formats

### Default

<pre>
<b><a href="#types">&lt;type&gt;</a></b></font>: <b><a href="#description">&lt;description&gt;</a></b>
</pre>

### Types

* Relevant changes
  * `feat` Commits, that adds or remove a new feature
  * `fix` Commits, that fixes a bug
* `refactor` Commits, that rewrite/restructure your code, however does not change any API behavior
* `style` Commits, that do not affect the meaning (white-space, formatting, missing semi-colons, etc)
* `test` Commits, that add missing tests or correcting existing tests
* `docs` Commits, that affect documentation only
* `build` Commits, that affect build components like build tool, ci pipeline, dependencies, project version, ...
* `chore` Miscellaneous commits e.g. modifying `.gitignore`

### Examples

* ```text
  feat: add email notifications on new direct messages
  ```

* ```text
  fix: add missing parameter to service call

  The error occurred because of <reasons>.
  ```

* ```text
  build: update dependencies
  ```

* ```text
  refactor: implement fibonacci number calculation as recursion
  ```

* ```text
  style: remove empty line
  ```

## Branch Naming

* Create all feature branches from issues in github, name will then be:
  * `feature/<issue-number>-<short-description>`

## Useful commands

* Fetch a spesific brach from remote

    ```bash
    git fetch origin <branch-name>:<branch-name>
    ```

* Fetch all branches from remote

    ```bash
    git fetch --all
    ```

* Reset local working directory to remote (use with caution, as it will remove all local changes!)
  
    ```bash
    git reset --hard origin/<branch-name>
    ```

* Remove local branch

    ```bash
    git branch -d <branch-name>
    ```

* Revert a commit

    ```bash
    git revert <commit-hash>
    ```

* Unstage a file (remove from staging area, but keep changes in working directory)

    ```bash
    git reset <file>
    ```

## Workflow

* Create a new branch from `dev` for each feature from issues in github
* Commit often and push to remote
* If a feature takes long, merge `dev` to feature branch to keep it up to date and still compatible
* Create merge request to `dev` when feature is done
* Review and merge to `dev`
* Merge `dev` to `main` once in a while when `dev` is stable
* Minor fixes and addons can be committed directly to `dev` without creating a new branch
