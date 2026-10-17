"""
AI-generated pytest-django unit tests for the patient app.

Scope:
    1. PatientRegistrationForm and PatientSearchForm (patient/forms/patients.py)
    2. Patient.age, Patient.full_name and patient_id generation in Patient.save()
    3. extract_common_keywords (patient/services.py)

All data is synthetic.
"""

import re
from datetime import UTC, date, datetime
from io import BytesIO
from unittest import mock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.utils import timezone

from patient.forms.patients import PatientRegistrationForm, PatientSearchForm
from patient.models import Patient
from patient.services import extract_common_keywords

REQUIRED_MSG = "This field is required."

REQUIRED_FIELDS = [
    "first_name",
    "last_name",
    "gender",
    "date_of_birth",
    "phone",
    "address",
    "emergency_contact_name",
    "emergency_contact_phone",
    "emergency_contact_relation",
]


# --------------------------------------------------------------------------
# Helpers and fixtures
# --------------------------------------------------------------------------
@pytest.fixture
def valid_data():
    """A complete, valid, fully synthetic registration payload."""
    return {
        "first_name": "Testa",
        "last_name": "Patientson",
        "gender": "F",
        "date_of_birth": "1990-05-20",
        "blood_group": "O+",
        "email": "patient.test@example.com",
        "phone": "0000000001",
        "address": "1 Synthetic Street, Testville",
        "emergency_contact_name": "Contact Tester",
        "emergency_contact_phone": "0000000002",
        "emergency_contact_relation": "Sibling",
        "allergies": "Synthetic allergen",
        "chronic_diseases": "",
        "medical_conditions": "Synthetic condition",
    }


def make_patient(**overrides):
    """Create and save a Patient with synthetic data (requires the DB)."""
    data = {
        "first_name": "Testa",
        "last_name": "Patientson",
        "gender": "F",
        "date_of_birth": date(1990, 5, 20),
        "phone": "0000000001",
        "address": "1 Synthetic Street, Testville",
        "emergency_contact_name": "Contact Tester",
        "emergency_contact_phone": "0000000002",
        "emergency_contact_relation": "Sibling",
    }
    data.update(overrides)
    return Patient.objects.create(**data)


def freeze_now(monkeypatch, year, month, day):
    """Patch django.utils.timezone.now to a fixed aware datetime."""
    fixed = datetime(year, month, day, 12, 0, 0, tzinfo=UTC)
    monkeypatch.setattr(timezone, "now", lambda: fixed)
    return fixed


def make_png_upload(name="synthetic.png"):
    from PIL import Image

    buf = BytesIO()
    Image.new("RGB", (1, 1), color=(255, 255, 255)).save(buf, format="PNG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/png")


# --------------------------------------------------------------------------
# 1a. PatientRegistrationForm: valid input
# --------------------------------------------------------------------------
def test_registration_form_valid_with_all_fields(valid_data):
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    assert form.errors == {}
    assert form.cleaned_data["first_name"] == "Testa"
    assert form.cleaned_data["last_name"] == "Patientson"
    assert form.cleaned_data["gender"] == "F"
    assert form.cleaned_data["date_of_birth"] == date(1990, 5, 20)
    assert form.cleaned_data["blood_group"] == "O+"
    assert form.cleaned_data["email"] == "patient.test@example.com"


def test_registration_form_valid_with_only_required_fields(valid_data):
    data = {k: valid_data[k] for k in REQUIRED_FIELDS}
    form = PatientRegistrationForm(data=data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["blood_group"] == ""
    assert form.cleaned_data["email"] == ""
    assert form.cleaned_data["allergies"] == ""
    assert form.cleaned_data["medical_conditions"] == ""
    assert form.cleaned_data["profile_picture"] is None


@pytest.mark.parametrize("gender", ["M", "F", "O"])
def test_registration_form_accepts_every_gender_choice(valid_data, gender):
    valid_data["gender"] = gender
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["gender"] == gender


@pytest.mark.parametrize(
    "blood_group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
)
def test_registration_form_accepts_every_blood_group(valid_data, blood_group):
    valid_data["blood_group"] = blood_group
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["blood_group"] == blood_group


def test_registration_form_accepts_valid_profile_picture(valid_data):
    form = PatientRegistrationForm(
        data=valid_data, files={"profile_picture": make_png_upload()}
    )
    assert form.is_valid(), form.errors
    assert form.cleaned_data["profile_picture"].name == "synthetic.png"


def test_registration_form_excludes_system_fields_and_adds_extra_fields():
    form = PatientRegistrationForm()
    assert "patient_id" not in form.fields
    assert "registration_date" not in form.fields
    assert "last_updated" not in form.fields
    assert "medical_conditions" in form.fields
    assert "profile_picture" in form.fields
    assert form.fields["date_of_birth"].widget.input_type == "date"


def test_registration_form_ignores_user_supplied_patient_id(valid_data):
    valid_data["patient_id"] = "P-FAKE-0001"
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    instance = form.save(commit=False)
    assert instance.patient_id is None


def test_registration_form_accepts_future_date_of_birth(valid_data):
    # Documents current behaviour: the form has no "not in the future" rule.
    valid_data["date_of_birth"] = "2999-01-01"
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["date_of_birth"] == date(2999, 1, 1)


# --------------------------------------------------------------------------
# 1b. PatientRegistrationForm: missing required fields
# --------------------------------------------------------------------------
@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_registration_form_missing_required_field(valid_data, field):
    del valid_data[field]
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors[field] == [REQUIRED_MSG]
    assert set(form.errors.keys()) == {field}


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_registration_form_blank_required_field(valid_data, field):
    valid_data[field] = ""
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors[field] == [REQUIRED_MSG]


def test_registration_form_whitespace_only_name_is_rejected(valid_data):
    valid_data["first_name"] = "     "
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors["first_name"] == [REQUIRED_MSG]


def test_registration_form_empty_data_reports_all_required_fields():
    form = PatientRegistrationForm(data={})
    assert not form.is_valid()
    assert set(form.errors.keys()) == set(REQUIRED_FIELDS)
    for field in REQUIRED_FIELDS:
        assert form.errors[field] == [REQUIRED_MSG]


# --------------------------------------------------------------------------
# 1c. PatientRegistrationForm: invalid input
# --------------------------------------------------------------------------
def test_registration_form_invalid_email(valid_data):
    valid_data["email"] = "not-an-email"
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors["email"] == ["Enter a valid email address."]


@pytest.mark.parametrize("bad_date", ["not-a-date", "2000-02-30", "2000-13-01"])
def test_registration_form_invalid_date_of_birth(valid_data, bad_date):
    valid_data["date_of_birth"] = bad_date
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors["date_of_birth"] == ["Enter a valid date."]


def test_registration_form_invalid_gender_choice(valid_data):
    valid_data["gender"] = "X"
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors["gender"] == [
        "Select a valid choice. X is not one of the available choices."
    ]


def test_registration_form_invalid_blood_group_choice(valid_data):
    valid_data["blood_group"] = "C+"
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors["blood_group"] == [
        "Select a valid choice. C+ is not one of the available choices."
    ]


def test_registration_form_non_image_profile_picture_rejected(valid_data):
    bad_file = SimpleUploadedFile(
        "notes.txt", b"this is not an image", content_type="text/plain"
    )
    form = PatientRegistrationForm(data=valid_data, files={"profile_picture": bad_file})
    assert not form.is_valid()
    assert form.errors["profile_picture"] == [
        "Upload a valid image. The file you uploaded was either not an image "
        "or a corrupted image."
    ]


# --------------------------------------------------------------------------
# 1d. PatientRegistrationForm: boundary values (max_length)
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "field, max_len",
    [
        ("first_name", 50),
        ("last_name", 50),
        ("phone", 15),
        ("emergency_contact_name", 100),
        ("emergency_contact_phone", 15),
        ("emergency_contact_relation", 50),
    ],
)
def test_registration_form_accepts_value_at_max_length(valid_data, field, max_len):
    valid_data[field] = "a" * max_len
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data[field] == "a" * max_len


@pytest.mark.parametrize(
    "field, max_len",
    [
        ("first_name", 50),
        ("last_name", 50),
        ("phone", 15),
        ("emergency_contact_name", 100),
        ("emergency_contact_phone", 15),
        ("emergency_contact_relation", 50),
    ],
)
def test_registration_form_rejects_value_over_max_length(valid_data, field, max_len):
    valid_data[field] = "a" * (max_len + 1)
    form = PatientRegistrationForm(data=valid_data)
    assert not form.is_valid()
    assert form.errors[field] == [
        f"Ensure this value has at most {max_len} characters (it has {max_len + 1})."
    ]


def test_registration_form_accepts_single_character_name(valid_data):
    valid_data["first_name"] = "A"
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["first_name"] == "A"


# --------------------------------------------------------------------------
# 1e. PatientRegistrationForm.save(): medical_conditions -> chronic_diseases
# --------------------------------------------------------------------------
def test_registration_form_save_commit_false_maps_medical_conditions(valid_data):
    valid_data["medical_conditions"] = "Synthetic condition B"
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    instance = form.save(commit=False)
    assert isinstance(instance, Patient)
    assert instance.pk is None
    assert instance.chronic_diseases == "Synthetic condition B"
    assert instance.first_name == "Testa"


def test_registration_form_save_overwrites_chronic_diseases_with_medical_conditions(
    valid_data,
):
    # Documents current behaviour: medical_conditions always wins, even when
    # it is empty and chronic_diseases was supplied.
    valid_data["chronic_diseases"] = "Synthetic condition A"
    valid_data["medical_conditions"] = ""
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    instance = form.save(commit=False)
    assert instance.chronic_diseases == ""


@pytest.mark.django_db
def test_registration_form_save_commit_true_persists_patient(valid_data, monkeypatch):
    freeze_now(monkeypatch, 2031, 3, 10)
    valid_data["medical_conditions"] = "Synthetic condition C"
    form = PatientRegistrationForm(data=valid_data)
    assert form.is_valid(), form.errors
    instance = form.save(commit=True)
    assert instance.pk is not None
    assert instance.patient_id == "P-2031-0001"
    stored = Patient.objects.get(pk=instance.pk)
    assert stored.chronic_diseases == "Synthetic condition C"
    assert stored.full_name == "Testa Patientson"


# --------------------------------------------------------------------------
# 1f. PatientSearchForm
# --------------------------------------------------------------------------
def test_search_form_valid_with_query():
    form = PatientSearchForm(data={"query": "Patientson"})
    assert form.is_valid(), form.errors
    assert form.cleaned_data == {"query": "Patientson"}


def test_search_form_valid_with_empty_data():
    form = PatientSearchForm(data={})
    assert form.is_valid(), form.errors
    assert form.cleaned_data == {"query": ""}


def test_search_form_valid_with_blank_query():
    form = PatientSearchForm(data={"query": ""})
    assert form.is_valid(), form.errors
    assert form.cleaned_data["query"] == ""


def test_search_form_whitespace_only_query_is_stripped_to_empty():
    form = PatientSearchForm(data={"query": "     "})
    assert form.is_valid(), form.errors
    assert form.cleaned_data["query"] == ""


def test_search_form_strips_surrounding_whitespace():
    form = PatientSearchForm(data={"query": "  Testa  "})
    assert form.is_valid(), form.errors
    assert form.cleaned_data["query"] == "Testa"


def test_search_form_preserves_patient_id_style_query():
    form = PatientSearchForm(data={"query": "P-2026-0001"})
    assert form.is_valid(), form.errors
    assert form.cleaned_data["query"] == "P-2026-0001"


def test_search_form_has_no_max_length_limit():
    long_query = "a" * 1000
    form = PatientSearchForm(data={"query": long_query})
    assert form.is_valid(), form.errors
    assert len(form.cleaned_data["query"]) == 1000


def test_search_form_field_configuration():
    form = PatientSearchForm()
    field = form.fields["query"]
    assert field.required is False
    assert field.label == "Search Patients"
    assert field.widget.attrs["placeholder"] == "Search by name, ID, or phone number"
    assert field.widget.attrs["class"] == "form-control"


def test_search_form_unbound_is_not_valid():
    form = PatientSearchForm()
    assert form.is_bound is False
    assert form.is_valid() is False


# --------------------------------------------------------------------------
# 2a. Patient.age
# --------------------------------------------------------------------------
def test_patient_age_before_birthday_this_year(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2000, 6, 16))
    assert patient.age == 25


def test_patient_age_on_birthday(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2000, 6, 15))
    assert patient.age == 26


def test_patient_age_day_after_birthday(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2000, 6, 14))
    assert patient.age == 26


def test_patient_age_earlier_month_birthday_already_passed(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(1990, 1, 31))
    assert patient.age == 36


def test_patient_age_later_month_birthday_not_yet_reached(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(1990, 12, 1))
    assert patient.age == 35


def test_patient_age_born_today_is_zero(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2026, 6, 15))
    assert patient.age == 0


def test_patient_age_under_one_year(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2025, 6, 16))
    assert patient.age == 0


def test_patient_age_exactly_one_year(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2025, 6, 15))
    assert patient.age == 1


def test_patient_age_leap_day_birthday_before_march_first(monkeypatch):
    freeze_now(monkeypatch, 2026, 2, 28)
    patient = Patient(date_of_birth=date(2000, 2, 29))
    assert patient.age == 25


def test_patient_age_leap_day_birthday_on_march_first(monkeypatch):
    freeze_now(monkeypatch, 2026, 3, 1)
    patient = Patient(date_of_birth=date(2000, 2, 29))
    assert patient.age == 26


def test_patient_age_year_boundary_new_years_day(monkeypatch):
    freeze_now(monkeypatch, 2026, 1, 1)
    patient = Patient(date_of_birth=date(2000, 12, 31))
    assert patient.age == 25


def test_patient_age_future_date_of_birth_is_negative(monkeypatch):
    # Documents current behaviour: no guard against future dates of birth.
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = Patient(date_of_birth=date(2026, 6, 16))
    assert patient.age == -1


def test_patient_age_without_date_of_birth_raises_attribute_error():
    patient = Patient()
    with pytest.raises(AttributeError):
        patient.age


# --------------------------------------------------------------------------
# 2b. Patient.full_name
# --------------------------------------------------------------------------
def test_patient_full_name_combines_first_and_last_name():
    patient = Patient(first_name="Testa", last_name="Patientson")
    assert patient.full_name == "Testa Patientson"


def test_patient_full_name_preserves_internal_characters():
    patient = Patient(first_name="Mary-Jane", last_name="O'Testerson")
    assert patient.full_name == "Mary-Jane O'Testerson"


def test_patient_full_name_with_empty_last_name_keeps_separator():
    patient = Patient(first_name="Testa", last_name="")
    assert patient.full_name == "Testa "


def test_patient_full_name_with_both_names_empty_is_single_space():
    patient = Patient(first_name="", last_name="")
    assert patient.full_name == " "


def test_patient_full_name_at_max_length_names():
    patient = Patient(first_name="a" * 50, last_name="b" * 50)
    assert patient.full_name == ("a" * 50) + " " + ("b" * 50)
    assert len(patient.full_name) == 101


# --------------------------------------------------------------------------
# 2c. Patient.save(): patient_id generation
# --------------------------------------------------------------------------
@pytest.mark.django_db
def test_first_patient_gets_id_ending_0001(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = make_patient()
    assert patient.patient_id == "P-2026-0001"


@pytest.mark.django_db
def test_patient_ids_increment_sequentially(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    ids = [make_patient().patient_id for _ in range(3)]
    assert ids == ["P-2026-0001", "P-2026-0002", "P-2026-0003"]


@pytest.mark.django_db
def test_patient_id_uses_current_year(monkeypatch):
    freeze_now(monkeypatch, 2031, 1, 1)
    patient = make_patient()
    assert patient.patient_id == "P-2031-0001"


@pytest.mark.django_db
def test_patient_id_matches_expected_format(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = make_patient()
    assert re.fullmatch(r"P-\d{4}-\d{4}", patient.patient_id)


@pytest.mark.django_db
def test_patient_id_zero_padding_boundary_9_to_10(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patients = [make_patient() for _ in range(10)]
    assert patients[8].patient_id == "P-2026-0009"
    assert patients[9].patient_id == "P-2026-0010"


@pytest.mark.django_db
def test_patient_id_grows_beyond_four_digits(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    with mock.patch.object(Patient.objects, "count", return_value=9999):
        patient = make_patient()
    assert patient.patient_id == "P-2026-10000"


@pytest.mark.django_db
def test_explicit_patient_id_is_not_overwritten(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = make_patient(patient_id="P-CUSTOM1")
    assert patient.patient_id == "P-CUSTOM1"
    assert Patient.objects.get(pk=patient.pk).patient_id == "P-CUSTOM1"


@pytest.mark.django_db
def test_resaving_existing_patient_keeps_patient_id(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = make_patient()
    original_id = patient.patient_id
    patient.first_name = "Updated"
    patient.save()
    patient.refresh_from_db()
    assert patient.patient_id == original_id == "P-2026-0001"
    assert patient.first_name == "Updated"


@pytest.mark.django_db
def test_patient_id_is_unique_across_patients(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    a = make_patient()
    b = make_patient(first_name="Other")
    assert a.patient_id != b.patient_id
    assert Patient.objects.filter(patient_id="P-2026-0001").count() == 1


@pytest.mark.django_db
def test_patient_id_collision_after_deletion_raises_integrity_error(monkeypatch):
    # Documents current behaviour: the ID is count()+1, so deleting an earlier
    # patient makes the next generated ID collide with an existing one.
    freeze_now(monkeypatch, 2026, 6, 15)
    first = make_patient()
    second = make_patient(first_name="Other")
    assert second.patient_id == "P-2026-0002"
    first.delete()
    with pytest.raises(IntegrityError), transaction.atomic():
        make_patient(first_name="Third")


@pytest.mark.django_db
def test_str_includes_generated_patient_id(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = make_patient()
    assert str(patient) == "Testa Patientson (P-2026-0001)"


@pytest.mark.django_db
@pytest.mark.xfail(
    reason="Generated ID 'P-YYYY-NNNN' is 11 chars but patient_id max_length is 10; "
    "SQLite does not enforce it, stricter backends would.",
    strict=False,
)
def test_generated_patient_id_fits_within_field_max_length(monkeypatch):
    freeze_now(monkeypatch, 2026, 6, 15)
    patient = make_patient()
    max_length = Patient._meta.get_field("patient_id").max_length
    assert len(patient.patient_id) <= max_length


# --------------------------------------------------------------------------
# 3. extract_common_keywords
# --------------------------------------------------------------------------
def test_extract_keywords_empty_list_returns_empty_list():
    assert extract_common_keywords([]) == []


def test_extract_keywords_empty_string_diagnosis_returns_empty_list():
    assert extract_common_keywords([""]) == []


def test_extract_keywords_counts_and_orders_by_frequency():
    diagnoses = ["Fever and cough", "cough with fever", "Severe cough"]
    assert extract_common_keywords(diagnoses) == [
        ("cough", 3),
        ("fever", 2),
        ("severe", 1),
    ]


def test_extract_keywords_is_case_insensitive():
    assert extract_common_keywords(["FEVER", "Fever", "fever"]) == [("fever", 3)]


def test_extract_keywords_removes_all_stopwords():
    text = "the and or a an of to with in on for"
    assert extract_common_keywords([text]) == []


def test_extract_keywords_removes_stopwords_but_keeps_other_words():
    result = extract_common_keywords(["pain in the chest and back"])
    assert result == [("pain", 1), ("chest", 1), ("back", 1)]


def test_extract_keywords_word_length_boundary():
    # Length 2 is excluded, length 3 is included.
    assert extract_common_keywords(["flu hi"]) == [("flu", 1)]


def test_extract_keywords_single_character_tokens_excluded():
    result = extract_common_keywords(["type 2 diabetes"])
    assert result == [("type", 1), ("diabetes", 1)]


def test_extract_keywords_splits_on_punctuation():
    result = extract_common_keywords(["fever, cough; fever."])
    assert result == [("fever", 2), ("cough", 1)]


def test_extract_keywords_splits_hyphenated_words():
    result = extract_common_keywords(["non-specific pain"])
    assert result == [("non", 1), ("specific", 1), ("pain", 1)]


def test_extract_keywords_keeps_alphanumeric_tokens_whole():
    assert extract_common_keywords(["covid19 covid19"]) == [("covid19", 2)]


def test_extract_keywords_counts_across_multiple_diagnoses():
    diagnoses = ["acute bronchitis", "chronic bronchitis", "acute sinusitis"]
    assert extract_common_keywords(diagnoses) == [
        ("acute", 2),
        ("bronchitis", 2),
        ("chronic", 1),
        ("sinusitis", 1),
    ]


def test_extract_keywords_limit_truncates_results():
    result = extract_common_keywords(["alpha alpha alpha beta beta gamma"], limit=2)
    assert result == [("alpha", 3), ("beta", 2)]


def test_extract_keywords_limit_of_one():
    result = extract_common_keywords(["alpha alpha beta"], limit=1)
    assert result == [("alpha", 2)]


def test_extract_keywords_limit_zero_returns_empty_list():
    assert extract_common_keywords(["alpha beta"], limit=0) == []


def test_extract_keywords_limit_larger_than_distinct_words():
    result = extract_common_keywords(["alpha beta"], limit=50)
    assert result == [("alpha", 1), ("beta", 1)]


def test_extract_keywords_default_limit_is_ten():
    words = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima"
    result = extract_common_keywords([words])
    assert len(result) == 10
    assert result == [
        (w, 1)
        for w in [
            "alpha",
            "bravo",
            "charlie",
            "delta",
            "echo",
            "foxtrot",
            "golf",
            "hotel",
            "india",
            "juliet",
        ]
    ]


def test_extract_keywords_whitespace_only_diagnosis_returns_empty_list():
    assert extract_common_keywords(["   \t  "]) == []


def test_extract_keywords_non_string_diagnosis_raises_attribute_error():
    with pytest.raises(AttributeError):
        extract_common_keywords([None])
