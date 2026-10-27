Feature: Patient Intake and Appointment Management
  As a clinic receptionist
  I want to register patients and manage appointments securely
  So that patient records remain accurate and valid

  Scenario: Successfully register a new patient with valid details
    Given the patient intake form is open
    When the receptionist enters patient ID "P500" with name "John Doe" and age 35
    Then the system should save the patient record successfully

  Scenario: Reject patient registration with invalid age boundary
    Given the patient intake form is open
    When the receptionist enters patient ID "P501" with name "Baby Invalid" and age 150
    Then the system should display an age validation error