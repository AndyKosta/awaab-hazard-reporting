
from datetime import date, datetime
from behave import given, when, then, use_step_matcher
from repairs.hazard_report import HazardReportingService, InvalidReportError

TIME_FORMAT = "%Y-%m-%d %H:%M"


def to_datetime(text):
    return datetime.strptime(text, TIME_FORMAT)


use_step_matcher("parse")


@given('current time "{now}"')
def current_time(context, now):
    context.service = HazardReportingService(now=to_datetime(now))
    context.report = None
    context.error = None


use_step_matcher("re")


@when(r'"(?P<name>[^"]*)" with tenancy "(?P<tenancy>[^"]*)" reports "(?P<level>[^"]*)" hazard')
def submit_report(context, name, tenancy, level):
    row = context.table[0]

    try:
        context.report = context.service.submit_report(
            name,
            tenancy,
            level,
            row["description"],
            to_datetime(row["reported_at"])
        )
    except InvalidReportError as error:
        context.error = str(error)


use_step_matcher("parse")


@then('report accepted with reference "{prefix}"')
def report_accepted(context, prefix):
    assert context.error is None, str(context.error)
    assert context.report is not None
    assert context.report.reference.startswith(prefix)


@then('deadline "{deadline}"')
def check_deadline(context, deadline):
    expected = to_datetime(deadline)
    actual = context.report.investigation_deadline
    assert actual == expected, f"Expected {expected}, got {actual}"


@then('summary due "{due}" if investigation finished "{finished}"')
def check_summary(context, due, finished):
    actual = context.service.summary_deadline(
        date.fromisoformat(finished))
    
    assert actual == date.fromisoformat(due)


@then('report rejected with message "{message}"')
def report_rejected(context, message):
    assert context.report is None
    assert context.error == message, f"Got: {context.error}"
