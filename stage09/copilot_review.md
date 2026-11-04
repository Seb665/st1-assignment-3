## Stage 9 GitHub Copilot review evidence

### Initial review

The first Copilot review incorrectly inspected the earlier repository commit:

49bf24b8327239602b1019beb72c4d00fa960420

It therefore reported that the Stage 9 query functions, service listing and interactive menu were still unimplemented. This response was rejected because it did not represent the current Stage 9 branch.

### Corrected review prompt

The review was restarted in a new Copilot chat and supplied with the following context:

Please review the CURRENT checked-out branch and CURRENT working tree, not commit 49bf24b8327239602b1019beb72c4d00fa960420.

The current Stage 9 checkpoint is:

950275f1c59cc44841ae917d3a4c2cf67e2d082e

Please inspect the current versions of:

project/smartcare/queries.py
project/smartcare/services.py
project/smartcare/console.py
project/tests/test_queries.py
project/tests/test_services.py
project/tests/test_workflows.py

Review the current implementation only.

Check specifically:

Purity of appointment_sort_key() and select_appointments().

Whether select_appointments() returns a new list, does not mutate its input, filters correctly by practitioner and optional AppointmentStatus, and sorts by date_time then appointment_id.

Whether AppointmentService.list_practitioner_appointments() keeps responsibilities correctly separated between service, data store and query layers.

Whether invalid practitioner IDs, unknown practitioners and invalid status values are handled correctly.

Whether the console converts status text correctly and recovers from expected ValueError and LookupError cases.

Whether cancelled appointments remain in history and cancellation frees the practitioner/time slot.

Whether object identity and enum identity are preserved.

Whether the current tests cover ordering, filtering, non-mutation, repeatability, fresh-list behaviour, service validation, workflows and recovery.

Identify important missing tests or defects.

Do not redesign the project or add persistence, databases, frameworks or dependencies.

Distinguish actual defects from optional improvements.

### Corrected Copilot response

Copilot reported:

Review result: no functional defects found in the Stage 9 checkpoint implementation.

Copilot confirmed that:

appointment_sort_key() and select_appointments() were pure and did not mutate their inputs.

Practitioner lookup, status validation and filtering/sorting responsibilities were appropriately divided between the service, data-store and query layers.

The console converted status text correctly and recovered from expected ValueError and LookupError cases.

Cancellation retained appointment history and allowed the former practitioner/time slot to be reused.

Existing tests covered ordering, filtering, non-mutation, repeatability, fresh-list behaviour, service validation, object identity, cancellation history, slot reuse and integrated workflows.

Copilot identified two optional test-coverage improvements:

Automated console tests for status-text conversion and menu/error recovery.

A service test using a non-string practitioner ID.

Copilot stated that these were test-coverage gaps rather than observed implementation defects.

## Human decision

The corrected Copilot review was accepted where it matched the implementation and observed test results.

The two suggested additional tests were considered optional rather than required fixes. Manual UI-01 and UI-02 testing already demonstrated console status conversion, error recovery, continued operation and unchanged valid state. Existing validation also handles invalid identifier types.

No Stage 9 implementation change was made solely because of the Copilot review.

The initial stale-commit review was rejected, demonstrating that AI review output was checked against the actual repository state rather than accepted automatically.