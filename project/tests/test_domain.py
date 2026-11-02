import pytest
from datetime import datetime

from smartcare.domain import (
    Patient,
    Practitioner,
    Appointment,
    AppointmentStatus,
)


def test_patient_rejects_blank_id():
    with pytest.raises(ValueError):
        Patient("   ", "Test Patient")


def test_practitioner_rejects_blank_specialty():
    with pytest.raises(ValueError):
        Practitioner("DR1", "Dr Test", "   ")

def test_repeated_cancellation_is_rejected_without_state_change():
    patient = Patient("P1", "Test Patient")
    practitioner = Practitioner("DR1", "Dr Test", "General")
    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
    )

    appointment.cancel()

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled():
    patient = Patient("P1", "Test Patient")
    practitioner = Practitioner("DR1", "Dr Test", "General")
    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        status=AppointmentStatus.COMPLETED,
    )

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status == AppointmentStatus.COMPLETED

def test_valid_patient_construction():
    patient = Patient("P1", "Test Patient")

    assert patient.patient_id == "P1"
    assert patient.name == "Test Patient"


def test_valid_practitioner_construction():
    practitioner = Practitioner("DR1", "Dr Test", "General")

    assert practitioner.practitioner_id == "DR1"
    assert practitioner.name == "Dr Test"
    assert practitioner.specialty == "General"


def test_new_appointment_starts_scheduled():
    patient = Patient("P1", "Test Patient")
    practitioner = Practitioner("DR1", "Dr Test", "General")

    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
    )

    assert appointment.status == AppointmentStatus.SCHEDULED


def test_scheduled_appointment_cancel_changes_status():
    patient = Patient("P1", "Test Patient")
    practitioner = Practitioner("DR1", "Dr Test", "General")

    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
    )

    appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED
