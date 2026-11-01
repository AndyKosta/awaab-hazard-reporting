
Feature: Damp and mould reporting

  As a council tenant
  I want to report damp or mould
  So I can check council deadlines

  Background:
    Given current time "2026-12-18 16:00"

  Scenario: Emergency report on Friday
    When "Amina Khan" with tenancy "HT-104522" reports "emergency" hazard
      | description                                           | reported_at      |
      | Black mould around the baby's cot and window leaking | 2026-12-18 15:30 |
    Then report accepted with reference "DMR-"
    And deadline "2026-12-19 15:30"

  Scenario: Significant report near Christmas
    When "John Smith" with tenancy "HT-209871" reports "significant" hazard
      | description                                   | reported_at      |
      | Damp patches spreading on the bedroom ceiling | 2026-12-18 09:15 |
    Then report accepted with reference "DMR-"
    And deadline "2027-01-06 17:00"
    And summary due "2027-01-11" if investigation finished "2027-01-06"

  Scenario Outline: Invalid reports
    When "<name>" with tenancy "<tenancy>" reports "<level>" hazard
      | description   | reported_at   |
      | <description> | <reported_at> |
    Then report rejected with message "<message>"

    Examples:
      | name       | tenancy   | level       | description               | reported_at      | message                                 |
      |            | HT-104522 | significant | Mould on kitchen wall     | 2026-12-18 10:00 | Name required                           |
      | Amina Khan | 104522    | significant | Mould on kitchen wall     | 2026-12-18 10:00 | Tenancy must match HT-123456            |
      | Amina Khan | HT-104522 | minor       | Mould on kitchen wall     | 2026-12-18 10:00 | Hazard must be emergency or significant |
      | Amina Khan | HT-104522 | significant | Mould                     | 2026-12-18 10:00 | Description needs 15 characters         |
      | Amina Khan | HT-104522 | significant | Mould on kitchen wall     | 2026-12-18 16:01 | Future date not allowed                 |
