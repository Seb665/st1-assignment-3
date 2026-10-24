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

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
