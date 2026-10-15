import pytest

def validate_patient_age(age: int) -> bool:
    """Validates that patient age falls within realistic medical bounds (0 to 120)."""
    return 0 <= age <= 120

@pytest.mark.parametrize("age,expected", [
    (-1, False),  # Below lower bound
    (0, True),    # Exact lower bound
    (25, True),   # Mid-range valid
    (120, True),  # Exact upper bound
    (121, False), # Above upper bound
])
def test_patient_age_boundaries(age, expected):
    assert validate_patient_age(age) == expected