
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta

BANK_HOLIDAYS = {
    date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 4),
    date(2026, 5, 25), date(2026, 8, 31), date(2026, 12, 25), date(2026, 12, 28),
    date(2027, 1, 1), date(2027, 3, 26), date(2027, 3, 29), date(2027, 5, 3),
    date(2027, 5, 31), date(2027, 8, 30), date(2027, 12, 27), date(2027, 12, 28),
}

EMERGENCY_HOURS = 24
INVESTIGATION_WORKINGDAYS = 10
SUMMARY_WORKINGDAYS = 3
SAFE_WORKINGDAYS = 5

HAZARD_LEVELS = ["emergency", "significant"]
MIN_DESCRIPTION_LENGTH = 15
TENANCY_REF_PATTERN = re.compile(r"^HT-\d{6}$")


class InvalidReportError(Exception):
    pass


def is_workingday(day):
    if day.weekday() >= 5:
        return False

    if day in BANK_HOLIDAYS:
        return False

    return True


def add_workingdays(start_day, number_of_days):
    current = start_day
    counted = 0

    while counted < number_of_days:
        current += timedelta(days=1)

        if is_workingday(current):
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

    def __init__(self, now):
        self.now = now
        self.reports = []
        self.next_number = 1

    def submit_report(self, tenant_name, tenancy_ref, hazard_level,
                      description, reported_at):

        self.check_report(
            tenant_name, tenancy_ref, hazard_level,description, reported_at)

        deadline = self.get_deadline(hazard_level, reported_at)
        reference = "DMR-" + str(self.next_number).zfill(5)
        self.next_number += 1
        report = HazardReport(
            reference=reference,
            tenant_name=tenant_name.strip(),
            tenancy_ref=tenancy_ref,
            hazard_level=hazard_level,
            description=description.strip(),
            reported_at=reported_at,
            investigation_deadline=deadline )
        self.reports.append(report)
        return report

    def check_report(self, tenant_name, tenancy_ref, hazard_level,
                     description, reported_at):

        if not tenant_name or not tenant_name.strip():
            raise InvalidReportError("Name required")

        if not tenancy_ref or not TENANCY_REF_PATTERN.match(tenancy_ref):
            raise InvalidReportError("Tenancy must match HT-123456")

        if hazard_level not in HAZARD_LEVELS:
            raise InvalidReportError(
                "Hazard must be emergency or significant")

        if not description or len(description.strip()) < MIN_DESCRIPTION_LENGTH:
            raise InvalidReportError("Description needs 15 characters")

        if reported_at > self.now:
            raise InvalidReportError("Future date not allowed")

    def get_deadline(self, hazard_level, reported_at):
        if hazard_level == "emergency":
            return reported_at + timedelta(hours=EMERGENCY_HOURS)

        last_day = add_workingdays(
            reported_at.date(),
             INVESTIGATION_WORKINGDAYS)
        
        return datetime( last_day.year, last_day.month, last_day.day, 17, 0)

    def summary_deadline(self, investigation_finished_on):
        return add_workingdays(
            investigation_finished_on,
            SUMMARY_WORKINGDAYS)

    def safe_deadline(self, investigation_finished_on):
        return add_workingdays(
            investigation_finished_on,
            SAFE_WORKINGDAYS)
