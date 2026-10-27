# Requirements Traceability Matrix (RTM) - Track C

| Req ID | Requirement Description | Source | Test Level | Associated Test Cases | Status |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Patient age must be between 0 and 120 years. | README / Code | Unit | `test_patient_age_boundaries` | Implemented |
| **REQ-02** | National ID / Passport number must match standard format. | Issue Tracker | Unit | `test_valid_national_id_format` | Implemented |
| **REQ-03** | Appointment date cannot be scheduled in the past. | Code Reverse-Eng | Unit | `test_appointment_future_date` | Implemented |
| **REQ-04** | Doctor availability must be checked before booking. | README | Integration | `test_doctor_schedule_conflict` | Implemented |
| **REQ-05** | Patient intake form must sanitize malicious script inputs. | Security Policy | Unit / Sec | `test_sql_injection_sanitization` | Implemented |
| **REQ-06** | Prescribed dosage must be within allowable numeric range. | Code Reverse-Eng | Unit | `test_dosage_equivalence_partition` | Implemented |
| **REQ-07** | Duplicate patient records must be flagged on creation. | Issue Tracker | Integration | `test_duplicate_patient_detection` | Implemented |
| **REQ-08** | Appointment cancellation must free up the time slot. | README | BDD / Acceptance | `feature: cancel_appointment` | Implemented |
| **REQ-09** | Medical record notes must be encrypted at rest in DB. | Security Policy | Integration | `test_record_encryption_at_rest` | Implemented |
| **REQ-10** | System must log all failed authentication attempts. | Issue Tracker | Integration | `test_audit_log_failed_login` | Implemented |