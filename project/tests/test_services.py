"""Focused tests for Stage 6 service operations."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)



def test_find_patient_returns_registered_object() -> None:
    """A known ID returns the actual registered Patient object."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)
    patient = service.register_patient('P1', 'Alex Example')

    result = service.find_patient('P1')

    assert result is patient


def test_find_patient_trims_surrounding_whitespace() -> None:
    """Surrounding whitespace in a valid ID is ignored."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)
    patient = service.register_patient('P1', 'Alex Example')

    assert service.find_patient('  P1  ') is patient


def test_find_patient_unknown_id_raises_lookup_error() -> None:
    """A valid but unknown ID reports absence."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(LookupError):
        service.find_patient('P999')


def test_find_patient_blank_id_raises_value_error() -> None:
    """A blank ID is invalid."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(ValueError):
        service.find_patient('   ')


def test_find_patient_id_is_case_sensitive() -> None:
    """Patient IDs remain case-sensitive."""
    data_store = SmartCareDataStore()
    service = PatientService(data_store)
    patient = service.register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError):
        service.find_patient('p1')

    assert service.find_patient('P1') is patient



def test_find_practitioner_returns_registered_object() -> None:
    """A known ID returns the actual registered Practitioner object."""
    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)
    practitioner = service.register_practitioner(
        'D1',
        'Dr Taylor',
        'General Practice',
    )

    result = service.find_practitioner('D1')

    assert result is practitioner


def test_find_practitioner_trims_surrounding_whitespace() -> None:
    """Surrounding whitespace in a valid ID is ignored."""
    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)
    practitioner = service.register_practitioner(
        'D1',
        'Dr Taylor',
        'General Practice',
    )

    assert service.find_practitioner('  D1  ') is practitioner


def test_find_practitioner_unknown_id_raises_lookup_error() -> None:
    """A valid but unknown practitioner ID reports absence."""
    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)

    with pytest.raises(LookupError):
        service.find_practitioner('D999')


def test_find_practitioner_blank_id_raises_value_error() -> None:
    """A blank practitioner ID is invalid."""
    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)

    with pytest.raises(ValueError):
        service.find_practitioner('   ')


def test_find_practitioner_id_is_case_sensitive() -> None:
    """Practitioner IDs remain case-sensitive."""
    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)
    practitioner = service.register_practitioner(
        'D1',
        'Dr Taylor',
        'General Practice',
    )

    with pytest.raises(LookupError):
        service.find_practitioner('d1')

    assert service.find_practitioner('D1') is practitioner


def test_cancel_appointment_returns_same_object_and_retains_history() -> None:
    """Cancellation returns the same stored appointment and retains it."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1',
        'Dr Taylor',
        'General Practice',
    )
    service = AppointmentService(data_store)

    appointment = service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9, 0),
    )

    result = service.cancel_appointment('A1')

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]


def test_cancel_appointment_twice_raises_value_error_without_change() -> None:
    """A cancelled appointment cannot be cancelled again."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1',
        'Dr Taylor',
        'General Practice',
    )
    service = AppointmentService(data_store)

    appointment = service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9, 0),
    )

    service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert service.find_appointment('A1') is appointment


def test_cancel_unknown_appointment_raises_lookup_error() -> None:
    """A valid but unknown appointment ID reports absence."""
    data_store = SmartCareDataStore()
    service = AppointmentService(data_store)

    with pytest.raises(LookupError):
        service.cancel_appointment('A999')


def test_cancel_blank_appointment_id_raises_value_error() -> None:
    """A blank appointment ID is invalid."""
    data_store = SmartCareDataStore()
    service = AppointmentService(data_store)

    with pytest.raises(ValueError):
        service.cancel_appointment('   ')


def test_cancel_completed_appointment_raises_value_error_without_change() -> None:
    """A COMPLETED appointment cannot be cancelled."""
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient(
        'P1',
        'Alex Example',
    )
    practitioner = PractitionerService(data_store).register_practitioner(
        'D1',
        'Dr Taylor',
        'General Practice',
    )
    service = AppointmentService(data_store)

    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(appointment)

    with pytest.raises(ValueError):
        service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.COMPLETED
    assert service.find_appointment('A1') is appointment

def test_register_patient_stores_registered_object():
    store = SmartCareDataStore()
    service = PatientService(store)

    patient = service.register_patient("P1", "Test Patient")

    assert store.find_patient("P1") is patient


def test_duplicate_patient_id_is_rejected_without_overwrite():
    store = SmartCareDataStore()
    service = PatientService(store)

    original = service.register_patient("P1", "Original Patient")

    with pytest.raises(ValueError):
        service.register_patient("P1", "Replacement Patient")

    assert store.find_patient("P1") is original

def test_valid_booking_uses_registered_objects_and_is_stored():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient = patient_service.register_patient("P1", "Test Patient")
    practitioner = practitioner_service.register_practitioner(
        "DR1", "Dr Test", "General"
    )

    appointment = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.status == AppointmentStatus.SCHEDULED
    assert store.find_appointment("A1") is appointment


def test_booking_unknown_participant_is_rejected_without_storage():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Test Patient")

    with pytest.raises(LookupError):
        appointment_service.book_appointment(
            "A1",
            "P1",
            "DR999",
            datetime(2026, 10, 1, 9, 0),
        )

    assert store.find_appointment("A1") is None

def test_same_practitioner_exact_time_is_rejected():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Test Patient")
    practitioner_service.register_practitioner(
        "DR1", "Dr Test", "General"
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
            "P1",
            "DR1",
            date_time,
        )

    assert store.find_appointment("A1") is original
    assert store.find_appointment("A2") is None


def test_different_practitioner_same_time_is_allowed():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Test Patient")

    practitioner1 = practitioner_service.register_practitioner(
        "DR1", "Dr One", "General"
    )
    practitioner2 = practitioner_service.register_practitioner(
        "DR2", "Dr Two", "Cardiology"
    )

    date_time = datetime(2026, 10, 1, 9, 0)

    appointment1 = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        date_time,
    )

    appointment2 = appointment_service.book_appointment(
        "A2",
        "P1",
        "DR2",
        date_time,
    )

    assert store.find_appointment("A1") is appointment1
    assert store.find_appointment("A2") is appointment2
    assert appointment1.practitioner is practitioner1
    assert appointment2.practitioner is practitioner2

def test_cancel_scheduled_appointment_returns_same_cancelled_object():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Test Patient")
    practitioner_service.register_practitioner(
        "DR1", "Dr Test", "General"
    )

    appointment = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    result = appointment_service.cancel_appointment("A1")

    assert result is appointment
    assert appointment.status == AppointmentStatus.CANCELLED


def test_cancelled_appointment_remains_retrievable():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Test Patient")
    practitioner_service.register_practitioner(
        "DR1", "Dr Test", "General"
    )

    appointment = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    appointment_service.cancel_appointment("A1")

    retrieved = appointment_service.find_appointment("A1")

    assert retrieved is appointment
    assert retrieved.status == AppointmentStatus.CANCELLED
    assert appointment in store.list_appointments()

def test_cancelled_appointment_does_not_occupy_practitioner_slot():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Test Patient")
    practitioner_service.register_practitioner(
        "DR1", "Dr Test", "General"
    )

    date_time = datetime(2026, 10, 1, 9, 0)

    original = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        date_time,
    )

    appointment_service.cancel_appointment("A1")

    replacement = appointment_service.book_appointment(
        "A2",
        "P1",
        "DR1",
        date_time,
    )

    assert original.status == AppointmentStatus.CANCELLED
    assert store.find_appointment("A1") is original
    assert store.find_appointment("A2") is replacement
    assert replacement.status == AppointmentStatus.SCHEDULED


def test_list_practitioner_appointments_returns_all_statuses_by_default():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient(
        "P1",
        "Test Patient",
    )
    practitioner_service.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    first = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )
    second = appointment_service.book_appointment(
        "A2",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 10, 0),
    )

    appointment_service.cancel_appointment("A1")

    result = appointment_service.list_practitioner_appointments(
        "DR1",
    )

    assert result == [first, second]
    assert result[0] is first
    assert result[1] is second
    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED


def test_list_practitioner_appointments_filters_by_status():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient(
        "P1",
        "Test Patient",
    )
    practitioner_service.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    cancelled = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )
    scheduled = appointment_service.book_appointment(
        "A2",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 10, 0),
    )

    appointment_service.cancel_appointment("A1")

    result = appointment_service.list_practitioner_appointments(
        "DR1",
        AppointmentStatus.SCHEDULED,
    )

    assert result == [scheduled]
    assert result[0] is scheduled
    assert cancelled not in result


def test_list_practitioner_appointments_known_empty_returns_new_empty_list():
    store = SmartCareDataStore()
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    practitioner_service.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    first_result = appointment_service.list_practitioner_appointments(
        "DR1",
    )
    second_result = appointment_service.list_practitioner_appointments(
        "DR1",
    )

    assert first_result == []
    assert second_result == []
    assert first_result is not second_result


def test_list_practitioner_appointments_unknown_practitioner_raises_lookup_error():
    store = SmartCareDataStore()
    appointment_service = AppointmentService(store)

    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments(
            "DR999",
        )


def test_list_practitioner_appointments_blank_id_raises_value_error():
    store = SmartCareDataStore()
    appointment_service = AppointmentService(store)

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(
            "   ",
        )


def test_list_practitioner_appointments_invalid_status_raises_value_error():
    store = SmartCareDataStore()
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    practitioner_service.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(
            "DR1",
            "scheduled",
        )


def test_list_practitioner_appointments_accepts_trimmed_registered_id():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient(
        "P1",
        "Test Patient",
    )
    practitioner_service.register_practitioner(
        "DR1",
        "Dr Test",
        "General",
    )

    appointment = appointment_service.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    result = appointment_service.list_practitioner_appointments(
        "  DR1  ",
    )

    assert result == [appointment]
    assert result[0] is appointment