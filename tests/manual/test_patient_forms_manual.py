import pytest
from patient.forms import PatientRegistrationForm


@pytest.mark.parametrize("field, rows", [
    ("medical_conditions", 2),
    ("address", 3),
    ("allergies", 2),
    ("chronic_diseases", 2),
])
def test_textarea_widgets_have_expected_rows(field, rows):
    form = PatientRegistrationForm()
    assert form.fields[field].widget.attrs["rows"] == rows


# --- save() behaviour (kills the commit=True -> commit=False mutant) ---------
from patient.models import Patient


def _valid_data():
    """Complete, fully synthetic registration payload (no real PII)."""
    return {
        "first_name": "Testa",
        "last_name": "Patientson",
        "gender": "F",
        "date_of_birth": "1990-05-20",
        "blood_group": "O+",
        "email": "patient.manual@example.com",
        "phone": "0000000001",
        "address": "1 Synthetic Street, Testville",
        "emergency_contact_name": "Contact Tester",
        "emergency_contact_phone": "0000000002",
        "emergency_contact_relation": "Sibling",
        "allergies": "Synthetic allergen",
        "chronic_diseases": "",
        "medical_conditions": "Synthetic condition",
    }


@pytest.mark.django_db
def test_save_default_persists_patient():
    form = PatientRegistrationForm(data=_valid_data())
    assert form.is_valid(), form.errors
    patient = form.save()  # default must be commit=True
    assert patient.pk is not None
    assert Patient.objects.filter(pk=patient.pk).exists()


@pytest.mark.django_db
def test_save_commit_false_does_not_persist():
    form = PatientRegistrationForm(data=_valid_data())
    assert form.is_valid(), form.errors
    patient = form.save(commit=False)
    assert patient.pk is None
    assert Patient.objects.count() == 0


@pytest.mark.django_db
def test_medical_conditions_copied_to_chronic_diseases():
    form = PatientRegistrationForm(data=_valid_data())
    assert form.is_valid(), form.errors
    patient = form.save()
    patient.refresh_from_db()
    assert patient.chronic_diseases == "Synthetic condition"
