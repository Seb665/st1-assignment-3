# SmartCare

Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified. Runtime uses only the standard library.

From this directory, using a Python environment with the development dependency installed:

```sh
python main.py
python -m pytest
```

If needed in the approved environment:

python -m pip install -r requirements-dev.txt

The demo registers synthetic records and books/finds an appointment. SmartCare uses session-only in-memory data, so records are lost when the program exits. FR-10 restart persistence is retired. Use synthetic information only.

domain.py contains the entities, appointment status and guarded cancellation behaviour. data_store.py holds the session collections through add/find/list methods. The services share that data-store instance and coordinate application workflows. Supplied and completed functionality includes registration, lookup, booking, appointment lookup, conflict checking and cancellation.

IDs are trimmed, non-blank and case-sensitive. Properties provide read-only identity and appointment state, while state changes occur through the appropriate domain/service behaviour.

Stage 6 functionality has been completed, including patient/practitioner lookup and appointment cancellation.

Stage 9 functionality has also been completed, including pure appointment queries, named-key ordering, practitioner appointment listing and the interactive console menu.

No PG Stage 10/11 rescheduling or assurance implementation is included because this is a UG-only group.

Service booking accepts IDs and a datetime using local, minute-precision date/time. The console parser accepts exactly:

YYYY-MM-DD HH:MM

Store lookups return None when a valid record is absent. Service lookups raise LookupError. Invalid values, duplicates, booking conflicts and illegal state transitions raise ValueError.

Returned appointment lists are new list containers containing the stored appointment objects. No age, duration, patient-conflict or past-date rules apply.

Stage 9 queries and console

From the project directory, run the interactive menu with:

python main.py --interactive

Run the full automated test suite with:

python -m pytest

Stage 9 query and workflow tests can also be run separately:

python -m pytest tests/test_queries.py -v
python -m pytest tests/test_workflows.py -v

queries.py contains the pure Stage 9 collection-processing functions.

appointment_sort_key() orders appointments by date_time and then appointment_id.

select_appointments() filters appointments by practitioner and optional AppointmentStatus, returning a new sorted list without modifying the source collection.

AppointmentService.list_practitioner_appointments() validates the practitioner and optional status, obtains the current appointment collection from the data store, and delegates filtering and ordering to the pure query function.

The interactive console supports:

Register patient

Find patient

Register practitioner

Find practitioner

Book appointment

Cancel appointment

Find appointment

List practitioner appointments

Exit

For practitioner appointment listings, leaving the status blank includes all statuses. Valid explicit status values are scheduled, cancelled and completed.

Expected ValueError and LookupError cases are displayed without terminating the menu session.

Cancelled appointments remain available in current-session history but no longer occupy their practitioner/date-time slot.

SmartCare remains session-only. Data is lost when the program exits. The common UG release does not add persistence, PG rescheduling or PG assurance functionality.

Release information

The common UG SmartCare application has completed Stage 12 integration and functional release verification. The final source package will be generated from the final submitted commit.

Stage 12 starting repository SHA: d523b8d5e812cddaf2bc23198cad81653d32cd05

Integrated Stage 9 application SHA: 68fb7828983323978dff21850b08143424974090

Final tested Stage 12 candidate SHA: ccb5557d9a08c28f34473a01ef73947f975fccf2

At the Stage 12 starting SHA, the complete automated test suite reported:

57 passed in 0.33s

After the reviewed Stage 12 release-readiness changes were merged into main, the final integrated candidate was verified using Python 3.13.14:

57 passed in 0.30s

The final tested executable checkpoint is ccb5557d9a08c28f34473a01ef73947f975fccf2, verified using Python 3.13.14 with 57 tests passing in 0.30s. The final submitted repository SHA will be the later evidence-only commit that records the completed release metadata; no executable application or automated test changes are being made after this tested checkpoint.