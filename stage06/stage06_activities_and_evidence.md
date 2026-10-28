# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [Group 3, Thursday tutorial 2:30 - 4:30]
- Members, GitHub usernames and cohorts: [Sebastian Riches Seb665 UG, Prajiet Eswaran Prajiet103 UG, Alexander Scola u3324662-Personal UG, Abril Perez u334202]
- Repository URL: [https://github.com/Seb665/st1-assignment-3/blob/main/stage06/stage06_activities_and_evidence.md?plain=1]
- Starting SHA: [...]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: [Implement patient lookup by ID]
- Context: [Clinic staff need to be able to retreive an existing patient using their patient ID. The lookup should return the patient already stored in SmartCare and clearly distinguish between an invalid ID and a valid ID that does not belong to a registered patient.]
- Requirement: [Find a patient by patient ID.]
- Acceptance criteria: [A known patient ID returns the actual registered Patient object, surrounding whitespace in a valid ID is handled according to the existing ID validation rules, patient IDs remain case-sensitive, a blank or invalid ID raises ValueError, a valid but unknown patient ID raises LookupError, Lookup does not create or replace patient records.]
- Scope: [Implement PatientService.find_patient(patient_id) using the existing SmartCareDataStore. Add focused tests for valid, invalid and unknown patient IDs. Do not change unrelated patient fields, introduce new search methods, add persistence or modify the overall architecture.]
- Definition of Done: [Definition of Done: find_patient() returns the actual stored patient for a known ID, handles invalid and unknown IDs with the correct exceptions and passes focused tests. Existing tests remain passing, the change is reviewed by another team member through a PR, any feedback is resolved and the relevant evidence is recorded in the Stage 6 record.]
- Owner: [Sebastian Riches]
- Actual issue link: [https://github.com/Seb665/st1-assignment-3/issues/1]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: [Implement appointment cancellation with retained history]
- Context: [Clinic staff need to be able to cancel a scheduled appointment without removing its record from SmartCare. The cancelled appointment should remain available in the current session so its history can still be retrieved.]
- Requirement: [FR-06 - Cancel only a SCHEDULED appointment. FR-07 - Retain the same appointment with CANCELLED status in current-session history.]
- Acceptance criteria: [Cancelling a SCHEDULED appointment changes its status to CANCELLED, the cancellation operation returns the same stored Appointment object, the cancelled appointment remains stored and retrievable during the current session, attempting to cancel the same appointment again raises ValueError and does not change its state, attempting to cancel the same appointment again raises ValueError and does not change its state, attempting to cancel a COMPLETED appointment raises ValueError and does not change its state, a valid but unknown appointment ID raises LookupError, a blank or invalid appointment ID raises ValueError.]
- Scope: [Implement AppointmentService.cancel_appointment(appointment_id) using the existing SmartCareDataStore and Appointment cancellation operation. Add focused tests for successful cancellation, retained history, invalid or unknown IDs and illegal cancellation attempts. Do not delete appointments, create replacement Appointment objects, directly change protected status fields, add persistence or modify unrelated booking behaviour.]
- Definition of Done: [cancel_appointment() correctly cancels a stored SCHEDULED appointment and returns the same object while preserving it in session history. Invalid, unknown, repeated and illegal cancellation attempts produce the required errors without unintended state changes. Focused tests and the exsiting test suite pass, the change is reviewed through a PR, feedback is resolved and the Stage 6 evidence is recorded.]
- Owner: [Sebastian Riches]
- Actual issue link: [https://github.com/Seb665/st1-assignment-3/issues/3]

## B Commit quality

| Original example | Strong or Weak | Reason                                                                                                                                                 |
|---|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| changes | [Weak]         | [It does not explain what was changed or why, so another team member cannot understand the prupose of the commit without inspecting the diff.]         |
| final version | [Weak]         | [It does not describe the actual engineering change and is also misleading because further changes may still be required.]                             |
| Add patient search by ID | [Strong]       | [It clearly identifies the specific behaviour added, making the purpose of the commit easy to understand and trace to the patient search requirement.] |
| fix stuff | [Weak]         | [It is vague and does not identify what problem was fixed, which makes the commit difficult to review or trace later.]                                 |
| Prevent cancellation of completed appointments | [Strong]      | [It describes a specific behaviour change and makes clear what rule the commit is reinforcing.]                                                        |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [The PR contains changes that are unrelated to appointment cancellation. This makes the change larger than necessary and makes it harder to understand exactly what is required for FR-06 and FR-07.]
- Responsibility and architecture concerns: [Restructuring unrelated code or changing patient fields could affect other parts of SmartCare without being required for the cancellation feature. Adding a new dependency may also introduce unnecessary complexity when the existing domain, service and data-store structure already supports the required behaviour.]
- Testing and review concerns: [A larger PR is harder to review because the reviewer has to separate the cancellation changes from unrelated modifications. Passing tests alone would not prove that the unrelated changes are safe or necessary, so each change would need to be checked against its own requirements and responsibilities.]
- Changes to remove or separate, with reasons: [The unrelated patient-field renaming, code restructuring and new dependency should be removed from the cancellation PR. If any of these changes are genuinely required, they should be handled as separate focused issues and PRs so they can be reviewed, tested and justified independently. The cancellation PR should contain only the changes needed to satisfy FR-06 and FR-07 and their related tests.]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [The review does not identify which requirements were checked, which tests were actually run, whether the implementation follows the intended responsibilities, whether the assertions are meaningful or whether unrelated changes are present in the diff.]
- Follow-up review question 1: [Which specific requirement and acceptance criteria does this implementation satisfy and what code in the diff supports that conclusion?]
- Follow-up review question 2: [Which tests were actually run, what was the observed result and do those tests check the required behaviour rather than only confirming that an object exists?]
- Follow-up review question 3: [Does the implementation preserve the intended responsibility boundaries between the domain object, service and data store? If not, identify the relevant lines.]
- Follow-up review question 4: [Are invalid, unknown and illegal-state cases handled with the correct exceptions and is stored state unchanged after a rejected operation?]
- Follow-up review question 5: [Does the diff contain any unrelated changes, unnecessary dependencies or modifications outside the issue scope that should be removed or separated?]
- Additional questions if useful: [Does cancellation return and retain the same stored Appointment object rather than deleting or replacing it? Are any assumptions being made that are not stated in the SmartCare requirements?]

## E Team workflow agreement

| Practice | Team agreement                                                                                                                                                                                               |
|---|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Branch naming | [Feature work will use clear branch names describing the task, such as feature/patient-search and feature/appointment-cancellation. Initial repository/setup work may already exist on main.]                |
| Commit message convention | [Use short, specific commit messages that describe the engineering change, perferably using an action such as Add, Fix, Prevent or Test. Avoid vague messages such as changes or 'fix stuff'.]               |
| PR size | [Keep each pull request focused on one issue or closely related requirement. Avoid unrelated refactoring, dependencies or feature changes in the same PR.]                                                   |
| Another-member review requirement | [Each feature PR should be reviewed by another group member before merge. If another member remains unavailable, this will be raised with the tutor and recorded honestly rather than fabricating a review.] |
| Merge rule | [Merge feature work ino main only after the acceptance criteria and relevant tests are satisfied, review feedback is addressed and the required review has been obtained where possible.]                    |
| Significant Copilot disclosure rule | [Record significnt GitHub Copilot assistance, inclduing the task or prompt, output summary, human check, Accept/Modify/Reject decision and verification evidence.]                                           |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement                                                                     | Owner              | Acceptance criteria or precise link                                                                                                                                                                                  | Status                          |
|----|---------------------------------------------------------------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| [https://github.com/Seb665/st1-assignment-3/issues/1] | [FR-02 - Find a patient by patient ID]                                          | [Sebastian Riches] | [Known patient ID returns the actual registered Patient object; blank/invalid ID raises ValueError; valid unknown ID raises LookupError; IDs are trimmed and remain case-sensitive.]                                 | [Drafted - issue to be created] |
| [https://github.com/Seb665/st1-assignment-3/issues/2] | [FR-03 supporting operation - Practitioner lookup]                              | [Sebastian Riches]  | [Known practitioner ID returns the actual registered Practitioner object; blank/invalid ID raises ValueError; valid unknown ID raises LookupError; IDs are trimmed and remain case-senstitive.]                      | [Drafted - issue to be created] |
| [https://github.com/Seb665/st1-assignment-3/issues/3] | [FR-06 - Cancel only a SCHEDULED appointment; FR-07 - Retain cancelled history] | [Sebastian Riches]  | [Cancelling a SCHEDULED appointment changes the same stored object to CANCELLED and keeps it retrievable. Repeated or illegal cancellation raises ValueError without changing state; unknown ID raises LookupError.] | [Drafted - issue to be created] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [PR#4 - Add patient search by ID - https://github.com/Seb665/st1-assignment-3/pull/4]
- Linked issue and requirement: [Issue #1 - implement patient lookup by ID; FR-02 - Find a patient by patient ID]
- Feature branch: [feature/patient-search]
- Changed behaviour: [PatientService.find_patient() now returns the actual registered Patient object for a known ID, accepts surrounding whitespace according to the existing validation rules, preserves case-sensitive IDs, raises ValueError for blank/invalid IDs and raises LookupError for a valid unknown ID.]
- Meaningful commits: [840ed898853f33078ea8a71bd5da27a39c4db870 - Add patient search by ID]
- Test command, directory and observed result: [From project/:python -m pytest tests/test_services.py -q -> 5 passed in 0.04s. python -m pytest -q -> 13 passed in 0.08s. Tested code SHA: 840ed898853f33078ea8a71bd5da27a39c4db870.]
- Another-member reviewer: [Prajiet Esawaran - Prajiet103]
- Human observations recorded before Copilot: [Prajiet reviewed the implementation and stated that the classes and implementation looked good and that the patient lookup code appeared solid.]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [The reviewer didd not identify any problems with the implementation or class responsibilities. No changes were requested.]
- Key feedback: [No corrective changes requested. Reviewer considered the implementation solid.]
- Author response/change and verification: [Pending review feedback.]
- Reviewer recheck and approval: [PR #4 approved by Prajiet103 - https://github.com/Seb665/st1-assignment-3/pull/4#pullrequestreview-5661468057]
- Merge outcome and SHA: [PR #4 merged successfully into main. Integrated main SHA: 539cd8f8d5aab6fe4670bd35f0baf04c5f77ba9a.]
- Significant Copilot assistance: [None used for the implementation.]
- Linked issue closure: [Issue #1 closed through the merged PR.]
- Each member updated main: [Pending merge.]
- Integrated verification after merge: [From project/, python -m pytest -q -> 13 passed in 0.11s at SHA 539cd8f8d5aab6fe4670bd35f0baf04c5f77ba9a.]

- PR link and title: [PR#5 - Add practitioner search by ID - https://github.com/Seb665/st1-assignment-3/pull/5]
- Linked issue and requirement: [Issue #2 - FR-03 supporting practitioner lookup]
- Feature branch: [feature/practitioner-search]
- Changed behaviour: [PractitionerService.find_practitioner() now returns the actual registered Practitioner object for a known ID, accepts surrounding whitespace according to the existing validation rules, preserves case-sensitive IDs, raises ValueError for blank/invalid IDs and raises LookupError for a valid unknown ID.]
- Meaningful commits: [d21b085 - Add practitioner search by ID]
- Test command, directory and observed result: [From project/: python -m pytest tests/test_services.py -q -> 10 passed. python -m pytest -q -> 18 passed. Tested code SHA: d21b085.]
- Another-member reviewer: [Alexander Scola - u3324662-Personal]
- Human observations recorded before Copilot: [Alex reviewed the practitioner-search changes and stated: "The changes provide function to required features."]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [The reviewer did not identify any problems with the implementation. No changes were requested.]
- Key feedback: [No corrective changes requested. Alex approved the implementation as providing the required functionality.]
- Author response/change and verification: [No code changes were required following the human and Copilot reviews. The integrated version was verified after merge with 18 passing tests.]
- Reviewer recheck and approval: [PR #5 approved by Alexander Scola - u3324662-Personal - https://github.com/Seb665/st1-assignment-3/pull/5]
- Merge outcome and SHA: [PR#5 merged successfully into main. Integrated main SHA: c3be270c61525548195f4b9aff746a9582a6984c.]
- Significant Copilot assistance: [Github Copilot was used after the human review to review PR#5 against the stated practitioner lookup requirements. Its review was evaluated by Sebastian and recorded as Modify; no code changes were required.]
- Linked issue closure: [Issue #2 closed through the merged PR.]
- Each member updated main: [Sebastian updated local main after the merge. Other members not independently verified.]
- Integrated verification after merge: [From project/, python -m pytest -q -> 18 passed in 0.22s at SHA c3be270c61525548195f4b9aff746a9582a6984c.]

PR link and title: [PR#6 - Add appointment cancellation and retained history - https://github.com/Seb665/st1-assignment-3/pull/6]
- Linked issue and requirement: [Issue #3 - FR-06 appointment cancellation and FR-07 retained history]
- Feature branch: [feature/appointment-cancellation]
- Changed behaviour: [AppointmentService.cancel_appointment() now retrieves the existing stored appointment, raises LookupError for a valid unknown appointment ID, uses the existing Appointment.cancel() domain method to enforce valid state transitions, returns the same Appointment object after cancellation and retains it in current-session history with CANCELLED status.]
- Meaningful commits: [5a52510 - Add appointment cancellation and retaiened history]
- Test command, directory and observed result: [From project/: python -m pytest tests/test_services.py -q -> 15 passed. python -m pytest -q -> 23 passed. Tested code SHA: 5a52510.]
- Another-member reviewer: [April Perez - 4brila1816-coder]
- Human observations recorded before Copilot: [April reviewed and approved the appointment-cancellation cahnges.]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [The reviewer did not identify any problems with the implementation. No changes were requested.]
- Key feedback: [No corrective changes requested. April approved the pull request.]
- Author response/change and verification: [No code changes were required following the human and Copilot reviews. The integrated version was verified after merge with 23 passing tests.]
- Reviewer recheck and approval: [PR #6 approved by April Perez - 4brila1816-coder - https://github.com/Seb665/st1-assignment-3/pull/6]
- Merge outcome and SHA: [PR#6 merged successfully into main. Integrated main SHA: 76e815c03416a03e7bb111d62b3fedca23782867.]
- Significant Copilot assistance: [Github Copilot was used after the human review to review PR#6 against FR-06 and FR-07. Its review was evaluated by Sebastian and recorded as Modify; no code changes were required.]
- Linked issue closure: [Issue #3 closed through the merged PR.]
- Each member updated main: [Sebastian updated local main after the merge. Other members not independently verified.]
  - Integrated verification after merge: [From project/, python -m pytest -q -> 23 passed in 0.14s at SHA 76e815c03416a03e7bb111d62b3fedca23782867.]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [Sebastian Riches - Github Copilot review of PR #4, patient lookup implementation.]
- Prompt/purpose and relevant issue/diff: [Copilot was asked to review the actual FR-02 patient lookup implementation and tests against the requirement, acceptance, criteria, SmartCare responsibilities and observed test evidence after the human review had already been completed.]
- Summary of output: [Copilot found no critical issues and considered the implementation broadly consistent with FR-02. It correctly identified that validation and whitespace handling are delegated to SmartCareDataStore, but raised this as an important concern. It also suggested additional testing for malformed non-blank IDs and explicit no-mutation behaviour. Copilot considered the implementaiton focused, maintainable and consistent with the service responsibilities.]
- Human check against actual code, requirements and tests: [The datastore contract was checked and confirms that find_patient() already validates and trims the ID through the supplied required_text() logic. The published ID contract requires strings that are trimmed, non-blank and case-sensitive; it does not define an additional malformed-ID format. The existing tests cover known lookup, whitespace handling, unknown IDs, blank IDs and case sesitivity, including object identity.]
- Decision — Accept / Modify / Reject: [Modify]
- Reason: [Copilot's overall review was useful, however its concerns required human interpretation. The suggestion to confirm datastore validation was useful and was verified. The claim that service-level validation was potentially missing was rejected because delegation to the datastore is the intended architecture. The suggested malformed non-blank ID test was rejected because no such format rule exists. The no-mutation test suggestion was teated as optional rather than required. The positive maintainability assessment was accepted.]
- Verification/evidence: [Human inspection confirmed that SmartCareDataStore.find_patient() performs the published ID validation and returns the stored object or None. Focused tests passed: 5 passed in 0.04s. Full suite passed: 13 passed in 0.08s. Tested SHA: 840ed898853f33078ea8a71bd5da27a39c4db870.]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [Prajiet reviewed the classes and patient lookup implementation and considered the implementation solid. He formally approved PR #4 and did not request any changes.]
- Copilot noticed: [Copilot also found the implementation broadly correct and maintainable but questioned whether datastore validation was sufficient and suggested additional tests for malformed non-blank IDs and explicit no-mutation behaviour.]
- Overlap: [Both the human reviewer and Copilot considered the implementation focused and consistent with the intended SmartCare structure and neither identified a critical defect.]
- What did the human reviewer notice that Copilot did not: [The human reviewer accepted the implementation as suitable within the existing project structure without treating the intentional datastore delegation as a problem.]
- What did Copilot identify that the human reviewer initially missed: [Copilot prompted an explicit check that SmartCareDataStore performs trimming and validation and suggested considering stronger regression evidence for non-mutation.]
- Unsupported or incorrect Copilot suggestion: [Copilot suggested testing malformed non-blank patient IDs but the published contract does not define an additional ID format beyond string, trimmed, non-blank and case-sensitive. This suggestion was therefore not adopted.]
- Human judgement accepted, modified or rejected, and why: [The Copilot review was modified. Its suggestion to verify datastore validation was accepted as a useful check, however no implementation change was required because the datastore already owns that validation. The malformed-ID suggestion was rejected because it introduced an unstated rule, while the no-mutation suggestion was treated as optional.]
- Which evidence justified merge approval: [The implementation satisfies FR-02 using the existing datastore responsibility, returns the actual registered Patient object and handles the required error cases. The focused suite passed 5 tests and the cumulative suite passed 13 tests at SHA 840ed898853f33078ea8a71bd5da27a39c4db870. PR #4 was independently reviewed and approved by Prajiet103 and the subsequent Copilot review identified no Critical defect.]



- Member and task: [Sebastian Riches - Github Copilot review of PR #5, practitioner lookup implementation.]
- Prompt/purpose and relevant issue/diff: [Copilot was asked to review the actual FR-03 supporting practitioner lookup implementation and tests against the stated requirement, SmartCare responsibilities, scope and observed test evidence after the human review had already been completed.]
- Summary of output: [Copilot found no critical or important issues and considered the implementation consistent with the stated pracitioner lookup requirements. It found the change narrowly scoped and considered the service and datastore responsibilities to be preserved. Copilot suggested one optional improvement: adding an explicit test to demonstrate that practitioner lookup does not insert or update datastore records.]
- Human check against actual code, requirements and tests: [The implementation was checked against the actual code and requirements. PracitionerService.find_practioner() delegates validation and retrieval to SmartCareDataStore.find_practitioner(), which is consistent with the existing project design. The focused tests cover known practitioner lookup, surrounding whitespace, unknown IDs, blank IDs, case sensitivity and returning the actual registered Practitioner object. Copilot's statement that the service validates and looks up the ID was adjusted because validation and retrieval are actually delegated to the datastore.]
- Decision — Accept / Modify / Reject: [Modify]
- Reason: [Copilot's overall conclusion that the implementation was correct, focused and non-blocking was accepting. Its description of the service/datastore responsibility split was modified to reflect the actual implementation where the datastore performs the existing ID validation and retrieval. The optional no-mutation test was considered useful as additional evidence but was not adopted because the stated requirements do not require a separate mutation test and the implementation performs only a lookup.]
- Verification/evidence: [Focused service tests passed: 10 passed. Full regression suite passed: 18 passed. Tested SHA: d21b085. Human review was completed first by Alexander Scola, who approved PR#5 and stated: "The changes provide function to required features."]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [Alex reviewed the practitioner lookup and approved it, stating that "The changes provide function to required features." No further changes were requested.]
- Copilot noticed: [Copilot found no critical or important issues and considered the practitioner lookup correct, narrowly scoped and consistent with the stated requirements. It also suggested an optional explicit test to demonstrate that lookup does not insert or update datastore records.]
- Overlap: [Both Alex and Copilot considered the practitioner lookup to provide the required functionality. Neither identified a critical defect.]
- What did the human reviewer notice that Copilot did not: [Alex directly assessed the implemented feature and approved it as providing the required functionality within the existing project.]
- What did Copilot identify that the human reviewer initially missed: [Copilot prompted a more explicit examination of the service and datastore responsibility split and suggested that an additional no-mutation test could provide stronger evidence, although it treated this as optional.]
- Unsupported or incorrect Copilot suggestion: [Copilot described the responsibility split as the service validating and looking up the practitioner ID while the datastore owns storage and retrieval. In the actual implementation, PractitionerService.find_practitioner() delegates both the existing ID validation and retrieval to SmartCareDataStore.find_practitioner(). This description was therefore corrected during the human check.]
- Human judgement accepted, modified or rejected, and why: [The Copilot review was modified. Its overall conclusion that the implementation was correct, focused and non-blocking was accepted. Its description of the validation responsibility was corrected to reflect the actual project design. The optional no-mutation test suggestion was considered useful but was not required by the stated Stage 6 contract and was therefore not adopted.]
- Which evidence justified merge approval: [PR#5 was independently reviewed and approved by Alexander Scola. The focused service suite passed 10 tests and the full regression suite passed 18 tests at tested commit d21b085. The implementation returns the actual registered Practitioner object, preserves the required ID behaviour and uses the existing SmartCareDataStore responsibility. Copilot identified no critical or important defects.]


Member and task: [Sebastian Riches - Github Copilot review of PR #6, appointment cancellation and retained-history implementation.]
- Prompt/purpose and relevant issue/diff: [Copilot was asked to review the actual FR-06 and FR-07 appointment cancellation implementation and tests against the stated requirements, SmartCare responsibilities, state-preservation rules, scope and observed test evidence after the human review had already been completed.]
- Summary of output: [Copilot found no critical or important issues and concluded that the implementation satisfies FR-06 and FR-07. It confirmed that cancellation is performed through Appointment.cancel(), only SCHEDULED appointments can be cancelled, the same stored Appointment object is retianed with CANCELLED status, repeated and COMPLETED cancellation are rejected, unknown IDs raise LookupError and blank/invalid IDs raise ValueError. Copilot also considered the change narrowly scoped. It suggested one Optional improvement: adding another explicit assertion that a failed cancellation leaves the datastore appointment list unchanged.]
- Human check against actual code, requirements and tests: [The review was consistent with the actual implementation and requirements. AppointmentService.cancel_appointment() retrieves the existing appointment, delegates the state-transition to Appointment.cancel() and returns the same object without deleting or replacing it. The tests verify cancellation, retained identity and history, repeated cancellation rejection, unknown and blank IDs and COMPLETED state preservation. Copilot's reference to the datastore owning "persistence" was corrected because SmartCare uses session-only-in-memory storage and does not implement persistence.]
- Decision — Accept / Modify / Reject: [Modify]
- Reason: [Copilot's overall assessment was accepted because it correctly identified that the implementation satisfies FR-06 and FR-07, preserves the intended responsibilities and contains no blocking defects. Its use of the term "persistence" was modified to "session-only-in-memory storage/retention" to remain consistent with the assignment's requirements. The oprtional extra datastore-list assertion was considered but not adopted becuase the existing tests already verify retained object identity, history and unchanged state after rejected transitions. ]
- Verification/evidence: [Focused service tests passed: 15 passed. Full regression suite passed: 23 passed. Commit: 5a52510. Human review was completed first by April Perez, who approved PR#6 without requesting changes.]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [April Perez reviewed the appointment-cancellation pull request and approved PR#6. No corrective changes were requested.]
- Copilot noticed: [Copilot found no critical or important issues and confirmed that cancellation uses Appointment.cancel(), preserves the same stored object, retains CANCELLED history, rejects repeated and COMPLETED cancellation and handles invalid and unknown IDs using the required exception behaviour. It also suggested an optional additional assertion that a rejected cancellation leaves the datastore appointment list unchanged.]
- Overlap: [Both April and Copilot considered the appointment-cancellation implementation acceptable and neither identified a blocking defect or requested a code change.]
- What did the human reviewer notice that Copilot did not: [April assessed and approved the implemented change as a member of the group before any Copilot review was consulted.]
- What did Copilot identify that the human reviewer initially missed: [Copilot provided a more detailed check of the domain, service and datastore responsibility split and explicitly considered state preservation for repeated and COMPLETED cancellation. It also suggested an optional additional assertion for unchanged datastore-list contents.]
- Unsupported or incorrect Copilot suggestion: [Copilot referred to the datastore as owning "persistence". SmartCare does not implement persistence; the datastore retains objects only in memory for the current program session. This terminology was corrected during the human evaluation. The otpional additional list assertion was not incorrect but it was not required since the existing tests already provide meaningful retained-history and state-preservation evidence.]
- Human judgement accepted, modified or rejected, and why: [The Copilot review was modified. Its conclusion that the implementation satisfies FR-06 and FR-07 and contains no blocking defects was accepted. The persistence terminology was corrected to session-only in-memory storage/retention. The optional additional test assertion was considered but not adopted since the existing test suite already verifies the required behaviour.]
- Which evidence justified merge approval: [PR#5 was independently reviewed and approved by April Perez. The focused service suite passed 15 tests and the full regression suite passed 23 tests at tested commit 5a52510. The implementation uses Appointment.cancel(), returns and retains the same stored Appointment object and correctly rejects invalid state transistions. Copilot identified no critical or important defects.]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [Sebastian Riches - Seb665]
- Implementation: [Implemented all three Stage 6 service operations: PatientService.find_patient(), PractitionerService.find_practitioner() and AppointmentService.cancel_appointment() through focused feature branches and pull requests.]
- Testing: [Created and extended project/tests/test_services.py with tests for patient and practitioner lookup, invalid and unknown IDs, object identity, cancellation, retianed history, repeated cancellation and COMPLETED-state rejection. Ran focused and full regression tests throughout Stage 6. Final integrated result: python -m pytest -q -> 23 passed in 0.14s at SHA 76e815c03416a03e7bb111d62b3fedca23782867.]
- Review: [Checked human-review feedback and then evaluated GitHub Copilot review output against the actual requirements, code and test evidence. Recorded Accept/Modify/Reject decisions rather than treating Copilot output as approval.]
- Issue refinement: [Created and refined issue #1 for FR-02 patient lookup, issue #2 for the supporting FR-03 practitioner lookup and issue #3 for FR-06/FR-07 appointment cancellation and retained history, including acceptance criteria and scope.]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [Corrected an indentation problem in the practitioner service tests, reran the affected tests, integrated each approved pull request into main and reran the full regression suite after merging.]
- Documentation or team support: [Maintained the Stage 6 evidence record, including issue, branch, commit, PR, reviewer, Copilot and integration evidence and coordinated the feature/review workflow across the three Stage 6 changes.]

Member: [Prajiet Eswaran - Prajiet103]
- Implementation: [...]
- Testing: [...]
- Review: [Independently reviewed PR#4 for the FR-02 patient lookup before the Copilot review. Commented that the classes and implementation looked good and that the patient lookup appeared solid and approved the PR without requesting changes.]
- Issue refinement: [...]
- Design and responsibility discussion: [Reviewed the patient lookup implementation and its use of the existing classes as part of PR#4.]
- Debugging or integration: [...]
- Documentation or team support: [Provided the required human review and approval for PR#4.]

Member: [Alexander Scola - u3324662]
- Implementation: [...]
- Testing: [work and evidence]
- Review: [Independently reviewed PR#5 for the supporting practitioner lookup before the Copilot review. Stated that "The changes provide function to required features" and formally approved the PR without requesting changes.]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [Reviewed the practitioner lookup implementation through PR#5 and assessed whether the change provided the required functionality.]
- Debugging or integration: [...]
- Documentation or team support: [Provided written responses for the Stage 6 exit question in Section K and drafted responses to all ten Stage 6 formative questions in Section L. Also provided the required another member human review and approval for PR#5.]

Member: [April Perez - 4brila1816-coder]
- Implementation: [...]
- Testing: [Independently reviewed PR#6 for FR-06 appointment cancellation and FR-07 retained history before the Copilot review and formally approved the PR without requesting corrective changes.]
- Review: [Independently reviewed PR#6 for FR-06 appointment cancellation and FR-07 retained history before the Copilot review and formally approved the PR without requesting corrective changes.]
- Issue refinement: [...]
- Design and responsibility discussion: [Reviewed the appointment cancellation change through PR#6. No separate design discussion was recorded.]
- Debugging or integration: [No separate debugging or integration activity recorded.]
- Documentation or team support: [Provided the required human review and approval for PR#6.]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[A high commit count does not necessarily show strong contribution because the commits could be very small, unclear or unnecessary. Strong contribution is better shown through meaningful implementation, testing, review, problem solving and evidence that the work actually meets the requirements.]

## L Stage 6 formative questions

1. What is version control?

[Version control is a system that records changes made to files over time. It allows developers to track who changed something, compare versions and recover earlier work if necessary.]

2. Why is a feature branch useful?

[A feature branch allows a developer to work on one focused change without directly changing the stable main branch. The work can then be tested and reviewed before it is merged into main.]

3. What makes a commit a good engineering commit?

[A good engineering commit contains a clear and coherent change and uses a message that explains what was changed. It should be focused enough that another developer can understand and review its purpose.]

4. What is a pull request?

[A pull request is a request to merge changes from one branch into another, usually into main. It allows the changes and Git diff to be reviewed and discussed before they are integrated.]

5. What is the purpose of code review?

[Code review checks whether a change meets the requirements, follows the intended responsibilities, has suitable tests and does not introduce unrelated or incorrect changes. It also allows another developer to provide feedback before the work is merged.]

6. What does a Git diff show?

[A Git diff shows the differences between versions of files, including lines that were added, removed or unchanged. It helps developers inspect exactly what has changed before committing, reviewing or merging work.]

7. What is a Definition of Done?

[A Definition of Done describes the conditions that must be satisfied before work can be considered complete. In Stage 6 this includes more than writing code, such as meeting the requirement, meaningful tests, review, resolved feedback and appropriate evidence.]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[GitHub Copilot can act as a review assistant by identifying possible problems, missing tests or questions that should be investigated. Its suggestions are not proof, so a human must check them against the actual requirements, code, diff and observed test results before accepting, modifying or rejecting them.]

9. Why should individual contribution not be judged only by commit count?

[Commit count does not show the quality or importance of the work. A person may make fewer commits but contribute significant implementation, testing, debugging, review or design work. Contribution should be judged using the actual engineering evidence and the value of the work completed.]

10. What is the Stage 6 engineering rule?

[Take a requirement through a focused and traceable engineering process: define the issue, make the change on a branch, test it, review the actual diff, respond to feedback, verify the result and only then integrate it into main.]

## M Completion and handover

- Starting SHA: [1534cb73c50605ed7990b5c414699975947c0e01]
- Final Stage 6 code SHA: [76e815c03416a03e7bb111d62b3fedca23782867]
- Test command: [python -m pytest -q]
- Working directory: [project/]
- Observed result: [23 passed in 0.14s]
- PR and another-member reviewer: [PR#4 - patient lookup - reviewed and approved by Prajiet Esawaran (Prajiet103); PR#5 - practitioner lookup - reviewed and approved by Alexander Scola (u3324662-Personal); PR#6 - appointment cancellation and retained history - reviewed and approved by April Perez (4brila1816-coder).]
- Unresolved issue or none: [No known unresolved Stage 6 product-code defects. Confirmation that every other group member pulled the final main and independently reran the integrated checks has not been recorded.]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [The tested Stage 6 code SHA is 76e815c03416a03e7bb111d62b3fedca23782867. A later evidence-only commit will contain the completed Stage 6 record; its SHA cannot be written into this file before that commit exists.]

- [x] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [x] Feature work reviewed by another member using the actual diff.
- [x] Human-first review and required Copilot comparison recorded.
- [x] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [x] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
