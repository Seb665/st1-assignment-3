from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_full_service_workflow_preserves_history_and_frees_slot():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patient = patients.register_patient(
        "P1",
        "Test Patient",
    )
    practitioner_one = practitioners.register_practitioner(
        "DR1",
        "Dr One",
        "General",
    )
    practitioner_two = practitioners.register_practitioner(
        "DR2",
        "Dr Two",
        "Cardiology",
    )

    assert patients.find_patient("P1") is patient
    assert practitioners.find_practitioner("DR1") is practitioner_one
    assert practitioners.find_practitioner("DR2") is practitioner_two

    date_time = datetime(2026, 10, 1, 9, 0)

    first = appointments.book_appointment(
        "A1",
        "P1",
        "DR1",
        date_time,
    )

    with pytest.raises(ValueError):
        appointments.book_appointment(
            "A_CONFLICT",
            "P1",
            "DR1",
            date_time,
        )

    assert store.find_appointment("A_CONFLICT") is None

    second = appointments.book_appointment(
        "A2",
        "P1",
        "DR2",
        date_time,
    )

    cancelled = appointments.cancel_appointment("A1")

    assert cancelled is first
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert appointments.find_appointment("A1") is first

    all_for_dr1 = appointments.list_practitioner_appointments("DR1")

    assert all_for_dr1 == [first]
    assert all_for_dr1[0] is first

    scheduled_for_dr1 = appointments.list_practitioner_appointments(
        "DR1",
        AppointmentStatus.SCHEDULED,
    )

    assert scheduled_for_dr1 == []

    replacement = appointments.book_appointment(
        "A3",
        "P1",
        "DR1",
        date_time,
    )

    assert replacement.status is AppointmentStatus.SCHEDULED
    assert appointments.find_appointment("A3") is replacement
    assert appointments.find_appointment("A1") is first
    assert second.practitioner is practitioner_two

    final_for_dr1 = appointments.list_practitioner_appointments("DR1")

    assert final_for_dr1 == [first, replacement]


def test_rejected_operations_leave_state_unchanged():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patient = patients.register_patient(
        "P1",
        "Test Patient",
    )
    practitioner = practitioners.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    before_patients = store.list_patients()
    before_practitioners = store.list_practitioners()
    before_appointments = store.list_appointments()

    with pytest.raises(ValueError):
        patients.register_patient(
            "P1",
            "Replacement Patient",
        )

    with pytest.raises(LookupError):
        appointments.book_appointment(
            "A_BAD",
            "UNKNOWN",
            "DR1",
            datetime(2026, 10, 1, 9, 0),
        )

    assert store.list_patients() == before_patients
    assert store.list_practitioners() == before_practitioners
    assert store.list_appointments() == before_appointments
    assert patients.find_patient("P1") is patient
    assert practitioners.find_practitioner("DR1") is practitioner
    assert store.find_appointment("A_BAD") is None


def test_repeated_cancellation_preserves_cancelled_state():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patients.register_patient(
        "P1",
        "Test Patient",
    )
    practitioners.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    appointment = appointments.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    appointments.cancel_appointment("A1")

    with pytest.raises(ValueError):
        appointments.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointments.find_appointment("A1") is appointment