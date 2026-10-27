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
