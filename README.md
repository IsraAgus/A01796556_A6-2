
# A01796556_A6-2

Activity 6.2 – Programming Exercise 3 and Unit Testing (Software Testing & Quality Assurance).

## Goals
- Implement a simple Hotel Reservation System in Python.
- Create unit tests and document results.
- Ensure the project complies with PEP 8.
- Run static analysis with flake8 and pylint (no issues).
- Achieve >= 85% code coverage and store evidence outputs in the repository.

## Tooling (planned)
- Python 3.x
- pytest + coverage
- flake8
- pylint

## Branching model
- main: stable submission branch
- develop: integration branch
- feature/*: feature branches

## Evidence
All execution outputs will be stored under `evidence/`:
- pytest results
- coverage report
- flake8 output
- pylint output

## Quickstart
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run tests
pytest -q

## Coverage
python -m coverage run -m pytest
python -m coverage report -m

## Linters
flake8 src tests
pylint src tests