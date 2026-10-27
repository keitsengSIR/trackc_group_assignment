# Requirements Traceability Matrix (RTM) - Track C

Statuses reflect the test evidence inspected for the Week 10 checkpoint.
A missing named test does not, by itself, prove that a feature is absent.

| Req ID | Requirement | Associated test / evidence | Checkpoint status |
|---|---|---|---|
| REQ-01 | Patient age must be between 0 and 120 years. | `test_patient_age_boundaries` in `test_patient_validation.py`; tests a standalone validation helper. | Partially verified; application-level enforcement not verified |
| REQ-02 | National ID / Passport number must match standard format. | `test_valid_national_id_format` not found in the searched Python files. | Test evidence not found |
| REQ-03 | Appointment date cannot be scheduled in the past. | `test_appointment_future_date` not found in the searched Python files. | Test evidence not found |
| REQ-04 | Doctor availability must be checked before booking. | `test_doctor_schedule_conflict` not found in the searched Python files. | Test evidence not found |
| REQ-05 | Patient intake form must sanitize malicious script inputs. | `test_sql_injection_sanitization` not found in the searched Python files. | Test evidence not found |
| REQ-06 | Prescribed dosage must be within allowable numeric range. | `test_dosage_equivalence_partition` not found in the searched Python files. | Test evidence not found |
| REQ-07 | Duplicate patient records must be flagged on creation. | `test_duplicate_patient_detection` not found in the searched Python files. | Test evidence not found |
| REQ-08 | Appointment cancellation must free up the time slot. | `test_cancelled_appointment_no_longer_blocks_time_slot` in `tests/test_appointment_validation.py` verifies the model-level slot-release rule. The cancellation view itself is not covered by this test. | Model-level behavior verified; view-level behavior not verified |
| REQ-09 | Medical record notes must be encrypted at rest in DB. | `test_record_encryption_at_rest` not found in the searched Python files. | Test evidence not found |
| REQ-10 | System must log all failed authentication attempts. | `test_audit_log_failed_login` not found in the searched Python files. | Test evidence not found |

## Week 10 testing evidence

- Latest selected test run: 17 passed in 8.49 seconds. Collection initially appeared to show the
  manual patient-form test file in two sections; collect-only confirmed 17 unique test cases.
- Combined patient and appointment statement coverage: 18% (517 covered of
  2,845 statements, as reported by pytest-cov).
- `patient/forms/patients.py` has 100% statement coverage in this run.
- Forms mutation score: v1 37.5%; v2 93.75% (15 of 16 mutants killed).
- One v2 forms mutant survived: `ReplaceAndWithOr 0`; equivalence has not been established.
- `test_patient_database_persistence` verifies that a synthetic patient can be saved and retrieved.
- Appointment tests cover valid persistence, doctor-overlap rejection,
  patient-overlap rejection, and model-level slot release after cancellation.
- The cancellation view itself has not been exercised by these appointment tests.
- Coverage and mutation results apply only to the measured modules and tests,
  not the whole application.
