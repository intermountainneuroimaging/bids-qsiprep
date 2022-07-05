# Contributing

## Getting started

1. Follow instructions to [install poetry](https://python-poetry.org/docs/#installation).
2. Follow instructions to [install pre-commit](https://pre-commit.com/#install)

After cloning the repo:

(If you need to change your python version:)

```shell
poetry env use <path/to/your/python/executable>
poetry update
```

1. `poetry install`: Install project and all dependencies (see
   __Dependency management__ below)
2. `pre-commit install`: Install pre-commit hooks (see __Linting and Testing__ below)

## Dependency management

This gear uses [`poetry`](https://python-poetry.org/) to manage dependencies,
develop, build and publish.

### Dependencies

Dependencies are listed in the `pyproject.toml` file.

#### Managing dependencies

* Adding: Use `poetry add [--dev] <dep>`
* Removing: Use `poetry remove [--dev] <dep>`
* Updating: Use `poetry update <dep>` or `poetry update` to update all deps.
  * Can also not update development dependencies with `--no-dev`
  * Update dry run: `--dry-run`

#### Using a different version of python

Poetry manages virtual environments and can create a virtual environment with
different versions of python, however that version must be installed on the machine.  

As mentioned above, you can configure the python version by using
`poetry env use <path/to/executable>`

#### Helpful poetry config options

See full options [Here](https://python-poetry.org/docs/configuration/#available-settings).

List current config: `poetry config --list`

* `poetry config virtualenvs.in-project <true|false|None>`: create virtual environment
inside project directory
* `poetry config virtualenvs.path <path>`: Path to virtual environment directory.

## Linting and Testing

Local linting and testing scripts are managed through
[`pre-commit`](https://pre-commit.com/).
Pre-commit allows running hooks which can be defined locally, or in other
repositories. Default hooks to run on each commit:

* `test:flywheel-lint`:
  * black: runs `black`.
  * hadolint: Dockerfile linter.
  * jsonlint: JSON syntax validator.
  * linkcheck: checks links are working.
  * markdownlint: Markdown file linter.
  * pydocstyle: checks python styling.
  * safety: checks your dependencies for known security vulnerabilities.
  * shellcheck: finds bugs in shell scripts.
  * yamllint: YAML linter.
* `test:helm-check`: Helm checker.
* `test:pre-commit:isort`: runs `isort`.
* `test:pre-commit:pylint`: gear files linter.
* `test:pre-commit:pylint-tests`: tests files linter.
* `test:pre-commit:pytest`: runs `pytest`.
* `test:pre-commit:mypy`: typing checker.
* `publish:docker:test`: builds docker image and publishes it to Docker Hub.

These hooks will all run automatically on commit, but can also be run manually
or just be disabled.

### pre-commit usage

* Run hooks manually:
  * Run on all files: `pre-commit run -a`
  * Run on certain files: `pre-commit run --files test/*`
* Update (e.g. clean and install) hooks: `pre-commit clean && pre-commit install`
* Disable all hooks: `pre-commit uninstall`
* Enable all hooks: `pre-commit install`
* Skip a hook on commit: `SKIP=<hook-name> git commit`
* Skip all hooks on commit: `git commit --no-verify`

### end-to-end testing

Most of the tests are run by the `tests:pre-commit:pytest` hook. However, the
"end-to-end" tests need the test Docker image and the Flywheel `API_KEY` for GA.

To run it, first build the Docker images. E.g.:

```shell
docker build -t flywheel/bids-qsiprep:local .
docker build --build-arg BASE="flywheel/bids-qsiprep:local" \
    -t flywheel/test_bids-qsiprep:local \
    -f tests/Dockerfile .
```

(*Note: the base Docker image is large (11.9GB), and so are these gear images)

Then, log into the Flywheel platform:

```shell
fw login <my_GA_api_key>
```

Then, run:

```shell
docker run -it --rm \
    -v $HOME/.config/flywheel/user.json:/home/qsiprep/.config/flywheel/user.json \
    --entrypoint /bin/bash \
    flywheel/test_bids-qsiprep:latest \
        -c 'poetry run pytest tests/end-to-end_tests'
```

## Adding a contribution

Every contribution should be associated with a ticket on the GEAR JIRA board, or be a
hotfix.  You should contribute by creating a branch titled with either
`hotfix-<hotfix_name>` or `GEAR-<gear_num>-<description>`.  For now, other branch names
will be accepted, but soon branch names will be rejected if they don't follow this pattern.

When contributing, make a Merge Request against the main branch.

### Merge requests

__Note__ that the `end-to-end_tests` and `integration_tests` require an API key, so
they are skipped in the GitLab CI run. So please make sure they run locally before
creating your Merge Request.

The merge request should contain at least two things:

1. Your relevant change
2. Update the corresponding entry under `docs/release_notes.md`

Adding the release notes does two things:

1. It makes it easier for the reviewer to identify what relevant changes they should
expect and look for in the MR, and
2. It makes it easier to create a release.

#### Populating release notes

For example, if the gear is currently on version `0.2.1` and you are working on a bugfix
under the branch GEAR-999-my-bugfix.  When you create a merge request against `main`,
you should add a section to `docs/release_notes.md` such as the following:

```markdown
## 0.2.2
BUG:
* Fixed my-bug, see [GEAR-999](https://flywheelio.atlassian.net/browse/GEAR-999)

```

Where the rest of the file contains release notes for previous versions.

#### Adding changelog entry

The [changelog](./docs/changelog.md) is a place to put more informal notes about large
design decisions.  This is useful to look back on design decisions made by you, or other
engineers and try to understand why. This is not required, but is encouraged for large
changes.

### Creating a release

When your merge request is reviewed and approved, you should pull from main locally:

```bash
git checkout main # Locally change to main branch
git pull origin main # Locally pull updates from main branch
```

Then update the versions accordingly:

1. Update poetry version: `poetry version <new_version>`
2. Update the version in the manifest:
    1. Update `"version"` key with new version
    2. Update `"custom.gear-builder.image"` key with new image version
3. Commit version changes

Then you can tag the version and push:

```bash
git tag <new_version>
git push origin main
git push origin --tags
```

Once you've pushed tags, you can go to the gitlab UI -> Project Overview -> Releases
and create a new release.  You can copy the release notes that are already populated in
the `docs/release_notes.md` document.
