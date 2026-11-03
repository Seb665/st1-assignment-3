from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_f8_01_same_practitioner_exact_time_conflict_is_rejected():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Patient One")
    patient_service.register_patient("P2", "Patient Two")
    practitioner_service.register_practitioner(
        "DR1",
        "Dr One",
        "General",
    )

    date_time = datetime(2026, 10, 1, 9, 0)

    original = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        date_time,
    )

    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            "A2",
            "P2",
            "DR1",
            date_time,
        )

    assert store.find_appointment("A1") is original
    assert store.find_appointment("A2") is None


def test_f8_02_cancelled_appointment_remains_retrievable():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Patient One")
    practitioner_service.register_practitioner(
        "DR1",
        "Dr One",
        "General",
    )

    appointment = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    result = appointment_service.cancel_appointment("A1")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.find_appointment("A1") is appointment
    assert appointment_service.find_appointment("A1") is appointment
    assert appointment in store.list_appointments()

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED