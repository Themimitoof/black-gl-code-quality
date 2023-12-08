# Black GitLab Code Quality

This project aim to convert [Black](https://github.com/psf/black) report to
[CodeClimate](https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md)
format that can be ingest by GitLab.

```
→ poetry run black-gl-cq src/black_gl_code_quality | jq
[
  {
    "type": "issue",
    "description": "Black would reformat",
    "location": {
      "lines": {
        "begin": 1,
        "end": 1
      },
      "path": "src/black_gl_code_quality/__main__.py"
    },
    "severity": "major"
  },
  {
    "type": "issue",
    "description": "Black would reformat",
    "location": {
      "lines": {
        "begin": 1,
        "end": 1
      },
      "path": "src/black_gl_code_quality/error.py"
    },
    "severity": "major"
  }
]
```

## Motivation

For security concerns, Docker-in-Docker has been disabled in all GitLab runners that I
have access/manage. Because the Code Quality template shipped with GitLab instances use
CodeClimate CLI that requires a Docker environment, we can't use it and an alternative
solution was required to obtain Black errors in our Code Quality reports.


## How to install

Simply run the following command:

```
pip install black-gl-code-quality
```

If you use Poetry, you can add it to your dev-dependencies:

```
poetry add --group dev black-gl-code-quality
```

## Usage

There is two ways to use this tool:

 - by piping Black
 - by calling `black-gl-code-quality` (or by it's alias `black-gl-cq`) directly


### Piping with Black

Piping with Black requires to forward  `stderr` to `stdout`. You can use the following
command in the `.gitlab-ci.yml`:

```
black --check src/ 2>&1 | black-gl-cq > black-code-quality-report.json
```

Here's an example for a GitLab-CI job:

```yaml
lint:black:
  stage: test
  script:
    - source .venv/bin/activate
    - black --check src/ 2>&1 | black-gl-cq > black-code-quality-report.json
  artifacts:
    when: always
    reports:
      codequality: black-code-quality-report.json
```

### Calling `black-gl-code-quality` directly

Calling `black-gl-code-quality` (or it's alias `black-gl-cq`) execute Black with the
`--check` argument. It forwards all arguments you pass if you need to configure Black
via the CLI.

Specifying source folders is **MANDATORY**.

Here's an example for a GitLab-CI job:

```yaml
lint:black:
  stage: test
  script:
    - source .venv/bin/activate
    - black-gl-cq src/ > black-code-quality-report.json
  artifacts:
    when: always
    reports:
      codequality: black-code-quality-report.json
```

Admit we want to skip string normalization:

```yaml
lint:black:
  stage: test
  script:
    - source .venv/bin/activate
    - black-gl-cq -S src/ > black-code-quality-report.json
  artifacts:
    when: always
    reports:
      codequality: black-code-quality-report.json
```

### Change severity

By default, all errors have the severity `major`. Depending how you consider Black issues
important, you can change the severity for all errors returned by the report by using
one of the following [values](https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#issues)
with the `BLACK_GL_SEVERITY` environment variable: `info`, `minor`, `major`, `critical`, `blocker`.

Here's an example for a GitLab-CI job:

```yaml
lint:black:
  stage: test
  variables:
    BLACK_GL_SEVERITY: minor
  script:
    - source .venv/bin/activate
    - black-gl-cq src/ > black-code-quality-report.json
  artifacts:
    when: always
    reports:
      codequality: black-code-quality-report.json
```


## Contributions

In case you have a suggestion or want a new feature, feel free to open a
[discussion](https://github.com/Themimitoof/black-gl-code-quality/discussions).

If you found a bug, you can [open an issue](https://github.com/Themimitoof/black-gl-code-quality/issues).

In order to maintain an overall good code quality, this project use the following tools:

 - [Black](https://github.com/psf/black)
 - [Isort](https://github.com/PyCQA/isort)
 - [Flake8](https://flake8.pycqa.org/en/latest/)

Linting and formatting tools are configured to match the [current default rules of Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

Please ensure to run these tools before commiting and submiting a Pull request. In case one of
these mentionned tools report an error, the CI will automatically fail.

In case you are able to fix by yourself a bug, enhance the code or implement a new
feature, feel free to send a [Pull request](https://github.com/Themimitoof/black-gl-code-quality/pulls).

## License

This project is released under the [BSD-3 Clause](LICENSE). Feel free to use,
contribute, fork and do what you want with it. Please keep all licenses, copyright
notices and mentions in case you use, re-use, steal, fork code from this repository.
