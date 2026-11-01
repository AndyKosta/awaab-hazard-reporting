Feature: Report a damp or mould hazard
  As a council tenant living with damp or mould
  I want to report the problem online and see when it must be dealt with
  So that I know the council is meeting its legal deadlines under Awaab's Law

  Background:
    Given the current time is "2026-12-18 16:00"

  Scenario: Tenant reports an emergency hazard on a Friday afternoon
    When "Amina Khan" with tenancy "HT-104522" reports an "emergency" hazard
      | description                                          | reported_at      |
      | Black mould around the baby's cot and window leaking | 2026-12-18 15:30 |
    Then the report is accepted with a reference starting "DMR-"
    And the investigation deadline is "2026-12-19 15:30"

  Scenario: Significant hazard reported just before the Christmas bank holidays
    When "John Smith" with tenancy "HT-209871" reports a "significant" hazard
      | description                                  | reported_at      |
      | Damp patches spreading on the bedroom ceiling | 2026-12-18 09:15 |
    Then the report is accepted with a reference starting "DMR-"
    And the investigation deadline is "2027-01-06 17:00"
    And if the investigation finishes on "2027-01-06" the written summary is due by "2027-01-11"

  Scenario Outline: Invalid reports are rejected with a clear message
    When "<name>" with tenancy "<tenancy>" reports a "<level>" hazard
      | description   | reported_at   |
      | <description> | <reported_at> |
    Then the report is rejected with the message "<message>"

    Examples:
      | name       | tenancy   | level       | description                       | reported_at      | message                                                |
      |            | HT-104522 | significant | Mould on the kitchen wall         | 2026-12-18 10:00 | Tenant name is required                                |
      | Amina Khan | 104522    | significant | Mould on the kitchen wall         | 2026-12-18 10:00 | Tenancy reference must look like HT-123456             |
      | Amina Khan | HT-104522 | minor       | Mould on the kitchen wall         | 2026-12-18 10:00 | Hazard level must be emergency or significant          |
      | Amina Khan | HT-104522 | significant | Mould                             | 2026-12-18 10:00 | Please describe the problem in at least 15 characters  |
      | Amina Khan | HT-104522 | significant | Mould on the kitchen wall         | 2026-12-18 16:01 | Report time cannot be in the future                    |
