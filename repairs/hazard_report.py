"""
Damp and mould hazard reporting prototype.

A council tenant reports a damp or mould problem and the system works out
the deadlines the council has to meet under Awaab's Law (phase 1,
in force from 27 October 2025):

  - emergency hazard   -> investigate and make safe within 24 hours
  - significant hazard -> investigate within 10 working days
  - written summary    -> to the tenant within 3 working days of the
                          investigation finishing
  - make safe          -> within 5 working days of the investigation
                          finishing (significant hazards)

Working days = Monday to Friday, not counting bank holidays in England.
"""

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta


# Bank holidays in England (taken from gov.uk/bank-holidays).
# Only 2026 and 2027 are needed for this prototype.
BANK_HOLIDAYS = {
    date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 4),
    date(2026, 5, 25), date(2026, 8, 31), date(2026, 12, 25), date(2026, 12, 28),
    date(2027, 1, 1), date(2027, 3, 26), date(2027, 3, 29), date(2027, 5, 3),
    date(2027, 5, 31), date(2027, 8, 30), date(2027, 12, 27), date(2027, 12, 28),
}

EMERGENCY_HOURS = 24
INVESTIGATION_WORKING_DAYS = 10
SUMMARY_WORKING_DAYS = 3
MAKE_SAFE_WORKING_DAYS = 5

HAZARD_LEVELS = ["emergency", "significant"]
MIN_DESCRIPTION_LENGTH = 15

# Tenancy references look like HT-123456
TENANCY_REF_PATTERN = re.compile(r"^HT-\d{6}$")


class InvalidReportError(Exception):
    """Raised when a hazard report fails validation."""
    pass


def is_working_day(day):
    """True if the day is Monday-Friday and not a bank holiday."""
    if day.weekday() >= 5:   # 5 = Saturday, 6 = Sunday
        return False
    if day in BANK_HOLIDAYS:
        return False
    return True


def add_working_days(start_day, number_of_days):
    """
    Count forward a number of working days from start_day.
    The start day itself is not counted (the clock starts the next day).
    """
    current = start_day
    counted = 0
    while counted < number_of_days:
        current = current + timedelta(days=1)
        if is_working_day(current):
            counted += 1
    return current


@dataclass
class HazardReport:
    reference: str
    tenant_name: str
    tenancy_ref: str
    hazard_level: str
    description: str
    reported_at: datetime
    investigation_deadline: datetime


class HazardReportingService:
    """Takes hazard reports from tenants and works out the legal deadlines."""

    def __init__(self, now):
        # 'now' is passed in so the tests can control the current time
        self.now = now
        self.reports = []
        self.next_number = 1

    def submit_report(self, tenant_name, tenancy_ref, hazard_level,
                      description, reported_at):
        self.check_report_is_valid(tenant_name, tenancy_ref, hazard_level,
                                   description, reported_at)

        deadline = self.work_out_investigation_deadline(hazard_level, reported_at)

        reference = "DMR-" + str(self.next_number).zfill(5)
        self.next_number += 1

        report = HazardReport(
            reference=reference,
            tenant_name=tenant_name.strip(),
            tenancy_ref=tenancy_ref,
            hazard_level=hazard_level,
            description=description.strip(),
            reported_at=reported_at,
            investigation_deadline=deadline,
        )
        self.reports.append(report)
        return report

    def check_report_is_valid(self, tenant_name, tenancy_ref, hazard_level,
                              description, reported_at):
        if tenant_name is None or tenant_name.strip() == "":
            raise InvalidReportError("Tenant name is required")

        if tenancy_ref is None or not TENANCY_REF_PATTERN.match(tenancy_ref):
            raise InvalidReportError("Tenancy reference must look like HT-123456")

        if hazard_level not in HAZARD_LEVELS:
            raise InvalidReportError("Hazard level must be emergency or significant")

        if description is None or len(description.strip()) < MIN_DESCRIPTION_LENGTH:
            raise InvalidReportError(
                "Please describe the problem in at least 15 characters")

        if reported_at > self.now:
            raise InvalidReportError("Report time cannot be in the future")

    def work_out_investigation_deadline(self, hazard_level, reported_at):
        if hazard_level == "emergency":
            # 24 clock hours - weekends and bank holidays still count
            return reported_at + timedelta(hours=EMERGENCY_HOURS)

        # significant hazard: end of the 10th working day
        last_day = add_working_days(reported_at.date(), INVESTIGATION_WORKING_DAYS)
        return datetime(last_day.year, last_day.month, last_day.day, 17, 0)

    def written_summary_deadline(self, investigation_finished_on):
        return add_working_days(investigation_finished_on, SUMMARY_WORKING_DAYS)

    def make_safe_deadline(self, investigation_finished_on):
        return add_working_days(investigation_finished_on, MAKE_SAFE_WORKING_DAYS)
