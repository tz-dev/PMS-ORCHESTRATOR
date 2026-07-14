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

Optional Markdown article generation:
#26 Article Source Setup and Rendering Contract
#27 Base Markdown Case Article Draft
#28 Example Decision and Optional Example Generation
#29 Final Integrated Markdown Case Article
#30 Final Article Check and Conservative Patch
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

Optional Markdown article generation:
#26 Article Source Setup and Rendering Contract
#27 Base Markdown Case Article Draft
#28 Example Decision and Optional Example Generation
#29 Final Integrated Markdown Case Article
#30 Final Article Check and Conservative Patch
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

Optional Markdown article generation:
#26 Article Source Setup and Rendering Contract
#27 Base Markdown Case Article Draft
#28 Example Decision and Optional Example Generation
#29 Final Integrated Markdown Case Article
#30 Final Article Check and Conservative Patch
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

Optional Markdown article generation:
#26 Article Source Setup and Rendering Contract
#27 Base Markdown Case Article Draft
#28 Example Decision and Optional Example Generation
#29 Final Integrated Markdown Case Article
#30 Final Article Check and Conservative Patch
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
Produce a PMS-DISCIPLINE Pre-Analysis YAML that prepares the case for later PMS Core application.

TECHNICAL INSTRUCTIONS:
- Use only the provided template, the CASE PACKET, the available PMS.yaml context, and any bounded case materials already read in step #1.
- Use the Pre-Analysis template as the only output structure.
- HIGH-PRIORITY YAML STRUCTURE RULE: preserve every field from the provided template, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no template field omitted.
- Fill fields precisely from the CASE PACKET, available PMS.yaml context, and any case materials already read in step #1.
- Use unknown, unclear, not_applicable, missing, unresolved, or insufficient where the input does not license a stronger value.
- Template sections may change only where valid YAML repair requires it.
- PMS.yaml supplies background reference only; the Pre-Analysis step is not Core application.
- Preliminary pressure, scan pressure, and risk markers remain pressure markers, not recommendation, authorization, application, routing, verdict, full Case Record generation, Markdown article generation, or final decision state.

PRE-ANALYSIS SCOPE:
This step may mark:
- case boundary
- input/source status
- intended use
- claim ceiling
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

OUTPUT:
Return only the completed Pre-Analysis YAML.
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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
Determine whether the Pre-Analysis YAML is usable as checked input for PMS Core case application. Where necessary, conservatively correct it so that it sufficiently conforms to the template and bounded task.

TECHNICAL INSTRUCTIONS:
- Use only the Pre-Analysis YAML from the previous step, the CASE PACKET, available PMS.yaml context, and the previously applied Pre-Analysis template structure.
- Re-run the Pre-Analysis from scratch only if the existing output is structurally unusable.
- Check structural conformity: root structure, required sections, required fields, allowed placeholders, valid YAML, and required handoff sections.
- Check substantive conformity: boundedness to the CASE PACKET, source-status discipline, intended-use discipline, claim ceiling, person-nearness, publicness, irreversibility, non-capture, rival pressure, falsifier conditions, correctability, and reopening conditions.
- Correct only where necessary to restore PMS-/YAML-conformity or to prevent overclaim, source-status laundering, premature recommendation, premature authorization, premature Core application, or premature finalization.
- Prefer the smallest sufficient correction.
- Preserve the original output wherever it already sufficiently conforms.
- Corrections remain conservative, bounded, and claim-weakening where needed.
- Use explicit uncertainty markers rather than inferential gap-filling.

STEP BOUNDARIES:
This check excludes:
- PMS Core application or PMS Core Case Application YAML generation
- invented source material, files, case facts, source status, or unavailable context
- conversion of preliminary pressure, scan pressure, or risk markers into recommendation, authorization, application, routing, verdict, full Case Record generation, Markdown article generation, or final decision state
- stylistic polish, extra reassurance, fuller commentary, or speculative completeness

CHECK SCOPE:
The check may identify and, where safely possible, correct:
- invalid YAML
- missing required sections or fields
- unresolved required placeholders
- source-status laundering
- claim ceiling overreach
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

If the Pre-Analysis YAML contains concrete defects that can be conservatively corrected inside this step, return:
- CHECK STATUS: corrected
- CORRECTIONS MADE: concise bullet list
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
- Preserve rival readings, falsifier conditions, reopening conditions, and correction conditions.

OUTPUT:
Return only the completed PMS Core Case Application YAML.
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
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
* Preserve source status, intended use, claim ceiling, non-capture, rival pressure, correctability, reopening conditions, and stop-capability from checked prior artifacts.

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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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
* loss of rival readings, non-capture, correctability, or reopening conditions
* unsupported strengthening of claims
* generated later pipeline artifacts

PATCH DISCIPLINE:
If correction is needed:

* Patch only within the MIP Gate YAML.
* HIGH-PRIORITY YAML PATCH RULE: preserve every existing template field, preserve field order as far as possible, add no new fields or sections, rename no fields, and leave no required field omitted.
* Keep PMS operators, dependencies, derived structures, and MIP-specific categories unchanged.
* Keep claims at or below the level licensed by the CASE PACKET and checked prior artifacts.
* Exclude invented files, new source claims, MIP application output, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a PMS-DISCIPLINE MIP Gate YAML only.

OUTPUT:
If the MIP Gate YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

PMS-DISCIPLINE MIP Gate YAML checked. Ready for the next allowed PMS-DISCIPLINE pipeline step named in the checked gate output.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
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
* Exclude invented files, new source claims, AHP output, Case Record output, Markdown output, MIP authority drift, and later pipeline artifacts from the corrected YAML.
* Patch only the smallest structurally necessary part; use bounded markers where a field cannot be supported.
* The corrected output remains a MIP Case Application YAML only.

OUTPUT:
If the MIP Case Application YAML is usable for the next PMS-DISCIPLINE pipeline step without correction, respond only:

MIP Case Application YAML checked. Ready for the next PMS-DISCIPLINE pipeline step.

If concrete defects can be conservatively corrected inside this step, return:

* CHECK STATUS: corrected
* CORRECTIONS MADE: concise bullet list
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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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

SOURCE AUTHORITY HIERARCHY:
For run metadata, file existence, exact paths, route state, branch state, and step status, use this order:

1. Authoritative Runner Manifest
2. Checked upstream artifact
3. Stage 1 output under review
4. Template default or placeholder
5. Model inference

A higher source overrides a lower source. Copy runner-manifest values exactly. Never substitute session.json for a produced output path unless the runner manifest itself names session.json for that field.

TASK:
Check the Stage 1 Artifact Index YAML from the previous step for structural and substantive conformity with the Stage 1 template, checked prior artifacts, source/read-status information, and the bounded task.

PURPOSE:
Determine whether the Stage 1 Artifact Index YAML is usable as checked Stage 1 output for Stage 2. Where necessary, conservatively correct it so that it accurately records the artifact state of this pipeline run.

TECHNICAL INSTRUCTIONS:

* Use only the Stage 1 Artifact Index YAML from the previous step, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, and the previously applied Stage 1 template structure.
* Re-run Stage 1 from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, artifact inventories, branch inventories, dependency map, status fields, and readiness fields.
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

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
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

1. YAML parses and preserves the Stage 1 root, required sections, required fields, and field order as far as possible.
2. Every completed step output listed by the runner manifest appears with the exact case-relative output path from that manifest.
3. No completed output is represented only by session.json unless the runner manifest explicitly assigns session.json to that artifact field.
4. Route, selected add-on, MIP, AHP, skipped-branch, and produced-output states match the runner manifest exactly.
5. Every configured case material is represented in case_material_index with the exact runner path, description, purpose, file-presence status, and supplied hash; no material is treated as a model source, template, or evidence merely because present.
6. Stage 2 and Stage 3 templates are marked deferred future-step resources, not missing or expected_but_missing.
7. No /mnt/data path, sandbox path, renamed attachment, duplicate upload name, helper script, or service-local file is treated as a run artifact.
8. No SHA-256 value is invented; unavailable hashes are marked unknown.
9. Unselected add-ons remain unselected/not_applicable and have no produced output path.
10. Skipped MIP or AHP branches remain visible and are not treated as missing-artifact defects.
11. Source status and intended use match the CASE PACKET exactly.
12. ready_for_stage_2 and blocker_notes follow the actual current-run artifacts; future-template upload state is not a blocker.
13. Stage 1 contains no layer digest, Stage 3 integration, new case analysis, or later-pipeline content.

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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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

SOURCE AUTHORITY HIERARCHY:

For exact metadata and provenance:
1. Authoritative Runner Case-Record Manifest
2. Checked Stage 1 Artifact Index
3. Stage 2 output under review
4. Stage 2 template default or placeholder
5. Model inference

For substantive digest content, the corresponding checked layer artifact controls. Checked Stage 1 controls selection and provenance. Template defaults and model inference cannot override either.

TASK:
Check the Stage 2 Layer Digest Extraction YAML from the previous step for structural and substantive conformity with the Stage 2 template, checked prior artifacts, checked Stage 1 output, and the bounded task.

PURPOSE:
Determine whether the Stage 2 Layer Digest Extraction YAML is usable as checked Stage 2 output for Stage 3. Where necessary, conservatively correct it so that it accurately extracts and preserves digest-level content without reanalysis or claim strengthening.

TECHNICAL INSTRUCTIONS:

* Use only the Stage 2 Layer Digest Extraction YAML from the previous step, CASE PACKET, PMS.yaml context, checked prior YAML artifacts, checked Stage 1 output, and the previously applied Stage 2 template structure.
* Re-run Stage 2 from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, layer digests, skipped branch digest, non-use digest, claim ceiling digest, correctability digest, and Stage 3 export.
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

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
* unsupported source or file assumptions
* digest content not grounded in checked artifacts
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

1. YAML parses and preserves the Stage 2 root, required sections, required fields, and field order as far as possible.
2. The imported Stage 1 reference and every case-record output path match the runner manifest exactly.
3. selected_artifacts_to_read matches checked Stage 1 exactly; no unselected, skipped, absent, or unavailable artifact is silently read.
4. Every digest identifies the exact selected source artifact path; session.json is not used as a substitute unless explicitly assigned by the runner manifest or checked Stage 1.
5. Each substantive digest is grounded in its corresponding checked layer artifact and contains no new analysis.
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
Wrap the YAML in a fenced yaml code block if the chat interface requires separation.

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
Check the Stage 3 Full Record Integration YAML from the previous step for structural and substantive conformity with the Stage 3 template, checked Stage 1, checked Stage 2, checked prior artifacts, and the bounded task.

PURPOSE:
Determine whether the Stage 3 Full Record Integration YAML is usable as checked integrated record output for the next PMS-DISCIPLINE pipeline step. Where necessary, conservatively correct it so that it remains structurally valid, bounded, non-authoritative, and faithful to checked Stage 1 and checked Stage 2.

TECHNICAL INSTRUCTIONS:

* Use only the Stage 3 Full Record Integration YAML from the previous step, CASE PACKET, PMS.yaml context, checked Stage 1, checked Stage 2, checked prior artifacts, and the previously applied Stage 3 template structure.
* Re-run Stage 3 from scratch only if the existing output is structurally unusable.
* Check structural conformity: root structure, required sections, required fields, valid YAML, integrated artifact record, integrated layer record, branch-status summary, skipped-branch summary, claim-ceiling summary, uncertainty summary, rival/correctability/reopening summary, human-confirmation summary, and next-step boundary.
* Check substantive conformity: fidelity to checked Stage 1 and checked Stage 2, source-status discipline, claim ceiling, non-use preservation, branch separation, MIP output preservation, AHP non-interference, rival pressure, non-capture, correctability, reopening conditions, stop-capability, and non-authority boundaries.
* Correct only the smallest necessary part.
* Preserve conforming content.
* Keep corrections conservative, bounded, and claim-weakening where needed.
* Use explicit uncertainty markers instead of inferential gap-filling.

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

* invalid YAML
* missing required sections or fields
* unresolved required placeholders
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

1. YAML parses and preserves the Stage 3 root, required sections, required fields, and field order as far as possible.
2. generated_from and all case-record provenance paths match the runner manifest exactly, including the exact Step #20 and Step #22 output paths.
3. Stage 1 controls artifact, route, branch, skipped, and non-use metadata; Stage 2 controls substantive digest content.
4. Integrated content is grounded in checked Stage 1 and checked Stage 2 and introduces no new analysis.
5. Source status, intended use, claim ceiling, person-nearness, publicness, and irreversibility do not drift from controlling checked sources.
6. Selected add-on, MIP, and AHP remain separate; AHP does not rescore, correct, or authorize MIP.
7. Skipped, rejected, absent, not_applicable, and non-used layers remain visible and are not converted into deficiencies.
8. Genuine substantive contradictions, uncertainty, rival pressure, non-capture, correctability, reopening conditions, and stop-capability remain visible.
9. Internal path discrepancies, template-status drift, and workflow QA notes are not converted into substantive case findings.
10. Attack Points are not proven defects, Hardening Backlog is not a mandate, and Precision Heuristic is not authority.
11. The record status reflects its actual pipeline position after integration and does not claim that a completed check is still merely awaiting that same check.
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
* COMPLETE CORRECTED PMS-DISCIPLINE STAGE 3 FULL RECORD INTEGRATION YAML

If the output is not safely correctable inside this step, then return:

* CHECK STATUS: not ready
* BLOCKING ISSUES
* REQUIRED CORRECTIONS
* NEXT ALLOWED STEP

Do not declare ready while any criterion remains FAIL.

---

## Prompt #26 — Article Source Setup and Rendering Contract

You are continuing a PMS-DISCIPLINE pipeline run.

This step establishes the source hierarchy and article-generation contract for rendering a completed PMS-DISCIPLINE case-record chain into Markdown prose.

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
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session.
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
Establish the article-generation source hierarchy and rendering contract for the PMS-DISCIPLINE Markdown case article.

PURPOSE:
Prepare the article-generation step by fixing which checked artifacts control the article, what the article may render, what it may not claim, and how unresolved or missing items must be preserved.

SOURCE HIERARCHY:
Use the following hierarchy for all later Markdown article generation:

1. Primary source for article rendering:
   Checked Stage 3 Full Record Integration YAML.

2. Secondary source for analytical depth:
   Checked Stage 2 Layer Digest Extraction YAML.

3. Provenance and artifact-trace source:
   Checked Stage 1 Artifact Index YAML.

4. Underlying checked artifacts:
   Read only where checked Stage 2 or checked Stage 3 explicitly marks a gap, contradiction, unresolved item, missing detail, or need to verify a layer-specific boundary.

SOURCE DISCIPLINE:

* Stage 3 controls the article’s case title, claim boundary, final posture, unresolved items, branch status, non-use, human-confirmation status, and permitted article-use boundary.
* Stage 2 supplies layer-level analytical depth but must not override Stage 3.
* Stage 1 supplies provenance, artifact status, branch status, and source-chain visibility.
* Underlying checked artifacts may verify a marked gap, but they may not introduce new article claims absent from Stage 2 or Stage 3.
* CASE PACKET supplies bounded source material only where the checked record chain already licenses reference to it.

NON-AUTHORITY CONTRACT:
The Markdown article is a rendering of the checked case-record chain.

It is not:

* a re-analysis
* a YAML output
* a verdict
* a truth certificate
* a PMS Base validation
* an add-on validation
* MIP or AHP authority
* publication permission
* implementation permission
* automated finality
* evidence by itself

The article may render:

* what the checked record permits the article to say
* what the checked record does not permit the article to say
* which artifacts were used, skipped, rejected, unavailable, or not applicable
* which layers were used, not used, rejected, scan-only, unsafe, unresolved, or human-review-required
* what remains unresolved, non-captured, weak, conditional, rival-pressured, or reopenable
* what would weaken, falsify, downgrade, suspend, refuse, redirect, or reopen the result

The article must preserve:

* source status
* intended use
* claim ceiling
* person-nearness limits
* publicness limits
* irreversibility limits
* non-capture
* rival pressure
* correctability
* reopening conditions
* stop-capability
* human-confirmation requirements where present

CASE CONTENT / WORKFLOW QA SEPARATION:

* Substantive case findings, substantive uncertainties, rival readings, claim limits, and reopening conditions belong to the article where the checked record supports them.
* Internal runner-path discrepancies, template-status drift, attachment-name drift, file-provenance inconsistencies, and workflow QA notes are not substantive findings about the case.
* Mention a workflow QA issue only when checked Stage 3 explicitly states that it materially limits the reliability or interpretation of the case record.
* When such a material limitation exists, describe it briefly as a record limitation, never as a fact about the case, a person, or a PMS operator.
* Do not let workflow metadata dominate the article’s case analysis or conclusion.

SOURCE-LOSS RULE:
Before drafting, inspect checked Stage 3 for missing, unresolved, contradictory, unintegrated, skipped, rejected, unsafe, unavailable, or human-review-required items.

If such items exist, later article prose must preserve them visibly.

The article must not silently smooth away:

* unresolved items
* missing details
* contradictions
* unintegrated material
* skipped branches
* add-on non-use
* MIP non-use or limits
* AHP non-use or limits
* human-review requirements
* source-status weakness
* claim-boundary restrictions
* correctability or reopening conditions

TITLE RULE:
The article must begin with the exact case title from checked Stage 3 as an H2 heading.

If checked Stage 3 does not contain an exact case title, use the title from checked Stage 2.

If checked Stage 2 also lacks a title, use the title from the checked Core output only if checked Stage 1 selected that artifact as current.

Do not invent a title.

Do not use a topic label, add-on label, working title, filename, or paper-section label as the article title unless the checked case record itself uses it as the exact case title.

OUTPUT:
Respond only:

Article-generation source hierarchy and rendering contract established.

---

## Prompt #27 — Base Markdown Case Article Draft

You are continuing a PMS-DISCIPLINE pipeline run.

The article-generation source hierarchy and rendering contract were established in the previous step.

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
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session.
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
Create a chapter-ready, analytically substantial Markdown case article draft from the checked PMS-DISCIPLINE case-record chain.

PURPOSE:
Render checked Stage 3 into polished Markdown prose, using checked Stage 2 for analytical depth and checked Stage 1 for provenance, without re-running analysis, strengthening claims, or treating the case record as a verdict.

SOURCE HIERARCHY:
Use:

1. Checked Stage 3 Full Record Integration YAML as the primary article source.
2. Checked Stage 2 Layer Digest Extraction YAML for layer-level analytical depth.
3. Checked Stage 1 Artifact Index YAML for provenance and artifact status.
4. Underlying checked artifacts only where checked Stage 2 or checked Stage 3 explicitly marks a gap, contradiction, unresolved item, missing detail, or need for layer-specific verification.

CASE CONTENT / WORKFLOW QA SEPARATION:

* Render substantive case content from checked Stage 3 and checked Stage 2.
* Use Stage 1 for provenance and branch status, not as a source of substantive case findings.
* Internal path discrepancies, template-status drift, attachment-name drift, file-provenance inconsistencies, and workflow QA notes are not case findings.
* Mention such a workflow issue only if checked Stage 3 explicitly marks it as materially limiting record reliability or interpretation; then present it briefly as a record limitation.
* Do not convert workflow metadata drift into uncertainty about the persons, scene, operators, or case substance.

TECHNICAL INSTRUCTIONS:

* Output Markdown only.
* Do not output YAML.
* Do not use code blocks.
* Do not add meta-commentary outside the article.
* Do not redo the YAML analysis.
* Do not re-run Core, add-on, MIP, AHP, or Case Record stages.
* Do not strengthen claims beyond checked Stage 3.
* Do not resolve contradictions by interpretation.
* Do not introduce new source material, files, inferred facts, or unavailable context.
* Do not treat YAML outputs as evidence.
* Do not treat AI-generated material as source evidence.
* Do not treat article readiness as truth, publication permission, implementation permission, or authority.
* Preserve unresolved, missing, contradictory, unintegrated, skipped, rejected, unsafe, unavailable, or human-review-required items where the checked record contains them.

MANDATORY TITLE RULE:
Begin with the exact case title from checked Stage 3 as an H2 heading:

## [EXACT CASE TITLE]

If checked Stage 3 lacks an exact title, use checked Stage 2. If checked Stage 2 also lacks a title, use the checked Core title only if checked Stage 1 selected that artifact as current.

REQUIRED STRUCTURE:

## [EXACT CASE TITLE]

### Case capsule

Include where present in checked Stage 3:

* Case file(s)
* Record chain status
* Stack
* Case type
* Concrete-scene status
* Output type
* Core status
* Add-on status
* MIP / AHP status
* Claim boundary
* Final status or decision posture
* Human confirmation status

If a field is absent, do not invent it. Mark it as absent, unresolved, or not supplied only where the checked record supports that.

### Why this case matters

Explain why the case matters according to checked Stage 3 and checked Stage 2.

Include where supported:

* why the case requires disciplined PMS use
* what readability-to-use pressure it creates
* what makes it structurally difficult
* why Core-only may or may not be sufficient
* why add-ons, MIP, or AHP were used, not used, rejected, scan-only, unsafe, unresolved, or left for human review
* why the case is not being solved metaphysically, empirically, clinically, legally, diagnostically, technically, or operationally unless checked Stage 3 explicitly licenses such a claim

### Source chain and integration status

Render the checked Stage 1 / Stage 2 / Stage 3 chain in readable prose.

Include where supported:

* which artifacts were selected as current
* which artifacts were unavailable, superseded, rejected, skipped, or not applicable
* which artifacts were integrated through digests
* whether underlying artifacts were consulted for any marked gap
* what was intentionally not imported
* whether any relevant item remains unresolved

This section should prevent source loss. It should not become a long file inventory unless the checked record requires it.

### Claim status and scope discipline

Render the checked Stage 3 claim boundary in prose.

Include where present:

* case type
* claim status
* concrete-scene status
* input/source status
* empirical boundary
* metaphysical boundary
* diagnostic boundary
* legal/forensic boundary
* implementation boundary
* PMS Base boundary
* operationalization status
* article-use boundary
* publicness limits
* person-nearness limits
* irreversibility limits
* correctability limits

Do not reduce this to one paragraph if the checked record contains more distinctions.

### Scene and frame structure

Render the case boundary and scene/frame structure from checked Stage 3 and checked Stage 2.

Include where present:

* scene boundary
* frame □
* what is inside the frame
* what is outside the frame
* protected constraints
* roles
* temporality Θ
* reversibility window
* exposure and asymmetry conditions
* non-capture zones

If the case is not a concrete scene, explain precisely what follows from that.

### PMS Core structural reading

Give a substantial PMS Core reading based on the checked Core digest and checked Stage 3 integration.

Do not only list operators. Transform the operator analysis into prose.

Render relevant PMS operators in repository order where they are active, weak, conditional, not applicable, analytic-only, or explicitly constrained:

Δ, ∇, □, Λ, Α, Ω, Θ, Φ, Χ, Σ, Ψ.

For each operator included by the checked record:

* explain its case-specific role
* mark active, weak, conditional, not applicable, or analytic-only status where relevant
* explain calibration issues
* explain dependency risks
* explain what would be overclaim if the operator were pushed too far

Do not invent operator assignments absent from checked Stage 2 or checked Stage 3.

Preserve special calibration for:
Χ, Φ, Σ, Ψ, Ω, Θ, and Λ.

### PMS dependency and calibration discipline

Explain:

* why later operators cannot be used cheaply
* where Σ or Ψ remain conditional
* why coherence is not proof
* why non-capture is not failure
* why PMS must not become a closure machine
* what dependency shortcuts would be invalid
* where the Core record refused over-assignment or marked omission risk

### Derived structures

Use this section only if checked Stage 2 or checked Stage 3 includes derived-structure material.

Render any included:

* Awareness_A
* Coherence_C
* Responsibility_R
* Action_E
* Dignity_in_Practice_D
* SELF_FIXPOINT

For each included structure:

* state whether it is active, weak, conditional, not applicable, or analytic-only
* explain why
* preserve that derived structures are formula-derived PMS projections, not primitives, scores, rankings, or person-level verdicts

If derived structures are absent or not relevant, say so briefly and do not fabricate a full derived-structure analysis.

### PMS drift-pattern status

Use this section only if checked Stage 2 or checked Stage 3 includes PMS drift-pattern material or explicitly marks it as not applicable.

Render where supported:

* AD_A>>E
* AD_Sigma_low
* related coherence, under-integration, or under-discrimination risks

Preserve:

* risk is not finding
* under-specification is not failure
* non-assignment is not low score
* non-use is not omission failure

### Add-on record and overlay reading

Use this section if any add-on was used, recommended, rejected, scan-only, not recommended, unsafe, human-review-required, unresolved, skipped, or otherwise relevant in the checked record.

Do not restrict this section only to add-ons that were applied. Non-use, rejection, scan-only, and skipped-branch records may matter.

For each relevant add-on:

* name the add-on explicitly
* state checked status
* explain why Core alone was or was not sufficient
* explain what the add-on makes visible if applied
* explain which add-on constructs are overlay handles, not PMS operators
* explain which add-on risks are risks, not findings
* explain how the add-on remains subordinate to PMS Base
* explain what the add-on must not redefine
* explain why rejected, skipped, or unused add-ons were not applied

For PMS-ANTICIPATION, preserve future-pressure and prediction/action-boundary discipline.

For PMS-CONFLICT, preserve conflict-threshold discipline and avoid disagreement-to-conflict overtriggering.

For PMS-CRITIQUE, preserve correction/critique boundaries and avoid complaint-to-verdict overtriggering.

For PMS-EDEN, preserve description/application firewall, no person-status claim, no diagnosis, no sex-truth claim, and no action authority.

For PMS-LOGIC, preserve logical-boundary discipline, non-closure, non-innocence if applicable, responsibility-without-ought if applicable, and no guilt/blame verdict.

For PMS-SEX, preserve sex-trigger discipline, no person ranking, no normality verdict, no exposure license, no adultness/maturity verdict, and no body/genital meaning as person truth.

### Layer interaction

Use this section if an add-on, MIP, AHP, or other later layer exists, was recommended, rejected, skipped, scan-only, unsafe, or remains unresolved.

Explain:

* what remains PMS Core
* what each layer sharpens
* what each layer must not redefine
* where overlay language could overreach
* where MIP/AHP language could over-evaluate
* where non-closure remains visible
* which layer boundaries checked Stage 3 preserves

### MIP / AHP record

Use this section if MIP or AHP was used, recommended, rejected, scan-only, not recommended, unsafe, human-review-required, unresolved, or skipped.

For MIP:

* state checked MIP status
* preserve that MIP output is produced by MIP’s own structure, not by PMS-DISCIPLINE
* preserve no person-ranking, no dignity score, no maturity verdict, no diagnostic use
* preserve A/M bands as qualitative bands if present, not hard scores
* preserve IA-box as asymmetry check, not verdict
* preserve Dignity-in-Practice as praxeological, not ontological

For AHP:

* state checked AHP status
* preserve that AHP is an optional second-order analysis-quality overlay
* preserve that AHP does not rescore, govern, certify, authorize, or finalize the case
* explain Precision Heuristic, Attack Points, and Hardening Backlog only where checked AHP output supports them
* mark Attack Points as review surfaces, not proven defects
* mark Hardening Backlog as next-iteration support, not mandate
* preserve AHP non-interference with MIP

### Non-capture and rival readings

Render all rival and non-capture material from checked Stage 3 and checked Stage 2.

Include where present:

* epistemological rival readings
* phenomenological rival readings
* language-practice rival readings
* ethical rival readings
* empirical rival readings
* institutional or technical rival readings
* anti-capture readings
* case-specific rival frames

Explain what each rival reading preserves that PMS, add-ons, MIP, or AHP may not fully capture.

Do not treat rival readings as defects.

A rival may weaken, redirect, or currently outperform the PMS reading if the checked record says so.

### Weakening, falsifier, and operationalization conditions

Render checked weakening, falsifier, reopening, and operationalization logic.

Include where present:

* what would weaken the Core reading
* what would weaken any add-on reading
* what would weaken MIP/AHP use
* what would make the reading under-discriminating
* what would make the reading over-assimilative
* what evidence, source material, scene data, or human review would be required for stronger claims
* what operationalization remains unfulfilled
* what reopening conditions remain active

### Misuse boundary

Give a substantial misuse-boundary section.

Include all boundaries relevant to the checked record:

* no diagnosis
* no person ranking
* no legal/forensic conclusion
* no metaphysical proof
* no empirical proof unless explicitly warranted
* no implementation validation
* no PMS Base validation
* no add-on-as-operator
* no drift-as-verdict
* no MIP maturity verdict
* no AHP authority layer
* no YAML-as-evidence
* no AI-output-as-evidence
* no closure-by-authority

### Report readiness and examples policy

Render the checked Stage 3 report-readiness and examples policy.

Do not automatically generate examples in this step.

Explain:

* whether examples are recommended, optional, not applicable, unsafe, or not needed
* what kinds of examples would fit if any
* what examples must avoid
* recommended example depth if supplied: micro, compact, worked, or flagship
* where examples should be inserted later if recommended
* when examples should be omitted entirely

If checked Stage 3 marks examples as not applicable or unsafe, do not propose example content.

LENGTH AND DEPTH:
Normal case target: 3,500–6,000 words.
Flagship or multi-layer case target: 6,000–9,000 words.

Do not compress below the analytical density of checked Stage 2 and checked Stage 3.

SPLIT RULE:
If the answer would be too long, split into exactly two parts.

Part 1 must include:

* title
* case capsule
* why this case matters
* source chain and integration status
* claim status and scope discipline
* scene and frame structure
* PMS Core structural reading
* PMS dependency and calibration discipline
* derived structures if present

End Part 1 with:

Ready for Part 2.

Do not continue into PMS drift-pattern status.

Part 2 must begin with:

### PMS drift-pattern status

or, if drift-pattern status is not present:

### Add-on record and overlay reading

Continue through:

### Report readiness and examples policy

Do not repeat Part 1.

OUTPUT:
Return Markdown only.
No YAML.
No code blocks.
No meta-commentary outside the article.

---

## Prompt #28 — Example Decision and Optional Example Generation

You are continuing a PMS-DISCIPLINE pipeline run.

The article-generation source hierarchy and rendering contract were established earlier.
The Base Markdown Case Article Draft was generated in the previous step.

AVAILABLE CONTEXT:

* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session.
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session.
* Base Markdown Case Article Draft is present in this conversation/session.
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

TASK:
Review the checked Stage 3 examples policy and the Base Markdown Case Article Draft. Decide whether examples should be generated for the final article.

PURPOSE:
Determine whether examples are needed, allowed, unsafe, unnecessary, or useful for readability, while preserving the claim boundary and preventing examples from becoming evidence, verdicts, or new analysis.

SOURCE HIERARCHY:
Use:

1. Checked Stage 3 Full Record Integration YAML as controlling source.
2. Checked Stage 2 Layer Digest Extraction YAML for layer-level depth.
3. Checked Stage 1 Artifact Index YAML for provenance and branch status.
4. Base Markdown Case Article Draft for article continuity.

EXAMPLE DECISION STATES:
Use exactly one:

* examples_not_applicable
* examples_unsafe
* examples_not_needed
* no_examples
* examples_optional
* examples_recommended
* examples_required_for_readability

DECISION RULE:
Examples are optional and case-dependent. They must not be generated automatically.

If checked Stage 3 marks examples as not applicable or unsafe, generate no examples. Output only a short Markdown note explaining why examples are omitted.

If examples are not needed, or if the compatibility decision `no_examples` is used, generate no examples. Output only a short Markdown note explaining why the article can remain example-free.

If examples are optional, recommended, or required for readability, generate only the number and depth justified by checked Stage 3 and the Base Draft.

Allowed number of examples:

* 0 if not applicable, unsafe, not needed, or `no_examples`
* 1 if one bounded illustration is sufficient
* 2 if contrast is needed
* 3 only if checked Stage 3 or the article structure benefits from three distinct examples

Do not default to three examples.

EXAMPLE STRUCTURE:
For each generated example, use:

### Example [number] — [example title]

**Type:** micro | compact | worked | flagship
**Recommended insertion point:** ...
**Example status:** illustrative only, not evidence

Then write the example as polished Markdown prose.

Each example must include:

* a bounded vignette or abstract illustration
* what the example demonstrates
* PMS Core hooks
* add-on hooks if relevant
* MIP / AHP status if relevant
* forbidden claims
* non-capture note
* article takeaway

Write readable prose. Avoid label-only examples.

STEP BOUNDARIES:
This step excludes:

* YAML output
* full case YAMLs
* re-running prior analysis
* changing checked Stage 1, Stage 2, or Stage 3
* adding new source material, facts, files, or unavailable context
* assigning scores unless explicitly warranted by checked source records
* converting risks into findings
* converting examples into verdicts
* diagnosing, ranking persons, or making legal/forensic, clinical, metaphysical, empirical, implementation, or PMS Base claims
* writing the final article conclusion

CLAIM DISCIPLINE:

* Examples are illustrative only.
* Do not generate an example from an internal runner-path discrepancy, template-status drift, attachment-name drift, file-provenance inconsistency, or workflow QA note.
* Workflow QA metadata is not case substance and must not be dramatized as a scene, person attribute, or PMS finding.
* Examples are not evidence.
* Examples must clarify the article’s claim boundary rather than dramatize the case.
* High-risk cases should use abstract, structural, or guardrail-only examples.
* Generated examples must remain bounded by checked Stage 3.

RECOMMENDED DEPTH:
Use the depth recommended in checked Stage 3 unless it conflicts with case boundaries.

Default depth guide:

* micro: 250–400 words each
* compact: 400–700 words each
* worked: 800–1,200 words each
* flagship: 1,200–1,800 words each

OUTPUT:
Return Markdown only.
No YAML.
No code blocks.
No meta-commentary outside the example decision and optional example prose.

---

## Prompt #29 — Final Integrated Markdown Case Article

You are continuing a PMS-DISCIPLINE pipeline run.

The article-generation source hierarchy and rendering contract were established earlier.
The Base Markdown Case Article Draft is present.
The Example Decision and optional examples from the previous step are present.

AVAILABLE CONTEXT:

* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session.
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session.
* Base Markdown Case Article Draft is present in this conversation/session.
* Example Decision and optional examples are present in this conversation/session.
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

TASK:
Produce the final integrated Markdown case article.

PURPOSE:
Integrate the Base Markdown Case Article Draft and the Example Decision into a final chapter-ready article while preserving checked Stage 3 as primary source, checked Stage 2 depth, checked Stage 1 provenance, and all claim boundaries.

SOURCE HIERARCHY:
Use:

1. Checked Stage 3 Full Record Integration YAML as primary source.
2. Checked Stage 2 Layer Digest Extraction YAML for analytical depth.
3. Checked Stage 1 Artifact Index YAML for provenance and artifact status.
4. Base Markdown Case Article Draft from Prompt #27.
5. Optional examples from Prompt #28, if examples were generated.

CASE CONTENT / WORKFLOW QA SEPARATION:

* Substantive case prose follows checked Stage 3 and checked Stage 2.
* Stage 1 provenance does not become a case finding.
* Internal path discrepancies, template-status drift, attachment-name drift, file-provenance inconsistencies, and workflow QA notes remain outside the case analysis unless checked Stage 3 explicitly marks a material reliability limitation.
* A material workflow limitation, if present, receives one bounded record-limitation statement and must not be repeated as substantive uncertainty or conclusion.

STEP BOUNDARIES:
This step excludes:

* redoing YAML analysis
* re-reading underlying artifacts unless the Base Draft or checked Stage 3 identifies a marked gap requiring resolution
* adding new case claims
* making the conclusion more certain than checked Stage 3 allows
* introducing new examples beyond Prompt #28
* converting examples into evidence
* producing YAML
* using code blocks
* adding meta-commentary outside the article

MANDATORY TITLE RULE:
Begin with the exact case title from checked Stage 3 as an H2 heading:

## [EXACT CASE TITLE]

If checked Stage 3 lacks an exact title, use checked Stage 2. If checked Stage 2 also lacks a title, use the checked Core title only if checked Stage 1 selected that artifact as current.

REQUIRED FINAL STRUCTURE:

## [EXACT CASE TITLE]

### Case capsule

### Why this case matters

### Source chain and integration status

### Claim status and scope discipline

### Scene and frame structure

### PMS Core structural reading

### PMS dependency and calibration discipline

### Derived structures

Use only if present.

### PMS drift-pattern status

Use only if present or explicitly marked not applicable.

### Add-on record and overlay reading

Use if any add-on was used, rejected, recommended, scan-only, unresolved, explicitly skipped, or explicitly not recommended.

### Layer interaction

Use if an add-on, MIP, AHP, or other later layer exists, was rejected, was skipped, or remains unresolved.

### MIP / AHP record

Use if MIP or AHP was used, rejected, recommended, scan-only, unresolved, explicitly skipped, or explicitly not recommended.

### Example 1 — [title]

Use only if examples were generated.

### Example 2 — [title]

Use only if examples were generated.

### Example 3 — [title]

Use only if examples were generated.

If only one or two examples were generated, include only those.
If no examples were generated, omit all example sections and preserve the examples-policy explanation elsewhere if useful.

### Non-capture and rival readings

### Weakening, falsifier, and operationalization conditions

### Misuse boundary

### Case conclusion

CONCLUSION REQUIREMENTS:
The conclusion must include:

1. Integrative result
2. What examples contribute, if examples were used
3. Why examples were omitted, if no examples were used and omission matters
4. What remains unclaimed
5. Boundary discipline
6. Final status / decision posture and human confirmation status, if available
7. Final methodological takeaway

The conclusion must stay within the checked record. It must not convert unresolved items into resolved findings, treat final status as automated, treat examples as evidence, or treat YAML completion as validation.

PRESERVATION RULE:
Preserve:

* operator-by-operator reading where checked Stage 2 or Stage 3 supports it
* derived-structure analysis where checked Stage 2 or Stage 3 includes it
* add-on signatures, risks, non-use, skipped status, rejection records, or unresolved status where relevant
* MIP/AHP boundary language where relevant
* falsifier, weakening, reopening, and operationalization conditions
* non-capture and rival readings
* claim boundaries
* missing or unintegrated items where they matter to article use

BOUNDARY RULES:
The article must preserve:

* no empirical proof unless explicitly warranted
* no diagnosis
* no person ranking
* no legal/forensic conclusion
* no metaphysical proof
* no implementation validation
* no PMS Base validation
* no drift finding unless explicitly warranted
* risk is not finding
* coherence is not proof
* non-assignment is not low score
* non-use is not omission failure
* non-capture remains possible
* resistance, refusal, non-fit, disagreement, rupture, or absence are not automatically drift
* Dignity-in-Practice remains praxeological, not ontological
* add-on terms remain overlay handles, not PMS operators
* MIP output remains MIP’s own output, not PMS-DISCIPLINE output
* AHP hardens artifact discipline only where warranted; it does not rescore, certify, govern, authorize, or finalize the case
* YAML output is not evidence
* AI output is not source evidence

LENGTH AND DEPTH:
Normal final case article target: 5,000–8,000 words.
Flagship or multi-layer final case article target: 8,000–12,000 words.

Do not compress below the depth of the Base Draft and source records.

SPLIT RULE:
If the final article is too long, split into exactly two parts.

Part 1 must include:

* title
* case capsule
* why this case matters
* source chain and integration status
* claim status and scope discipline
* scene and frame structure
* PMS Core structural reading
* PMS dependency and calibration discipline
* derived structures if present
* PMS drift-pattern status if present

End Part 1 with:

Part 1 finished. Ready to go for Part 2.

Part 2 must begin with:

### Add-on record and overlay reading

If there is no add-on section, begin with the next applicable required section.

Do not repeat Part 1.

OUTPUT:
Return Markdown only.
No YAML.
No code blocks.
No meta-commentary outside the article.

---

## Prompt #30 — Final Article Check and Conservative Patch

You are continuing a PMS-DISCIPLINE pipeline run.

The final integrated Markdown case article was generated in the previous step.

AVAILABLE CONTEXT:

* Checked Stage 1 Artifact Index YAML is present in this conversation/session.
* Checked Stage 2 Layer Digest Extraction YAML is present in this conversation/session.
* Checked Stage 3 Full Record Integration YAML is present in this conversation/session.
* Base Markdown Case Article Draft is present in this conversation/session.
* Example Decision and optional examples are present in this conversation/session.
* Final Integrated Markdown Case Article is present in this conversation/session.
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

TASK:
Review the final Markdown case article against the checked PMS-DISCIPLINE record chain and conservatively patch only where needed.

PURPOSE:
Determine whether anything in the final article needs to be updated, expanded, weakened, removed, clarified, or restored so that the article remains faithful to checked Stage 3, preserves Stage 2 depth, preserves Stage 1 provenance, and stays within PMS-DISCIPLINE article boundaries.

SOURCE HIERARCHY:
Use:

1. Checked Stage 3 Full Record Integration YAML.
2. Checked Stage 2 Layer Digest Extraction YAML.
3. Checked Stage 1 Artifact Index YAML.
4. Base Markdown Case Article Draft.
5. Generated examples, if any.
6. Final Integrated Markdown Case Article.

CHECK DISCIPLINE:

* Keep the check strict and conservative.
* Preserve faithful article content.
* Patch only concrete defects.
* Prefer exact find/replace or insertion patches.
* Full rewrite is allowed only if the article is structurally unusable.
* Keep patches claim-weakening where needed.
* Preserve Markdown format.
* Keep the exact case title rule.
* Preserve unresolved, missing, contradictory, unintegrated, skipped, non-used, rejected, unsafe, or human-review-required items where the checked record contains them.

STEP BOUNDARIES:
This check excludes:

* re-running prior YAML stages
* changing checked YAML artifacts
* adding new source material, files, inferred facts, or unavailable context
* producing new analysis
* strengthening claims beyond checked Stage 3
* resolving contradictions by interpretation
* generating new examples unless existing examples require bounded correction
* turning article readiness into truth, validation, authority, implementation permission, or publication approval

CHECK DIMENSIONS:

1. Source fidelity
   Check whether the article:

* follows checked Stage 3 as primary source
* preserves checked Stage 2 depth where needed
* uses checked Stage 1 only for provenance and artifact status
* avoids re-analysis
* avoids claims not present in the checked record chain

2. Source-loss and omission
   Check whether the article preserves:

* unresolved items
* missing items
* contradictory items
* unintegrated items
* skipped branches
* non-use records
* rejected layer records
* human-review requirements
* source limitations
* checked output status

3. Claim boundary
   Check whether the article avoids unlicensed:

* empirical proof
* diagnosis
* legal or forensic conclusion
* metaphysical proof
* implementation validation
* PMS Base validation
* maturity verdict
* dignity score
* person-level ranking
* publication permission
* automated finality

4. Core preservation
   Check whether the article:

* preserves the Core reading without total capture
* preserves operator calibration
* preserves dependency discipline
* avoids cheap Σ or Ψ closure
* avoids operator over-assignment
* preserves omitted, weak, conditional, or analytic-only operators where relevant

5. Add-on boundary
   Check whether the article:

* treats add-ons as overlays, not PMS Base
* preserves add-on non-use and rejection records
* avoids add-on overdetermination
* preserves subordination to PMS Base
* avoids redefining PMS operators through add-on language

6. MIP / AHP boundary
   Check whether the article:

* uses MIP only where the checked record supports MIP
* treats MIP output as MIP’s own output
* avoids person-ranking, dignity scoring, maturity verdicts, hard A/M scoring, and IA-box verdicts
* treats AHP only as optional second-order analysis-quality overlay where checked AHP output exists
* preserves AHP non-interference with MIP
* keeps Precision Heuristic from becoming authority
* keeps Attack Points from becoming proven defects
* keeps Hardening Backlog from becoming mandate

7. Examples
   Check whether examples:

* were generated only if allowed, recommended, or required by checked Stage 3
* remain illustrative only
* avoid evidence status
* avoid verdict status
* avoid unlicensed scores, diagnoses, rankings, legal/forensic claims, metaphysical claims, implementation claims, or PMS Base claims
* clarify the article boundary rather than dramatize or overstate the case

8. Rival and non-capture discipline
   Check whether the article:

* preserves rival readings
* preserves non-capture
* allows rivals to weaken or redirect the reading where the checked record supports that
* avoids treating rival readings as defects

9. Weakening, falsifier, operationalization, and reopening
   Check whether the article preserves:

* weakening conditions
* falsifier conditions
* operationalization limits
* reopening conditions
* correctability
* stop-capability

10. Workflow QA separation
    Check whether the article:

* distinguishes substantive case uncertainty from internal workflow metadata drift
* avoids presenting runner-path discrepancies, template-status drift, attachment-name drift, file-provenance inconsistencies, or workflow QA notes as case findings
* mentions workflow QA only where checked Stage 3 marks a material reliability limitation
* presents any such limitation briefly as a record limitation, not as a person, scene, operator, or case conclusion

11. Conclusion discipline
    Check whether the conclusion:

* stays within the checked record
* avoids greater certainty than checked Stage 3 allows
* distinguishes article readiness from truth, validation, authority, implementation permission, or publication approval
* preserves final status / decision posture and human-confirmation status where available

PATCH DISCIPLINE:
If correction is needed:

* Patch only the Markdown article.
* Use exact find/replace or insertion instructions where possible.
* Keep existing article structure unless the structure itself causes the defect.
* Preserve supported analytical depth.
* Restore missing boundary language rather than deleting analysis.
* Weaken overclaims rather than replacing them with silence.
* Remove or revise only the smallest necessary text.
* Patch examples only to restore boundary discipline, source fidelity, or illustrative-only status.
* The corrected article remains a Markdown rendering of the checked record chain only.

OUTPUT FORMAT:

### Final check status

Use one:

* article_ready_with_no_patch_required
* article_ready_after_minor_patch
* major_revision_required
* source_record_insufficient_for_article
* human_review_required_before_article_use

### Main issues

List only actual issues.

If no issues exist, write:
none

### Exact patches

If no patch is needed, write:
none

For each patch, use:

**Patch [number] — [short title]**

Find:

[exact text]

Replace with:

[replacement text]

or:

Insert after:

[exact anchor text]

Insert:

[new text]

### Do not patch

List tempting changes that should remain untouched because they would strengthen claims, add new analysis, delete boundary discipline, erase unresolved items, remove non-use records, or over-smooth the article.

If no such tempting changes are relevant, write:
none
