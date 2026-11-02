# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete] 
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test                                                                                                                                                                                               | Negative test                                                                                                                                                       | Key assertion                                                                                                                                                |
|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01 Register patient | [Register a patient using a valid unused patient ID and required name. Confirm that the patient is stored and can be retrieved from the shared data store.]                                                 | [Attempt to register another patient using an ID that is already registered. Expect ValueError and confirm that the original patient remains stored and unchanged.] | [data_store.find_patient('P1') is patient for successful registration and after a duplicate attempt the stored object is still the original patient.]        |
| FR-05 Prevent practitioner conflict | [create bookings for two different appointments at the same time with two different practitioners and both appointments should be allowed.]                                                                 | [Try to book an appointment at the same time as a different appointment with the same practitioner and it should give an error. ]                                   | [The valid appointments are stored whereas the invalid appointments with both the same time and same practitioner are rejected and not stored.]              |
| FR-06 Cancel appointment | [Cancel a SCHEDULED appointment using AppointmentService.cancel_appointment(). Confirm that the appointment changes to AppointmentStatus.CANCELLED and the returned object is the same stored appointment.] | [Attempt to cancel an appointment that is already CANCELLED. Expect ValueError and confirm that its status remains CANCELLED.]                                      | [result is appointment and appointment.status is AppointmentStatus.CANCELLED; after the rejected repeated cancellation, the status remains CANCELLED.]       |
| FR-07 Retain cancelled history | [Cancel a SCHEDULED appointment and then look it up againd during the same session. Confirm that the cancelled appointment remains retrievable and is the same stored object.]                              | [Check that cancellation does not delete, replace or remove the appointment from current-session history.]                                                          | [service.find_appointment('A1') is appointment and the same appointment remains present in the datastore appointment list with AppointmentStatus.CANCELLED.] |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Weak]  Why: [This assertion always passes and does not check any SmartCare behaviour. A test containing only this assertion could pass even if the required feature was completely broken.]

`assert appointment is not None`
Judgement: [Weak/unclear]  Why: [This confirms that some appointment object exists but it does not prove that it is the correct stored appointment, that it has the expected ID or participants or that it is in the required status.]

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour]  Why: [This directly checks the observable cancellation state required by FR-06. However, by itself it does not prove that the same appointment object was retained or that it remains retrievable in current-session history.]

`assert len(results) > 0`
Judgement: [Weak/unclear]  Why: [This only proves that the results collection contains at least one item. It does not prove that the expected appointment is present, that unrelated records are excluded or that the returned objects are correct.]

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour]  Why: [This verifies that lookup for A1 returns the exact same stored Appointment object rather than a replacement object. This provides strong evidence for object identity and retained current-session storage, although another assertion is still needed to verify the appointment's status.]

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 

#### Blank Identifier

- Input/state: attempt to use an empty or whitespace-only required ID, such as ' ' for a patient ID.
- Expected result: ValueError is raised and no record is created or changed.
- Supporting contract: required IDs must be strings, trimmed and non-blank. Invalid or blank required values raise ValueError.

#### Whitespace-only name

- Input/state: attempt to register a patient or practitioner with a required name containing only whitespace.
- Expected result: ValueError is raised and the invalid object is not registered.
- Supporting contract: required text fields such as names must contain non-whitespace text. Invalid required values raise ValueError.

#### Same-time practitioner booking

- Input/state: a SCHEDULED appointment already exists for practitioner D1 at a particular datetime. Attempt to book another appointment for D1 at that exact datetime.
- Expected result: ValueError is raised and the new appointment is not stored. Booking a different practitioner at the same time remains valid.
- Supporting contract: FR-05 defines a conflict as the same practitioner, exact datetime and an existing SCHEDULED appointment.

#### Cancelled appointment

- Input/state: an appointment for practitioner D1 at a particular datetime has been cancelled. Attempt to book another appointment for D1 at that same datetime.
- Expected result: the new booking is allowed because the previous appointment is no longer SCHEDULED. The cancelled appointment remains retained in current-session history.
- Supporting contract: only existing SCHEDULED appointments occupy a practitioner/time slot. FR-07 also requires cancelled appointments to remain retrievable in the current session.

#### Invalid status transition

- Input/state: attempted to cancel an appointment that is already CANCELLED or has status COMPLETED. 
- Expected result: ValueError is raised and the appointment's existing status remains unchanged.
- Supporting contract: FR-06 permits cancellation only from SCHEDULED; cancellation from CANCELLED or COMPLETED is an invalid transition and must not mutate the appointment.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate                     | What is wrong                                                                                                                                                                                        | Rewritten test intention                                                                                                                                                                                                    |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 - Asserts not None          | [Only confirms that an object was returned. It does not prove that the correct object was returned, that its values are correct or that the required behvaiour was satisfied.]                       | [Test the specific operation and verify the expected object or state using a stronger assertion, such as confirming that lookup returns the exact registerd object.]                                                        |
| 2 - Asserts not None          | [Only confirms that some object exists. An incorrect or unrelated object could still make the test pass.]                                                                                            | [Test the required behaviour directly, such as checking the correct appointment status, participant identity, stored object or documented exception.]                                                                       |
| 3 - Asserts True              | [The assertion is unconditional and will always pass, so it provides no evidence about SmartCare behaviour.]                                                                                         | [Replace it with an assertion tied to an actual requirement, such as checking that cancellation changes and appointment to CANCELLED or that an invalid operation raises the documented exception.]                         |
| 4 - Assumes SMS notifications | [The test assumes an SMS feature exists even though SMS notifications are not part of the SmartCare requirements. This invents behaviour and could cause a correct implementation to fail the test.] | [Replace the SMS expectation with a documented SmartCare outcome, such as verifying that a valid booking is stored with the correct registered participants and SCHEDULED status.]                                          |
| 5 - Assumes SMS notifications | [The test again depends on an unstated SMS feature, so it is not traceable to an approved requirement.]                                                                                              | [Replace the SMS expectation with a requirement-based test, such as verifying that cancelling an appointment changes its status to CANCELLED and that the same appointment remians retrievable in current-session history.] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
[100% code coverage only shows that every line of code was executed during testing. It does not prove that the tests checked the correct requirements, used meanginful assertions, covered all important scenarios or detected incorrect behaviour. A test suite could execute every line while still using weak assertions such as assert True or is not None. Therefore, high coverage can still coexist with poor verification if the tests do not actually demonstrate that the software meets its requirements.]

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion                                                                                                                                                                     | Test ID     | Test type                     | Test name / location                                                                      | Expected behaviour                                                                                                  | Result / observed status                           | Supplied or student-authored |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|---|
| [FR-01]     | [AC-01.1 - Valid required data with an unused ID is stored]                                                                                                                              | [TEST - 01] | [Service - positive]          | [tests/test_services.py::test_register_patient_stores_registered_object]                  | [A valid patient is returned and the exact same object is stored under the supplied ID.]                            | [Passed - focused service run: 2 passed in 0.18s.] | [complete] |
| [FR-01]     | [AC-01.2 - Registration with an existing patient ID is rejected.]                                                                                                                        | [TEST - 02] | [Service - negative]          | [tests/test_services.py::test_duplicate_patient_id_is_rejected_without_overwrite]         | [A duplicate patient ID raises ValueError and the original stored patient remains unchanged.]                       | [Passed - focused service run: 2 passed in 0.18s.] | [complete] |
| [FR-01]     | [Revision 2 validation requirement - patient IDs must be trimmed and non-blank.]                                                                                                         | [TEST - 03] | [Domain - boundary]           | [tests/test_domain.py::test_patient_rejects_blank_id]                                     | [A blank or whitespace-only patient ID raises ValueError.]                                                          | [Passed - focused domain run: 4 passed in 0.18s.]  | [complete] |
| [FR-03]     | [Revision 2 validation requirement - practitioner ID, name and specialty must be non-blank text.]                                                                                        | [TEST - 04] | [Domain - negative]           | [tests/test_domain.py::test_practitioner_rejects_blank_specialty]                         | [A whitespace-only specialty raises ValueError.]                                                                    | [Passed - focused domain run: 4 passed in 0.18s.]  | [complete] |
| [FR-04]     | [AC-03.1 - Registered participants, a unique appointment ID and a free time produce a stored SCHEDULED appointment.]                                                                     | [TEST - 05] | [Service - positive]          | [tests/test_services.py::test_valid_booking_uses_registered_objects_and_is_stored]        | [Booking succeeds, starts as SCHEDULED, uses the actual registered patient and practitioner objects and is stored.] | [Passed - focused service run: 2 passed in 0.16s.] | [complete] |
| [FR-04]     | [AC-03.2 - Booking an unknown patient or practitioner is rejected.]                                                                                                                      | [TEST - 06] | [Service - negative]          | [tests/test_services.py::test_booking_unknown_participant_is_rejected_without_storage]    | [LookupError is raised and no appointment is added.]                                                                | [Passed - focused service run: 2 passed in 0.16s.] | [complete] |
| [FR-05]     | [AC-04.1 - Same practitioner, exact datetime and existing SCHEDULED appointment conflicts.]                                                                                              | [TEST - 07] | [Service - negative/boundary] | [tests/test_services.py::test_same_practitioner_exact_time_is_rejected]                   | [The conflicting booking raises ValueError and the rejected appointment is not stored.]                             | [Passed - focused service run: 2 passed in 0.14s.] | [complete] |
| [FR-05]     | [AC-04.2 - Another practitioner at the same time is allowed.]                                                                                                                            | [TEST - 08] | [Service - positive/boundary] | [tests/test_services.py::test_different_practitioner_same_time_is_allowed]                | [Both appointments are successfully stored becuase they use different practitioners.]                               | [Passed - focused service run: 2 passed in 0.14s.] | [complete] |
| [FR-06]     | [AC-05.1 - Cancelling a SCHEDULED appointment changes it to CANCELLED.]                                                                                                                  | [TEST - 09] | [Service - positive]          | [tests/test_services.py::test_cancel_scheduled_appointment_returns_same_cancelled_object] | [Cancellation returns the same appointment object and changes its status to CANCELLED.]                             | [Passed - focused service run: 2 passed in 0.16s.] | [complete] |
| [FR-07]     | [AC-05.2 - Cancelled history remians retrievable in the current session.]                                                                                                                | [TEST - 10] | [Serice - positive]           | [tests/test_services.py::test_cancelled_appointment_remains_retrievable]                  | [The cancelled appointment remains stored and lookup returns the exact same object.]                                | [Passed - focused service run: 2 passed in o.16s.] | [complete] |
| [FR-06]     | [AC-05.3 - Repeated cancellation is rejected.]                                                                                                                                           | [TEST - 11] | [Domain - negative]           | [tests/test_domain.py::test_repeated_cancellation_is_rejected_without_state_change]       | [A second cancellation raises ValueError and the appointment remains CANCELLED.]                                    | [Passed - focused domain run: 4 passed in 0.18s.]  | [complete] |
| [FR-06]     | [Revision 2 cancellation rule - only SCHEDULED appointments may be cancelled.]                                                                                                           | [TEST - 12] | [Domain - boundary]           | [tests/test_domain.py::test_completed_appointment_cannot_be_cancelled]                    | [Cancelling a COMPLETED appointment raises ValueError and its status remains COMPLETED.]                            | [Passed - focused domain run: 4 passed in 0.18s.]  | [complete] |
| [FR-05]     | [Revision 2 conflict rule - only an existing SCHEDULED appointment for the same practitioner at the exact datetime occupies the slot; a cancelled appointment does not occupy the slot.] | [TEST - 13] | [Service - boundary]          | [tests/test_services.py::test_cancelled_appointment_does_not_occupy_practitioner_slot] | [After an existing appointment is cancelled, another appointment for the same practitioner at the exact same datetime is allowed and stored, while the cancelled appointment remains retained in history.] | [Passed - focused service run: 1 passed in 0.19s.] | [complete] |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID   | Requirement | Acceptance criterion                                                                             | Positive / Negative / Boundary | Test intention                                                                                                        | Observable result expected                                                                                                    | Added evidence beyond supplied tests                                                                                                                                                       |
|-----------|-------------|--------------------------------------------------------------------------------------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [TEST-01] | [FR-01]     | [AC-01.1]                                                                                        | [Positive]                     | [Register a patient using valid required data and an unused ID through PatientService.]                               | [The returned patient is the exact same object stored under P1.]                                                              | [Provides a focused student-authored service test with direct FR-01/AC-01.1 traceability and explicitly verifies stored object identity.]                                                  |
| [TEST-02] | [FR-01]     | [AC-01.2]                                                                                        | [Negative]                     | [Attempt to register a second patient using an existing patient ID.]                                                  | [ValueError is raised and the original patient remains stored as the same object.]                                            | [Provides an isolated student-authored check that duplicate registration does not overwrite existing state and links the behaviour directly to AC-01.2.]                                   |
| [TEST-03] | [FR-01]     | [Revision 2 validation requirement - patient IDs must be trimmed and non-blank.]                 | [Boundary]                     | [Construct a patient using whitespace-only patient ID.]                                                               | [ValueError is raised.]                                                                                                       | [Provides independently authored and directly traceable evidence for the Revision 2 blank-ID boundary. It confirms an existing supplied-test intention in a focused domain test.]          |
| [TEST-04] | [FR-03]     | [Revision 2 validation requirement - practitioner ID, name and specialy must be non-blank text.] | [Negative]                     | [Construct a practitioner using a whitespace-only specialty.]                                                         | [ValueError is raised.]                                                                                                       | [Provides a focused student-authored validation test with direct traceability to the practitioner required field rule.]                                                                    |
| [TEST-05] | [FR-04]     | [AC-03.1]                                                                                        | [Positive]                     | [Register real patient and practitioner objects and book a valid appointment using their IDs.]                        | [The appointment is stored, begins as SCHEDULED and refers to the actual registered patient and practitioner objects.]        | [Gives AC-03.1 its own student-authored service test and directly combines identity, status and storage assertions under one traceable TEST ID.]                                           |
| [TEST-06] | [FR-04]     | [AC-03.2]                                                                                        | [Negative]                     | [Attempt to book an appointment using a valid patient but an unknown practitioner ID.]                                | [LookupError is raised and appointment A1 is not stored.]                                                                     | [Explicitly checks the service-boundary exception and verifies that rejecting booking leaves appointment storage unchanged.]                                                               |
| [TEST-07] | [FR-05]     | [AC-04.1]                                                                                        | [Negative / Boundary]          | [Attempt a second booking for the same practitioner at the exact datetime of an existing SCHEDULED appointment.]      | [ValueError is raised, the original appointment remains stored and the rejected appointment is absent.]                       | [Gives AC-04.1 a focused student-authored test that checks both the exception and unchanged storage after rejection.]                                                                      |
| [TEST-08] | [FR-05]     | [AC-04.2]                                                                                        | [Positive / Boundary]          | [Book two appointments at the same exact datetime using two different practitioners.]                                 | [Both appointments are stored successfully and each refers to the correct practitioner.]                                      | [Separately verifies the allowed side of the practitioner-conflict boundary and directly traces it to AC-04.2.]                                                                            |
| [TEST-09] | [FR-06]     | [AC-05.1]                                                                                        | [Positive]                     | [Cancel a SCHEDULED appointment through AppointmentService.cancel_appointment().]                                     | [The service returns the same appointment object and its status becomes CANCELLED.]                                           | [Adds service-level cancellation evidence through the completed Stage 6 operation rather than only exercising the domain cancel() method.]                                                 |
| [TEST-10] | [FR-07]     | [AC-05.2]                                                                                        | [Positive]                     | [Cancel an appointment and retrieve it again during the same session.]                                                | [Lookup returns the exact same cancelled appointment and it remains present in the session appointment list.]                 | [Directly verifies retained current-session history through the completed service workflow and checks object identity after cancellation.]                                                 |
| [TEST-11] | [FR-06]     | [AC-05.3]                                                                                        | [Negative]                     | [Cancel a SCHEDULED appointment and then attempt to cancel the same appointment again.]                               | [The second cancellation raises ValueError and the appointment remains CANCELLED.]                                            | [Provides a focused student-authored illegal-transition test with an explicit unchanged-state assertion and direct AC-05.3 traceability.]                                                  |
| [TEST-12] | [FR-06]     | [Revision 2 cancellation rule - only SCHEDULED appointments may be cancelled.]                   | [Boundary]                     | [Attempt to cancel an appointment constructed with COMPLETED status.]                                                 | [ValueError is raised and the status remains COMPLETED.]                                                                      | [Adds a separate status-boundary case showing that the cancellation guard also protects a COMPLETED appointment from invalid mutation.]                                                    |
| [TEST-13] | [FR-05]     | [Revision 2 conflict rule - a cancelled appointment does not occupy the practitioner/time slot.] | [Boundary]                     | [Book an appointment, cancel it, then book another appointment for the same practitioner at the exact same datetime.] | [The second booking succeeds and is stored, while the original cancelled appointment remains retained with CANCELLED status.] | [Added evidence beyond supplied tests: Directly verifies the documented status boundary between a SCHEDULED appointment that occupies the slot and a CANCELLED appointment that does not.] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID   | Arrange                                                                                                 | Act                                                                      | Assert                                                                                                                                                   | Why meaningful / why assertion proves criterion                                                                                                                  |
|-----------|---------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [TEST-01] | [Create a fresh SmartCareDataStore and PatientService.]                                                 | [Register patient P1 with valid required data.]                          | [store.find_patient("P1") is patient.]                                                                                                                   | [Confirms that successful registration stores the exact patient object created by the service, directly supporting AC-01.1]                                      |
| [TEST-02] | [Create a fresh store and register an original patient with ID P1.]                                     | [Attempt to register another patient using the same ID.]                 | [ValueError is raised and store.find_patient("P1") is original.]                                                                                         | [Confirms duplicate registration is rejected and also proves that the existing stored patient was not overwritten, supporting AC-01.2.]                          |
| [TEST-03] | [Prepare a whitespace-only patient ID and a valid patient name.]                                        | [Attempt to construct the Patient.]                                      | [ValueError is raised.]                                                                                                                                  | [Directly checks the Revision 2 boundary requiring patient IDs to contain non-blank text.]                                                                       |
| [TEST-04] | [Prepare a valid practitioner ID and name with a whitespace-only specialty.]                            | [Attempt to construct the Practitioner.]                                 | [ValueError is raised.]                                                                                                                                  | [Directly checks that the required practitioner specialty cannot contain only whitespace.]                                                                       |
| [TEST-05] | [Create one fresh shared store and register a valid patient and practitioner.]                          | [Book appointment A1 using their registered IDs and a valid datetime.]   | [The appointment refers to the exact registered patient and practitioner objects, has SCHEDULED status and store.find_appointment("A1") is appointment.] | [These assertions jointly show that a valid booking uses the registered participants, starts in the required status and is actually stored, supporting AC-03.1.] |
| [TEST-06] | [Create a fresh shared store and register patient P1 but do not register practitioner DR999.]           | [Attempt to book appointment A1 using the unknown practitioner ID.]      | [LookupError is raised and store.find_appointment("A1") is None.]                                                                                        | [Confirms that an unknown participant prevents booking and that the rejected operation leaves no appointment stored, supporting AC-03.2.]                        |
| [TEST-07] | [Register a patient and practitioner then create SCHEDULED appointment A1 for DR1 at a fixed datetime.] | [Attempt to book A2 for the same practitioner at that exact datetime.]   | [ValueError is raised, A1 remains the original stored appointment and A2 is absent.]                                                                     | [Checks the exact same-practitioner/same-time conflict and confirms rejected storage does not alter the valid exisitng booking, supporting AC-04.1.] |
| [TEST-08] | [Register one patient and two different practitioners in a fresh shared store.]                         | [Book one appointment for each practitioner at the exact same datetime.] | [Both appointment IDs are stored and each appointment refers to its correct practitioner.]                                                               | [Demonstrates that the conflict rule is practitioner-specific and that different practitioners may use the same exact time, supporting AC-04.2.] |
| [TEST-09] | [Register a valid patient and practitioner and create a SCHEDULED appointment.]                         | [Call AppointmentService.cancel_appointment("A1").]                      | [The returned result is the original appointment and its status is AppointmentStatus.CANCELLED.]                                                         | [Confirms both the required state transition and preservation of the same appointment object through the service workflow, supporting AC-05.1.] |
| [TEST-10] | [Create and store a valid SCHEDULED appointment, then cancel it through the appointment service.]       | [Retrieve appointment A1 again using find_appointment.]                  | [The retrieved object is the original appointment, remains CANCELLED and is present in store.list_appointments().]                                       | [Directly demonstrates that cancellation does not delete or replace the appointment and that cancelled history remians retrievable during the current session, supporting AC-05.2.] |
| [TEST-11] | [Construct a valid SCHEDULED appointment and cancel it once so its status becomes CANCELLED.]           | [Attempt to call cancel() on the same appointment again.]                | [ValueError is raised and the status remains AppointmentStatus.CANCELLED.]                                                                               | [Confrims repeated cancellation is rejected and proves the failed transition does not mutate the existing state, supporting AC-05.3.] |
| [TEST-12] | [Construct an appointment with AppointmentStatus.COMPLETED.]                                            | [Attempt to call cancel().]                                              | [ValueError is raised and the appointment remains COMPLETED.]                                                                                            | [Confirms that cancellation is guarded to SCHEDULED appointments only and that an invalid COMPLETED-to-CANCELLED transition cannot change the object.] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID   | Behaviour                                                                                            | Test file/function                                                                  | Result                                            |
|-----------|------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------------------------------------------------|
| [TEST-03] | [Reject a blank or whitespace-only patient ID with ValueError.]                                      | [tests/test_domain.py::test_patient_rejects_blank_id]                               | [Passed - focused domain run: 4 passed in 0.18s.] |
| [TEST-04] | [Reject a practitioner with a whitespace-only specialty using ValueError.]                           | [tests/test_domain.py::test_practitioner_rejects_blank_specialty]                   | [Passed - focused domain run: 4 passed in 0.18s.] |
| [TEST-11] | [Reject repeated cancellation of an already CANCELLED appointment and preserve its existing status.] | [tests/test_domain.py::test_repeated_cancellation_is_rejected_without_state_change] | [Passed - focused domain run: 4 passed in 0.18s.] |
| [TEST-12]  | [Reject cancellation of a COMPLETED appointment and leave its status unchanged.]                     | [tests/test_domain.py::test_completed_appointment_cannot_be_cancelled]              | [Passed - focused domain run: 4 passed in 0.18s.] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID   | Behaviour                                                                                                                                                                                       | Requirement / criterion                                                                                 | Test file/function                                                                        | Result                                                  |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------|
| [TEST-01] | [Register a valid patient and store the exact returned patient object.]                                                                                                                         | [FR-01 / AC-01.1]                                                                                       | [tests/test_services.py::test_register_patient_stores_registered_object]                  | [Passed - focused service run: 2 passed in 0.18s.]      |
| [TEST-02] | [Reject duplicate patient registration and preserve the original stored patient.]                                                                                                               | [FR-01 / AC-01.2]                                                                                       | [tests/test_services.py::test_duplicate_patient_id_is_rejected_without_overwrite]         | [Passed - focused service run: 2 passed in 0.18s.]      |
| [TEST-05] | [Book a valid appointment using actual registered patient and practitioner objects, with SCHEDULED status and retained storage.]                                                                | [FR-04 / AC-03.1]                                                                                       | [tests/test_services.py::test_valid_booking_uses_registered_objects_and_is_stored]        | [Passed - focused service run: 2 passed in 0.16s.]      |
| [TEST-06] | [Reject booking with an unknown practitioner and confirm no appointment is stored.]                                                                                                             | [FR-04 / AC-03.2]                                                                                       | [tests/test_services.py::test_booking_unknown_participant_is_rejected_without_storage]    | [Passed - focused service run: 2 passed in 0.16s.]      |
| [TEST-07] | [Reject an exact-time SCHEDULED conflict for the same practitioner and preserve the existing appointment.]                                                                                      | [FR-05 / AC-04.1]                                                                                       | [tests/test_services.py::test_same_practitioner_exact_time_is_rejected]                   | [Passed - focused FR-05 run: 2 passed in 0.14s.]        |
| [TEST-08] | [Allow two different practitioners to have appointments at the same exact datetime.]                                                                                                            | [FR-05 / AC-04.2]                                                                                       | [tests/test_services.py::test_different_practitioner_same_time_is_allowed]                | [Passed - focused FR-05 run: 2 passed in 0.14s.]        |
| [TEST-09] | [Cancel a SCHEDULED appointment through the service, return the same object and change its status to CANCELLED.]                                                                                | [FR-06 / AC-05.1]                                                                                       | [tests/test_services.py::test_cancel_scheduled_appointment_returns_same_cancelled_object] | [Passed - focused cancellation run: 2 passed in 0.16s.] |
| [TEST-10] | [Retain a cancelled appointment in current-session history and return the same object through lookup.]                                                                                          | [FR-07 / AC-05.2]                                                                                       | [tests/test_services.py::test_cancelled_appointment_remains_retrievable]                  | [Passed - focused cancellation run: 2 passed in 0.16s.] |
| [TEST-13] | [Allow a new appointment for the same practitioner and exact datetime after the previous appointment has been cancelled, while retaining the cancelled appointment in current-session history.] | [FR-05 - Revision 2 conflict rule: a cancelled appointment does not occupy the practitioner/time slot.] | [tests/test_services.py::test_cancelled_appointment_does_not_occupy_practitioner_slot]                      | [Passed - focused service run: 1 passed in 0.19s.]      |


## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour                                | Boundary/invalid input                                                                                             | Expected result                                                                                                                                       | Test ID   |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| [Patient ID validation]                  | [Whitespace-only patient ID such as "  "]                                                                          | [ValueError is raised and no valid patient object is created.]                                                                                        | [TEST-03] |
| [Practitioner required-field validation] | [Whitespace-only practitioner specialty]                                                                           | [ValueError is raised and the invalid practitioner is not created.]                                                                                   | [TEST-04] |
| [Duplicate patient registration]         | [Attempt to register a second patient using an already registered paitent ID.]                                     | [ValueError is raised and the original patient remains stored unchanged.]                                                                             | [TEST-02] |
| [Booking with an unknown participant]    | [Valid patient ID with an unknown practitioner ID.]                                                                | [LookupError is raised and the appointment is not stored.]                                                                                            | [TEST-06] |
| [Exact practitioner booking conflict]    | [A second SCHEDULED appointment for the same practitioner at the exact same datetime.]                             | [ValueError is raised, the original appointment remains stored and the rejected appointment is not added.]                                            | [TEST-07] |
| [Practitioner-conflict boundary]         | [Two appointments at the exact same dattime but with different practitioners.]                                     | [Both bookings are allowed because the conflict rule applies only to the same practitioner.]                                                          | [TEST-08] |
| [Repeated cancellation]                  | [Attempt to cancel an appointment that is already CANCELLED.]                                                      | [ValueError is raised and the appointment remains CANCELLED.]                                                                                         | [TEST-11] |
| [Invalid cancellation state]             | [Attempt to cancel a COMPLETED appointment.]                                                                       | [ValueError is raised and the appointment remains COMPLETED.]                                                                                         | [TEST-12] |
| [Cancelled practitioner-slot reuse]      | [An existing appointment for the same practitioner and exact datetime has status CANCELLED rather than SCHEDULED.] | [A replacement booking at the same practitioner and exact datetime is allowed and stored, while the original cancelled appointment remains retained.] | [TEST-13] |


## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [FR-05 - Prevent practitioner booking conflicts.]
Acceptance criterion: [AC-04.1 - An existing SCHEDULED appointment for the same practitioner at the exact same datetime causes a booking conflict.]
Behaviour to test: [A second appointment using the same practitioner and exact datetime must be rejected with ValueError and must not be stored.]
Human-first test idea/categories: [Register a patient and practitioner, create one SCHEDULED appointment, then attempt to book a second appointment with a different appointment ID but the same practitioner and exact datetime. Expect ValueError, then verify that the original appointment remains stored and the rejected appointment was not added.]
Prompt and purpose: [Github Copilot was asked to act as a software test-design assistant for FR-05 / AC-04.1. The prompt requested valid, invalid and meaningful boundary pytest candidates using only the current SmartCare public contracts and shared SmartCareDataStore, with no invented behaviour or unrelated architecture. The purpose was to compare Copilot's proposed test ideas against the group's human-first design and determine whether each candidate should be accepted, modified or rejected.]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [1 - Allow booking where there is no SCHEDULED appointment for the same practitioner at the exact same datetime.]
- What it claims to verify: [No practitioner conflict exists, so booking should succeed.]
- Requirement trace: [FR-05 / AC-04.1.]
- Assertion quality: [Potentially useful, but too broad as written.]
- Human critique: [Copilot combined more than one situation into a signle candidate, including a different practitioner at the same time and the same practitioner at a different time. These are separate behaviours and should be tested independently. It also referred to non-existent SmartCare fields such as DoctorId and StartAt.]
- Decision: [Modify.]
- Reason: [Keep the idea but split it into clear cases using the actual SmartCare API and terminology.]
- Final test reference if accepted/modified: [tests/test_services.py::test_different_practitioner_same_time_is_allowed]
- Actual verification result: [Passed as part of the focused FR-05 run: 2 passed in 0.14s.]

- Copilot test idea/candidate: [2 - Reject a second booking when the same practitioner already has a SCHEDULED appointment at the exact same datetime.]
- What it claims to verify: [A practitioner conflict should be detected.]
- Requirement trace: [FR-05 / AC-04.1.]
- Assertion quality: [Strong test intention but the proposed description did not specify the documented ValueError or verify that rejected state remained unchanged.]
- Human critique: [The central idea matches AC-04.1 but Copilot used incorrect field names and architecture. The final test should use AppointmentService.book_appointment(), expect ValueError, confirm that the original appointment remains stored and confirm that the rejected appointment was not added.]
- Decision: [Modify.]
- Reason: [The requirement trace was correct but the test needed to use the actual SmartCare public API and stronger observable assertions.]
- Final test reference if accepted/modified: [tests/test_services.py::test_same_practitioner_exact_time_is_rejected]
- Actual verification result: [Passed as part of the focused FR-05 run: 2 passed in 0.14s.]

- Copilot test idea/candidate: [3 - Allow the same practitioner to have another appointment at a different datetime.]
- What it claims to verify: [The conflict rule applies only to the exact same datetime.]
- Requirement trace: [FR-05 / AC-04.1.]
- Assertion quality: [Useful boundary intention.]
- Human critique: [This is a meaningful boundary because the requirement specifies an exact-time conflict. However, Copilot again used incorrect names such as DoctorId and StartAt. A real test should use a valid SmartCare minute-precision datetime, such as 09:00 and 09:01, rather than a vague +/- different timestamp.]
- Decision: [Modify.]
- Reason: [The boundary idea is valid but it must be expressed using the actual SmartCare API and datetime contract.]
- Final test reference if accepted/modified: [Not retained as a separate test in the current suite because the existing FR-05 tests already establish the exact-time conflict and allowed alternative behaviour.]
- Actual verification result: [Not separately executed.]

- Copilot test idea/candidate: [4 - Allow another booking at the same practitioner/time when the existing appointment is not SCHEDULED.]
- What it claims to verify: [Only a SCHEDULED appointment occupies the conflict slot.]
- Requirement trace: [FR-05 / AC-04.1.]
- Assertion quality: [Useful boundary idea but part of the proposed setup was invalid.]
- Human critique: [Copilot incorrectly introduced a NoShow status, which does not exist in SmartCare. The supported statuses are SCHEDULED, CANCELLED and COMPLETED. The Stage 7 requirements specifically state that a cancelled appointment does not occupy the slot, so the candidate can be corrected to use a CANCELLED appointment only.]
- Decision: [Modify.]
- Reason: [The underlying boundary is valid but the invented NoShow status and incorrect SmartCare field names must be removed.]
- Final test reference if accepted/modified: [Not yet implemented as a separate Stage 7 test.]
- Actual verification result: [Not separately executed.]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [Candidate 4 initially looked convincing because it correctly focused on the rule that only a SCHEDULED appointment should create a practitioner/time conflict. However, it also introduced a NoShow status that deos not exist in SmartCare and used incorrect field names such as DoctorId and StartAt.]
Why was it weak? [Although the general test idea matched the conflict rule, parts of the proposed test were based on behaviour and terminology that are not part of the actual SmartCare system. A test using an unsupported NoShow status or incorrect fields could fail for the wrong reason and would not provide reliable evidence for the requirement.]
How did you strengthen it? [I checked the candidate against the actual SmartCare domain and Stage 7 requirements. I removed the invented NoShow status, used the supported CANCELLED status where appropriate and based the test design on the real AppointmentService.book_appointment() workflow, date_time values and observable results.]
Accepted / modified / rejected test decisions and evidence: [See Section H Copilot candidate critique. Candidates 1-4 were all modified. Candidates 1 and 2 were retained through the implemented FR-05 tests and passed their focused test run. Candidates 3 and 4 were not retianed as separate tests because their useful behvaviour was either already covered or did not add enoguh independent evidence to justify another test.]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command            | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation                                                                                                                                                                            |
|--------------------|-------------------|----|--------|--------|-----------------|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [python -m pytest] | [project/]        | [1acb087fd64d88971144315d4148129c90476812] | [36]   | [0]    | [None]          | [None identified]                         | [Full accumulated regression suite passed in 0.26s. The supplied tests, Stage 6 tests and all currently implemented Stage 7 tests, including the cancelled-slot reuse boundary test, passed together.] |

Individual test runs and changed-order independence evidence: [python -m pytest tests/test_services.py::test_different_practitioner_same_time_is_allowed tests/test_domain.py::test_completed_appointment_cannot_be_cancelled tests/test_services.py::test_register_patient_stores_registered_object -v -> 3 passed in 0.19s. These selected tests passed when run together in a different order and each establishes fresh state, supporting test independence.]
Optional tutor-led demonstration notes: [Leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [The Stage 7 TEST IDs were derived from the approved requirements and acceptance criteria, implemented as domain and service tests, then verified through focused test runs and the full regression suite. TEST-13 was added to cover the cancelled-slot reuse boundary and passed its focused run before the full suite was rerun successfully. No product or test defects were identified in the verified runs.]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [The suite does not prove every possible input combination or any later-stage functionality such as practitioner appointment listing, queries or the interactive console. Those behaviours are outside the current Stage 7 scope and are completed in later stages.![img.png](img.png)]
Coverage if used: [Not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [Code coverage was not measured, so no line-level uncovered areas were identified. From a requirement perspective, the cancelled-slot reuse boundary is still important because it is part of the documented practitioner-conflict behaviour. Even 100% code average would not prove correctness because code can be executed without meaningful assertions or without checking the correct requirements.]
Optional fixtures/parametrisation used and why, if any: [Not used. The tests use simple local setup with a fresh SmartCareDataStore and fresh objects in each case because this keeps the tests easy to read and helps ensure that they remain independent.]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[Verification asks whether the software has been implemented correctly against the specified requirements.]

2. What question does validation answer?
[Validation asks whether the software being built actually meets the intended user or problem need.]

3. What is a unit test?
[A unit test checks a small part of the program, such as a class or method, to confrim that it behaves as expected.]

4. What is a pytest fixture?
[A pytest fixture provides reusable setup data or objects for tests and can help give each test fresh state without repeating the same setup code.]

5. What is parametrisation in pytest?
[Parametrisation allows the same test function to run multiple times using different sets of inputs and expected results.]

6. What is regression testing?
[Regression testing means rerunning existing tests alter changes to make sure previously working behaviour has not been broken.]

7. What does code coverage tell us, and what does it not prove?
[Code coverage shows which parts of the code were executed during testing. It does not prove that the requirements are correct, that all important scenarios were tested or that the assertions are meaningful.]

8. What makes an assertion weak?
[An assertion is weak when it does not directly check the required behaviour or could still pass even if the feature is incorrect, such as assert True or only checking that an object is not None.]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[GitHub Copilot can suggest test cases, boundaries and assertions but humans must review each suggestion against the actual requirements and code before accepting it.]

10. What is the Stage 7 engineering rule?
[The Stage 7 engineering rule is to design tests from the approved requirements, use meangingful observable assertions and keep the evidence tracebale from the requirement to the test and verified result.]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
