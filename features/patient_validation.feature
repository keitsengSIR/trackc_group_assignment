Feature: Patient Data and Appointment Validation
  As a Healthcare Administrator
  I want patient age boundaries and appointment slots validated automatically
  So that data entry errors and overlapping schedules are prevented.

  Scenario Outline: Validating patient age constraints
    Given a patient registration form with age <age>
    When the validation service checks the record
    Then the validation outcome should be <status>

    Examples:
      | age | status   |
      | -5  | Rejected |
      | 0   | Accepted |
      | 45  | Accepted |
      | 150 | Rejected |

  Scenario: Preventing duplicate medical identification numbers
    Given an existing patient with medical ID "MED-9988"
    When a new patient is registered with medical ID "MED-9988"
    Then the system should reject the registration due to a duplicate ID violation