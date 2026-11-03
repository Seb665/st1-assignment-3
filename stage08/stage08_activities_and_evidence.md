# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [Stage 7 verified application baseline SHA 9071ab07b904e9518bf40d605fa741502631cd26; SmartCare A3 Requirements Baseline 2026 revision 2.]
- Baseline test command / working directory / observed result / evidence: [python -m pytest from project/ -> 40 passed in 0.20s before Stage 8 preparation.]
- Clean preparation SHA if a record-only commit followed Stage 7: [Stage 7 evidence-only main SHA 3e95e32. The Stage 8 preparation utility subsequently reported clean baseline Git SHA a43ee399be009eb70dfc25ffaa425cf790c1caae after Pranav's preparation setup.]
- Branch and preparer / how teammates obtained this branch: [debug/stage08; prepared in Sebastian Riches' local repository with tutor support using the supplied Stage 8 preparation utility. The prepared branch was pushed as origin/debug/stage08. Teammate retrieval will be recorded when it occurs.]
- Downloaded tool version, source SHA256 and --check outcome: [Stage 8 tool version 1.1. Baseline/source SHA256 reported by the utility: b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375. python prepare_debugging.py project --check reported preflight PASS, baseline Git SHA a43ee399be009eb70dfc25ffaa425cf790c1caae, project unchanged and both proposed fault signatures verified in a temporary copy.]
- --apply and --verify output summaries / artefact references: [python prepare_debugging.py project --apply reported preflight PASS and prepared F8-01 practitioner conflict and F8-02 retained-history lookup. The utility verified the expected failures test_f8_01_conflict and test_f8_02_history (2 failed). python prepare_debugging.py project --verify then reported exactly 2 expected failures with both approved symptom signatures present.]
- Bounded diff inspected and recovery location (not committed): [The preparation utility reported backup/hash metadata in project/.stage8_faults/, with --restore reserved for setup recovery only. Inspection showed the controlled application change was bounded to project/smartcare/data_store.py. Local recovery metadata must not be committed.]
- Prepared faulty-state commit SHA: [76a9a8d (Prepare debug stage 08). This commit contains the controlled Stage 8 changes to project/smartcare/data_store.py.]
- Preparation or recovery issues and resolution, if any: [No preparation or recovery failure was observed. The Stage 8 utility reported successful --check, --apply and --verify results. No --restore recovery was required. A later commit, 3bca0d5, updated .gitignore but did not alter the prepared SmartCare fault code.]
- Initial prepared full-suite command / result / key failures: [python -m pytest -q 33 passed, 7 failed in 0.58s.]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [A second appointment for the same practitioner at the exact same datetime was incorrectly allowed, while an appointment for a different practitioner at that same datetime was incorrectly rejected as a conflict.]
- Expected behaviour and requirement: [Under FR-05 / AC-04.1, and existing SCHEDULED appointment for the same practitioner at the exact same datetime must cause a conflict. Under AC-04.2, a different practitioner at the same datetime must be allowed.]
- Minimal synthetic reproduction steps: [Register a patient and two practitioners. Book A1 for practitioner DR1 at a fixed datetime. Attempt A2 for DR1 at that same datetime and observe that no ValueError is raised. Then attempt a booking for DR2 at the same datetime and observe that a conflict ValueError is incorrectly raised.]
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_01_same_practitioner_exact_time_conflict_is_rejected failed because the second booking for the same practitioner at the exact same datetime did not raise the required ValueError (Failed: DID NOT RASE <class 'ValueError'>).]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [Inspection of SmartCareDataStore.has_practitioner_conflict() confirmed that the practitioner comparison was reversed. The method used appointment.practitioner.practitioner_id != practitioner_id, causing appointments for different practitioners to be treated as conflicts while failing to detect and existing appointment for the same practitioner. This directly matches the observed failing tests.]
- Smallest justified fix / diff / why other behaviour is preserved: [Changed the practitioner comparison in SmartCareDataStore.has_pracitioner_conflict() from != practitioner_id to == practitioner_id. This restores the documented same-practitioner conflict rule while leaving the existing exact-datetime, SCHEDULED-status and excluded-appointment checks unchanged. No unrelated production behaviour was modified.]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [After a SCHEDULED appointment is cancelled, the appointment object changes to CANCELLED but subsequent store lookup returns None and service lookup raises LookupError, making the retained appointment appear absent.]
- Expected behaviour and requirement: [FR-06 requires a valid SCHEDULED cancellation to change the same appointment to CANCELLED. FR-07 / AC-05.2 require the cancelled appointment to remain retained and retrievable in the current session, with FR-08 supporting appointment lookup.]
- Minimal synthetic reproduction steps: [Register a patient and practitioner, book appointment A1, cancel A1, confirm its status becomes CANCELLED, then call store.find_appointment("A1") and AppointmentService.find_appointment("A1"). The cancelled appointment should still be returned as the same stored object.]
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable failed because store.find_appointment("A1") returned None instead of the same retained cancelled appointment object.]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [Inspection of SmartCareDataStore.find_appointment() confirmed that the modified method excludes appointments whose status value is "cancelled". The cancelled appointment remains in the store's appointment collection, but find_appointment() returns None for it. The service then interprets that None as absence and raises LookupError, which breaks retianed-history lookup.]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [The practitioner comparison inside SmartCareDataStore.has_practitioner_conflict() may have been reversed or changed incorrectly. This is plausible because the observed behaviour is the opposite of the required rule: same-practitioner bookings are allowed while different-practitioner bookings are treated as conflicts.]
Evidence intended to inspect / competing explanation / discriminating check: [Inspect has_practitioner_conflict() and compare its practitioner-ID, datetime and SCHEDULED-status conditions. A competing explanation is that AppointmentService.book_appointment() may be passing the wrong practitioner ID. The discriminating check is to inspect the actual arguments passed by the service and then evaluate the store method for the same practitioner and for a different practitioner at the same datetime.]
Member and saved sequence/time or commit showing this preceded consultation: [Sebastian Riches. The human hypothesis and failing F8-01 regression test were recorded and committed before any GitHub Copilot consultation at commit 6e4a18e0fb4eac929ad7924cb49189dfb80d0c79.]

### F8-02 human entry
Likely cause and why plausible: [SmartCareDataStore.find_appointment() appears to exclude appointments whose status is CANCELLED, causing a retained cancelled appointment to be treated as absent during lookup.]
Evidence intended to inspect / competing explanation / discriminating check: [Inspect find_appointment() and compare list_appointments() membership with direct store lookup after cancellation. A competing explanation is that cancellation deletes the appointment. The discriminating check is to confirm that the cancelled object remains in list_appointments() while find_appointment("A1") returns None.]
Member and saved sequence/time or commit showing this preceded consultation: [Sebastian Riches. The human hypothesis and failing F8-02 regression test were recorded and committed before any GitHub Copilot consultation at commit 6e4a18e0fb4eac929ad7924cb49189dfb80d0c79.]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [Sebastian Riches used the required Stage 8 diagnostic prompt in a fresh GitHub Copilot chat after the human-first hypothesis had already been recorded at pre-Copilot commit 02c2138e84774432fb7cbaaa644d3b5a29360004. Copilot returned three ranked diagnostic suggestions.]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot ranked the reversed practitioner comparison as the most likely cause and recommended checking whether has_practitioner_conflict() uses != rather than ==. Inspection of the actual debug/stage08 code confirmed appointment.practitioner.practitioner_id != practitioner_id. This exactly explains why same-practitioner conflicts are missed and different practitioners are incorrectly blocked. Classification: Correct. Decision: Accept.]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that pytest might be loading a stale or different copy of the SmartCare package. The actual test run was performed from the intended repository and project/ working directory on debug/stage08 and the inspected data_store.py on that branch contains the reversed comparison that matches the failure. The different from main is intentional because Stage 8 uses a prepared debugging branch. Classification: Plausible diagnostic check but contradicted by the available evidence. Decision: Reject as the root cause.]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that the booking path might pass an unexpected practitioner ID or use a different datastore instance. The regression test creates one shared SmartCareDataStore, passes it to the services and uses the correct registered practitioner IDs. The failure is already directly explained by the reversed comparison inside has_practitioner_conflict(). Classification: Plausible alternative but not supported by the observed evidence. Decision: Reject as the root cause.]
Final human conclusion and comparison with initial hypothesis: [The final diagnosis confirms the original human hypothesis. F8-01 is caused by the reversed practitioner-ID comparison in SmartCareDataStore.has_practitioner_conflict(): != is used where the conflict rule requires matching the same practitioner. Copilot's first suggestion agreed with the diagnosis, while its stale-import and wrong-ID/store alternatives were not supported by the actual branch, test setup or inspected code.]

### F8-02 Copilot review
Actual prompt / output reference and member: [Sebastian Riches used the required Stage 8 diagnostic prompt in a fresh GitHub Copilot chat after the human-first hypothesis had already been recorded at pre-Copilot commit 02c2138e84774432fb7cbaaa644d3b5a29360004. Copilot returned three ranked diagnostic suggestions.]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot ranked the explicit exclusion of cancelled appointments in SmartCareDataStore.find_appointment() as the most likely cause. Inspection of the running debug/stage08 code confirmed the condition appointment.status.value != "cancelled". The regression test also showed that the appointment had changed to CANCELLED while store.find_appointment("A1") returned None. Classification: Correct. Decision: Accept.]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that cancellation or list_appointments() might remove or filter the appointment. The observed evidence contradicts this as the root cause because the appointment remains retained in the store collection; the failure occurs specifically when find_appointment() applies its status condition. Classification: Plausible diagnostic alternative but not supported by the evidence. Decision: Reject as the root cause.]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that the stored appointment ID might no longer match "A1". The appointment was created and retained with ID "A1" and the failure appeared only after cancellation. The inspected find_appointment() status filter directly explains the failed lookup, while no evidence showed the ID changing. Classification: Plausible alternative but not supported by the observed evidence. Decision: Reject as the root cause.]
Final human conclusion and comparison with initial hypothesis: [The final diagnosis confirms the original human hypothesis. F8-02 is caused by SmartCareDataStore.find_appointment() excluding appointments whose status is CANCELLED. The cancelled appointment remains stored but the lookup method returns None, which then causes the service layer to raise LookupError. Copilot's first suggestion agreed with the supported diagnosis, while the removal/filtering and ID-mismatch alternatives were contradicted by the inspected state and code.]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory                                 | Actual result and artefact reference                                                                                                                                                            |
|---|----|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| F8-01 before repair | [6e4a18e0fb4eac929ad7924cb49189dfb80d0c79] | [python -m pytest tests/test_regressions.py -v from project/] | [test_f8_01_same_practitioner_exact_time_conflict_is_rejected FAILED because the expected ValueError was not raised. Focused run: 2 failed in 0.34s.]                                           |
| F8-01 after repair | [complete] | [complete]                                                    | [complete]                                                                                                                                                                                      |
| F8-02 before repair | [6e4a18e0fb4eac929ad7924cb49189dfb80d0c79] | [python -m pytest tests/test_regressions.py -v from project/] | [test_f8_02_cancelled_appointment_remains_retrievable FAILED because store.find_appointment("A1") returned None instead of the retained cancelled appointment. Focused run: 2 failed in 0.34s.] |
| F8-02 after repair | [complete] | [complete]                                                    | [complete]                                                                                                                                                                                      |
| Full suite after both repairs, before refactor | [complete] | [complete]                                                    | [complete]                                                                                                                                                                                      |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
