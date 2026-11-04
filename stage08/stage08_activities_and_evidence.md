# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [Group 3: 2:30 - 4:30]
Members and UG/PG cohorts: [Sebastian Riches (Seb665) UG; Alexander Scola (u3324662-personal) UG; April Perez (4brila1816-coder) UG; Prajiet Eswaran (Prajiet103) UG]
Record owner / contribution links for each member: [Record owner: Sebastian Riches. Contribution evidence: Sebastian Riches — Sections C-H, Issues #11-#13 and PR #14; Abril Perez — human review and integration of PR #14; Alexander Scola — Stage 8 formative-question work in Section K; Prajiet Eswaran — no substantive Stage 8 artefact was identified in the shared evidence available when this record was finalised. See Section I157.]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation. - Symptom. This describes an observable problem but does not explain why it occurs.
- The data-store removal path is probably being called. - Hypothesis/opinion. This proposes a possible explanation that would need evidence. In the actual SmartCare project there is no public delete operation, so it cannot simply be accepted as fact.
- The failing test shows store.find_appointment('A1') returns None. - Evidence. This is a concrete observed result from an executed test.
- The service layer is badly designed. - Hypothesis/opinion. This is a broad judgement rather than specific evidence explaining the observed defect.
- Traceback points to smartcare/services.py line 42 in the example. - Evidence about failure location, but not root cause proof. A traceback identifies where a failure was observed. It does not prove that this location caused the underlying defect.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [See the five classifications above. Each statement has been classified as a symptom, evidence or hypothesis/opinion with a reason. The traceback is treated as evidence of where the failure was observed, not proof of the root cause.]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [I used the cancelled-appointment history scenario. Expected behaviour: under FR-06 and FR-07 / AC-05.2, cancelling a SCHEDULED appointment should change the same appointment object to CANCELLED while keeping it retained and retrievable during the current session. Observed behaviour: the appointment changed to CANCELLED, but SmartCareDataStore.find_appointment("A1") returned None and the service lookup consequently raised LookupError. Minimal reproduction: register patient P1 and practitioner DR1, book appointment A1, cancel A1, confirm its status is CANCELLED, then attempt to find A1 through the store and service. Initial hypothesis: SmartCareDataStore.find_appointment() may be excluding appointments once their status becomes CANCELLED. Evidence to inspect: the conditions inside find_appointment(), whether A1 remains present in list_appointments() after cancellation, and the difference between direct store lookup and service lookup.]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [A test expecting cancelled appointments to be deleted would be a test defect, because FR-07 requires cancelled appointments to remain retained in current-session history. The test should therefore be changed to expect the same cancelled appointment to remain retrievable, rather than changing the production code to delete it. A test expecting different practitioners at the same datetime to conflict would also be a test defect, because AC-04.2 allows different practitioners to have appointments at the same time. Only the same practitioner at the exact same datetime with an existing SCHEDULED appointment should cause the FR-05 conflict.]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [The hypothetical method contains several code smells: excessive length, duplicated status strings, mixed responsibilities, direct collection manipulation, printing inside business logic and deeply nested conditionals. Small refactorings could include renaming unclear variables, extracting repeated conflict logic into a focused helper, replacing magic status strings with the existing AppointmentStatus enum, and keeping collection access behind the existing SmartCareDataStore boundary. The classifications are: rename appt to appointment — refactoring; extract a repeated conflict helper — refactoring; add rescheduling — feature; restore retained cancellation lookup — repair; replace a magic status string with the existing enum — refactoring. Throughout any refactor, required external behaviour must remain unchanged, including booking conflict rules, exception behaviour, object identity, cancellation state transitions and retained current-session history.]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [I used the F8-02 retained-history failure. The failing assertion was assert store.find_appointment("A1") is appointment. The expected value was the same retained cancelled Appointment object, while the observed value was None. The failure occurred in tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable, with the application path running from the regression test through AppointmentService.cancel_appointment() and then SmartCareDataStore.find_appointment("A1"). FR-07 / AC-05.2 requires a cancelled appointment to remain retained and retrievable during the current session. Ranked possible causes were: (1) find_appointment() filters out CANCELLED appointments — check the lookup condition and compare it with the appointment status; (2) cancellation removes the appointment from storage — check list_appointments() after cancellation; (3) the appointment ID no longer matches "A1" — inspect appointment.appointment_id before and after cancellation. The traceback alone does not prove the root cause because it shows where the incorrect result became visible, not necessarily where the faulty decision was introduced.]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [Changing code immediately after seeing a failure is poor debugging practice because the visible failure may only be a symptom rather than the root cause. Making changes without first reproducing the problem, checking the requirement and gathering evidence can lead to fixing the wrong area, hiding the real defect or introducing new problems. A better approach is to reproduce the failure, compare it with the expected behaviour, form a testable hypothesis, inspect evidence and then make the smallest justified repair.]


Classification responses (1–5, each with reason): [1. Appointment disappears after cancellation — Symptom, because it describes an observed problem without explaining the cause. 2. The data-store removal path is probably being called — Hypothesis/opinion, because it proposes an explanation that requires evidence. 3. The failing test shows store.find_appointment("A1") returns None — Evidence, because it is a concrete observed test result. 4. The service layer is badly designed — Hypothesis/opinion, because it is a broad judgement rather than specific evidence. 5. The traceback points to a line in smartcare/services.py — Evidence of where the failure was observed, but not proof of the root cause.]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [Expected: after cancellation, the same appointment should remain retained and retrievable with status CANCELLED under FR-06 and FR-07 / AC-05.2. Observed: the appointment became CANCELLED but store lookup returned None and service lookup raised LookupError. Reproduction: register P1 and DR1, book A1, cancel A1, then attempt store and service lookup. Hypothesis: SmartCareDataStore.find_appointment() may be excluding cancelled appointments. Evidence to inspect: the lookup condition, list_appointments() membership after cancellation and the difference between store and service lookup.]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [Failure: assert store.find_appointment("A1") is appointment; expected the same retained cancelled appointment, observed None; failing test tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable; call path: regression test → AppointmentService.cancel_appointment() → SmartCareDataStore.find_appointment("A1"); requirement: FR-07 / AC-05.2. Ranked causes: (1) find_appointment() filters CANCELLED appointments — inspect its condition; (2) cancellation removes the appointment — inspect list_appointments(); (3) the stored ID changes or no longer matches — inspect appointment.appointment_id before and after cancellation.]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [Stage 7 verified application baseline SHA 9071ab07b904e9518bf40d605fa741502631cd26; SmartCare A3 Requirements Baseline 2026 revision 2.]
- Baseline test command / working directory / observed result / evidence: [python -m pytest from project/ -> 40 passed in 0.20s before Stage 8 preparation.]
- Clean preparation SHA if a record-only commit followed Stage 7: [Stage 7 evidence-only main SHA 3e95e32. The Stage 8 preparation utility subsequently reported clean baseline Git SHA a43ee399be009eb70dfc25ffaa425cf790c1caae after Pranav's preparation setup.]
- Branch and preparer / how teammates obtained this branch: [debug/stage08; prepared in Sebastian Riches' local repository with tutor support using the supplied Stage 8 preparation utility. The prepared branch was pushed as origin/debug/stage08 and was subsequently available to the group through GitHub and PR #14. Abril Perez reviewed the branch through PR #14. No separate local teammate fetch/checkout of the prepared branch was recorded.]
- Downloaded tool version, source SHA256 and --check outcome: [Stage 8 tool version 1.1. Baseline/source SHA256 reported by the utility: b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375. python prepare_debugging.py project --check reported preflight PASS, baseline Git SHA a43ee399be009eb70dfc25ffaa425cf790c1caae, project unchanged and both proposed fault signatures verified in a temporary copy.]
- --apply and --verify output summaries / artefact references: [python prepare_debugging.py project --apply reported preflight PASS and prepared F8-01 practitioner conflict and F8-02 retained-history lookup. The utility verified the expected failures test_f8_01_conflict and test_f8_02_history (2 failed). python prepare_debugging.py project --verify then reported exactly 2 expected failures with both approved symptom signatures present.]
- Bounded diff inspected and recovery location (not committed): [The preparation utility reported backup/hash metadata in project/.stage8_faults/, with --restore reserved for setup recovery only. Inspection showed the controlled application change was bounded to project/smartcare/data_store.py. Local recovery metadata must not be committed.]
- Prepared faulty-state commit SHA: [76a9a8d (Prepare debug stage 08). This commit contains the controlled Stage 8 changes to project/smartcare/data_store.py.]
- Preparation or recovery issues and resolution, if any: [No preparation or recovery failure was observed. The Stage 8 utility reported successful --check, --apply and --verify results. No --restore recovery was required. A later commit, 3bca0d5, updated .gitignore but did not alter the prepared SmartCare fault code.]
- Initial prepared full-suite command / result / key failures: [python -m pytest -q from project/ -> 7 failed, 33 passed in 0.58s.]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [A second appointment for the same practitioner at the exact same datetime was incorrectly allowed, while an appointment for a different practitioner at that same datetime was incorrectly rejected as a conflict.]
- Expected behaviour and requirement: [Under FR-05 / AC-04.1, an existing SCHEDULED appointment for the same practitioner at the exact same datetime must cause a conflict. Under AC-04.2, a different practitioner at the same datetime must be allowed.]
- Minimal synthetic reproduction steps: [Register a patient and two practitioners. Book A1 for practitioner DR1 at a fixed datetime. Attempt A2 for DR1 at that same datetime and observe that no ValueError is raised. Then attempt a booking for DR2 at the same datetime and observe that a conflict ValueError is incorrectly raised.]
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_01_same_practitioner_exact_time_conflict_is_rejected failed because the second booking for the same practitioner at the exact same datetime did not raise the required ValueError (Failed: DID NOT RAISE <class 'ValueError'>).]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [Inspection of SmartCareDataStore.has_practitioner_conflict() confirmed that the practitioner comparison was reversed. The method used appointment.practitioner.practitioner_id != practitioner_id, causing appointments for different practitioners to be treated as conflicts while failing to detect an existing appointment for the same practitioner. This directly matches the observed failing tests.]
- Smallest justified fix / diff / why other behaviour is preserved: [Changed the practitioner comparison in SmartCareDataStore.has_practitioner_conflict() from != practitioner_id to == practitioner_id. This restores the documented same-practitioner conflict rule while leaving the existing exact-datetime, SCHEDULED-status and excluded-appointment checks unchanged. No unrelated production behaviour was modified.]
- Repair SHA / focused verification result: [58205cee0d2462f08fe830e287e639b50bfd10d1; python -m pytest "tests/test_regressions.py::test_f8_01_same_practitioner_exact_time_conflict_is_rejected" -v from project/ -> 1 passed in 0.11s.]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [After a SCHEDULED appointment is cancelled, the appointment object changes to CANCELLED but subsequent store lookup returns None and service lookup raises LookupError, making the retained appointment appear absent.]
- Expected behaviour and requirement: [FR-06 requires a valid SCHEDULED cancellation to change the same appointment to CANCELLED. FR-07 / AC-05.2 require the cancelled appointment to remain retained and retrievable in the current session, with FR-08 supporting appointment lookup.]
- Minimal synthetic reproduction steps: [Register a patient and practitioner, book appointment A1, cancel A1, confirm its status becomes CANCELLED, then call store.find_appointment("A1") and AppointmentService.find_appointment("A1"). The cancelled appointment should still be returned as the same stored object.]
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable failed because store.find_appointment("A1") returned None instead of the same retained cancelled appointment object.]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [Inspection of SmartCareDataStore.find_appointment() confirmed that the modified method excludes appointments whose status value is "cancelled". The cancelled appointment remains in the store's appointment collection, but find_appointment() returns None for it. The service then interprets that None as absence and raises LookupError, which breaks retained-history lookup.]
- Smallest justified fix / diff / why other behaviour is preserved: [Removed the status-based exclusion from SmartCareDataStore.find_appointment() so that lookup is based on the validated appointment ID regardless of the stored appointment's status. This restores retained-history lookup without changing cancellation, booking, participant registration or other store behaviour.]
- Repair SHA / focused verification result: [5e5cc6ca596446f6183d04b2e1cff6a635acbce8; python -m pytest "tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable" -v from project/ -> 1 passed in 0.17s.]

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
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that pytest might be loading a stale or different copy of the SmartCare package. The actual test run was performed from the intended repository and project/ working directory on debug/stage08 and the inspected data_store.py on that branch contains the reversed comparison that matches the failure. The difference from main is intentional because Stage 8 uses a prepared debugging branch. Classification: Plausible diagnostic check but contradicted by the available evidence. Decision: Reject as the root cause.]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that the booking path might pass an unexpected practitioner ID or use a different datastore instance. The regression test creates one shared SmartCareDataStore, passes it to the services and uses the correct registered practitioner IDs. The failure is already directly explained by the reversed comparison inside has_practitioner_conflict(). Classification: Plausible alternative but not supported by the observed evidence. Decision: Reject as the root cause.]
Final human conclusion and comparison with initial hypothesis: [The final diagnosis confirms the original human hypothesis. F8-01 is caused by the reversed practitioner-ID comparison in SmartCareDataStore.has_practitioner_conflict(): != is used where the conflict rule requires matching the same practitioner. Copilot's first suggestion agreed with the diagnosis, while its stale-import and wrong-ID/store alternatives were not supported by the actual branch, test setup or inspected code.]

### F8-02 Copilot review
Actual prompt / output reference and member: [Sebastian Riches used the required Stage 8 diagnostic prompt in a fresh GitHub Copilot chat after the human-first hypothesis had already been recorded at pre-Copilot commit 02c2138e84774432fb7cbaaa644d3b5a29360004. Copilot returned three ranked diagnostic suggestions.]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot ranked the explicit exclusion of cancelled appointments in SmartCareDataStore.find_appointment() as the most likely cause. Inspection of the running debug/stage08 code confirmed the condition appointment.status.value != "cancelled". The regression test also showed that the appointment had changed to CANCELLED while store.find_appointment("A1") returned None. Classification: Correct. Decision: Accept.]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that cancellation or list_appointments() might remove or filter the appointment. The observed evidence contradicts this as the root cause because the appointment remains retained in the store collection; the failure occurs specifically when find_appointment() applies its status condition. Classification: Plausible diagnostic alternative but not supported by the evidence. Decision: Reject as the root cause.]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [Copilot suggested that the stored appointment ID might no longer match "A1". The appointment was created and retained with ID "A1" and the failure appeared only after cancellation. The inspected find_appointment() status filter directly explains the failed lookup, while no evidence showed the ID changing. Classification: Plausible alternative but not supported by the observed evidence. Decision: Reject as the root cause.]
Final human conclusion and comparison with initial hypothesis: [The final diagnosis confirms the original human hypothesis. F8-02 is caused by SmartCareDataStore.find_appointment() excluding appointments whose status is CANCELLED. The cancelled appointment remains stored but the lookup method returns None, which then causes the service layer to raise LookupError. Copilot's first suggestion agreed with the supported diagnosis, while the removal/filtering and ID-mismatch alternatives were contradicted by the inspected state and code.]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory                                                                                         | Actual result and artefact reference                                                                                                                                                            |
|---|----|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| F8-01 before repair | [6e4a18e0fb4eac929ad7924cb49189dfb80d0c79] | [python -m pytest tests/test_regressions.py -v from project/]                                                         | [test_f8_01_same_practitioner_exact_time_conflict_is_rejected FAILED because the expected ValueError was not raised. Regression-file run: 2 failed in 0.34s.]                                   |
| F8-01 after repair | [58205cee0d2462f08fe830e287e639b50bfd10d1] | [python -m pytest "tests/test_regressions.py::test_f8_01_same_practitioner_exact_time_conflict_is_rejected" -v from project/] | [Passed - 1 passed in 0.11s. The same-practitioner exact-time conflict is now correctly rejected.]                                                                                              |
| F8-02 before repair | [6e4a18e0fb4eac929ad7924cb49189dfb80d0c79] | [python -m pytest tests/test_regressions.py -v from project/]                                                         | [test_f8_02_cancelled_appointment_remains_retrievable FAILED because store.find_appointment("A1") returned None instead of the retained cancelled appointment. Focused run: 2 failed in 0.34s.] |
| F8-02 after repair | [5e5cc6ca596446f6183d04b2e1cff6a635acbce8] | [python -m pytest "tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable" -v from project/] | [Passed - 1 passed in 0.17s. The same cancelled appointment is now retained and retrievable by both store and service lookup.]                                                                  |
| Full suite after both repairs, before refactor | [5e5cc6ca596446f6183d04b2e1cff6a635acbce8] | [python -m pytest from project/]                                                                                                                    | [Passed - 42 passed in 0.26s. Both Stage 8 regression tests also passed together: 2 passed in 0.13s.]                                                                                           |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [The F8-01 regression test requires the second same-practitioner, exact-time booking to raise ValueError and also checks that the original appointment remains stored while the rejected appointment is absent. This detects the reversed practitioner-conflict comparison and protects existing stored state. The F8-02 regression test checks that cancellation returns the same appointment object, changes its status to CANCELLED, keeps it retrievable through both store and service lookup, retains it in current-session history, and continues to reject repeated cancellation with ValueError. These assertions would fail if cancelled history were hidden, replaced or deleted.]
Unrelated failures investigated / resolution: [No unrelated failures remained after the two supported repairs. The complete accumulated suite passed with 42 tests, so no additional product or test defect was identified before refactoring.]

## H. Refactoring decision and before/after verification

Smell and exact location: [Magic status string in SmartCareDataStore.has_practitioner_conflict() in project/smartcare/data_store.py, where the method compares appointment.status.value == "scheduled" instead of using the existing AppointmentStatus enum.]
Small proposed structural change / why justified: [Replace the magic string comparison with appointment.status is AppointmentStatus.SCHEDULED. AppointmentStatus was already imported in data_store.py, so no new import was required. This removes duplicated knowledge of the enum's string value and makes the conflict rule clearer without changing behaviour. The refactor plan was recorded before editing at commit 8ab040c8fd437ca3081a9e216322ad565a126a76.]
External behaviour to preserve / relevant tests: [Same-practitioner exact-time SCHEDULED bookings must still be rejected, different practitioners at the same time must remain allowed, cancelled appointments must not occupy the slot and all existing booking/cancellation/history behaviour must remain unchanged. Relevant protection includes the Stage 8 F8-01 regression test, Stage 7 conflict tests and the full accumulated suite.]
Before result: see G, full passing suite. [Pre-refactor repaired baseline at SHA a414958a63dade9048181b07a0afb8e2a0217208; python -m pytest from project/ -> 42 passed in 0.26s. Stage 8 regression file -> 2 passed in 0.13s.]
Actual change / diff / separate refactor SHA: [Changed the practitioner conflict status check in SmartCareDataStore.has_practitioner_conflict() from the magic string comparison appointment.status.value == "scheduled" to the existing enum comparison appointment.status is AppointmentStatus.SCHEDULED. No other production behaviour was changed. Refactor SHA: 4960649f8052aea3fdfdee5a88c515c36347ab79.]
Focused and full after-refactor commands / working directory / results / evidence: [python -m pytest "tests/test_regressions.py::test_f8_01_same_practitioner_exact_time_conflict_is_rejected" -v from project/ -> 1 passed in 0.13s. python -m pytest tests/test_regressions.py -v from project/ -> 2 passed in 0.16s. python -m pytest from project/ -> 42 passed in 0.31s.]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [Accepted. The refactor removes a magic status string and makes the intent of the practitioner-conflict rule clearer by using the existing AppointmentStatus enum. The focused regression test, both Stage 8 regression tests and the full accumulated suite all remained passing, providing evidence that required external behaviour was preserved.]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [Issue #11 - f8-01 Fix practitioner conflict detection; Issue #12 - F8-02 Restore cancelled appointment lookup; Issue #13 - Refactor practitioner conflict status comparison. All three issues were created by Sebastian Riches and correspond to the two diagnosed Stage 8 defects and the separate behaviour-preserving refactor.]
Branch / prepared, repair and refactor checkpoints: [debug/stage08; prepared faulty-state commit 76a9a8d; F8-01 repair commit 58205cee0d2462f08fe830e287e639b50bfd10d1; F8-02 repair commit 5e5cc6ca596446f6183d04b2e1cff6a635acbce8; passing pre-refactor evidence commit a414958a63dade9048181b07a0afb8e2a0217208; refactor commit 4960649f8052aea3fdfdee5a88c515c36347ab79; refactor-evidence plan commit 8ab040c8fd437ca3081a9e216322ad565a126a76.]
PR link and another member's reviewer identity: [Pull Request #14 — Complete Stage 8 debugging and refactoring; reviewed by Abril Perez.]
Key human feedback, difference from Copilot findings and response/outcome: [Abril Perez reviewed the Stage 8 changes and commented, "I have reviewed this and approve of changes made". No corrective changes were requested. The human review assessed the completed changes for integration, whereas GitHub Copilot had earlier provided diagnostic hypotheses that were independently checked against code and runtime evidence before the repairs were made.]
Actual review approval / merge evidence: [PR #14 received human approval from Abril Perez and was successfully merged and closed into main.]
Integrated code SHA and team pull/retest command / working directory / result: [Integrated main SHA 85534225ee63ce8b0b8e76744bbae5ebe3ca6f20. Sebastian Riches switched to main, pulled the merged result and ran python -m pytest from project/, which reported 42 passed in 0.35s. git status --short from the repository root produced no output. No separate post-merge pull/retest result from the other members has been recorded.]
Evidence-only later SHA / explanation if different: [Not applicable yet. No later evidence-only commit has been made after the integrated Stage 8 verification.]
Each member's substantive contribution and artefact: [Sebastian Riches completed the Stage 8 technical debugging work, including reproducing both controlled defects, recording the human-first hypotheses, creating the two regression tests, evaluating Copilot diagnoses, repairing F8-01 and F8-02, completing the behaviour-preserving refactor, maintaining the Stage 8 evidence record, creating Issues #11–#13 and opening PR #14. Abril Perez completed the required human review and integration of PR #14, approving the changes with the comment "I have reviewed this and approve of changes made". Abril also contributed to completing Sections I and J of the Stage 8 evidence record and assisted with reviewing and incorporating Alexander Scola's formative-question responses into Section K. Alexander Scola contributed the Stage 8 formative-question responses and helped complete the associated learning/evidence component. Prajiet Eswaran assisted in keeping the group on track by checking in through the group chat, confirming that members were progressing toward the required deadline and asking clarifying questions to ensure that each member understood their allocated components of the assignment.]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [For F8-01, Copilot suggested that pytest might be loading a stale or different copy of the SmartCare package. This initially sounded convincing because Copilot noticed that the main version of data_store.py contained the correct == comparison while the prepared debugging version contained !=. However, this explanation lacked evidence for the actual failing run. Inspection showed that the tests were intentionally running on the prepared debug/stage08 branch, where the reversed comparison was present. The stale-import explanation was therefore rejected.]
2. What evidence changed your group's view? [The most important evidence came from the actual failing regression tests and direct inspection of the prepared data_store.py. F8-01 showed that the same practitioner at the same time was incorrectly allowed while a different practitioner was rejected, and inspection confirmed the reversed != practitioner comparison. F8-02 showed that a cancelled appointment remained an object with CANCELLED status but lookup returned None, and inspection confirmed that find_appointment() explicitly filtered out cancelled appointments. This runtime and code evidence allowed the group to distinguish supported causes from plausible but unsupported alternatives.]
3. How did regression tests protect the refactoring? [The Stage 8 regression tests captured the required behaviours that had previously failed. Before refactoring, both regression tests passed and the full suite reported 42 passing tests. After replacing the magic "scheduled" status string with AppointmentStatus.SCHEDULED, the focused F8-01 test still passed, both Stage 8 regression tests still passed, and the full suite again passed with 42 tests. This provided evidence that the structural change improved clarity without changing required external behaviour.]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [First reproduce and observe the failure, identify the expected behaviour from the approved requirement or contract, inspect the relevant evidence and form a testable hypothesis before changing the code]

2. Where should expected behaviour come from during debugging?

Response: [Expected behaviour should come from the approved requirements, acceptance criteria and documented public contracts, rather than assumptions or simply copying what the current code does]

3. What is a debugging hypothesis?

Response: [A debugging hypothesis is a testable proposed explanation for why an observed failure is occurring. Evidence should then be gathered to support or reject it.]

4. What is a regression test and why is it retained?

Response: [A regression test checks required behaviour, particularly behaviour associated with a previous defect. It is retained so future changes can detect if the same defect or another related problem is introduced again.]

5. What is meant by root cause?

Response: [The root cause is the underlying code or design decision that explains why the observed failure occurs, rather than only the location where the symptom appears]

6. What is refactoring?

Response: [Refactoring is changing the internal structure of working code to improve qualities such as readability or maintainability without changing its required external behaviour]

7. What is a swallowed exception?

Response: [A swallowed exception occurs when an exception is caught but then ignored or hidden instead of being handled or reported appropriately. This can make failures difficult to diagnose and may make the program appear to succeed when an error actually occurred.]

8. What is a code smell?

Response: [A code smell is a sign in the code that suggests a possible structural or maintainability problem, such as duplicated logic, magic strings, unclear naming or excessive complexity]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [Copilot-generated diagnoses should be treated as hypotheses or suggestions. They must be checked against the actual requirements, code, failing tests and runtime evidence before they are accepted, modified or rejected.]

10. What is the Stage 8 engineering rule?

Response: [Diagnose before fixing: reproduce the failure, use the requirements to define expected behaviour, record a human hypothesis, gather evidence to identify the root cause, make the smallest justified repair, retain regression tests and verify that any later refactoring preserves behaviour.]

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [Final Stage 8 evidence-only commit not yet created. The final submitted repository SHA will differ from the tested integrated code SHA only because the Stage 8 evidence record is being completed; no further project code changes are intended.]
Unresolved issues or incomplete checks / owner / next action: [No unresolved Stage 8 product defects or failing tests remain. Sebastian Riches will commit the completed Stage 8 evidence record, verify that the project code is unchanged from the tested integrated SHA, confirm the working tree is clean and then complete the Stage 9 handover.]
Handover note: [Stage 8 debugging and refactoring are functionally complete. Both controlled defects were reproduced, diagnosed and repaired with retained regression tests. One behaviour-preserving refactor was verified, PR #14 received human approval from Abril Perez and was merged into main, and the integrated full suite passed with 42 tests. After the final evidence-only record commit and verification, the same project will be ready to continue to Stage 9.]
