# Approved-Data Intake Readiness Report

Generated UTC: `2026-06-15T23:31:26+00:00`

## Public-Safe Scope

This is a header-only readiness report. It does not include approved well-log rows, private workbook rows, restricted identifiers, occurrence probabilities, saturation predictions, trained metrics, or sensitive outputs.

## Summary

- Source label: `demo_public_safe`
- Input mode: `inline_headers`
- Header count: `7`
- Recognized header count: `7`
- Ready for schema design: `True`
- Ready for training: `False`
- Ready for public release: `False`

## Header Roles

- Predictors: DEPTH; GR; RHOB; Rt
- Derived features: none
- QC headers: CAL1
- Context headers: none
- Target-only headers: Sh; NMR_SAT
- Unresolved headers: none
- Unknown headers: none

## Blocked Reasons

- `approved_rows_not_loaded_public_safe_validator`
- `missing_log_adapter_blocked_until_mentor_approval`
- `saturation_target_requires_authoritative_field_and_fraction_or_percent_policy`
- `target_authority_not_confirmed`
- `validation_plan_required_before_training`
- `whole_well_compartment_or_geographic_split_policy_required`

## Mentor Questions

- Which saturation field is authoritative: Sgh, S_h, Sh, or NMR_SAT?
- Should occurrence use source-style classes, saturation thresholds, or mentor-reviewed intervals?
- Are MTE/IGS separate wells and are *_refined processing stages in the workbook?
- Do we have enough caliper coverage to apply washout filtering?
- Which wells become blind validation after full recovery?
- Are missing-log adapters allowed, or should missing curves simply block that feature set?

## Guardrails

- Stability remains methane 5 ppt admissibility/context only, not hydrate proof.
- Occurrence and saturation labels are Y-only target/calibration/validation fields.
- Target-only fields must never enter `X_allowed`.