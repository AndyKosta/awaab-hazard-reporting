
# Damp and Mould Hazard Reporting

This is a small Awaab's law Python project which enables council tenants to submit complaints about damp/mould and works out   timeframes for addressing these issues and focuses on rules introduced on 27 October 2025. This is basic prototype for demonstrating requirements and testing not a complete council reporting system.

## User Story

I am a council tenant and want to report that my home is damp or has mould in it and know when council should do something about it.

## What Program Does

- Takes tenant's name and tenancy reference (e.g. HT-123456).
- Takes care of critical and emergency hazard reports.
- Must be at least 15 characters long.
- Does not accept reports from date in future.
- Estimates a 24-hour period for emergency hazards.
- Estimates investigation time of 10 working days for significant hazards (excluding weekends and bank holidays).
- Calculates when summary is due (3 working days after investigation).
- Gives each accepted report a unique reference starting with DMR.

## How to Run

Create virtual environment:

```bash
python -m venv venv
```

Activate it

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

Run BDD tests:

```bash
behave
```

Run unit tests:

```bash
pytest
```

## Test Results

  project has:
- 3 BDD scenarios (7 test cases)
- 5 unit tests

All tests passed in documented run.


