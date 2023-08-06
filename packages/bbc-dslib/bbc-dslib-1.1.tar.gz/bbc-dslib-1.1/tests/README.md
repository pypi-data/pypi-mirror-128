# Testing dslib

## Installation of testing environment

Go to your dslib repository folder and run the following command:

```bash
pip install -e '.[testing]'
```

## Running a test file

Go to the `tests` folder (where this README.md is located) and run a command of this type:

```bash
pytest -vv ./test_bigquery.py
```

## Code coverage

Go to the `tests` folder (where this README.md is located).

Report test coverage of module ``dslib.google._bigquery`` by test file ``./google/test_bigquery.py``:

```bash
coverage erase
pytest ./google/test_bigquery.py --cov=dslib.google._bigquery
coverage html
```

You can then browse ``htmlcov/index.html``.

```bash
open $(pwd)/htmlcov/index.html
```

One-liner:

```bash
coverage erase && pytest ./google/test_bigquery.py --cov=dslib.google._bigquery && coverage html && open $(pwd)/htmlcov/index.html
```
