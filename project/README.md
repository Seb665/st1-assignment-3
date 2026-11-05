# SmartCare

Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified. Runtime uses only the standard library.

From this directory, using a Python environment with the development dependency installed:

```sh
python main.py
python -m pytest
```

If needed in your approved environment: `python -m pip install -r requirements-dev.txt`.

The demo registers synthetic records and books/finds an appointment. All supplied tests pass. Data exists only in this session and is lost on exit; FR-10 restart persistence is retired. Use synthetic information only.

`domain.py` contains the entities, status and guarded cancellation. `data_store.py` holds three dictionaries through add/find/list methods. The three services share that object. Supplied registration, booking, appointment lookup and conflict checking work. IDs are trimmed, non-blank and case-sensitive. Properties provide read-only identity/appointment state; changes go through domain methods. No special architecture terminology is required.

Stage 6 functionality has been completed, including patient/practitioner lookup and appointment cancellation. Stage 9 functionality has also been completed, including pure appointment queries, named-key ordering, practitioner appointment listing and the interactive console menu. No PG rescheduling or assurance solution is included.

Service booking accepts IDs and a `datetime` (local, minute precision). Console parser accepts exactly `YYYY-MM-DD HH:MM`. Store lookups return None when absent; service lookups raise LookupError. Invalid values, duplicates, conflicts and illegal transitions raise ValueError. Lists are new containers holding the stored objects. No age, duration, patient-conflict or past-date rules apply.

Stage 9 adds pure appointment queries, practitioner appointment listing and the interactive SmartCare menu.

From the project directory, run the interactive menu with: python main.py --interactive

Run the full automated test suite with: python -m pytest

Stage 9 query and workflow tests can also be run separately:

python -m pytest tests/test_queries.py -v
python -m pytest tests/test_workflows.py -v

queries.py contains the pure Stage 9 collection-processing functions. appointment_sort_key() orders appointments by date_time and then appointment_id. select_appointments() filters appointments by practitioner and optional AppointmentStatus, returning a new sorted list without modifying the source collection.

AppointmentService.list_practitioner_appointments() validates the practitioner and optional status, obtains the current appointment collection from the data store, and delegates filtering and ordering to the pure query function.

The interactive console supports:

1. Register patient

2. Find patient

3. Register practitioner

4. Find practitioner

5. Book appointment

6. Cancel appointment

7. Find appointment

8. List practitioner appointments

0. Exit

For practitioner appointment listings, leaving the status blank includes all statuses. Valid explicit status values are scheduled, cancelled and completed.

Expected ValueError and LookupError cases are displayed without terminating the menu session.

Cancelled appointments remain available in the current-session history but no longer occupy their practitioner/date-time slot.

SmartCare remains session-only. Data is lost when the program exits. Stage 9 does not add persistence, rescheduling or assurance functionality.

## Release information

The common UG SmartCare release is being verified through Stage 12.

Stage 12 starting repository SHA:

d523b8d5e812cddaf2bc23198cad81653d32cd05

The last integrated Stage 9 application SHA was:

68fb7828983323978dff21850b08143424974090

At the Stage 12 starting SHA, the complete automated test suite passed:

57 passed in 0.33s

The final tested/submitted release SHA will be recorded after Stage 12 release verification is complete.