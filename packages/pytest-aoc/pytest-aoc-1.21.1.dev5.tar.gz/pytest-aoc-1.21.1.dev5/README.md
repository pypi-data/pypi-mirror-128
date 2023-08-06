# pytest-aoc

This pytest plugin downloads puzzle inputs for [Advent of Code][1] and
synthesizes fixtures that you can use in your tests.

![PyPI - Implementation](https://img.shields.io/pypi/implementation/pytest-aoc?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-aoc?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/pytest-aoc?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/j0057/pytest-aoc?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/pytest-aoc?style=flat-square)

[1]: https://adventofcode.com/

## Installing and configuring

Installing is easy: `python -m pip install pytest-aoc`. Next you will need to configure
_two_ things: for which event (year) the plugin should download inputs, and a
valid session cookie. These are normally valid for about a month or so.

To set the year, put it in `setup.cfg`:

    [tool:pytest]
    aoc_year = 2018

Then, put a valid session ID in a file named `.cookie` and also name this file
in your `.gitignore`.

With these two things in place, when running pytest, this plugin will download
any missing inputs, and generate pytest fixtures that you can use in your test
functions, see 'Using' and 'Fixtures', below.

## Using

With this plugin properly configured, you can write tests like this:

    def test_01a(day01_numbers):
        assert sum(day01_numbers) == 123

Here, the parameter `day01_numbers` is a fixture that contains the numbers on
each line in the file `input/day01.txt`.

## Fixtures

These fixtures are synthesized for each available day. They're not executed
until you ask for them in a test.

- `dayNN_text`: The text in the input file, but stripped of any leading and trailing whitespace.
  ~ `"spam"`

- `dayNN_raw`: The raw text in the input file.
  ~ `"eggs\n"`

- `dayNN_lines`: A list of stripped lines.
  ~ `["spam", "eggs", "albatross"]`

- `dayNN_numbers`: A list of numbers.
  ~ `[1, 1, 2, 3, 5, 8]`

- `dayNN_number`: A single number.
  ~ `5`

- `dayNN_grid`: A list of lists, representing a grid of textual values.
  ~ `[["spam", "eggs"], ["ham", "albatross"]]`

- `dayNN_number_grid`: A list of lists, representing a grid of numbers.
  ~ `[[8, 1, 6], [3, 5, 7], [4, 9, 2]]`

## Command-line and configuration options

You can pass the options from the command line or set them in setup.cfg. The
command line takes precedence.

- `--aoc-year`/`aoc_year`: The year for which to download puzzle inputs.
  (Mandatory)
- `--aoc-session-id`: The session ID to use for requesting puzzle inputs. This
  one has no equivalent setup.cfg key; that's a security feature. (Optional)
- `--aoc-session-file`/`aoc_session_file`: The file from which to read the
  session ID. (Optional; default `.cookie`)
- `--aoc-input-dir`/`aoc_input_dir`: The directory in which inputs are stored.
  Will be created if it doesn't exist. (Optional; default `input`)

## Developing / testing

Set environment variables using `. .envrc` or by automatically loading them
using `direnv allow`.

Create a virtualenv named `env` and install an editable versionof this package
with all extra development dependencies:

    python -m venv env
    python -m pip install -U -e .[dev]

Run tests directly, to test against the current Python, or via tox to test
against multiple Python versions:

    python -m pytest
    python -m tox

## Releasing

This package is currently using [setuptools-version-command][svc] to derive
the version number from the Git tags using `git describe`. 

Tag the release version (or it will be a post-release on a previous version),
where `x.y.z` is the version:

    git tag -a x.y.z

Check that the version is actually sane:

    ./setup.py --version

Bake an sdist and a wheel into a clean `dist` directory:

    rm -f dist/*
    python -m build

Upload the goods to PyPI:

    python -m twine upload dist/*

Upload the goods to Github, where again `x.y.z` is the version:

    git push github master --tags
    gh release create --prerelease x.y.z dist/* 

(Leave out the `--prerelease` flag as necessary.)
