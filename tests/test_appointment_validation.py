import datetime

import pytest
from django.core.exceptions import ValidationError

from appointment.models import Appointment
from patient.models import Patient
from users.models import User


@pytest.fixture
def doctor(db):
    return User.objects.create_user(
        username="synthetic_doctor_1",
        password="test-only-password",
        first_name="Test",
        last_name="Doctor",
        role=User.DOCTOR,
    )


@pytest.fixture
def another_doctor(db):
    return User.objects.create_user(
        username="synthetic_doctor_2",
        password="test-only-password",
        first_name="Another",
        last_name="Doctor",
        role=User.DOCTOR,
    )


@pytest.fixture
def patient(db):
    return Patient.objects.create(
        first_name="Test",
        last_name="Patient",
        gender="F",
        date_of_birth=datetime.date(1990, 5, 20),
        phone="0000000001",
        address="1 Synthetic Street",
        emergency_contact_name="Test Contact",
        emergency_contact_phone="0000000002",
        emergency_contact_relation="Sibling",
    )


@pytest.fixture
def another_patient(db):
    return Patient.objects.create(
        first_name="Another",
        last_name="Patient",
        gender="M",
        date_of_birth=datetime.date(1985, 3, 10),
        phone="0000000003",
        address="2 Synthetic Street",
        emergency_contact_name="Another Contact",
        emergency_contact_phone="0000000004",
        emergency_contact_relation="Sibling",
    )


def make_appointment(patient, doctor, start="09:00", end="09:30"):
    return Appointment(
        patient=patient,
        doctor=doctor,
        created_by=doctor,
        date=datetime.date(2030, 6, 10),
        start_time=datetime.time.fromisoformat(start),
        end_time=datetime.time.fromisoformat(end),
        appointment_type=Appointment.REGULAR,
        reason="Synthetic test appointment",
    )


@pytest.mark.django_db
def test_valid_appointment_can_be_saved(patient, doctor):
    appointment = make_appointment(patient, doctor)

    appointment.save()

    assert appointment.pk is not None
    assert Appointment.objects.filter(pk=appointment.pk).exists()


@pytest.mark.django_db
def test_overlapping_appointment_for_doctor_is_rejected(
    patient, another_patient, doctor
):
    make_appointment(patient, doctor).save()

    conflicting = make_appointment(
        another_patient, doctor, start="09:15", end="09:45"
    )

    with pytest.raises(ValidationError, match="Doctor already has an appointment"):
        conflicting.save()


@pytest.mark.django_db
def test_overlapping_appointment_for_patient_is_rejected(
    patient, doctor, another_doctor
):
    make_appointment(patient, doctor).save()

    conflicting = make_appointment(
        patient, another_doctor, start="09:15", end="09:45"
    )

    with pytest.raises(ValidationError, match="Patient already has an appointment"):
        conflicting.save()


@pytest.mark.django_db
def test_cancelled_appointment_no_longer_blocks_time_slot(
    patient, another_patient, doctor
):
    original = make_appointment(patient, doctor)
    original.save()

    original.status = Appointment.CANCELLED
    original.save()

    replacement = make_appointment(another_patient, doctor)
    replacement.save()

    assert replacement.pk is not None
    assert replacement.status == Appointment.SCHEDULED
