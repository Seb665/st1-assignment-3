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
