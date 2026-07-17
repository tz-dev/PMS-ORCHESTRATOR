# PMS DISCIPLINE - PROMPTS & INSTRUCTIONS

## Prompt Sequence Matrix

Use the prompt sequence according to the checked branch status of the PMS-DISCIPLINE run.

### Case A — Core only

Use when the checked Add-on Recommendation Gate keeps the run Core-only or recommends no add-on, and no later MIP/AHP branch is entered.

Prompt sequence:

```text
#1  Read PMS.yaml and optional case materials
#2  Apply Pre-Analysis Template
#3  Check Pre-Analysis YAML
#4  Apply PMS Core Case Application Template
#5  Check PMS Core Case Application YAML
#6  Apply Add-on Recommendation Gate Template
#7  Check Add-on Recommendation Gate YAML

#20 Apply Case Record Stage 1
#21 Check Case Record Stage 1
#22 Apply Case Record Stage 2
#23 Check Case Record Stage 2
#24 Apply Case Record Stage 3
#25 Check Case Record Stage 3

Prospective follow-up preparation:
#26 Iteration Handoff and Follow-up Preparation

Optional Markdown article generation:
#27 Article Source Setup and Rendering Contract
#28 Base Markdown Case Article Draft
#29 Example Decision and Optional Example Generation
#30 Final Integrated Markdown Case Article
#31 Final Article Check and Conservative Patch
```

Skip:

```text
#8–#19
```

---

### Case B — Core + selected add-on

Use when the checked Add-on Recommendation Gate selects exactly one supported add-on, the selected add-on is read and applied, and no later MIP/AHP branch is entered.

Prompt sequence:

```text
#1  Read PMS.yaml and optional case materials
#2  Apply Pre-Analysis Template
#3  Check Pre-Analysis YAML
#4  Apply PMS Core Case Application Template
#5  Check PMS Core Case Application YAML
#6  Apply Add-on Recommendation Gate Template
#7  Check Add-on Recommendation Gate YAML
#8  Read Selected PMS Add-on YAML
#9  Apply Selected PMS Add-on Case Application Template
#10 Check Selected PMS Add-on Case Application YAML

#20 Apply Case Record Stage 1
#21 Check Case Record Stage 1
#22 Apply Case Record Stage 2
#23 Check Case Record Stage 2
#24 Apply Case Record Stage 3
#25 Check Case Record Stage 3

Prospective follow-up preparation:
#26 Iteration Handoff and Follow-up Preparation

Optional Markdown article generation:
#27 Article Source Setup and Rendering Contract
#28 Base Markdown Case Article Draft
#29 Example Decision and Optional Example Generation
#30 Final Integrated Markdown Case Article
#31 Final Article Check and Conservative Patch
```

Skip:

```text
#11–#19
```

---

### Case C — Core + selected add-on + MIP

Use when the selected add-on output is checked, MIP Gate recommends MIP source reading, MIP is read and applied, MIP output is checked, and the checked AHP Gate does not authorize AHP application.

Prompt sequence:

```text
#1  Read PMS.yaml and optional case materials
#2  Apply Pre-Analysis Template
#3  Check Pre-Analysis YAML
#4  Apply PMS Core Case Application Template
#5  Check PMS Core Case Application YAML
#6  Apply Add-on Recommendation Gate Template
#7  Check Add-on Recommendation Gate YAML
#8  Read Selected PMS Add-on YAML
#9  Apply Selected PMS Add-on Case Application Template
#10 Check Selected PMS Add-on Case Application YAML
#11 Apply MIP Gate Template
#12 Check MIP Gate YAML
#13 Read MIP YAML
#14 Apply MIP Case Application
#15 Check MIP Case Application YAML
#16 Apply AHP Gate Template
#17 Check AHP Gate YAML

#20 Apply Case Record Stage 1
#21 Check Case Record Stage 1
#22 Apply Case Record Stage 2
#23 Check Case Record Stage 2
#24 Apply Case Record Stage 3
#25 Check Case Record Stage 3

Prospective follow-up preparation:
#26 Iteration Handoff and Follow-up Preparation

Optional Markdown article generation:
#27 Article Source Setup and Rendering Contract
#28 Base Markdown Case Article Draft
#29 Example Decision and Optional Example Generation
#30 Final Integrated Markdown Case Article
#31 Final Article Check and Conservative Patch
```

Skip:

```text
#18–#19
```

---

### Case D — Core + selected add-on + MIP + AHP

Use when the selected add-on output is checked, MIP is authorized and checked, AHP Gate authorizes AHP source use, and AHP output is checked.

Prompt sequence:

```text
#1  Read PMS.yaml and optional case materials
#2  Apply Pre-Analysis Template
#3  Check Pre-Analysis YAML
#4  Apply PMS Core Case Application Template
#5  Check PMS Core Case Application YAML
#6  Apply Add-on Recommendation Gate Template
#7  Check Add-on Recommendation Gate YAML
#8  Read Selected PMS Add-on YAML
#9  Apply Selected PMS Add-on Case Application Template
#10 Check Selected PMS Add-on Case Application YAML
#11 Apply MIP Gate Template
#12 Check MIP Gate YAML
#13 Read MIP YAML
#14 Apply MIP Case Application
#15 Check MIP Case Application YAML
#16 Apply AHP Gate Template
#17 Check AHP Gate YAML
#18 Apply AHP Module
#19 Check AHP Module Output YAML

#20 Apply Case Record Stage 1
#21 Check Case Record Stage 1
#22 Apply Case Record Stage 2
#23 Check Case Record Stage 2
#24 Apply Case Record Stage 3
#25 Check Case Record Stage 3

Prospective follow-up preparation:
#26 Iteration Handoff and Follow-up Preparation

Optional Markdown article generation:
#27 Article Source Setup and Rendering Contract
#28 Base Markdown Case Article Draft
#29 Example Decision and Optional Example Generation
#30 Final Integrated Markdown Case Article
#31 Final Article Check and Conservative Patch
```

Skip:

```text
NONE
```

---

### General branch rule

Only run a branch when the checked gate output or checked prior state licenses that branch.

A skipped branch must remain visible later in the Case Record stages as skipped, not applicable, rejected, scan-only, unsafe, unresolved, or not recommended, according to the checked record.

Case Record stages are run after the last checked analytical branch output.

Markdown article generation is optional and occurs only after checked Case Record Stage 3.

---

## Prompt #1 — Read PMS.yaml and Optional Case Materials

You are beginning a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:
- PMS.yaml
- optional user-provided case-material files listed in the runner-generated block below

TASK:
First read PMS.yaml carefully and completely.

After PMS.yaml has been read, read every case-material file listed in the runner-generated block completely. If no case-material files are listed, keep this as a PMS.yaml-only reading step.

PURPOSE:
Establish PMS.yaml as the PMS Base reference and, where supplied, establish the user-provided files as bounded case-material context for later PMS-DISCIPLINE use.

TECHNICAL INSTRUCTIONS:
- Read PMS.yaml before reading any case material.
- Keep this as a source- and material-reading step only.
- PMS.yaml remains the PMS Base reference.
- User-provided materials remain bounded case inputs; they are not PMS Base, PMS add-ons, MIP/AHP, templates, validation, proof, or authority.
- Use descriptions and purposes from the runner block only as user-supplied orientation metadata.
- Do not perform Pre-Analysis, Core application, routing, scoring, Case Record generation, article drafting, or final decision work in this step.
- Do not invent inaccessible archive contents, missing documents, statistics, citations, provenance, or unavailable context.
- If any listed file or archive entry cannot be read, state that limitation instead of claiming complete access.

READING FOCUS:
Preserve for later context:
- PMS.yaml is the PMS Base reference.
- PMS operators Δ–Ψ are the base operator grammar.
- Derived axes are PMS-internal projections, not independent primitives.
- PMS is structural, non-diagnostic, non-person-ranking, non-prescriptive, and non-authorizing.
- PMS application requires distance, reversibility, dignity-in-practice, non-capture, rival openness, and claim restraint.
- YAML representation is not validation, proof, implementation, or authority.
- Case materials remain distinguishable by filename, description, purpose, source status, and claim boundary.
- Claims contained in a material are not automatically claims established by the pipeline.

{RUNNER_CASE_MATERIALS}

OUTPUT:
If no additional case-material files are configured, respond only:

PMS.yaml read completely.

If all listed case-material files were accessible and read completely after PMS.yaml, respond only:

PMS.yaml and all listed case materials read completely.

If one or more listed files or archive entries could not be read completely, respond only:

PMS.yaml read completely. Case-material reading incomplete: [list the inaccessible file or archive entry and the limitation].

---

## Prompt #2 — Apply PMS-DISCIPLINE Pre-Analysis Template

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:
- pms_discipline_pre_analysis_template.yaml

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in the previous step.
- PMS.yaml remains the PMS Base reference.
- Any runner-listed case materials were read in step #1 where accessible and remain bounded case-material context.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply pms_discipline_pre_analysis_template.yaml to the CASE PACKET.

PURPOSE:
Produce a PMS-DISCIPLINE Pre-Analysis YAML that either prepares a permitted analysis target for later PMS Core application or records a binding pipeline stop where PMS-DISCIPLINE requires it.

TECHNICAL INSTRUCTIONS:
- Use only the provided template, the CASE PACKET, the available PMS.yaml context, and any bounded case materials already read in step #1.
- Use the Pre-Analysis template as the only output structure.
- HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
- Fill fields precisely from the CASE PACKET, available PMS.yaml context, and any case materials already read in step #1.
- Use unknown, unclear, not_applicable, missing, unresolved, or insufficient where the input does not license a stronger value.
- Template sections may change only where valid YAML repair requires it.
- PMS.yaml supplies background reference only; the Pre-Analysis step is not Core application.
- Distinguish the requested output from the pipeline case. A prohibited requested output may proceed through a separately named reframed target only where no mandatory hard-stop rule is triggered.
- MANDATORY PERSON-NEAR STOP RULE: when the requested output is a prohibited whole-person, character, motive, status, diagnostic, forensic, or person-ranking conclusion; the input is minimal, low, insufficient, fragmentary, hypothetical, or unverified; person-nearness is high or severe; irreversibility is high or severe; and the requested-output entry condition is not satisfied, set `pipeline_case_disposition: stop`. Do not use `proceed_reframed` in the current run. Set `permitted_analysis_target: not_applicable`, `reframing_required_before_core: false`, `reframing_status: not_needed`, and `hard_gate_effect: stop_pipeline`. Any redirect is only a possible new case or run.
- Apply the template hierarchy strictly: explicit scope prohibitions, failed entry/protection conditions, and triggered hard gates override aggregate or `mixed` pressure markers.
- `scope_and_pipeline_disposition.pipeline_case_disposition: stop` is a binding PMS-DISCIPLINE pipeline stop. It is a scope-control result, not a person verdict or prohibited final case decision.
- Preliminary operator pressure, add-on scan pressure, and risk markers remain pressure markers. They must not be converted into recommendation, authorization, application, verdict, full Case Record generation, Markdown article generation, or final decision state.

PRE-ANALYSIS SCOPE:
This step may mark:
- case boundary
- input/source status
- intended use
- claim ceiling
- requested-output disposition and pipeline-case disposition
- original and permitted analysis targets
- hard-gate status, basis, and effect
- person-nearness
- publicness
- irreversibility
- preliminary operator pressure
- derived-structure pressure
- rival pressure
- non-capture zones
- falsifier, weakening, and reopening conditions
- correctability requirements
- later gate pressure only where the template asks for it
- handoff information for later Core use
- case-record seed information for later use

CLAIM DISCIPLINE:
- Keep the output bounded to the CASE PACKET.
- Preserve source status and intended use.
- Lower or limit claims where input, publicness, person-nearness, irreversibility, or rival pressure require it.
- Mark unlicensed claims and uncertainty explicitly.
- Preserve correction and reopening conditions.
- Do not use `mixed` preliminary pressure to weaken a hard prohibition, failed entry condition, triggered hard gate, refusal, suspension, or stop.
- Do not construct a same-run permitted analysis target to bypass the mandatory person-near stop rule.
- Where `pipeline_case_disposition` is `stop`, set all dependent handoff and final-status fields consistently: `core_handoff.export_status: refused`, `final_pre_analysis_status.status: stop_before_core`, and `final_pre_analysis_status.next_allowed_step: stop`.

OUTPUT:
Return only the completed Pre-Analysis YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.
- For `falsifier_and_weakening_conditions.reopening_conditions[*].condition`, use exactly one literal allowed value per list item: `new evidence`, `scope change`, `demonstrated error`, `stronger rival`, or `other`.
- Never combine, qualify, concatenate, or paraphrase these enum values. Values such as `new evidence plus scope change`, `new evidence or stronger rival`, or `material scope change` are invalid.
- Where multiple reopening conditions apply, create one `reopening_conditions` list item per condition with a distinct `condition_id` such as `RO1`, `RO2`, and `RO3`. Preserve the case-specific explanation in each item’s `reopening_effect`.
- Use `condition: other` only when no listed enum accurately represents the trigger; describe the exact trigger in `reopening_effect`.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #3 — Check PMS-DISCIPLINE Pre-Analysis YAML

You are continuing a PMS-DISCIPLINE pipeline run.

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in an earlier step.
- PMS.yaml remains the PMS Base reference.
- The PMS-DISCIPLINE Pre-Analysis Template was applied in the previous step.
- The Pre-Analysis YAML from the previous step is present in this conversation/session.
- The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the Pre-Analysis YAML from the previous step for structural and substantive conformity with the previously applied Pre-Analysis template and the PMS-DISCIPLINE use constraints of this step.

PURPOSE:
Determine whether the Pre-Analysis YAML permits a checked handoff to PMS Core, permits Core only on a completed reframed target, or requires revision, suspension, or a binding pipeline stop. Where necessary, conservatively correct it so that it sufficiently conforms to the template and bounded task.

TECHNICAL INSTRUCTIONS:
- Use only the Pre-Analysis YAML from the previous step, the CASE PACKET, available PMS.yaml context, and the previously applied Pre-Analysis template structure.
- Re-run the Pre-Analysis from scratch only if the existing output is structurally unusable.
- Check structural conformity: root structure, required sections, required fields, allowed placeholders, valid YAML, and required handoff sections.
- Check substantive conformity: boundedness to the CASE PACKET, source-status discipline, intended-use discipline, claim ceiling, requested-output and pipeline-case disposition, original and permitted targets, hard-gate hierarchy, person-nearness, publicness, irreversibility, non-capture, rival pressure, falsifier conditions, correctability, and reopening conditions.
- Correct only where necessary to restore PMS-/YAML-conformity or to prevent overclaim, source-status laundering, premature recommendation, premature authorization, premature Core application, or premature finalization.
- Prefer the smallest sufficient correction.
- Preserve the original output wherever it already sufficiently conforms.
- Corrections remain conservative, bounded, and claim-weakening where needed.
- Use explicit uncertainty markers rather than inferential gap-filling.
- Validate `falsifier_and_weakening_conditions.reopening_conditions[*].condition` as a single exact enum token per list item: `new evidence`, `scope change`, `demonstrated error`, `stronger rival`, or `other`.
- A combined, qualified, or paraphrased value is a concrete correctable defect. Split multiple triggers into separate `reopening_conditions` records with distinct condition IDs, preserving their specific effects in `reopening_effect`.
- Treat `scope_and_pipeline_disposition` as binding scope control, not as a preliminary pressure marker.
- Apply the mandatory person-near stop rule from Prompt #2. If the prior YAML uses `proceed_reframed` despite that rule, this is a concrete semantic defect and must be corrected to `pipeline_case_disposition: stop` with all dependent fields made consistent.
- Verify that hard prohibitions, failed entry/protection conditions, and triggered hard gates cannot be overridden by `pressure_status: mixed`, a constructed same-run reframed target, or a generic `ready_with_limits` handoff.
- Verify that `pipeline_case_disposition: stop` blocks Core and all later analysis steps. A stop may be removed only by a corrected Pre-Analysis artifact, not by commentary or reassurance.

STEP BOUNDARIES:
This check excludes:
- PMS Core application or PMS Core Case Application YAML generation
- invented source material, files, case facts, source status, or unavailable context
- conversion of preliminary operator pressure, add-on scan pressure, or risk markers into recommendation, authorization, application, verdict, full Case Record generation, Markdown article generation, or final decision state; this does not prohibit the template's binding scope and pipeline disposition
- stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:
- invalid YAML
- missing required sections or fields
- unresolved required placeholders
- source-status laundering
- claim ceiling overreach
- requested-output and pipeline-case disposition conflation
- mandatory person-near stop incorrectly represented as `proceed_reframed`
- hard prohibition or hard gate overridden by aggregate pressure
- Core handoff targeting a refused output, a mandatory-stop case, or an unreframed target
- inconsistent stop status, handoff, or next-step fields
- combined, qualified, or paraphrased reopening-condition enum values
- premature Core analysis
- premature operator assignment
- preliminary pressure treated as final assignment
- scan pressure treated as recommendation, authorization, or application
- premature routing, verdict, full Case Record generation, Markdown article generation, or final decision execution
- missing non-capture, rival, falsifier, correctability, or reopening markers
- unsupported file assumptions
- unsupported layer references
- unsupported strengthening of claims

PATCH DISCIPLINE:
If correction is needed:
- Patch only within the Pre-Analysis YAML.
- HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
- Keep claims at or below the level licensed by the CASE PACKET and PMS.yaml context.
- Keep invented evidence, sources, files, case facts, and out-of-scope outputs out of the corrected YAML.
- Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
- Use unknown, unclear, not_applicable, missing, unresolved, insufficient, or similarly bounded markers where stronger values are not licensed.
- The corrected output remains a Pre-Analysis YAML only.

OUTPUT:
If the Pre-Analysis YAML is usable for Core without correction, respond only:

Pre-Analysis YAML checked. Ready for PMS Core case application.

If the Pre-Analysis YAML correctly and consistently sets `scope_and_pipeline_disposition.pipeline_case_disposition: stop` without requiring correction, respond only:

Pre-Analysis YAML checked. PMS-DISCIPLINE pipeline stop confirmed.

If the Pre-Analysis YAML contains concrete defects that can be conservatively corrected inside this step, return:
- CHECK STATUS: corrected
- CORRECTIONS MADE: concise bullet list
- Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
- COMPLETE CORRECTED PRE-ANALYSIS YAML

If the Pre-Analysis YAML is not safely correctable inside this step, return:
- CHECK STATUS: not ready
- BLOCKING ISSUES
- REQUIRED CORRECTIONS
- NEXT ALLOWED STEP

---

## Prompt #4 — Apply PMS Core Case Application Template

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:
- pms_core_case_application_template.yaml

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in an earlier step.
- PMS.yaml remains the PMS Base reference.
- The checked Pre-Analysis YAML is present in this conversation/session.
- The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply pms_core_case_application_template.yaml to the CASE PACKET under the constraints of the checked Pre-Analysis YAML.

PURPOSE:
Produce a completed PMS Core Case Application YAML.

TECHNICAL INSTRUCTIONS:
- Use only the provided Core template, the CASE PACKET, the checked Pre-Analysis YAML, and the available PMS.yaml context.
- Use the Core Case Application template as the only output structure.
- HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
- Fill fields precisely from the CASE PACKET, checked Pre-Analysis YAML, and available PMS.yaml context.
- Use unknown, unclear, not_applicable, missing, unresolved, under_specified, or insufficient where the input does not license a stronger value.
- Template sections may change only where valid YAML repair requires it.
- Use the checked Pre-Analysis YAML as constraint on boundary, source status, input status, intended use, claim ceiling, person-nearness, publicness, irreversibility, rival pressure, non-capture, falsifier conditions, correctability, reopening conditions, and preliminary decision pressure.
- Use PMS.yaml as PMS Base reference for operator grammar, dependency discipline, derived structures, and application guardrails.
- Treat the checked Pre-Analysis YAML as constraint, not as a Core analysis result.
- Template completion is not validation, evidence, truth certification, case closure, or permission for publication or implementation.
- Core pressure markers remain pressure markers, not recommendation, authorization, routing, verdict, full Case Record generation, Markdown article generation, or final decision state.

CORE APPLICATION SCOPE:
This step may produce:
- PMS entry condition status
- application discipline status
- case typing and claim boundary
- checked Pre-Analysis import
- Core principle alignment
- PMS operator analysis Δ–Ψ
- operator dependency checks
- derived structure discipline
- derived axes projection
- self-model analysis, where scoped and warranted
- asymmetry drift pattern status, where scoped and warranted
- example operator-chain application
- computational representation limits
- AI-interface PMS alignment limits
- analysis quality control
- operationalization requirements
- guardrails
- limits
- case synthesis
- Core handoff
- Case Record handoff
- final structural formula as PMS-internal compressed reading only

CLAIM DISCIPLINE:
- Keep findings bounded, reversible, non-diagnostic, non-person-ranking, and open to correction.
- Preserve source status and intended use.
- Respect the claim ceiling declared or corrected in Pre-Analysis.
- Lower or limit claims where input status, publicness, person-nearness, irreversibility, rival pressure, or non-capture require it.
- Mark operator activation only where structurally warranted.
- Mark weak, inactive, under-specified, or non-applicable operators explicitly.
- In `ai_interface_pms_alignment.modes`, `axiomatic.case_status` and `derived_axes_inspection.case_status` accept only `active` or `inactive`; use `inactive` when unused. Only `ai_architecture.case_status` may use `not_applicable`.
- Preserve rival readings, falsifier conditions, reopening conditions, and correction conditions.

OUTPUT:
Return only the completed PMS Core Case Application YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #5 — Check PMS Core Case Application YAML

You are continuing a PMS-DISCIPLINE pipeline run.

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in an earlier step.
- PMS.yaml remains the PMS Base reference.
- The checked Pre-Analysis YAML is present in this conversation/session.
- The PMS Core Case Application Template was applied in the previous step.
- The PMS Core Case Application YAML from the previous step is present in this conversation/session.
- The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the PMS Core Case Application YAML from the previous step for structural and substantive conformity with the previously applied Core template, PMS.yaml, and the checked Pre-Analysis constraints.

PURPOSE:
Determine whether the PMS Core Case Application YAML is usable as checked Core output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it sufficiently conforms to the template, PMS.yaml, and checked Pre-Analysis boundaries.

TECHNICAL INSTRUCTIONS:
- Use only the PMS Core Case Application YAML from the previous step, the CASE PACKET, checked Pre-Analysis YAML, available PMS.yaml context, and the previously applied Core template structure.
- Re-run the Core application from scratch only if the existing output is structurally unusable.
- Check structural conformity: root structure, required sections, required fields, allowed placeholders, valid YAML, operator sections Δ–Ψ, dependency sections, derived-structure sections, quality-control sections, and handoff sections.
- Check substantive conformity: operator grammar, dependency discipline, derived structures as projections, source-status discipline, intended-use discipline, claim ceiling, non-capture, rival pressure, falsifier conditions, correctability, reopening conditions, and non-authority boundaries.
- Correct only where necessary to restore PMS-/YAML-conformity or to prevent overclaim, source-status laundering, operator over-assignment, dependency violation, derived-structure reification, premature recommendation, premature authorization, or premature finalization.
- Prefer the smallest sufficient correction.
- Preserve the original output wherever it already sufficiently conforms.
- Corrections remain conservative, bounded, and claim-weakening where needed.
- Use explicit uncertainty, under-specification, weak activation, inactive status, or non-applicability markers rather than inferential gap-filling.

STEP BOUNDARIES:
This check excludes:
- production or application of the next pipeline step
- invented source material, files, case facts, source status, or unavailable context
- conversion of Core pressure markers into recommendation, authorization, routing, verdict, full Case Record generation, Markdown article generation, or final decision state
- stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:
- invalid YAML
- missing required sections or fields
- unresolved required placeholders
- source-status laundering
- claim ceiling overreach
- operator over-assignment or under-assignment
- dependency violation
- derived-structure reification
- loss of non-capture or rival pressure
- missing falsifier, correctability, or reopening markers
- unsupported file assumptions
- unsupported strengthening of claims
- premature recommendation, authorization, routing, verdict, full Case Record generation, Markdown article generation, or final decision execution
- unsupported out-of-scope decision or application

PATCH DISCIPLINE:
If correction is needed:
- Patch only within the PMS Core Case Application YAML.
- HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
- Keep PMS operators, dependencies, and derived structures unchanged.
- Keep claims at or below the level licensed by the CASE PACKET and checked Pre-Analysis.
- Keep invented evidence, sources, files, case facts, new PMS primitives, and out-of-scope outputs out of the corrected YAML.
- Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
- Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, weak, inactive, or similarly bounded markers where stronger values are not licensed.
- The corrected output remains a PMS Core Case Application YAML only.

OUTPUT:
If the PMS Core Case Application YAML is usable for the next checked step without correction, respond only:

PMS Core Case Application YAML checked. Ready for next PMS-DISCIPLINE pipeline step.

If the PMS Core Case Application YAML contains concrete defects that can be conservatively corrected inside this step, return:
- CHECK STATUS: corrected
- CORRECTIONS MADE: concise bullet list
- Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
- COMPLETE CORRECTED PMS CORE CASE APPLICATION YAML

If the PMS Core Case Application YAML is not safely correctable inside this step, return:
- CHECK STATUS: not ready
- BLOCKING ISSUES
- REQUIRED CORRECTIONS
- NEXT ALLOWED STEP

---

## Prompt #6 — Apply PMS-DISCIPLINE Add-on Recommendation Gate Template

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:
- pms_discipline_addon_recommendation_gate_template.yaml

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in an earlier step.
- PMS.yaml remains the PMS Base reference.
- The checked Pre-Analysis YAML is present in this conversation/session.
- The checked Core Case Application YAML is present in this conversation/session.
- The CASE PACKET remains the bounded source material for this run.
- Add-on sources and add-on case templates have not been read in this step.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply pms_discipline_addon_recommendation_gate_template.yaml to determine whether the checked Core output should remain Core-only or whether exactly one supported add-on family should be recommended as the next reading step.

PURPOSE:
Produce a completed PMS-DISCIPLINE Add-on Recommendation Gate YAML.

TECHNICAL INSTRUCTIONS:
- Use only the provided gate template, CASE PACKET, checked Pre-Analysis YAML, checked Core Case Application YAML, and available PMS.yaml context.
- Use the Add-on Recommendation Gate template as the only output structure.
- HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
- Fill fields precisely from the available inputs.
- Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
- Keep all findings bounded to the CASE PACKET, checked Pre-Analysis YAML, checked Core Case Application YAML, and PMS.yaml context.
- Treat add-on recommendation as a bounded next-step suggestion only, not as authorization, routing execution, classification, claim strengthening, truth certification, or final decision.
- Recommend at most one supported add-on family.
- Supported add-on families are only: ANTICIPATION, CRITIQUE, CONFLICT, LOGIC, EDEN, SEX.
- If no supported add-on is structurally warranted, mark Core-only or no add-on recommendation.
- If multiple add-on pressures appear, use the template’s multiple-candidate pressure review to select the strongest single candidate, preserve Core-only, require revision, suspend, redirect, or mark unclear.
- If surface cues appear without structural trigger, preserve them as false-trigger or non-use records rather than recommending the add-on.

STEP BOUNDARIES:
This step excludes:
- invented source material, files, case facts, source status, add-on source files, add-on case templates, or unavailable context
- reading, summarizing, or applying add-on sources or add-on case application templates
- add-on case application output
- Case Record generation
- Markdown article generation
- final decision execution

ADD-ON GATE SCOPE:
This step may produce:
- checked prior output import
- case and claim boundary review
- Core-only sufficiency review
- supported add-on scan
- candidate scan records for supported add-on families
- multiple-candidate pressure review
- single-add-on rule application
- false-trigger and non-use record
- discipline constraints review
- gate result
- selected add-on next-step indication at family level only
- add-on gate handoff
- quality checks
- final add-on gate status

CLAIM DISCIPLINE:
- Preserve source status, intended use, and the claim ceiling declared or corrected in the checked Pre-Analysis and checked Core output.
- Preserve person-nearness, publicness, irreversibility, rival pressure, non-capture, falsifier conditions, correctability, and reopening conditions.
- Keep add-on relevance separate from add-on authorization.
- Keep add-on non-use available as a disciplined result.
- Keep Core-only available as a disciplined result.
- Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-DISCIPLINE Add-on Recommendation Gate YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #7 — Check PMS-DISCIPLINE Add-on Recommendation Gate YAML

You are continuing a PMS-DISCIPLINE pipeline run.

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in an earlier step.
- PMS.yaml remains the PMS Base reference.
- The checked Pre-Analysis YAML is present in this conversation/session.
- The checked Core Case Application YAML is present in this conversation/session.
- The PMS-DISCIPLINE Add-on Recommendation Gate Template was applied in the previous step.
- The Add-on Recommendation Gate YAML from the previous step is present in this conversation/session.
- The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the Add-on Recommendation Gate YAML from the previous step for structural and substantive conformity with the previously applied gate template, PMS.yaml, checked Pre-Analysis constraints, and checked Core constraints.

PURPOSE:
Determine whether the Add-on Recommendation Gate YAML is usable as checked gate output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it sufficiently conforms to the template, PMS.yaml, checked Pre-Analysis, checked Core output, and bounded task.

TECHNICAL INSTRUCTIONS:
- Use only the Add-on Recommendation Gate YAML from the previous step, CASE PACKET, checked Pre-Analysis YAML, checked Core Case Application YAML, available PMS.yaml context, and the previously applied gate template structure.
- Re-run the Add-on Recommendation Gate from scratch only if the existing output is structurally unusable.
- Check structural conformity: root structure, required sections, required fields, allowed placeholders, valid YAML, supported add-on family enum, candidate scan records, single-add-on rule, false-trigger/non-use record, gate result, selected add-on next-step block, selection consistency, authorization boundary, handoff, quality checks, and final gate status.
- Check substantive conformity: Core-only sufficiency, add-on recommendation restraint, false-trigger handling, non-use visibility, single-add-on discipline, claim ceiling preservation, person-nearness caution, rival pressure, non-capture, correctability, and reopening conditions.
- Correct only where necessary to restore PMS-/YAML-conformity or to prevent overclaim, source-status laundering, false-trigger escalation, multi-add-on recommendation, authorization drift, unsupported filename assumptions, out-of-scope leakage, or premature finalization.
- Prefer the smallest sufficient correction.
- Preserve the original output wherever it already sufficiently conforms.
- Corrections remain conservative, bounded, and claim-weakening where needed.
- Use explicit uncertainty markers rather than inferential gap-filling.

STEP BOUNDARIES:
This check excludes:
- invented source material, files, case facts, source status, add-on source files, add-on case templates, or unavailable context
- reading, summarizing, or applying add-on sources or add-on case application templates
- add-on case application output
- Case Record generation
- Markdown article generation
- final decision execution
- stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:
- invalid YAML
- missing required sections or fields
- unresolved required placeholders
- unsupported add-on family
- multiple add-ons recommended
- selected_addon inconsistent with gate_status
- selected_addon_next_step inconsistent with gate_result
- add-on recommendation treated as authorization
- add-on application performed inside the gate
- add-on source file or add-on case template assumed or invented
- surface cue treated as structural trigger without warrant
- false-trigger or non-use record missing where required
- Core-only sufficiency not considered
- source-status laundering
- claim ceiling overreach
- loss of person-nearness, publicness, irreversibility, rival pressure, non-capture, correctability, or reopening constraints
- Case Record generation
- Markdown article generation
- final decision execution
- unsupported strengthening of claims
- unsupported out-of-scope decision or application

PATCH DISCIPLINE:
If correction is needed:
- Patch only within the Add-on Recommendation Gate YAML.
- HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
- Keep PMS operators, dependencies, derived structures, and supported add-on families unchanged.
- Keep claims at or below the level licensed by the CASE PACKET, checked Pre-Analysis, and checked Core output.
- Keep unsupported add-ons, invented files, out-of-scope outputs, and new source claims out of the corrected YAML.
- Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
- Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, none, weak, false_trigger, not_recommended, core_only, or similarly bounded markers where stronger values are not licensed.
- The corrected output remains an Add-on Recommendation Gate YAML only.

OUTPUT:
If the Add-on Recommendation Gate YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

Add-on Recommendation Gate YAML checked. Ready for the next allowed PMS-DISCIPLINE pipeline step named in the checked gate output.

If the Add-on Recommendation Gate YAML contains concrete defects that can be conservatively corrected inside this step, return:
- CHECK STATUS: corrected
- CORRECTIONS MADE: concise bullet list
- Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
- COMPLETE CORRECTED ADD-ON RECOMMENDATION GATE YAML

If the Add-on Recommendation Gate YAML is not safely correctable inside this step, return:
- CHECK STATUS: not ready
- BLOCKING ISSUES
- REQUIRED CORRECTIONS
- NEXT ALLOWED STEP

---

## Prompt #8 — Read Selected PMS Add-on YAML

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:
- PMS-{SELECTED_ADDON}.yaml

CONTEXT AVAILABLE:
- PMS.yaml has been read completely in an earlier step.
- PMS.yaml remains the PMS Base reference.
- Checked Pre-Analysis YAML, checked Core Case Application YAML, and checked Add-on Recommendation Gate YAML are present in this conversation/session.
- The checked Add-on Recommendation Gate selected exactly one supported add-on family as the next reading step.
- The provided PMS-{SELECTED_ADDON}.yaml corresponds to the selected or user-confirmed add-on family.

SELECTED ADD-ON FAMILY:
{SELECTED_ADDON}

SUPPORTED ADD-ON FAMILIES:
- ANTICIPATION
- CRITIQUE
- CONFLICT
- LOGIC
- EDEN
- SEX

CASE INPUTS:
- none for this step

TASK:
Read PMS-{SELECTED_ADDON}.yaml carefully and completely.

PURPOSE:
Establish PMS-{SELECTED_ADDON}.yaml as the selected add-on source reference for the later PMS-DISCIPLINE add-on case application step.

TECHNICAL INSTRUCTIONS:
- Use only the provided add-on YAML and the available checked context from previous steps.
- Confirm internally that the provided add-on YAML corresponds to the selected or user-confirmed add-on family.
- Keep this as a source-reading step only.
- Case application, template output, Case Record generation, Markdown article generation, final decision execution, invented source material, invented files, invented case facts, invented source status, invented add-on case templates, and unavailable context are outside this step.

READING FOCUS:
Preserve for later context:
- selected add-on role and scope
- relation to PMS Base
- operator emphases and trigger logic
- non-trigger conditions and overuse risks
- claim boundaries
- non-authority boundaries
- case-application constraints
- source-specific guardrails for later add-on case application

OUTPUT:
If the provided file corresponds to the selected or user-confirmed add-on family, respond only:

PMS-{SELECTED_ADDON}.yaml read completely.

If the provided file does not correspond to the selected or user-confirmed add-on family, respond only:

Selected add-on source mismatch. Provide the PMS YAML for the selected or user-confirmed add-on family.

---

## Prompt #9 — Apply Selected PMS Add-on Case Application Template

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* pms_addon_SELECTED_ADDON_case_application_template.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* PMS-{SELECTED_ADDON}.yaml was read in the previous step.
* The CASE PACKET remains the bounded source material for this run.

SELECTED ADD-ON FAMILY:
{SELECTED_ADDON}

SUPPORTED ADD-ON FAMILIES:

* ANTICIPATION
* CRITIQUE
* CONFLICT
* LOGIC
* EDEN
* SEX

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply pms_addon_SELECTED_ADDON_case_application_template.yaml to the CASE PACKET under the constraints of PMS.yaml, the checked prior YAML artifacts, and the already-read PMS-{SELECTED_ADDON}.yaml source.

PURPOSE:
Produce a completed PMS-{SELECTED_ADDON} Add-on Case Application YAML.

TECHNICAL INSTRUCTIONS:

* Use the provided add-on case template as the output structure for this step.
* Fill fields only from the CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and the already-read selected add-on source.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Mark under-supported fields with bounded values such as unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, weak, inactive, or none.
* Keep the selected add-on subordinate to PMS Base, checked Core, source status, intended use, claim ceiling, non-capture, rival pressure, correctability, and reopening conditions.
* Treat the checked Add-on Recommendation Gate as selection context, not as authorization or claim strengthening.
* Apply only the selected add-on family named above.
* For EDEN, `source_and_claim_burden_discipline.source_status_preserved.counter_scene_material` must use exactly one of `present`, `partial`, `absent`, or `needs_review`; use `absent`, not `none`, when no counter-scene material is supplied.

STEP BOUNDARIES:
This step excludes:

* new source material, invented files, inferred case facts, or unavailable context
* re-running Pre-Analysis, Core, or the Add-on Recommendation Gate
* changing the selected add-on family
* applying any other add-on family
* converting add-on relevance into proof, verdict, mandate, publication permission, or final decision
* generating later pipeline artifacts

ADD-ON APPLICATION SCOPE:
This step may produce:

* selected add-on case application YAML
* add-on-specific trigger review
* non-trigger and false-trigger review
* add-on-specific operator emphasis
* claim-ceiling effect
* rival and non-capture constraints
* correctability and reopening conditions
* add-on synthesis
* quality checks
* handoff to the add-on output check

CLAIM DISCIPLINE:

* Preserve source status and intended use.
* Keep claims at or below the ceiling set by checked Pre-Analysis and checked Core.
* Weaken or mark unlicensed any add-on reading that exceeds the available material.
* Keep persons, groups, and institutions out of ranking, diagnosis, certainty labeling, or moral closure.
* Preserve rival readings and stop-capability.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-{SELECTED_ADDON} Add-on Case Application YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #10 — Check Selected PMS Add-on Case Application YAML

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* PMS-{SELECTED_ADDON}.yaml was read earlier.
* The selected add-on case template was applied in the previous step.
* The produced PMS-{SELECTED_ADDON} Add-on Case Application YAML is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

SELECTED ADD-ON FAMILY:
{SELECTED_ADDON}

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the PMS-{SELECTED_ADDON} Add-on Case Application YAML from the previous step for structural and substantive conformity with the selected add-on case template, PMS.yaml, the checked prior YAML artifacts, and the already-read PMS-{SELECTED_ADDON}.yaml source.

PURPOSE:
Determine whether the selected add-on output is usable for the next PMS-DISCIPLINE pipeline step. Where needed, conservatively correct the YAML so that it remains bounded, structurally valid, and consistent with the selected add-on’s role.

TECHNICAL INSTRUCTIONS:

* Use only the add-on output from the previous step, the CASE PACKET, PMS.yaml context, checked prior YAML artifacts, the selected add-on source context, and the selected add-on case template structure.
* Re-run the add-on application from scratch only if the existing YAML is structurally unusable.
* Check template conformity: root structure, required sections, required fields, valid YAML, selected add-on family, source import, trigger review, non-trigger review, quality checks, handoff, and final status.
* Check substantive conformity: PMS Base preservation, Core subordination, gate-selection consistency, source-status discipline, claim ceiling, add-on trigger discipline, false-trigger handling, rival pressure, non-capture, correctability, reopening conditions, and non-authority boundaries.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* runner-reported invalid YAML or deterministic structural findings
* runner-reported missing or unexpected fields, type mismatches, or invalid configured values
* unresolved required placeholders only where they create a concrete semantic or boundary defect
* selected add-on mismatch
* unsupported source or file assumption
* selected source missing, mismatched, or treated as PMS Base
* checked Core overwritten or strengthened
* Add-on Recommendation Gate treated as authorization
* add-on trigger inflated from surface cues
* false-trigger or non-trigger conditions omitted
* another add-on applied inside this output
* source-status laundering
* claim ceiling overreach
* forecast, certainty, mandate, verdict, ranking, diagnosis, or finality drift
* loss of rival readings, non-capture, correctability, or reopening conditions
* unsupported strengthening of claims
* generated later pipeline artifacts

PATCH DISCIPLINE:
If a correction is needed:

* Patch only within the selected add-on output YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep PMS operators, dependencies, derived structures, and supported add-on families unchanged.
* Keep claims at or below the level licensed by the CASE PACKET, checked prior artifacts, and selected add-on source.
* Exclude unsupported add-ons, invented files, new source claims, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a selected PMS add-on case application YAML only.

OUTPUT:
If the selected add-on output is already usable without correction, respond only:

PMS-{SELECTED_ADDON} Add-on Case Application YAML checked. Ready for the next PMS-DISCIPLINE pipeline step.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED PMS-{SELECTED_ADDON} ADD-ON CASE APPLICATION YAML

If the output is not safely correctable inside this step, return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

---

## Prompt #11 — Apply PMS-DISCIPLINE MIP Gate Template

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* pms_discipline_mip_gate_template.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* The selected PMS add-on source was read earlier if an add-on was selected.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* The CASE PACKET remains the bounded source material for this run.
* Runner-listed case materials and their step #1 read status are present in the authoritative runner manifest where configured.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply pms_discipline_mip_gate_template.yaml to determine whether the current checked PMS-DISCIPLINE case state should proceed to MIP source reading, remain without MIP, require revision, downgrade, suspend, refuse, redirect, or require human review.

PURPOSE:
Produce a completed PMS-DISCIPLINE MIP Gate YAML.

TECHNICAL INSTRUCTIONS:

* Use only the provided MIP Gate template, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and checked selected add-on output where present.
* Use the MIP Gate template as the only output structure.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from the available inputs.
* Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Treat the MIP Gate as a bounded recommendation/checkpoint for whether MIP source reading is warranted.
* Keep MIP recommendation separate from MIP application, MIP scoring, person assessment, implementation authority, or finality.
* Runner routing remains binary: `not_recommended`, `scan_only`, or unsafe overall outcomes preselect `no_mip`; `recommended` or `recommended_with_limits` preselect `use_mip`, which includes step #13 source reading followed by step #14 bounded case application. No source-reading-only route is created.
* Preserve source status, intended use, claim ceiling, non-capture, rival pressure, correctability, reopening conditions, and stop-capability from checked prior artifacts.

MIP TRIGGER CALIBRATION:

MIP must not be triggered merely because a constructed, illustrative, hypothetical, workplace, organizational, or conflict case could involve real persons if instantiated.

Do not treat the following as sufficient MIP triggers by themselves:

* routine handoff of responsibility;
* routine role or process coordination;
* deadline pressure;
* delayed response;
* reduced practical options;
* future-risk language;
* hypothetical real-person transfer;
* general organizational friction;
* user curiosity about maturity or dignity language.

MIP becomes structurally relevant only when the checked case state itself centers, or would directly carry into, one or more of the following:

* person-near practice;
* person-evaluative judgment;
* responsibility attribution under asymmetry;
* role-capacity assessment;
* dignity-in-practice pressure;
* face, status, humiliation, or revision-capacity pressure;
* public reputational exposure;
* irreversible or consequential action toward real persons, groups, offices, or institutions.

A constructed case may therefore remain no-MIP when it is role/process-oriented and explicitly avoids personal blame. A constructed case may trigger MIP when its own theory or intended use is built around face/status loss, revision incapacity, dignity-in-practice pressure, responsibility attribution, role-capacity evaluation, reputational exposure, or person-near judgment if transferred to real parties.

This is not a lower MIP threshold. It is a distinction between generic hypothetical person involvement and structurally person-near transfer pressure.

STEP BOUNDARIES:
This step excludes:

* reading or applying a MIP source
* producing a MIP case application YAML
* assigning MIP bands, scores, boxes, modules, person rankings, or maturity verdicts
* changing checked Pre-Analysis, checked Core, checked Add-on Gate, or checked Add-on output
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts

MIP GATE SCOPE:
This step may produce:

* checked prior output import
* MIP applicability review
* burden and source-status review
* red-zone review
* D-module sensitivity review
* A/M-band and IA-box sensitivity review without assigning bands or boxes
* rival and non-capture review
* correctability review
* MIP recommendation output
* MIP gate handoff
* MIP gate quality checks
* final MIP gate status

CLAIM DISCIPLINE:

* Keep claims at or below the ceiling set by checked prior artifacts.
* Mark MIP pressure as pressure only, not as MIP result.
* Preserve Core-only or add-on-only sufficiency where MIP is not structurally warranted.
* Treat person-nearness, publicness, irreversibility, and action-power pressure as caution signals, not automatic MIP triggers.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-DISCIPLINE MIP Gate YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #12 — Check PMS-DISCIPLINE MIP Gate YAML

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* The PMS-DISCIPLINE MIP Gate Template was applied in the previous step.
* The MIP Gate YAML from the previous step is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the MIP Gate YAML from the previous step for structural and substantive conformity with the MIP Gate template, PMS.yaml, checked prior YAML artifacts, and the bounded task.

PURPOSE:
Determine whether the MIP Gate YAML is usable as checked gate output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it sufficiently conforms to the template, PMS.yaml, checked prior outputs, and MIP gate boundaries.

TECHNICAL INSTRUCTIONS:

* Use only the MIP Gate YAML from the previous step, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked selected add-on output where present, and the previously applied MIP Gate template structure.
* Re-run the MIP Gate from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, prior-output import, applicability review, burden review, red-zone review, D-module sensitivity review, A/M-band and IA-box sensitivity review, recommendation output, handoff, quality checks, and final gate status.
* Check substantive conformity: MIP recommendation restraint, source-status discipline, claim ceiling, person-nearness caution, publicness, irreversibility, action-power pressure, non-capture, rival pressure, correctability, reopening conditions, and non-authority boundaries.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

STEP BOUNDARIES:
This check excludes:

* reading or applying a MIP source
* producing MIP case application output
* assigning MIP bands, scores, boxes, modules, person rankings, or maturity verdicts
* changing checked prior artifacts outside the MIP Gate YAML
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
* unsupported source or file assumptions
* checked prior outputs ignored, overwritten, or strengthened
* MIP recommendation treated as MIP application
* MIP pressure treated as score, band, box, module result, person ranking, or maturity verdict
* red-zone review omitted or softened
* D-module, A/M-band, or IA-box sensitivity converted into actual assignment
* source-status laundering
* claim ceiling overreach
* person-nearness, publicness, irreversibility, or action-power pressure inflated into automatic MIP use
* hypothetical real-person transfer treated as sufficient MIP trigger without person-evaluative, responsibility-attributive, role-capacity, dignity-in-practice, face/status, reputational, or consequential action pressure
* routine role/process coordination, deadline pressure, delay, or option-space reduction over-escalated into MIP where the case explicitly avoids personal blame or person assessment
* face/status/revision-capacity pressure wrongly dismissed as no-MIP merely because the case is constructed or not currently about real named persons
* loss of rival readings, non-capture, correctability, or reopening conditions
* unsupported strengthening of claims
* generated later pipeline artifacts

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the MIP Gate YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep PMS operators, dependencies, derived structures, and MIP-specific categories unchanged.
* Keep claims at or below the level licensed by the CASE PACKET and checked prior artifacts.
* Preserve the calibrated distinction between role/process-only cases and structurally person-near transfer cases.
* When the overall gate recommendation was wrongly set to no-MIP, correct `mip_recommendation_output.recommendation_status` to `recommended_with_limits` only when the checked gate wrongly ignores person-evaluative, responsibility-attributive, role-capacity, dignity-in-practice, face/status, reputational, or consequential action pressure.
* When MIP source reading is recommended, set `mip_recommendation_output.MIP_source_read_recommendation.status` to `recommended`, never to `recommended_with_limits`.
* Evaluate `mip_recommendation_output.MIP_case_application_recommendation.status` separately as a semantic gate field. This distinction does not create a separate runner route: `mip_recommendation_output.recommendation_status` controls the existing binary `no_mip` versus `use_mip` route, and `use_mip` proceeds through source reading before bounded case application.
* Correct over-triggered MIP to not_recommended when the case contains only routine role/process pressure, deadline pressure, delay, option loss, or hypothetical real-person transfer without person-evaluative center.
* Exclude invented files, new source claims, MIP application output, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a PMS-DISCIPLINE MIP Gate YAML only.

OUTPUT:
If the MIP Gate YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

PMS-DISCIPLINE MIP Gate YAML checked. Ready for the next allowed PMS-DISCIPLINE pipeline step named in the checked gate output.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED PMS-DISCIPLINE MIP GATE YAML

If the output is not safely correctable inside this step, return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

---

## Prompt #13 — Read MIP YAML

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* MIP.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* The checked MIP Gate named MIP source reading as the next allowed step.

CASE INPUTS:

* none for this step

TASK:
Read MIP.yaml carefully and completely.

PURPOSE:
Establish MIP.yaml as the MIP source and case-application reference for the next PMS-DISCIPLINE MIP application step.

TECHNICAL INSTRUCTIONS:

* Use only MIP.yaml and the available checked context from previous steps.
* Confirm internally that the checked MIP Gate allows MIP source reading.
* Keep this as a source-reading step only.
* Case application, template output, scoring, band assignment, module assignment, source invention, file invention, unavailable context, and later pipeline artifacts are outside this step.

READING FOCUS:
Preserve for later context:

* MIP model role and scope
* relation to PMS Base
* A–C–R–P–D structure
* A-score, M-score, IA-box, and D-module mechanics
* Red Zones and non-use conditions
* source-status and evidence-burden requirements
* non-authority boundaries
* case-application constraints
* conditions under which MIP weakens, suspends, redirects, or refuses application

OUTPUT:
If the checked MIP Gate allows MIP source reading, respond only:

MIP.yaml read completely.

If the checked MIP Gate does not allow MIP source reading, respond only:

MIP source reading is not authorized by the checked MIP Gate.

---

## Prompt #14 — Apply MIP Case Application

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* MIP.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* MIP.yaml was read completely in the previous step.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply the MIP case-application structure in MIP.yaml to the CASE PACKET under the constraints of PMS.yaml, checked prior YAML artifacts, and the checked MIP Gate.

PURPOSE:
Produce a completed MIP Case Application YAML.

TECHNICAL INSTRUCTIONS:

* Use MIP.yaml as the MIP source and case-application structure for this step.
* Fill fields only from the CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked MIP Gate, and MIP.yaml.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the MIP case-application structure, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from the available inputs.
* Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Keep MIP subordinate to PMS Base, checked Core, source status, intended use, claim ceiling, non-capture, rival pressure, correctability, reopening conditions, and stop-capability.
* Treat the checked MIP Gate as MIP-selection context, not as MIP result, score, band, module assignment, person assessment, implementation authority, or finality.
* Apply only MIP.

CONDITIONAL TRANSFER / BOUNDARY USE:

If the checked MIP Gate recommended MIP only because of conditional person-near transfer pressure, apply MIP as a bounded transfer-risk, burden, red-zone, role-capacity, responsibility, dignity-in-practice, and claim-boundary review.

In that mode:

* do not treat the constructed case as a real-person assessment;
* do not assign hard A/M scores;
* do not activate D;
* do not create a D-profile;
* do not treat IA-box handling as a verdict;
* do not rank, diagnose, blame, or evaluate persons;
* mark unsupported MIP fields as not_applicable, insufficient, unknown, or scan_only where the MIP source permits;
* preserve the result as boundary-focused and conditional.

STEP BOUNDARIES:
This step excludes:

* re-running Pre-Analysis, Core, Add-on Gate, Add-on Application, or MIP Gate
* changing the checked MIP Gate result
* adding source material, files, inferred case facts, or unavailable context
* treating MIP output as proof, verdict, diagnosis, person ranking, maturity judgment, mandate, or implementation permission
* generating later pipeline artifacts

MIP APPLICATION SCOPE:
This step may produce:

* MIP case application YAML
* A–C–R–P–D analysis where structurally warranted
* A-score and M-score handling only where licensed by MIP.yaml and the case material
* IA-box and D-module handling only where licensed by MIP.yaml and the case material
* Red Zone review
* non-use and refusal conditions
* source-status and evidence-burden review
* rival and non-capture constraints
* correctability and reopening conditions
* bounded MIP synthesis
* MIP quality checks
* handoff to MIP output check

CLAIM DISCIPLINE:

* Preserve source status and intended use.
* Keep claims at or below the ceiling set by checked prior artifacts.
* Treat under-supported MIP fields as under-supported rather than filling by inference.
* Keep persons, groups, and institutions out of ranking, diagnosis, certainty labeling, or moral closure.
* Preserve rival readings and stop-capability.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed MIP Case Application YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #15 — Check MIP Case Application YAML

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* MIP.yaml was read completely in an earlier step.
* The MIP Case Application YAML from the previous step is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the MIP Case Application YAML from the previous step for structural and substantive conformity with MIP.yaml, PMS.yaml, checked prior YAML artifacts, checked MIP Gate, and the bounded task.

PURPOSE:
Determine whether the MIP Case Application YAML is usable as checked MIP output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it remains structurally valid, source-bounded, non-authoritative, and consistent with MIP’s own case-application structure.

TECHNICAL INSTRUCTIONS:

* Use only the MIP Case Application YAML from the previous step, MIP.yaml, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and checked MIP Gate.
* Re-run MIP application from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, MIP case-application structure, A–C–R–P–D structure, A-score handling, M-score handling, IA-box handling, D-module handling, Red Zone review, non-use/refusal conditions, source-status and evidence-burden review, quality checks, handoff, and final status.
* Check substantive conformity: MIP source fidelity, checked MIP Gate consistency, PMS Base preservation, checked Core subordination, selected add-on subordination where present, source-status discipline, intended-use discipline, claim ceiling, non-capture, rival pressure, correctability, reopening conditions, and non-authority boundaries.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

STEP BOUNDARIES:
This check excludes:

* applying AHP
* generating AHP Gate output
* changing checked prior artifacts outside the MIP output YAML
* changing the checked MIP Gate result
* changing PMS.yaml or MIP.yaml
* adding source material, files, inferred case facts, or unavailable context
* treating MIP output as proof, verdict, diagnosis, person ranking, dignity score, maturity judgment, mandate, publication permission, implementation permission, or finality
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* runner-reported invalid YAML or deterministic structural findings
* runner-reported missing or unexpected fields, type mismatches, or invalid configured values
* unresolved required placeholders only where they create a concrete semantic or boundary defect
* unsupported source or file assumptions
* MIP.yaml structure ignored, overwritten, or replaced
* checked prior outputs ignored, overwritten, or strengthened
* checked MIP Gate treated as MIP result rather than selection context
* MIP output treated as PMS-DISCIPLINE verdict
* A-score or M-score treated as hard score where MIP/source status does not license it
* A/M bands over-hardened beyond MIP.yaml
* IA-box treated as verdict rather than asymmetry check
* D-module activated without warrant
* Dignity-in-Practice treated as ontological dignity, person ranking, or dignity score
* Red Zone review omitted or softened where required
* conditional person-near transfer pressure converted into real-person assessment
* constructed-case MIP use converted into hard A/M scoring, D activation, D-profile, IA-box verdict, maturity verdict, person ranking, or blame assignment
* boundary-focused MIP application over-expanded beyond the checked MIP Gate
* MIP application wrongly treating role/process-only material as person-capacity or dignity-in-practice evidence
* non-use or refusal conditions ignored
* source-status laundering
* evidence-burden overreach
* claim ceiling overreach
* person-nearness, publicness, irreversibility, or action-power pressure inflated into MIP authority
* loss of rival readings, non-capture, correctability, reopening conditions, or stop-capability
* unsupported strengthening of claims
* generated AHP, Case Record, Markdown article, or later pipeline artifacts

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the MIP Case Application YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template/source-derived field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep PMS operators, MIP structures, A–C–R–P–D categories, A-score/M-score handling, IA-box handling, D-module handling, and Red Zone categories unchanged.
* Keep claims at or below the level licensed by the CASE PACKET, checked prior artifacts, checked MIP Gate, and MIP.yaml.
* If the MIP branch was entered only for conditional person-near transfer or boundary review, patch over-strong scoring, D activation, IA verdicts, person assessment, or maturity language back to bounded scan, boundary, burden, red-zone, or not_applicable language.
* Exclude invented files, new source claims, AHP output, Case Record output, Markdown output, MIP authority drift, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a MIP Case Application YAML only.

OUTPUT:
If the MIP Case Application YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

MIP Case Application YAML checked. Ready for the next PMS-DISCIPLINE pipeline step.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED MIP CASE APPLICATION YAML

If the output is not safely correctable inside this step, return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

---

## Prompt #16 — Apply PMS-DISCIPLINE AHP Gate Template

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* pms_discipline_ahp_gate_template.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* MIP - Maturity in Practice.yaml was read earlier if MIP was applied.
* Checked MIP Case Application YAML is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply pms_discipline_ahp_gate_template.yaml to determine whether the checked MIP output should proceed to AHP source reading, remain without AHP, require revision, downgrade, suspension, refusal, redirection, or human review.

PURPOSE:
Produce a completed PMS-DISCIPLINE AHP Gate YAML.

TECHNICAL INSTRUCTIONS:

* Use only the provided AHP Gate template, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and checked MIP output.
* Use the AHP Gate template as the only output structure.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from the available inputs.
* Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Treat the AHP Gate as a bounded checkpoint for whether AHP source reading is warranted.
* Keep AHP recommendation separate from AHP application, Precision Heuristic generation, Attack Points generation, Hardening Backlog generation, scoring, assessment, publication permission, or finality.
* Preserve source status, intended use, claim ceiling, non-capture, rival pressure, correctability, reopening conditions, and stop-capability from checked prior artifacts.

STEP BOUNDARIES:
This step excludes:

* reading or applying an AHP source
* producing AHP output
* generating Precision Heuristic, Attack Points, or Hardening Backlog
* changing checked prior artifacts
* rescoring A-score, M-score, IA-box, D-module, or other MIP structures
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts

AHP GATE SCOPE:
This step may produce:

* checked prior output import
* checked MIP output import
* existing MIP analysis requirement review
* structured case fields requirement review
* AHP trigger review
* precision-need review
* attack-surface need review
* hardening-need review
* transmission and reuse review
* score hygiene and D-language review
* non-interference review
* non-trigger review
* rival and non-capture review
* correctability review
* AHP recommendation output
* AHP gate handoff
* AHP gate quality checks
* final AHP gate status

CLAIM DISCIPLINE:

* Keep claims at or below the ceiling set by checked prior artifacts.
* Mark AHP pressure as pressure only, not as AHP result.
* Treat AHP as optional second-order analysis-quality overlay, not as a case judgment.
* Preserve MIP sufficiency where AHP is not structurally warranted.
* Treat transmission, reuse, publicness, score language, D-language, and hardening pressure as caution signals, not automatic AHP triggers.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-DISCIPLINE AHP Gate YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #17 — Check PMS-DISCIPLINE AHP Gate YAML

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* Checked MIP Case Application YAML is present in this conversation/session.
* The PMS-DISCIPLINE AHP Gate Template was applied in the previous step.
* The AHP Gate YAML from the previous step is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the AHP Gate YAML from the previous step for structural and substantive conformity with the AHP Gate template, PMS.yaml, checked prior YAML artifacts, checked MIP output, and the bounded task.

PURPOSE:
Determine whether the AHP Gate YAML is usable as checked gate output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it sufficiently conforms to the template, checked prior outputs, and AHP gate boundaries.

TECHNICAL INSTRUCTIONS:

* Use only the AHP Gate YAML from the previous step, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked MIP output, and the previously applied AHP Gate template structure.
* Re-run the AHP Gate from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, checked-output imports, existing MIP analysis review, structured case fields review, trigger review, precision review, attack-surface review, hardening review, non-interference review, recommendation output, handoff, quality checks, and final gate status.
* Check substantive conformity: AHP recommendation restraint, source-status discipline, MIP-output preservation, non-interference with MIP scores/modules, claim ceiling, transmission and reuse risk, D-language risk, score hygiene, hardening pressure, rival pressure, non-capture, correctability, reopening conditions, and non-authority boundaries.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

STEP BOUNDARIES:
This check excludes:

* reading or applying an AHP source
* producing AHP output
* generating Precision Heuristic, Attack Points, or Hardening Backlog
* changing checked prior artifacts outside the AHP Gate YAML
* rescoring A-score, M-score, IA-box, D-module, or other MIP structures
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
* unsupported source or file assumptions
* checked prior outputs ignored, overwritten, or strengthened
* AHP recommendation treated as AHP application
* AHP pressure treated as score, verdict, assessment, publication permission, or finality
* Precision Heuristic, Attack Points, or Hardening Backlog generated inside the gate
* MIP A-score, M-score, IA-box, D-module, or other structures rescored or altered
* non-interference review omitted or softened
* transmission, reuse, publicness, D-language, score-language, or hardening pressure inflated into automatic AHP use
* source-status laundering
* claim ceiling overreach
* loss of rival readings, non-capture, correctability, or reopening conditions
* unsupported strengthening of claims
* generated later pipeline artifacts

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the AHP Gate YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep PMS operators, MIP structures, and AHP-specific gate categories unchanged.
* Keep claims at or below the level licensed by the CASE PACKET and checked prior artifacts.
* Exclude invented files, new source claims, AHP application output, MIP rescoring, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a PMS-DISCIPLINE AHP Gate YAML only.

OUTPUT:
If the AHP Gate YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

PMS-DISCIPLINE AHP Gate YAML checked. Ready for the next allowed PMS-DISCIPLINE pipeline step named in the checked gate output.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED PMS-DISCIPLINE AHP GATE YAML

If the output is not safely correctable inside this step, return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

---

## Prompt #18 — Apply AHP Module

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* MIP - Maturity in Practice - AHP Module.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* Checked MIP Case Application YAML is present in this conversation/session.
* Checked PMS-DISCIPLINE AHP Gate YAML is present in this conversation/session.
* The checked AHP Gate names AHP application or AHP source use as the next allowed step.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Apply the AHP module from "MIP - Maturity in Practice - AHP Module.yaml" to the checked MIP Case Application YAML under the constraints of PMS.yaml, checked prior YAML artifacts, and the checked AHP Gate.

PURPOSE:
Produce a completed AHP Module Output YAML as an optional second-order analysis-quality overlay for the checked MIP output.

TECHNICAL INSTRUCTIONS:

* Use only the provided AHP module, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked MIP output, and checked AHP Gate.
* Use the AHP module’s case schema / overlay structure as the output structure for this step.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the AHP case-application structure, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from the available inputs.
* Use unknown, unclear, not_applicable, missing, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Treat AHP as an optional second-order analysis-quality overlay for precision, attack-surface visibility, and hardening backlog.
* Keep AHP subordinate to checked MIP output, PMS Base, source status, intended use, claim ceiling, non-capture, rival pressure, correctability, and reopening conditions.
* Preserve the AHP non-interference rule: AHP does not alter MIP A-score, M-score, IA-box, D-module, Red Zones, source status, or checked prior outputs.
* Generate only AHP-specific overlay content licensed by the AHP module and the checked AHP Gate.

STEP BOUNDARIES:
This step excludes:

* re-running Pre-Analysis, Core, Add-on Gate, Add-on Application, MIP Gate, MIP Application, or AHP Gate
* changing checked prior artifacts
* rescoring A-score, M-score, IA-box, D-module, or other MIP structures
* activating D-module or creating D-profiles
* treating AHP as person assessment, maturity verdict, score, ranking, publication permission, or finality
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts

AHP APPLICATION SCOPE:
This step may produce:

* AHP Module Output YAML
* Precision Heuristic Summary
* Attack Points / attack-surface visibility
* Hardening Backlog
* scope-leakage review
* evidence-linkage review
* misreadability review
* transmission-status review
* score-hygiene and D-language review
* reversibility and iteration review
* non-interference confirmation
* AHP quality checks
* AHP handoff to output check

CLAIM DISCIPLINE:

* Keep claims at or below the ceiling set by checked prior artifacts.
* Treat AHP output as analysis-quality support, not as case judgment.
* Mark attack points as review points, not as defects proven by AHP itself.
* Mark hardening backlog items as next-iteration tasks, not as mandates.
* Preserve MIP output without strengthening or weakening its scores/modules.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed AHP Module Output YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #19 — Check AHP Module Output YAML

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present in this conversation/session.
* Checked MIP Case Application YAML is present in this conversation/session.
* Checked PMS-DISCIPLINE AHP Gate YAML is present in this conversation/session.
* The AHP module was applied in the previous step.
* The AHP Module Output YAML from the previous step is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

TASK:
Check the AHP Module Output YAML from the previous step for structural and substantive conformity with the AHP module, PMS.yaml, checked prior YAML artifacts, checked MIP output, checked AHP Gate, and the bounded task.

PURPOSE:
Determine whether the AHP Module Output YAML is usable as checked AHP output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it remains structurally valid, non-interfering, bounded, and consistent with AHP’s role as second-order analysis-quality overlay.

TECHNICAL INSTRUCTIONS:

* Use only the AHP Module Output YAML from the previous step, the AHP module structure, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked MIP output, and checked AHP Gate.
* Re-run AHP application from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, Precision Heuristic Summary, Attack Points, Hardening Backlog, quality checks, non-interference fields, and final status.
* Check substantive conformity: AHP optional-overlay role, MIP-output preservation, non-interference with scores/modules, source-status discipline, claim ceiling, attack-surface accuracy, hardening backlog restraint, transmission-status handling, score hygiene, D-language caution, rival pressure, non-capture, correctability, and reopening conditions.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

STEP BOUNDARIES:
This check excludes:

* re-running prior pipeline stages
* changing checked prior artifacts outside the AHP output YAML
* rescoring A-score, M-score, IA-box, D-module, or other MIP structures
* activating D-module or creating D-profiles
* converting attack points into proven defects
* converting hardening backlog into mandate, publication permission, implementation permission, or finality
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* runner-reported invalid YAML or deterministic structural findings
* runner-reported missing or unexpected fields, type mismatches, or invalid configured values
* unresolved required placeholders only where they create a concrete semantic or boundary defect
* unsupported source or file assumptions
* checked prior outputs ignored, overwritten, or strengthened
* AHP output treated as case judgment, score, ranking, maturity verdict, or finality
* MIP A-score, M-score, IA-box, D-module, Red Zones, or checked MIP structures altered
* Precision Heuristic used as authority rather than analysis-quality summary
* Attack Points treated as proven failures rather than review surfaces
* Hardening Backlog treated as mandate rather than next-iteration support
* source-status laundering
* claim ceiling overreach
* transmission-status upgrade without support
* score-hygiene or D-language risks omitted
* loss of rival readings, non-capture, correctability, or reopening conditions
* generated later pipeline artifacts

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the AHP Module Output YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep PMS operators, checked MIP structures, and AHP overlay categories unchanged.
* Keep claims at or below the level licensed by the CASE PACKET and checked prior artifacts.
* Exclude invented files, new source claims, MIP rescoring, AHP authority drift, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains an AHP Module Output YAML only.

OUTPUT:
If the AHP Module Output YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

AHP Module Output YAML checked. Ready for the next PMS-DISCIPLINE pipeline step.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED AHP MODULE OUTPUT YAML

If the output is not safely correctable inside this step, return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

---

## Prompt #20 — Apply PMS-DISCIPLINE Case Record Stage 1 Artifact Index

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* pms_case_record_stage_1_artifact_index_template.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present if MIP routing occurred.
* MIP.yaml was read earlier if MIP was applied.
* MIP Case Application YAML and its output-check result are present if MIP was applied.
* Checked PMS-DISCIPLINE AHP Gate YAML is present if AHP routing occurred.
* AHP module YAML was read earlier if AHP was applied.
* AHP Module Output YAML and its output-check result are present if AHP was applied.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

AUTHORITATIVE RUNNER MANIFEST:
{RUNNER_STAGE_1_MANIFEST}

CURRENT-STEP SELF-REFERENCE RULE:

* Stage 1 indexes upstream run artifacts from steps #1–#19 only.
* The current Stage 1 output path is runner execution metadata, not an upstream artifact.
* Do not list the current Stage 1 output as produced, missing, deferred, selected, excluded, superseded, or deliberately not imported.
* The current output does not need to exist before generation.
* Do not infer or enumerate unselected local source and template files. Preserve their route status using not_selected, not_applicable, skipped, or another template-allowed bounded marker, with no invented path or presence claim.

SOURCE AUTHORITY HIERARCHY:
For run metadata, file existence, exact paths, route state, branch state, and step status, use this order:

1. Authoritative Runner Manifest
2. Checked upstream artifact
3. Generated downstream artifact
4. Template default or placeholder
5. Model inference

Conflict rule:

* A higher source always overrides a lower source for the same metadata field.
* Copy runner-manifest values exactly. Do not normalize paths, abbreviate them, or replace an output path with session.json.
* Template defaults are placeholders, not evidence.
* Model inference may fill only fields genuinely absent from every higher source, and then only with an explicit bounded marker.

TASK:
Apply pms_case_record_stage_1_artifact_index_template.yaml to produce a complete artifact index for the current PMS-DISCIPLINE pipeline run.

PURPOSE:
Produce a Stage 1 Artifact Index YAML that records which source files, case materials, templates, checked outputs, optional branches, skipped branches, and missing artifacts exist for this run.

TECHNICAL INSTRUCTIONS:

* Use only the provided Stage 1 template, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and available source/read-status information.
* Use the Stage 1 template as the only output structure.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from the available inputs.
* Use present, absent, not_applicable, skipped, missing, unknown, unclear, unresolved, under_specified, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Distinguish PMS/MIP/AHP source files, user-provided case materials, templates, read confirmations, unchecked outputs, checked outputs, optional branches, skipped branches, and unavailable artifacts.
* Populate the template case_material_index from the runner-generated CASE MATERIAL INVENTORY. Preserve exact case-relative paths, descriptions, purposes, hashes, and file-presence status.
* Material presence is not evidence, correctness, completeness, relevance, or successful reading. Preserve step #1 reading limitations if the record contains them.
* Preserve branch status for selected add-on, MIP, and AHP.
* Mark unselected add-ons as unselected, skipped, or not_applicable rather than silently omitting them.
* Preserve source status, intended use, claim ceiling, and artifact provenance where visible.
* Treat the runner-generated manifest above as authoritative for local path, file-presence, route, skipped-branch, and produced-output status.
* Use only project-relative source/template paths, case-relative material paths, and case-relative output paths from the runner manifest.
* Ignore AI-service attachment names, /mnt/data paths, sandbox paths, renamed uploads, duplicate attachments, helper scripts, and other service-local files.
* Do not invent SHA-256 values. If the runner manifest does not provide a hash, set sha256_if_available to unknown.
* The Stage 2 and Stage 3 templates are future-step runner resources. Mark them deferred, not missing or expected_but_missing. Their current non-upload status is not a Stage 1 blocker.
* Local presence of an unselected add-on source or template does not mean it was read or applied. Unselected add-on outputs are not_applicable and must not receive an output path.
* A deliberately skipped MIP or AHP branch is not a missing-artifact defect.
* ready_for_stage_2 may be yes when all actual current-run artifacts and branch statuses are accurately marked. It must not be set to no solely because a future-step Stage 2 or Stage 3 template has not yet been uploaded.

STEP BOUNDARIES:
This step excludes:

* re-running Pre-Analysis, Core, Add-on Gate, Add-on Application, MIP Gate, MIP Application, AHP Gate, or AHP Application
* checking or patching prior outputs
* extracting layer digests
* integrating a full record
* changing checked prior artifacts
* producing new substantive analysis
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts

STAGE 1 SCOPE:
This step may produce:

* source file inventory
* case-material inventory
* template inventory
* checked output inventory
* read-confirmation inventory
* optional branch inventory
* skipped branch inventory
* missing artifact inventory
* source-status and intended-use index
* artifact dependency map
* Stage 1 readiness status for Stage 1 output check

CLAIM DISCIPLINE:

* Treat Stage 1 as an artifact index only.
* Artifact or case-material presence does not imply correctness, truth, relevance, or successful reading.
* Checked status records prior output-check status; it does not create new authority.
* Missing or skipped artifacts remain visible.
* Optional branches remain optional.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-DISCIPLINE Stage 1 Artifact Index YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #21 — Check PMS-DISCIPLINE Case Record Stage 1 Artifact Index

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present if MIP routing occurred.
* Checked MIP Case Application YAML is present if MIP was applied.
* Checked PMS-DISCIPLINE AHP Gate YAML is present if AHP routing occurred.
* Checked AHP Module Output YAML is present if AHP was applied.
* The Stage 1 Artifact Index YAML from the previous step is present in this conversation/session.
* Runner-listed case materials and their step #1 read status are present in the authoritative runner manifest where configured.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

AUTHORITATIVE RUNNER MANIFEST:
{RUNNER_STAGE_1_MANIFEST}

STAGE-1 SELF-REFERENCE CHECK RULE:

* The Stage 1 YAML under review indexes upstream run artifacts from steps #1–#19.
* Step #20 is the artifact under review and is not required to index its own output path.
* Absence of `outputs/step_20_stage_1_artifact_index.yaml` from the Stage 1 inventory is not a defect.
* A Stage 1 YAML that imports its own current production status as an upstream artifact should be conservatively corrected by removing that self-reference.
* Do not require a complete installation inventory. Unselected local sources and templates may remain not_selected or not_applicable without a path or local-presence assertion.

SOURCE AUTHORITY HIERARCHY:
For run metadata, file existence, exact paths, route state, branch state, and step status, use this order:

1. Authoritative Runner Manifest
2. Checked upstream artifact
3. Stage 1 output under review
4. Template default or placeholder
5. Model inference

A higher source overrides a lower source. Copy runner-manifest values exactly. Never substitute session.json for a produced output path unless the runner manifest itself names session.json for that field.

TASK:
Check the Stage 1 Artifact Index YAML from the previous step for semantic, provenance, route, and boundary conformity with the Stage 1 template, checked prior artifacts, source/read-status information, and the bounded task. Use runner-generated local validation as authoritative for deterministic YAML structure when available.

PURPOSE:
Determine whether the Stage 1 Artifact Index YAML is usable as checked Stage 1 output for Stage 2. Where necessary, conservatively correct it so that it accurately records the artifact state of this pipeline run.

TECHNICAL INSTRUCTIONS:

* Use only the Stage 1 Artifact Index YAML from the previous step, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and the previously applied Stage 1 template structure.
* Re-run Stage 1 from scratch only if the runner-generated local validation handoff reports a blocking structural defect that cannot be patched conservatively.
* Do not independently re-audit YAML syntax, duplicate keys, the complete key tree, types, or configured enum values when local validation is authoritative. Address only the exact structural findings supplied by the runner; otherwise perform semantic review only.
* Check substantive conformity: artifact existence, case-material inventory fidelity, checked-output status, source/read-status distinction, optional branch status, skipped branch status, missing artifact status, source status, intended use, and dependency ordering.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative and bounded.
* Use explicit uncertainty markers instead of inferential gap-filling.
* Treat the runner-generated manifest above as authoritative for local paths, route states, skipped branches, and produced output existence.
* Reject or correct AI-service-local paths, including /mnt/data paths, sandbox paths, renamed upload copies, duplicate attachment names, and helper scripts.
* Reject invented SHA-256 values. Use unknown when the runner manifest supplies no hash.
* Stage 2 and Stage 3 templates must be deferred future-step resources, not missing or expected_but_missing artifacts. Their non-upload during Stage 1 must not block Stage 2 readiness.
* Local presence of unselected add-on sources/templates must not be converted into selected, read, applied, or produced output status.
* Skipped MIP or AHP branches must remain visible as skipped or not_applicable, not as defects.
* If the only stated blocker is that the Stage 2 or Stage 3 template was not uploaded during Stage 1, correct that blocker, mark the future templates deferred, and set readiness according to the actual run artifacts.

STEP BOUNDARIES:
This check excludes:

* re-running prior pipeline stages
* changing checked prior artifacts outside the Stage 1 YAML
* extracting layer digests
* integrating a full record
* producing new substantive analysis
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* runner-reported invalid YAML or deterministic structural findings
* runner-reported missing or unexpected fields, type mismatches, or invalid configured values
* unresolved required placeholders only where they create a concrete semantic or boundary defect
* unsupported source or file assumptions
* checked outputs mislabeled as unchecked or absent
* unchecked outputs mislabeled as checked
* optional branches silently omitted
* skipped branches mislabeled as absent defects
* source files confused with templates
* templates confused with applied outputs
* read confirmations confused with analysis outputs
* case materials omitted, assigned an invented path/hash, confused with model sources/templates, or treated as evidence merely because present
* artifact presence treated as correctness
* source-status laundering
* claim ceiling overreach
* generated Stage 2 or Stage 3 content inside Stage 1

MANDATORY CRITERIA LEDGER:
Evaluate every criterion separately and mark it PASS or FAIL. A general statement such as “coherent,” “complete,” or “ready” is not sufficient.

1. Runner-generated local YAML validation is respected: exact reported structural findings are handled, and when the runner reports clean structure or no handoff, no independent full-key-tree audit is performed.
2. Every completed upstream step output from steps #1–#19 that is relevant to the selected route appears with the exact case-relative output path from the runner manifest; the Stage 1 output under review is not required to index itself.
3. No completed upstream output is represented only by session.json unless the runner manifest explicitly assigns session.json to that artifact field.
4. Route, selected add-on, MIP, AHP, skipped-branch, and produced-output states match the runner manifest exactly.
5. Every configured case material is represented in case_material_index with the exact runner path, description, purpose, file-presence status, and supplied hash; no material is treated as a model source, template, or evidence merely because present.
6. Stage 2 and Stage 3 templates are marked deferred future-step resources, not missing or expected_but_missing.
7. No /mnt/data path, sandbox path, renamed attachment, duplicate upload name, helper script, or service-local file is treated as a run artifact.
8. No SHA-256 value is invented; unavailable hashes are marked unknown.
9. Unselected add-ons remain unselected/not_applicable and have no produced output path.
10. Skipped MIP or AHP branches remain visible and are not treated as missing-artifact defects.
11. Source status and intended use match the CASE PACKET exactly.
12. ready_for_stage_2 and blocker_notes follow the actual current-run artifacts; future-template upload state is not a blocker.
13. Stage 1 contains no layer digest, Stage 3 integration, new case analysis, later-pipeline content, or self-reference that treats step #20 as its own upstream artifact.

READINESS RULE:
The output may be declared ready only if every criterion is PASS after any correction. Any FAIL must be corrected inside Stage 1 or reported as blocking.

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the Stage 1 Artifact Index YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep claims at or below the level licensed by the artifact state and checked prior outputs.
* Exclude invented files, invented read confirmations, new source claims, layer digests, full-record integration, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a PMS-DISCIPLINE Stage 1 Artifact Index YAML only.

OUTPUT:
Always return the completed criteria ledger first, with all 13 numbered criteria marked PASS or FAIL and one concise reason per criterion.

If all criteria are PASS without correction, then return:

* CHECK STATUS: ready
* FINAL RESULT: PMS-DISCIPLINE Stage 1 Artifact Index YAML checked. Ready for Stage 2 Layer Digest Extraction.

If concrete defects can be conservatively corrected inside this step, then return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* CRITERIA AFTER CORRECTION: repeat all 13 criteria as PASS or FAIL
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED PMS-DISCIPLINE STAGE 1 ARTIFACT INDEX YAML

If the output is not safely correctable inside this step, then return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

Do not declare ready while any criterion remains FAIL.

---

## Prompt #22 — Apply PMS-DISCIPLINE Case Record Stage 2 Layer Digest Extraction

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* pms_case_record_stage_2_layer_digest_extraction_template.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present if MIP routing occurred.
* Checked MIP Case Application YAML is present if MIP was applied.
* Checked PMS-DISCIPLINE AHP Gate YAML is present if AHP routing occurred.
* Checked AHP Module Output YAML is present if AHP was applied.
* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

AUTHORITATIVE RUNNER CASE-RECORD MANIFEST:
{RUNNER_CASE_RECORD_MANIFEST}

CURRENT-STEP OUTPUT RULE:

* The current step's expected output path, current status, and temporary output-existence value are runner execution metadata only.
* Do not copy current-step execution metadata into the generated or reviewed YAML.
* Do not place the current step's own output status in notes, missing-item registers, deliberately-not-imported items, workflow findings, tensions, blockers, readiness fields, or case findings.
* The current output does not need to exist before generation and must not be classified as missing, deferred, excluded, unresolved, or deliberately not imported.
* Preserve genuine substantive contradictions, but do not convert temporary runner metadata into case substance.

SOURCE AUTHORITY HIERARCHY:

For exact metadata and provenance:
1. Authoritative Runner Case-Record Manifest
2. Checked Stage 1 Artifact Index
3. Checked layer artifact
4. Stage 2 template default or placeholder
5. Model inference

For substantive digest content:
1. The corresponding checked layer artifact
2. Checked Stage 1 only for selection, status, and provenance
3. Stage 2 template structure
4. Model inference only as an explicit bounded marker

Conflict rules:

* Exact paths, file existence, routes, branch states, and step states follow the runner manifest.
* Artifact selection and provenance follow checked Stage 1 unless the runner manifest exposes an exact metadata conflict, in which case the runner manifest controls that metadata field.
* Copy each selected artifact path exactly. Do not replace it with session.json, a chat attachment name, or a temporary path.
* Preserve genuine substantive contradictions between checked artifacts; do not resolve them through template hierarchy or inference.

TASK:
Apply pms_case_record_stage_2_layer_digest_extraction_template.yaml to extract bounded layer digests from checked pipeline artifacts.

PURPOSE:
Produce a Stage 2 Layer Digest Extraction YAML that summarizes the checked outputs layer by layer without re-running, correcting, strengthening, or integrating them.

TECHNICAL INSTRUCTIONS:

* Use only the provided Stage 2 template, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and checked Stage 1 Artifact Index YAML.
* Use the Stage 2 template as the only output structure.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from checked artifacts only.
* Use not_applicable, skipped, absent, unknown, unclear, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Extract only digest-level content from checked artifacts.
* For PMS Core digests, preserve each operator's canonical identity, canonical name, definition-level function, dependency status, analytic weight, and checked case-specific role.
* Do not rename, repurpose, merge, or substitute PMS operators during compression.
* A case-specific gloss may explain an operator's role, but it must not replace the canonical operator meaning.
* For example, `Λ` remains `Non-Event` and may represent a structured absence or expected occurrence that fails, remains delayed, or remains unresolved within a frame. It must not be redefined as continuity merely because continuity is present elsewhere in the case.
* When a compact digest cannot preserve an operator distinction safely, use a more general description without assigning that description to the wrong operator.
* Preserve each layer’s claim ceiling, non-use, skipped-branch status, uncertainty, correctability, rival pressure, and handoff.
* Keep selected add-on, MIP, and AHP digests separate.
* Keep AHP as optional second-order analysis-quality overlay where present.
* Preserve AHP non-interference: AHP does not alter MIP scores, bands, boxes, modules, source status, or checked prior outputs.

STEP BOUNDARIES:
This step excludes:

* re-running Pre-Analysis, Core, Add-on Gate, Add-on Application, MIP Gate, MIP Application, AHP Gate, or AHP Application
* checking or patching prior outputs
* changing Stage 1
* integrating a full record
* producing new substantive analysis
* resolving contradictions by interpretation
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts

STAGE 2 SCOPE:
This step may produce:

* Pre-Analysis digest
* Core digest
* Add-on Gate digest
* selected add-on digest if applicable
* MIP Gate digest if applicable
* MIP digest if applicable
* AHP Gate digest if applicable
* AHP digest if applicable
* skipped branch digest
* non-use digest
* uncertainty digest
* rival pressure digest
* claim ceiling digest
* correctability and reopening digest
* Stage 2 export for Stage 3 integration
* Source-read confirmations may be indexed from Stage 1, but Stage 2 digest content must come from checked outputs, not from source files alone.

CLAIM DISCIPLINE:

* Treat Stage 2 as digest extraction only.
* Digest does not replace the checked source artifact.
* Digest compression must not strengthen claims.
* Digest compression must not erase uncertainty, non-use, skipped branches, or source limitations.
* Preserve contradictions as contradictions where checked artifacts leave them unresolved.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-DISCIPLINE Stage 2 Layer Digest Extraction YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #23 — Check PMS-DISCIPLINE Case Record Stage 2 Layer Digest Extraction

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present if MIP routing occurred.
* Checked MIP Case Application YAML is present if MIP was applied.
* Checked PMS-DISCIPLINE AHP Gate YAML is present if AHP routing occurred.
* Checked AHP Module Output YAML is present if AHP was applied.
* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* The Stage 2 Layer Digest Extraction YAML from the previous step is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

AUTHORITATIVE RUNNER CASE-RECORD MANIFEST:
{RUNNER_CASE_RECORD_MANIFEST}

CURRENT-STEP OUTPUT RULE:

* The current step's expected output path, current status, and temporary output-existence value are runner execution metadata only.
* Do not copy current-step execution metadata into the generated or reviewed YAML.
* Do not place the current step's own output status in notes, missing-item registers, deliberately-not-imported items, workflow findings, tensions, blockers, readiness fields, or case findings.
* The current output does not need to exist before generation and must not be classified as missing, deferred, excluded, unresolved, or deliberately not imported.
* Preserve genuine substantive contradictions, but do not convert temporary runner metadata into case substance.

SOURCE AUTHORITY HIERARCHY:

For exact metadata and provenance:
1. Authoritative Runner Case-Record Manifest
2. Checked Stage 1 Artifact Index
3. Stage 2 output under review
4. Stage 2 template default or placeholder
5. Model inference

For substantive digest content, the corresponding checked layer artifact controls. Checked Stage 1 controls selection and provenance. Template defaults and model inference cannot override either.

TASK:
Check the Stage 2 Layer Digest Extraction YAML from the previous step for semantic, digest, route, and boundary conformity with the Stage 2 template, checked prior artifacts, checked Stage 1 output, and the bounded task. Use runner-generated local validation as authoritative for deterministic YAML structure when available.

PURPOSE:
Determine whether the Stage 2 Layer Digest Extraction YAML is usable as checked Stage 2 output for Stage 3. Where necessary, conservatively correct it so that it accurately extracts and preserves digest-level content without reanalysis or claim strengthening.

TECHNICAL INSTRUCTIONS:

* Use only the Stage 2 Layer Digest Extraction YAML from the previous step, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked Stage 1 output, and the previously applied Stage 2 template structure.
* Re-run Stage 2 from scratch only if the runner-generated local validation handoff reports a blocking structural defect that cannot be patched conservatively.
* Do not independently re-audit YAML syntax, duplicate keys, the complete key tree, types, or configured enum values when local validation is authoritative. Address only the exact structural findings supplied by the runner; otherwise perform semantic review only.
* Check substantive conformity: digest fidelity, checked-artifact grounding, branch separation, source-status discipline, claim-ceiling preservation, uncertainty preservation, non-use preservation, MIP/AHP separation, AHP non-interference, rival pressure, correctability, and reopening conditions.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

STEP BOUNDARIES:
This check excludes:

* re-running prior pipeline stages
* changing checked prior artifacts outside the Stage 2 YAML
* changing checked Stage 1
* integrating a full record
* producing new substantive analysis
* resolving contradictions by interpretation
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* runner-reported invalid YAML or deterministic structural findings
* runner-reported missing or unexpected fields, type mismatches, or invalid configured values
* unresolved required placeholders only where they create a concrete semantic or boundary defect
* unsupported source or file assumptions
* digest content not grounded in checked artifacts
* PMS operator identity or function changed during digest compression
* compression that strengthens claims
* compression that erases uncertainty or source limits
* skipped branches omitted or misrepresented
* non-use converted into deficiency
* selected add-on, MIP, or AHP digests mixed together
* AHP output treated as MIP correction or rescoring
* Attack Points treated as proven defects
* Hardening Backlog treated as mandate
* Precision Heuristic treated as authority
* source-status laundering
* claim ceiling overreach
* loss of rival readings, non-capture, correctability, or reopening conditions
* generated Stage 3 integration inside Stage 2

MANDATORY CRITERIA LEDGER:
Evaluate every criterion separately and mark it PASS or FAIL. A general statement such as “coherent,” “faithful,” or “ready” is not sufficient.

1. Runner-generated local YAML validation is respected: exact reported structural findings are handled, and when the runner reports clean structure or no handoff, no independent full-key-tree audit is performed.
2. The imported Stage 1 reference and every upstream case-record output path match the runner manifest exactly; current-step execution metadata is not imported into Stage 2.
3. selected_artifacts_to_read matches checked Stage 1 exactly; no unselected, skipped, absent, or unavailable artifact is silently read.
4. Every digest identifies the exact selected source artifact path; session.json is not used as a substitute unless explicitly assigned by the runner manifest or checked Stage 1.
5. Each substantive digest is grounded in its corresponding checked layer artifact and contains no new analysis; every PMS operator preserves its canonical identity, canonical function, and checked case-specific role without renaming, repurposing, merging, or substitution.
6. Route, branch, skipped, rejected, non-use, and not_applicable states are preserved exactly.
7. Digest compression does not strengthen claims, erase uncertainty, erase source limits, or turn contradictions into resolved findings.
8. Core, selected add-on, MIP, and AHP remain separate; AHP does not rescore or correct MIP.
9. Rival pressure, non-capture, claim ceiling, correctability, reopening conditions, and stop-capability are preserved where present.
10. Attack Points are not treated as proven defects, Hardening Backlog is not a mandate, and Precision Heuristic is not authority.
11. Stage 2 contains no Stage 3 integration, article prose, new source material, or later-pipeline artifact.
12. Stage 3 export/readiness fields accurately reflect the checked Stage 2 result and any real blockers.

READINESS RULE:
The output may be declared ready only if every criterion is PASS after any correction. Any FAIL must be corrected inside Stage 2 or reported as blocking.

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the Stage 2 Layer Digest Extraction YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep claims at or below the level licensed by checked artifacts and checked Stage 1.
* Exclude invented files, new source claims, new analysis, full-record integration, MIP rescoring, AHP authority drift, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a PMS-DISCIPLINE Stage 2 Layer Digest Extraction YAML only.

OUTPUT:
Always return the completed criteria ledger first, with all 12 numbered criteria marked PASS or FAIL and one concise reason per criterion.

If all criteria are PASS without correction, then return:

* CHECK STATUS: ready
* FINAL RESULT: PMS-DISCIPLINE Stage 2 Layer Digest Extraction YAML checked. Ready for Stage 3 Full Record Integration.

If concrete defects can be conservatively corrected inside this step, then return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* CRITERIA AFTER CORRECTION: repeat all 12 criteria as PASS or FAIL
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED PMS-DISCIPLINE STAGE 2 LAYER DIGEST EXTRACTION YAML

If the output is not safely correctable inside this step, then return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

Do not declare ready while any criterion remains FAIL.

---

## Prompt #24 — Apply PMS-DISCIPLINE Case Record Stage 3 Full Record Integration

You are continuing a PMS-DISCIPLINE pipeline run.

FILES PROVIDED:

* pms_case_record_stage_3_full_case_record_integration_template.yaml

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present if MIP routing occurred.
* Checked MIP Case Application YAML is present if MIP was applied.
* Checked PMS-DISCIPLINE AHP Gate YAML is present if AHP routing occurred.
* Checked AHP Module Output YAML is present if AHP was applied.
* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

AUTHORITATIVE RUNNER CASE-RECORD MANIFEST:
{RUNNER_CASE_RECORD_MANIFEST}

CURRENT-STEP OUTPUT RULE:

* The current step's expected output path, current status, and temporary output-existence value are runner execution metadata only.
* Do not copy current-step execution metadata into the generated or reviewed YAML.
* Do not place the current step's own output status in notes, missing-item registers, deliberately-not-imported items, workflow findings, tensions, blockers, readiness fields, or case findings.
* The current output does not need to exist before generation and must not be classified as missing, deferred, excluded, unresolved, or deliberately not imported.
* Preserve genuine substantive contradictions, but do not convert temporary runner metadata into case substance.

SOURCE AUTHORITY HIERARCHY:

For exact metadata and provenance:
1. Authoritative Runner Case-Record Manifest
2. Checked Stage 1 Artifact Index
3. Checked Stage 2 Layer Digest Extraction
4. Stage 3 template default or placeholder
5. Model inference

For substantive integrated content:
1. Checked Stage 2 Layer Digest Extraction
2. Checked Stage 1 for provenance, route, branch, and artifact status only
3. Underlying checked artifacts only for a gap explicitly marked by Stage 1 or Stage 2
4. Stage 3 template structure
5. Model inference only as an explicit bounded marker

Conflict rules:

* Exact output paths and run states follow the runner manifest. In particular, the Stage 2 source reference must use the exact Step #22 output path, not session.json.
* Preserve genuine substantive contradictions as contradictions.
* Internal path discrepancies, template-status drift, attachment-name drift, and workflow QA notes are metadata issues, not substantive case findings.

TASK:
Apply pms_case_record_stage_3_full_case_record_integration_template.yaml to integrate checked Stage 1 and checked Stage 2 into a bounded full record for this PMS-DISCIPLINE pipeline run.

PURPOSE:
Produce a Stage 3 Full Record Integration YAML that consolidates artifact status, layer digests, branch status, claim ceiling, non-use, rival pressure, correctability, reopening conditions, and permitted next-step boundaries.

TECHNICAL INSTRUCTIONS:

* Use only the provided Stage 3 template, CASE PACKET, PMS.yaml context, checked Stage 1 Artifact Index YAML, checked Stage 2 Layer Digest Extraction YAML, and checked prior artifacts only where needed to verify fidelity to checked Stage 1 and checked Stage 2; Stage 3 must still fill from checked Stage 1 and checked Stage 2.
* Use the Stage 3 template as the only output structure.
* HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
* Fill fields precisely from checked Stage 1 and checked Stage 2.
* Use not_applicable, skipped, absent, unknown, unclear, unresolved, under_specified, insufficient, none, or another field-allowed bounded marker where the input does not license a stronger value.
* Integrate only what Stage 1 and Stage 2 already establish.
* Preserve canonical PMS operator identities and functions exactly as established by the checked Core and preserved by checked Stage 2.
* Do not use integration prose to rename, repurpose, merge, or substitute an operator.
* Preserve layer separation inside the integrated record.
* Preserve selected add-on, MIP, and AHP branch status.
* Preserve AHP as optional second-order analysis-quality overlay where present.
* Preserve AHP non-interference and MIP output integrity.
* Preserve source status, intended use, claim ceiling, non-capture, rival pressure, correctability, reopening conditions, and stop-capability.
* Record decision-state posture only as an integrated status; execution remains outside this stage.

STEP BOUNDARIES:
This step excludes:

* re-running prior pipeline stages
* checking or patching prior outputs
* changing checked Stage 1 or checked Stage 2
* producing new substantive analysis
* changing MIP scores, bands, boxes, modules, Red Zones, or source status
* treating AHP as MIP correction, MIP rescoring, or person assessment
* converting Attack Points into proven defects
* converting Hardening Backlog into mandate
* resolving contradictions by interpretation
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts

STAGE 3 SCOPE:
This step may produce:

* integrated artifact-status record
* integrated layer-digest record
* branch-status summary
* skipped-branch and non-use summary
* claim-ceiling summary
* uncertainty summary
* rival and non-capture summary
* correctability and reopening summary
* human-confirmation requirement summary where relevant
* permitted next-step boundary
* Stage 3 readiness status for Stage 3 output check

CLAIM DISCIPLINE:

* Treat Stage 3 as integration only.
* Integration does not create new authority.
* Integration must not strengthen checked prior claims.
* Integration must not erase uncertainty, skipped branches, non-use, source limitations, or rival pressure.
* Preserve unresolved contradictions where checked prior artifacts leave them unresolved.
* Mark uncertainty explicitly.

OUTPUT:
Return only the completed PMS-DISCIPLINE Stage 3 Full Record Integration YAML.
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #25 — Check PMS-DISCIPLINE Case Record Stage 3 Full Record Integration

You are continuing a PMS-DISCIPLINE pipeline run.

AVAILABLE CONTEXT:

* PMS.yaml was read earlier and remains the PMS Base reference.
* Checked Pre-Analysis YAML is present in this conversation/session.
* Checked Core Case Application YAML is present in this conversation/session.
* Checked Add-on Recommendation Gate YAML is present in this conversation/session.
* Checked selected PMS add-on case application YAML is present if an add-on was applied.
* Checked PMS-DISCIPLINE MIP Gate YAML is present if MIP routing occurred.
* Checked MIP Case Application YAML is present if MIP was applied.
* Checked PMS-DISCIPLINE AHP Gate YAML is present if AHP routing occurred.
* Checked AHP Module Output YAML is present if AHP was applied.
* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session.
* The Stage 3 Full Record Integration YAML from the previous step is present in this conversation/session.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

AUTHORITATIVE RUNNER CASE-RECORD MANIFEST:
{RUNNER_CASE_RECORD_MANIFEST}

CURRENT-STEP OUTPUT RULE:

* The current step's expected output path, current status, and temporary output-existence value are runner execution metadata only.
* Do not copy current-step execution metadata into the generated or reviewed YAML.
* Do not place the current step's own output status in notes, missing-item registers, deliberately-not-imported items, workflow findings, tensions, blockers, readiness fields, or case findings.
* The current output does not need to exist before generation and must not be classified as missing, deferred, excluded, unresolved, or deliberately not imported.
* Preserve genuine substantive contradictions, but do not convert temporary runner metadata into case substance.

SOURCE AUTHORITY HIERARCHY:

For exact metadata and provenance:
1. Authoritative Runner Case-Record Manifest
2. Checked Stage 1 Artifact Index
3. Checked Stage 2 Layer Digest Extraction
4. Stage 3 output under review
5. Stage 3 template default or placeholder
6. Model inference

For substantive content, checked Stage 2 controls the integrated layer substance. Checked Stage 1 controls provenance, route, branch, and artifact status. Template defaults and model inference cannot override either.

TASK:
Check the Stage 3 Full Record Integration YAML from the previous step for semantic, integrated-record, route, and boundary conformity with the Stage 3 template, checked Stage 1, checked Stage 2, checked prior artifacts, and the bounded task. Use runner-generated local validation as authoritative for deterministic YAML structure when available.

PURPOSE:
Determine whether the Stage 3 Full Record Integration YAML is usable as checked integrated record output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it remains structurally valid, bounded, non-authoritative, and faithful to checked Stage 1 and checked Stage 2.

TECHNICAL INSTRUCTIONS:

* Use only the Stage 3 Full Record Integration YAML from the previous step, CASE PACKET, PMS.yaml context, checked Stage 1, checked Stage 2, checked prior artifacts, and the previously applied Stage 3 template structure.
* Re-run Stage 3 from scratch only if the runner-generated local validation handoff reports a blocking structural defect that cannot be patched conservatively.
* Do not independently re-audit YAML syntax, duplicate keys, the complete key tree, types, or configured enum values when local validation is authoritative. Address only the exact structural findings supplied by the runner; otherwise perform semantic review only.
* Check substantive conformity: fidelity to checked Stage 1 and checked Stage 2, source-status discipline, claim ceiling, non-use preservation, branch separation, MIP output preservation, AHP non-interference, rival pressure, non-capture, correctability, reopening conditions, stop-capability, and non-authority boundaries.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.
* Treat Stage 3 lifecycle fields as generation-time artifact state. A conforming step #24 record may remain `stage_3_full_record_ready_for_output_check`, `ready`, and `stage_3_output_check` while step #25 records the separate check result. Do not patch those fields solely because the check is now being performed or completed.

STEP BOUNDARIES:
This check excludes:

* re-running prior pipeline stages
* changing checked prior artifacts outside the Stage 3 YAML
* changing checked Stage 1 or checked Stage 2
* producing new substantive analysis
* changing MIP scores, bands, boxes, modules, Red Zones, or source status
* treating AHP as MIP correction, MIP rescoring, person assessment, or authority layer
* converting Attack Points into proven defects
* converting Hardening Backlog into mandate
* resolving contradictions by interpretation
* adding source material, files, inferred case facts, or unavailable context
* generating later pipeline artifacts
* stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:

* runner-reported invalid YAML or deterministic structural findings
* runner-reported missing or unexpected fields, type mismatches, or invalid configured values
* unresolved required placeholders only where they create a concrete semantic or boundary defect
* unsupported source or file assumptions
* integrated content not grounded in checked Stage 1 or checked Stage 2
* integration that strengthens claims
* integration that erases uncertainty or source limits
* skipped branches omitted or misrepresented
* non-use converted into deficiency
* selected add-on, MIP, or AHP branches mixed together
* AHP output treated as MIP correction or rescoring
* Attack Points treated as proven defects
* Hardening Backlog treated as mandate
* Precision Heuristic treated as authority
* source-status laundering
* claim ceiling overreach
* loss of rival readings, non-capture, correctability, reopening conditions, or stop-capability
* generated later pipeline artifacts

MANDATORY CRITERIA LEDGER:
Evaluate every criterion separately and mark it PASS or FAIL. A general statement such as “coherent,” “bounded,” or “ready” is not sufficient.

1. Runner-generated local YAML validation is respected: exact reported structural findings are handled, and when the runner reports clean structure or no handoff, no independent full-key-tree audit is performed.
2. generated_from and all case-record provenance paths match the runner manifest exactly, including the exact Step #20 and Step #22 output paths.
3. Stage 1 controls artifact, route, branch, skipped, and non-use metadata; Stage 2 controls substantive digest content.
4. Integrated content is grounded in checked Stage 1 and checked Stage 2 and introduces no new analysis; canonical PMS operator identities, functions, and checked case-specific roles remain unchanged.
5. Source status, intended use, claim ceiling, person-nearness, publicness, and irreversibility do not drift from controlling checked sources.
6. Selected add-on, MIP, and AHP remain separate; AHP does not rescore, correct, or authorize MIP.
7. Skipped, rejected, absent, not_applicable, and non-used layers remain visible and are not converted into deficiencies.
8. Genuine substantive contradictions, uncertainty, rival pressure, non-capture, correctability, reopening conditions, and stop-capability remain visible.
9. Internal path discrepancies, template-status drift, and workflow QA notes are not converted into substantive case findings.
10. Attack Points are not proven defects, Hardening Backlog is not a mandate, and Precision Heuristic is not authority.
11. The Stage 3 record preserves its generation-time lifecycle status, normally ready for the separate Stage 3 output check. Completion of this current review is recorded in the step #25 check artifact and is not back-propagated into the Stage 3 record merely because the review has now occurred.
12. Stage 3 contains no article prose, new source material, later-pipeline artifact, truth certificate, release authorization, or implementation permission.

READINESS RULE:
The output may be declared ready only if every criterion is PASS after any correction. Any FAIL must be corrected inside Stage 3 or reported as blocking.

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the Stage 3 Full Record Integration YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep claims at or below the level licensed by checked Stage 1, checked Stage 2, and checked prior artifacts.
* Exclude invented files, new source claims, new analysis, MIP rescoring, AHP authority drift, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a PMS-DISCIPLINE Stage 3 Full Record Integration YAML only.

OUTPUT:
Always return the completed criteria ledger first, with all 12 numbered criteria marked PASS or FAIL and one concise reason per criterion.

If all criteria are PASS without correction, then return:

* CHECK STATUS: ready
* FINAL RESULT: PMS-DISCIPLINE Stage 3 Full Record Integration YAML checked. Ready for the next PMS-DISCIPLINE pipeline step.

If concrete defects can be conservatively corrected inside this step, then return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
* CRITERIA AFTER CORRECTION: repeat all 12 criteria as PASS or FAIL
* Put the complete corrected artifact in exactly one fenced `yaml` code block. The block must contain only the corrected YAML and must use the reviewed source artifact's exact root key. Do not include any second YAML block.
* COMPLETE CORRECTED PMS-DISCIPLINE STAGE 3 FULL RECORD INTEGRATION YAML

If the output is not safely correctable inside this step, then return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

Do not declare ready while any criterion remains FAIL.

---

## Prompt #26 — Iteration Handoff and Follow-up Preparation

You are continuing a PMS-DISCIPLINE pipeline run.

This step prepares a prospective Iteration Handoff after the completed Case Record Stages 1–3 and before optional Markdown article generation.

This step is not Case Record Stage 4. It does not continue the current case analysis. It assesses whether a separately bounded future case could usefully deepen, test, weaken, differentiate, or redirect specific aspects of the current checked record.

AVAILABLE CONTEXT:

* Checked Stage 1 Artifact Index YAML is present in this conversation/session when semantic review steps are enabled. If semantic review steps are disabled, use the direct Stage 1 output only as unchecked context.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session when semantic review steps are enabled. If semantic review steps are disabled, use the direct Stage 2 output only as unchecked context.
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session when semantic review steps are enabled. If semantic review steps are disabled, use the direct Stage 3 output only as unchecked context.
* The CASE PACKET remains bounded source material for the current run.
* The runner-generated manifest below controls exact source paths, review status, and current-step boundaries.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

{RUNNER_ITERATION_HANDOFF_MANIFEST}

TASK:
Apply `pms_discipline_iteration_handoff_template.yaml`.

Produce a lightweight Iteration Handoff YAML that gives a model preselection for the user. The runner will show this preselection to the user in a confirmation window where each proposed target can be accepted, refined, replaced, split, merged, rejected, or annotated. The user-confirmation fields remain pending in this prompt output; the runner fills them after user review.

SOURCE HIERARCHY:

1. Checked Stage 3 Full Record Integration YAML controls the current integrated result, claim ceiling, unresolved items, rival pressure, limits, final posture, and reopening conditions.
2. Checked Stage 2 Layer Digest Extraction YAML supplies layer-specific depth, selective shallowness, non-use, and uncertainty.
3. Checked Stage 1 Artifact Index YAML supplies provenance, actual artifacts, branch state, and eligible carry-forward references.
4. Underlying checked artifacts may be consulted only where Stage 1, Stage 2, or Stage 3 explicitly identifies a gap, contradiction, unresolved item, or need for layer-specific verification.
5. The CASE PACKET remains bounded source material only where the checked record chain licenses reference to it.
6. Optional article outputs, examples, final article prose, article checks, drafting notes, and article wording are not sources for this handoff.

MIP AND AHP HANDOFF RULE:

If MIP or AHP was used, recommended, rejected, skipped, unresolved, or preserved as non-use in checked Stage 1–3, include its handoff-relevant status only through the checked Case Record.

For MIP, preserve only checked MIP status, source burden, qualitative A/M or IA/D handling where present, red-zone or non-use conditions, and claim-boundary effects already preserved by Stage 3.

For AHP, preserve only checked analysis-quality implications such as precision pressure, attack-surface visibility, hardening backlog, misreadability, transmission risk, score-language hygiene, D-language caution, reversibility, and iteration support.

AHP-derived items may justify follow-up questions or required new material, but they must remain review surfaces, not proven defects or mandates.

Do not rescore MIP, activate D, upgrade evidence, authorize stronger claims, or preselect MIP/AHP for a future follow-up case.

SOURCE EXCLUSION RULE:
Do not derive any Iteration Handoff finding, urgency, target, follow-up question, or material requirement from:

ASSESS:

* current analytical depth relative to the original intended use;
* whether the current case remains sufficient for that original intended use;
* materially developed areas;
* selectively shallow, unresolved, or blocked areas;
* the value of a separately bounded follow-up case;
* iteration urgency and reasons;
* factors that raise or lower urgency;
* minimum follow-up coverage implied by urgency;
* candidate follow-up targets with stable target IDs;
* required new material for each target;
* expected discriminative value for each target;
* whether an iteration outlook might later be appropriate in an article.

USER-RESPONSE SUPPORT STRUCTURE:

The template contains fields for later user response. Preserve these fields even though they remain pending here. Do not pre-fill user notes, revised questions, target responses, or effective targets as if the user had already confirmed them.

The later runner dialog may record:

* action per proposed target: accept, refine, replace, split, merge, reject;
* user note per target;
* a user-revised or replacement question;
* the user's reason why the revised question is more precise;
* the prior checked-record point the user thinks it builds on;
* additional material needed;
* chronology or trajectory notes;
* article visibility: exclude, summarize, include;
* additional user-created follow-up questions.

These later user notes may guide a future case. They are not verified facts, current-case findings, evidence, operator activations, or confirmation of the prior analysis.

ITERATION URGENCY SCALE:

Use exactly one level:

* none — no material follow-up value is visible; further analysis would probably add volume without discrimination.
* low — one optional refinement could be useful, but the current case is sufficient for its original use and no stronger-use pressure is visible.
* moderate — follow-up is useful before stronger reuse or broader claims, but the current case may close for its original use.
* high — stronger use would be risky without a new bounded follow-up case, and multiple material dimensions need coverage.
* critical — the next intended use or claim should not continue without a new bounded case that addresses all blocking targets.

MINIMUM COVERAGE GUIDANCE:

* none: no minimum material target.
* low: at least one material target if a handoff is prepared.
* moderate: at least two material targets, or one central target with two clearly distinct subquestions.
* high: at least three material targets across at least two distinct dimensions.
* critical: all blocking targets must be identified; the minimum is determined by the blockers rather than a fixed count.

A material target counts only when it includes a concrete follow-up question, a basis in the checked record, required new material or an explicit unknown-material marker, and an expected discriminative value.

PROSPECTIVE LANGUAGE ONLY:

Use formulations such as:

* test whether
* examine whether
* clarify whether
* compare
* distinguish
* may confirm, weaken, differentiate, or redirect

Do not write as if the follow-up case already has findings.

FORBIDDEN:

* Do not create new case findings.
* Do not assign or preassign PMS operators for the future case.
* Do not recommend or preselect an add-on route.
* Do not recommend or preselect MIP or AHP.
* Do not inherit the current claim ceiling into a future case.
* Do not treat prior checked analysis as evidence.
* Do not treat user notes as verified facts.
* Do not describe the current case as incomplete merely because further iteration is possible.
* Do not use the final article, article drafts, or examples as sources.
* Do not produce Markdown article prose.

OUTPUT:
FIELD-SPECIFIC VALUE RULE:
- Explicit allowed values declared by the template field override generic uncertainty or bounded markers.
- Never place `none`, `not_applicable`, `unknown`, `unclear`, or another generic marker into a field whose explicit enum does not allow it.
- Use the closest semantically correct permitted value and preserve remaining uncertainty in an adjacent explanatory field.

Preserve the template root and field structure as far as possible.
Set `user_response.status` to `pending`, `user_response.overall_decision` to `pending`, and `effective_followup_preparation.status` to `pending_user_confirmation` unless the model recommendation is `no_material_iteration_value` and no material target is proposed. Leave `user_response.target_responses`, `user_response.additional_questions`, and `effective_followup_preparation.effective_targets` empty until the runner records the user's confirmation or revision.
Return exactly one plain fenced `yaml` code block. The block must contain only the completed YAML. Do not include prose before or after it, and do not add an ID, title, attributes, or metadata to the opening fence.

---

## Prompt #27 — Article Source Setup and Rendering Contract

You are continuing a PMS-DISCIPLINE pipeline run.

This step establishes the source hierarchy and selected article-profile contract for rendering the completed case-record chain into Markdown prose.

AVAILABLE CONTEXT:

* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session.
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session.
* The Iteration Handoff YAML from step #26 is present if actually produced. It is prospective planning context only, not a source for current case findings.
* Checked prior PMS-DISCIPLINE artifacts are present where applicable.
* The CASE PACKET remains the bounded source material for this run.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

{RUNNER_ARTICLE_PROFILE_CONTRACT}

TASK:
Establish the source hierarchy and rendering contract for the selected article profile.

SOURCE HIERARCHY:

1. Checked Stage 3 Full Record Integration YAML controls the article's substantive integrated record, title, claim boundary, final posture, unresolved items, and permitted use.
2. Checked Stage 2 Layer Digest Extraction YAML supplies layer-level analytical depth without overriding Stage 3.
3. Checked Stage 1 Artifact Index YAML supplies provenance and artifact status. It is not a source of new case findings.
4. The Iteration Handoff may be considered only as prospective follow-up context. It must not alter the current case result, route, claim ceiling, operator status, source status, or sufficiency assessment.
   Use the runner-generated `ITERATION OUTLOOK HANDOFF` block to determine whether an Iteration outlook may be rendered later, which effective targets are article-visible, and which user notes must remain excluded.
5. Underlying checked artifacts may be consulted only where Stage 2 or Stage 3 explicitly identifies a gap, contradiction, unresolved item, or need for layer-specific verification.
6. The CASE PACKET remains bounded source material only where the checked record chain licenses reference to it.

COMMON RENDERING DISCIPLINE:

* Do not re-run analysis.
* Do not strengthen claims.
* Do not treat YAML, workflow completion, or AI-generated prose as evidence.
* Preserve material unresolved items, source limits, rival pressure, weakening conditions, reopening conditions, and distinctive misuse risks.
* Keep workflow QA separate from case substance.
* Mention an internal workflow issue only when checked Stage 3 states that it materially limits record reliability or interpretation.
* Do not import temporary runner execution metadata, local installation inventory, attachment names, drafting metadata, or profile-selection metadata into article prose.
* State each provenance fact, route decision, claim boundary, non-use result, and non-authority warning once at the point where it contributes most.

PROFILE APPLICATION:

For `case_article`:

* Stage 1 controls provenance silently unless a material record limitation must be disclosed.
* Preserve the case-specific analysis rather than narrating the complete workflow.
* Do not require an audit capsule, full source-chain section, generic boundary catalogue, full inactive-layer inventory, report-readiness section, or examples-policy section.
* Mention inactive layers only when their non-use prevents a case-specific false trigger or materially explains the result.

For `full_analysis_article`:

* Preserve detailed provenance, layer decisions, relevant non-use, claim boundaries, and reopening conditions.
* Detailed does not mean repetitive.
* Do not turn the article into a raw file inventory or a transcript of every pipeline step.

TITLE RULE:
The final article begins with the exact case title from checked Stage 3 as an H2 heading. Fall back to checked Stage 2, then to the checked Core title only when Stage 1 selected that artifact as current. Do not invent a title.

OUTPUT:
Respond only:

Article-generation source hierarchy and selected profile contract established.

---

## Prompt #28 — Base Markdown Case Article Draft

You are continuing a PMS-DISCIPLINE pipeline run.

The source hierarchy and selected article-profile contract were established in the previous step.

AVAILABLE CONTEXT:

* Checked Stage 1 Artifact Index YAML is present.
* Checked Stage 2 Layer Digest Extraction YAML is present.
* Checked Stage 3 Full Record Integration YAML is present.
* The Iteration Handoff YAML from step #26 is present if actually produced. It is prospective planning context only, not current-case evidence.
* Checked prior PMS-DISCIPLINE artifacts are present where applicable.
* The CASE PACKET remains the bounded source material.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

{RUNNER_ARTICLE_PROFILE_CONTRACT}

TASK:
Create the base Markdown article draft for the selected article profile.

SOURCE HIERARCHY:

1. Checked Stage 3 is the primary article source.
2. Checked Stage 2 supplies analytical depth.
3. Checked Stage 1 supplies provenance and branch status only.
4. The Iteration Handoff may not change the article's current-case result. Do not render an iteration outlook unless the handoff contains a confirmed user decision and article_outlook explicitly permits it.
5. Underlying checked artifacts may verify an explicitly marked gap but may not introduce new claims.

COMMON TECHNICAL RULES:

* Output Markdown only.
* Do not output YAML or code blocks.
* Do not add meta-commentary outside the article.
* Begin with `## [EXACT CASE TITLE]`.
* Do not re-run Core, add-on, MIP, AHP, or Case Record analysis.
* Do not resolve contradictions through interpretation.
* Do not introduce new facts, files, source material, or context.
* Preserve the controlling source status, claim ceiling, unresolved conditions, rival pressure, correctability, and reopening conditions.
* Preserve case-specific operator calibration and layer separation.
* Keep add-on handles distinct from PMS operators.
* Keep MIP and AHP results distinct and include them only where active or case-specifically relevant.
* Keep workflow QA metadata out of case findings.
* Do not generate examples in this step.
* Do not repeat the same boundary or non-use statement in multiple sections.

ITERATION OUTLOOK RENDERING:

* Render an `### Iteration outlook` section only when the runner-generated `ITERATION OUTLOOK HANDOFF` says `render_iteration_outlook: yes`.
* If `render_iteration_outlook: no`, omit the section entirely. Do not mention that an outlook was omitted.
* The section is prospective only. It must state that any follow-up would be a new, separately bounded case.
* Do not describe the current case as incomplete when the handoff states that it is sufficient for the original intended use.
* Do not convert proposed follow-up questions into current-case findings, operator activations, add-on recommendations, MIP/AHP recommendations, evidence, or claim authority.
* Use only article-visible effective targets and permitted summary points from the runner-generated handoff. Excluded raw user notes must not appear.
* For `case_article`, keep the outlook brief: current sufficiency, one to three follow-up focuses, and the new-case boundary.
* For `full_analysis_article`, the outlook may include depth status, urgency, reasons, selected effective questions, required new material, expected discriminative value, and the carry-forward boundary.

PROFILE-SPECIFIC STRUCTURE:

For `case_article`, use this structure unless a section is genuinely not applicable:

## [EXACT CASE TITLE]

### Why this case matters

Explain the case-specific closure pressure, structural tension, and why the case is mapped rather than solved.

### Structural reading

Render the main PMS Core movement in compact but substantial prose. Apply the runner-generated canonical PMS operator naming rule throughout the article: at the first occurrence of each operator in every paragraph, write the symbol followed by its canonical English name in parentheses, for example `**Δ** (Difference)`. Later occurrences of the same operator within that paragraph may use the symbol alone. Symbol-only formulas remain permitted. Preserve important dependencies and calibrations, and include an active add-on, MIP, or AHP contribution only where it adds a case-specific result.

Center the structural reading on the operators that carry the case's main movement. Do not produce a mandatory operator-by-operator catalogue.

Group weak, conditional, dependency-limited, inactive, or analytic-only operators by shared calibration function. Normally place them in no more than one compact calibration paragraph unless an individual operator contributes a distinct case-specific result that cannot be preserved by grouping.

Do not create a separate paragraph or subsection for an operator merely to show that it was considered. Do not repeat the same calibration point in different operator-specific wording.

### What the analysis shows

State the central structural movement or formula, what the active layers make visible, and where residue, non-capture, or unresolved structure remains.

### Rival reading and reopening conditions

Preserve the strongest case-specific rival reading, relevant weakening or falsifier conditions, operationalization limits where material, and conditions that would reopen the result.

### Case-specific boundary

State only the distinctive misuse or escalation risks created by this case. Normally select the two to four risks nearest to the case material and actual analysis.

Do not repeat a generic catalogue of every PMS-DISCIPLINE prohibition. Mention broader legal, clinical, forensic, HR, automated-decision, publication, implementation, or institutional-use boundaries only when the case, intended use, active layer, or checked record creates concrete proximity to that misuse.

### Case takeaway

Give a concise synthesis of what the case shows and what remains open.

For `case_article`, do not require or recreate:

* an audit-style case capsule;
* a full source-chain and integration-status section;
* workflow correction history;
* a complete claim-boundary catalogue;
* a complete list of inactive operators;
* individual subsections for every unused add-on;
* generic MIP or AHP non-use exposition;
* a layer-interaction section when no later layer contributes;
* report-readiness or examples-policy planning;
* a generic misuse-boundary catalogue;
* remote legal, clinical, forensic, HR, automated-decision, publication, implementation, or institutional-use prohibitions without concrete case proximity.

For `full_analysis_article`, use a detailed structure appropriate to the checked record. It may include:

* case capsule;
* why the case matters;
* source chain and integration status;
* claim status and scope discipline;
* scene and frame structure;
* substantial PMS Core reading;
* dependency and calibration discipline;
* derived structures and drift status where present;
* active and materially relevant inactive-layer decisions;
* layer interaction;
* MIP/AHP record where applicable;
* rival and non-capture readings;
* weakening, falsifier, operationalization, and reopening conditions;
* misuse boundary;
* report readiness.

For `full_analysis_article`, do not repeat identical provenance, route, boundary, or non-authority statements across multiple sections. Local availability of an unused file is not an analytical result.

LENGTH GUIDANCE:

* `case_article`: normally about 1,500–3,500 words. There is no minimum. Preserve analytical sufficiency without restoring audit structure.
* `full_analysis_article`: normally about 5,000–8,000 words, with additional length only where an actual multi-layer record requires it. There is no artificial minimum.

OUTPUT:
Return Markdown only.
No YAML.
No code blocks.
No meta-commentary outside the article.

---

## Prompt #29 — Example Decision and Optional Example Generation

You are continuing a PMS-DISCIPLINE pipeline run.

The base Markdown article draft exists for the selected profile.

AVAILABLE CONTEXT:

* Checked Stage 1, Stage 2, and Stage 3 outputs are present.
* The Iteration Handoff YAML from step #26 is present if actually produced. It is prospective planning context only, not current-case evidence.
* The Base Markdown Case Article Draft is present.
* The CASE PACKET remains the bounded source material.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

{RUNNER_ARTICLE_PROFILE_CONTRACT}

TASK:
Decide whether an additional illustrative example is permitted and useful, and generate it only when warranted.

DECISION STATES:
Use exactly one:

* examples_not_applicable
* examples_unsafe
* examples_not_needed
* examples_optional
* examples_recommended
* examples_required_for_readability
* no_examples

COMMON RULES:

* Examples are illustrative, not evidentiary.
* Do not add new case claims, new source material, new operator assignments, new layer triggers, scores, verdicts, diagnoses, legal conclusions, or implementation authority.
* Preserve the article's claim ceiling and case-specific boundaries.
* Do not dramatize uncertainty, conflict, person-nearness, harm, or institutional consequence beyond the checked record.
* Drafting metadata belongs only in this step and must not appear in the final article.

PROFILE RULES:

For `case_article`:

* Default to no additional example when the case scene already makes the structural movement readable.
* Generate at most one additional example.
* Prefer a micro or compact vignette.
* Generate a longer worked example only when checked Stage 3 or the base draft shows that readability otherwise fails.
* Do not use an example merely to increase article length.

For `full_analysis_article`:

* One or more examples may be generated where the checked examples policy supports them.
* Preserve substantial examples without thinning their internal analysis.
* Do not create examples simply to mirror every layer or every unused branch.

OUTPUT FORMAT:

### Example decision

[exactly one decision state]

### Reason

[brief source-grounded reason]

### Generated example

Write `none` when no example is generated.

When an example is generated, provide the complete Markdown example body. Do not include drafting labels such as `Type`, `Recommended insertion point`, or generation metadata inside the example body.

---

## Prompt #30 — Final Integrated Markdown Case Article

You are continuing a PMS-DISCIPLINE pipeline run.

The Base Markdown Case Article Draft and the Example Decision are present.

AVAILABLE CONTEXT:

* Checked Stage 1, Stage 2, and Stage 3 outputs are present.
* The Base Markdown Case Article Draft is present.
* The Example Decision and any generated example are present.
* The Iteration Handoff YAML from step #26 is present if actually produced. It is prospective planning context only, not current-case evidence.
* The CASE PACKET remains the bounded source material.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

{RUNNER_ARTICLE_PROFILE_CONTRACT}

TASK:
Produce the final Markdown article for the selected profile.

SOURCE HIERARCHY:

1. Checked Stage 3 controls the integrated record and claim boundary.
2. Checked Stage 2 supplies analytical depth.
3. Checked Stage 1 supplies provenance only.
4. The Iteration Handoff may not alter current-case findings or claim boundaries. Render iteration outlook content only when user-confirmed and explicitly permitted by the handoff.
5. The Base Draft controls the article's profile-specific structure unless it conflicts with the checked record.
6. Generated examples may be inserted only when the Example Decision permits them.

ITERATION OUTLOOK INTEGRATION:

* Preserve a valid Iteration outlook from the Base Draft when it follows the runner-generated handoff.
* Add an Iteration outlook only when the Base Draft omitted one and the runner-generated `ITERATION OUTLOOK HANDOFF` says `render_iteration_outlook: yes`.
* Remove or weaken any outlook wording that treats follow-up questions as current findings, evidence, route recommendations, claim-ceiling changes, or proof that the current case is incomplete.
* Do not include excluded raw user notes. User notes marked `summarize` may be paraphrased; notes marked `include` may be included only when still bounded as planning context.
* The outlook must make clear that a follow-up case begins again with its own boundary, source status, intended use, and Pre-Analysis.

COMMON INTEGRATION RULES:

* Output Markdown only.
* Begin with the exact case title as an H2 heading.
* Preserve supported case-specific analysis, active-layer results, rival pressure, unresolved items, weakening conditions, and reopening conditions.
* Preserve canonical PMS operator naming. In every rewritten or newly inserted paragraph, the first occurrence of each operator must use `SYMBOL (Canonical Name)` according to the runner-generated naming rule.
* Do not replace canonical operator names with case-specific descriptions. A description may follow the canonical name.
* Do not introduce new analysis or strengthen claims.
* Do not import workflow history, local file inventory, temporary runner metadata, prompt instructions, example-generation metadata, or audit-planning language into article prose.
* Remove drafting labels such as `Type`, `Recommended insertion point`, `Example decision`, and generation metadata from inserted examples.
* State each boundary, provenance fact, route decision, and non-use result once.
* Do not treat article readiness as truth, publication permission, implementation permission, or authority.

PROFILE INTEGRATION:

For `case_article`:

* Preserve the analytical substance of the Base Draft without restoring omitted audit structure.
* Do not expand the article merely to reproduce the length, section count, operator inventory, branch inventory, or boundary catalogue of Stage 1, Stage 2, Stage 3, or the full-analysis profile.
* Preserve compact grouping of weak, conditional, dependency-limited, inactive, or analytic-only operators.
* Do not unpack grouped operators into separate paragraphs or subsections merely because the checked record lists them separately.
* Give an individual weak or inactive operator separate treatment only when it contributes a distinct case-specific result that would otherwise be lost.
* Do not repeat the same calibration limit in multiple operator-specific formulations.
* Omission of generic workflow history, inactive-layer inventories, repeated non-authority language, report-readiness planning, and non-material provenance detail is intentional and is not source loss.
* Mention inactive add-ons, MIP, or AHP only where their non-use prevents a case-specific false trigger or materially explains the result.
* Keep the case-specific boundary focused on the risks nearest to the actual material and analysis.
* Do not restore remote legal, clinical, forensic, HR, automated-decision, publication, implementation, or institutional-use prohibitions unless the checked record establishes concrete proximity to that misuse.
* Insert no more than one generated example.

For `full_analysis_article`:

* Preserve detailed record depth where the checked source supports it.
* Do not repeat the same provenance fact, branch decision, claim boundary, non-use statement, or non-authority warning across the case capsule, layer sections, misuse section, and conclusion.
* Do not mistake a full analysis article for a file inventory or chronological transcript of the runner.

NO-EXAMPLE RULE:
When the decision state unambiguously indicates no example, preserve the Base Draft as the final article except for necessary cleanup. Do not rewrite or expand it merely because this integration step exists.

OUTPUT:
Return Markdown only.
No YAML.
No code blocks.
No meta-commentary outside the article.

---

## Prompt #31 — Final Article Check and Conservative Patch

You are continuing a PMS-DISCIPLINE pipeline run.

The final Markdown article was generated for the selected profile.

AVAILABLE CONTEXT:

* Checked Stage 1, Stage 2, and Stage 3 outputs are present.
* The Iteration Handoff YAML from step #26 is present if actually produced. It is prospective planning context only, not current-case evidence.
* The Base Markdown Case Article Draft is present.
* The Example Decision and any generated example are present.
* The Final Integrated Markdown Case Article is present.
* Checked prior PMS-DISCIPLINE artifacts are present where applicable.
* The CASE PACKET remains the bounded source material.

CASE PACKET:
CASE TITLE:
{CASE_TITLE}

CASE MATERIAL:
{CASE_MATERIAL}

SOURCE STATUS:
{SOURCE_STATUS}

INTENDED USE:
{INTENDED_USE}

{RUNNER_ARTICLE_PROFILE_CONTRACT}

TASK:
Review the final Markdown article against the checked record and the selected article profile. Patch only concrete defects.

COMMON CHECKS:

1. Source fidelity
   * Stage 3 remains primary.
   * Stage 2 depth is preserved where needed.
   * Stage 1 is used for provenance, not new case findings.
   * No new analysis or source material appears.

2. Claim boundary
   * Source status, claim ceiling, material unresolved items, rival pressure, and reopening conditions remain intact.
   * No unlicensed diagnosis, person ranking, legal/forensic conclusion, metaphysical proof, empirical proof, implementation validation, PMS Base validation, maturity verdict, dignity score, or authority claim appears.

3. Structural fidelity
   * Core calibration and dependencies remain understandable.
   * Every paragraph containing PMS operator prose uses the canonical English name in parentheses at the first occurrence of each operator in that paragraph.
   * Symbol-only formulas are permitted, but they do not satisfy the naming requirement for later prose in the same paragraph.
   * Canonical operator names are not replaced by case-specific glosses or functions.
   * Active add-on, MIP, and AHP results remain separate.
   * Inactive layers are not presented as findings.
   * Workflow QA metadata is not converted into case substance.

4. Examples
   * Any example is permitted by the recorded decision.
   * It remains illustrative only.
   * Drafting labels and insertion metadata are absent from the final article.

5. Iteration outlook
   * An Iteration outlook appears only when permitted by the runner-generated handoff.
   * It remains prospective and does not change the current case result, claim ceiling, route, operator status, source status, layer result, sufficiency assessment, or final posture.
   * It does not treat prior checked analysis as evidence for the future case.
   * It does not include raw user notes whose article_visibility is `exclude`.
   * It states or preserves that any follow-up is a new, separately bounded analysis.

6. Conclusion
   * The conclusion stays within the checked record.
   * It preserves the controlling posture and does not create publication or implementation authority.

PROFILE CHECKS:

For `case_article`:

* The article remains a focused case article rather than a narrative audit dossier.
* Absence of a case capsule, full source-chain inventory, workflow correction history, inactive-layer catalogue, generic misuse catalogue, report-readiness section, or examples-policy section is not a defect.
* Omission of generic workflow history, repeated boundary language, and non-material provenance detail is not source loss.
* Do not restore material merely because it exists in Stage 1, Stage 2, or Stage 3.
* Restore omitted material only when its absence changes the case-specific structural analysis, controlling claim boundary, active-layer result, material unresolved tension, rival reading, weakening condition, reopening condition, or distinctive misuse risk.
* Weak, conditional, dependency-limited, inactive, or analytic-only operators should normally be grouped by shared calibration function.
* Separate treatment of such an operator is justified only when it contributes a distinct case-specific result that would be lost through grouping.
* Flag separate operator paragraphs that merely repeat the same limitation in different wording as removable excess.
* The case-specific boundary should normally prioritize the two to four misuse or escalation risks nearest to the material and actual analysis.
* Flag remote legal, clinical, forensic, HR, automated-decision, publication, implementation, or institutional-use prohibitions as removable excess unless the checked record establishes concrete proximity to them.
* Flag unnecessary internal workflow narration, repeated inactive-layer notes, repeated calibration points, or generic boundary repetition as removable excess.

For `full_analysis_article`:

* Detailed provenance and layer decisions may remain.
* Flag repeated provenance, route, boundary, and non-authority language when it adds no new case-specific function.
* Flag local installation inventory, temporary runner state, or drafting metadata as removable excess.
* Do not reduce supported analytical depth merely to make the article shorter.

PATCH DISCIPLINE:

* Patch only the Markdown article.
* Prefer exact find/replace or insertion patches.
* Full rewrite is allowed only when the article is structurally unusable.
* Keep supported content.
* Weaken overclaims rather than replacing them with silence.
* Remove only the smallest unnecessary or unsupported text.
* Do not use the check to convert one profile into the other.

OUTPUT FORMAT:

### Final check status

Use one:

* article_ready_with_no_patch_required
* article_ready_after_minor_patch
* major_revision_required
* source_record_insufficient_for_article
* human_review_required_before_article_use

### Main issues

List only actual issues. Write `none` when there are none.

### Exact patches

Write `none` when no patch is needed.

For each patch:

**Patch [number] — [short title]**

Find:

[exact text]

Replace with:

[replacement text]

or:

Insert after:

[exact anchor text]

Insert:

[text]

---

