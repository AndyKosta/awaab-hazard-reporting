from datetime import date, datetime

from behave import given, when, then, use_step_matcher

from repairs.hazard_report import HazardReportingService, InvalidReportError


TIME_FORMAT = "%Y-%m-%d %H:%M"


def to_datetime(text):
    return datetime.strptime(text, TIME_FORMAT)


@given('the current time is "{now}"')
def step_current_time(context, now):
    context.service = HazardReportingService(now=to_datetime(now))
    context.report = None
    context.error = None


# regex matcher used here so an empty tenant name ("") can still match
use_step_matcher("re")


@when(r'"(?P<name>[^"]*)" with tenancy "(?P<tenancy>[^"]*)" reports an? "(?P<level>[^"]*)" hazard')
def step_submit_report(context, name, tenancy, level):
    row = context.table[0]
    try:
        context.report = context.service.submit_report(
            tenant_name=name,
            tenancy_ref=tenancy,
            hazard_level=level,
            description=row["description"],
            reported_at=to_datetime(row["reported_at"]),
        )
    except InvalidReportError as error:
        context.error = str(error)


use_step_matcher("parse")


@then('the report is accepted with a reference starting "{prefix}"')
def step_report_accepted(context, prefix):
    assert context.error is None, "Report was rejected: " + str(context.error)
    assert context.report.reference.startswith(prefix)


@then('the investigation deadline is "{deadline}"')
def step_investigation_deadline(context, deadline):
    expected = to_datetime(deadline)
    actual = context.report.investigation_deadline
    assert actual == expected, "Expected " + str(expected) + " but got " + str(actual)


@then('if the investigation finishes on "{finished}" the written summary is due by "{due}"')
def step_summary_deadline(context, finished, due):
    actual = context.service.written_summary_deadline(date.fromisoformat(finished))
    assert actual == date.fromisoformat(due), "Summary due date was " + str(actual)


@then('the report is rejected with the message "{message}"')
def step_report_rejected(context, message):
    assert context.report is None, "Report should not have been accepted"
    assert context.error == message, "Got message: " + str(context.error)
