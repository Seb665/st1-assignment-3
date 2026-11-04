from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


def build_query_data():
    """Create reusable synthetic appointments for Stage 9 query tests."""
    patient = Patient("P1", "Test Patient")
    practitioner_one = Practitioner("DR1", "Dr One", "General")
    practitioner_two = Practitioner("DR2", "Dr Two", "Cardiology")

    late_scheduled = Appointment(
        "A3",
        patient,
        practitioner_one,
        datetime(2026, 10, 1, 10, 0),
        AppointmentStatus.SCHEDULED,
    )

    completed = Appointment(
        "A2",
        patient,
        practitioner_one,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )

    cancelled = Appointment(
        "A1",
        patient,
        practitioner_one,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.CANCELLED,
    )

    other_practitioner = Appointment(
        "B1",
        patient,
        practitioner_two,
        datetime(2026, 10, 1, 8, 0),
        AppointmentStatus.SCHEDULED,
    )

    source = [
        late_scheduled,
        other_practitioner,
        completed,
        cancelled,
    ]

    return (
        source,
        cancelled,
        completed,
        late_scheduled,
        other_practitioner,
    )


def test_appointment_sort_key_uses_datetime_then_id():
    source, cancelled, _, _, _ = build_query_data()

    key = appointment_sort_key(cancelled)

    assert key == (cancelled.date_time, cancelled.appointment_id)
    assert source[3] is cancelled


def test_select_appointments_filters_practitioner_and_orders_results():
    source, cancelled, completed, late_scheduled, _ = build_query_data()
    original_order = list(source)

    result = select_appointments(source, "DR1")

    assert [appointment.appointment_id for appointment in result] == [
        "A1",
        "A2",
        "A3",
    ]
    assert result[0] is cancelled
    assert result[1] is completed
    assert result[2] is late_scheduled
    assert source == original_order


def test_select_appointments_supports_default_and_explicit_status_filters():
    source, _, _, _, _ = build_query_data()

    all_statuses = select_appointments(source, "DR1")
    scheduled = select_appointments(
        source,
        "DR1",
        AppointmentStatus.SCHEDULED,
    )
    cancelled = select_appointments(
        source,
        "DR1",
        AppointmentStatus.CANCELLED,
    )
    completed = select_appointments(
        source,
        "DR1",
        AppointmentStatus.COMPLETED,
    )
    no_match = select_appointments(
        source,
        "DR2",
        AppointmentStatus.CANCELLED,
    )

    assert [appointment.appointment_id for appointment in all_statuses] == [
        "A1",
        "A2",
        "A3",
    ]
    assert [appointment.appointment_id for appointment in scheduled] == ["A3"]
    assert [appointment.appointment_id for appointment in cancelled] == ["A1"]
    assert [appointment.appointment_id for appointment in completed] == ["A2"]
    assert no_match == []


def test_select_appointments_returns_new_list_for_empty_and_sorted_inputs():
    empty_source = []

    empty_result = select_appointments(empty_source, "DR1")

    assert empty_result == []
    assert empty_result is not empty_source

    source, cancelled, completed, late_scheduled, _ = build_query_data()
    sorted_source = [cancelled, completed, late_scheduled]

    result = select_appointments(sorted_source, "DR1")

    assert result == sorted_source
    assert result is not sorted_source
    assert result[0] is cancelled
    assert result[1] is completed
    assert result[2] is late_scheduled


def test_select_appointments_is_repeatable_and_does_not_mutate_source():
    source, _, _, _, _ = build_query_data()

    original_order = list(source)
    original_fields = [
        (
            appointment.appointment_id,
            appointment.patient,
            appointment.practitioner,
            appointment.date_time,
            appointment.status,
        )
        for appointment in source
    ]

    first_result = select_appointments(source, "DR1")
    second_result = select_appointments(source, "DR1")

    assert first_result == second_result
    assert first_result is not second_result
    assert source == original_order

    after_fields = [
        (
            appointment.appointment_id,
            appointment.patient,
            appointment.practitioner,
            appointment.date_time,
            appointment.status,
        )
        for appointment in source
    ]

    assert after_fields == original_fields