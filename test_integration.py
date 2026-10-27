import pytest
from patient.models import Patient


@pytest.mark.django_db
def test_patient_database_persistence():
    """Verify a synthetic patient record persists and can be retrieved."""
    patient = Patient.objects.create(
        first_name="Testa",
        last_name="Patientson",
        gender="F",
        date_of_birth="1990-05-20",
        phone="0000000001",
        address="1 Synthetic Street, Testville",
        emergency_contact_name="Contact Tester",
        emergency_contact_phone="0000000002",
        emergency_contact_relation="Sibling",
    )

    assert patient.pk is not None

    saved_patient = Patient.objects.get(pk=patient.pk)
    assert saved_patient.first_name == "Testa"
    assert saved_patient.last_name == "Patientson"
    assert saved_patient.patient_id
