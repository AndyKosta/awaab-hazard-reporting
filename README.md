# Damp and Mould Hazard Reporting (Awaab's Law prototype)

A small Python prototype for a local authority. Council tenants report a
damp or mould hazard and the system works out the legal deadlines the
council must meet under Awaab's Law (phase 1, from 27 October 2025).

## User story

As a council tenant living with damp or mould,
I want to report the problem online and see when it must be dealt with,
so that I know the council is meeting its legal deadlines.

## Acceptance criteria

1. A report needs a tenant name, a tenancy reference (HT-123456), a hazard
   level (emergency or significant) and a description of at least 15 characters.
2. A report cannot be dated in the future.
3. Emergency hazards must be investigated within 24 hours.
4. Significant hazards must be investigated within 10 working days
   (weekends and bank holidays do not count).
5. A written summary is due within 3 working days of the investigation finishing.
6. Every accepted report gets a unique reference starting DMR-.

## How to run

```
python -m venv venv
venv\Scripts\activate          (Windows)
source venv/bin/activate       (Mac/Linux)
pip install -r requirements.txt
behave
pytest
```
Results: 3 scenarios (7 test cases) passing, 5 unit tests passing.