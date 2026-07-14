# PMS-DISCIPLINE

PMS-DISCIPLINE is a methodological use-discipline for applying PMS-based analysis to bounded cases.

It is not PMS Base, not a validator, not governance, not an authority layer, and not a substitute for human judgment. Its role is to make PMS use more explicit, bounded, inspectable, correctable, and resistant to over-application.

PMS-DISCIPLINE defines how a case should be prepared, routed, checked, limited, and recorded when PMS Core, selected add-ons, downstream MIP review, downstream AHP review, and final case-record artifacts may become relevant.

---

## Status

Version: `v1.0`

This repository contains:

* the PMS-DISCIPLINE paper,
* prompt and instruction material,
* YAML templates for disciplined PMS case use,
* add-on application templates,
* MIP and AHP gate templates,
* staged case-record templates.

The repository is designed for manual, AI-assisted, or tool-assisted use, but no file in this repository is itself a validator or authority source.

---

## What PMS-DISCIPLINE Is

PMS-DISCIPLINE is an application discipline.

It helps answer questions such as:

* What is the bounded case?
* What is the source status?
* What is the intended use?
* What is the claim ceiling?
* Has PMS Core been applied before any add-on?
* Is an add-on really warranted, or is this only a topical cue?
* Does the case remain Core-only?
* Does the case create downstream MIP pressure?
* Can AHP even become relevant?
* What was checked, corrected, skipped, downgraded, suspended, refused, or redirected?
* What may be carried forward as a checked artifact?

PMS-DISCIPLINE is mainly concerned with **use**, not theory creation.

---

## What PMS-DISCIPLINE Is Not

PMS-DISCIPLINE is not:

* PMS Base,
* a replacement for `PMS.yaml`,
* a validator,
* a truth engine,
* governance,
* a scoring system,
* a maturity model,
* a publication license,
* an action authorization layer,
* a person-ranking tool,
* a substitute for human confirmation,
* a substitute for source checking,
* a substitute for correction.

A completed template is not a verdict.

A case-pass record is not closure.

A YAML file is not evidence.

An AI output is not evidence.

---

## Relationship to PMS Core

PMS Core remains primary.

Every disciplined PMS case must begin from PMS Base grammar. In operational use, `PMS.yaml` is read first. Any supplied case materials are then inspected and read as bounded case input before Pre-Analysis, add-on routing, downstream review, or article rendering.

For ZIP packages, the archive inventory should be inspected before accessible contained files are read. Case materials do not become PMS Base, templates, validation, checked artifacts, or evidence merely because they were supplied to the workflow.

PMS-DISCIPLINE does not revise PMS operators, dependencies, derived structures, or base guardrails. It only constrains how PMS-based case use is staged, checked, limited, and recorded.

---

## Supported Add-on Families

The ordinary PMS-DISCIPLINE add-on path supports the following selected add-on families:

* `ANTICIPATION`
* `CRITIQUE`
* `CONFLICT`
* `LOGIC`
* `EDEN`
* `SEX`

A case may remain Core-only.

A case may proceed into exactly one selected add-on when the checked Add-on Recommendation Gate supports it and the route is confirmed.

Multiple add-on pressure does not automatically authorize multiple add-on application. It usually indicates decomposition, revision, narrowing, or a stronger case-boundary problem.

---

## MIP and AHP Are Not Add-ons

MIP and AHP are downstream layers, not ordinary add-ons.

MIP is a downstream non-add-on review/application layer. It may become relevant only after earlier checked artifacts create sufficient MIP pressure and the MIP Gate supports review.

AHP is a later second-order analysis-quality overlay. It may become relevant only after checked MIP output exists. AHP does not rescore MIP, does not activate D, does not raise source status, and does not authorize stronger claims.

AHP cannot be reached directly from Core, from the Add-on Gate, or from an add-on output alone.

---

## Basic Route Logic

A disciplined case may follow different routes depending on checked gate results and human route confirmation.

Typical route families include:

```text
Core only
Core + selected add-on
Core + MIP
Core + selected add-on + MIP
Core + MIP + AHP
Core + selected add-on + MIP + AHP
```

The exact route is not selected by topic labels. It is selected through checked artifacts, gate outputs, route confirmation, and claim-boundary discipline.

---

## Human Route Confirmation

PMS-DISCIPLINE separates gate recommendation from route confirmation.

A gate may recommend, reject, downgrade, suspend, refuse, redirect, or mark uncertainty. But the route still requires explicit confirmation where the prompt sequence demands it.

Human route confirmation does not turn a non-recommended layer into a gate-recommended layer. It also does not authorize stronger claims by itself.

Overrides must be recorded as overrides.

---

## Checked Artifacts

Only checked artifacts may be carried forward.

The rule is:

```text
ready
→ the original YAML becomes the checked artifact.

corrected
→ the complete corrected YAML becomes the checked artifact.
   Audit prose is not the artifact.

not ready
→ stop, correct, or rerun.
   Do not carry the unchecked YAML forward.
```

A superseded pre-correction artifact must not be silently reused in later gates, case records, Markdown rendering, or publication-facing outputs.

---

## Review Modes

PMS-DISCIPLINE supports a strict review distinction.

### Full Review Mode

Full Review Mode is the default. It includes semantic review, structural checking, and correction where needed.

### Fast Mode

Fast Mode may skip some semantic review steps by user choice.

Skipped review does not become validation.

Skipped output remains:

```text
unchecked_by_user_choice
```

No skipped review may be called correction, acceptance, validation, certification, or approval.

---

## Repository Structure

Current repository structure:

```text
PMS-DISCIPLINE/
├─ PMS-DISCIPLINE.md
├─ examples/
│  └─ Prompts and Instructions.md
├─ img/
│  └─ logo.png
└─ templates/
   ├─ pms_core_case_application_template.yaml
   ├─ pms_discipline_pre_analysis_template.yaml
   ├─ pms_discipline_addon_recommendation_gate_template.yaml
   ├─ pms_discipline_mip_gate_template.yaml
   ├─ pms_discipline_ahp_gate_template.yaml
   ├─ pms_addon_anticipation_case_application_template.yaml
   ├─ pms_addon_conflict_case_application_template.yaml
   ├─ pms_addon_critique_case_application_template.yaml
   ├─ pms_addon_eden_case_application_template.yaml
   ├─ pms_addon_logic_case_application_template.yaml
   ├─ pms_addon_sex_case_application_template.yaml
   ├─ pms_case_record_stage_1_artifact_index_template.yaml
   ├─ pms_case_record_stage_2_layer_digest_extraction_template.yaml
   └─ pms_case_record_stage_3_full_case_record_integration_template.yaml
```

---

## Main Files

### `PMS-DISCIPLINE.md`

The main paper.

It defines PMS-DISCIPLINE as a bounded application discipline for responsible PMS use. It explains source status, claim ceilings, add-on discipline, downstream MIP/AHP boundaries, stop capability, correction, templates, case-pass records, and AI-assisted use.

### `examples/Prompts and Instructions.md`

Operational prompt and instruction sequence.

This file contains the routed prompt sequence for disciplined case application. It includes Core, Add-on Gate, selected add-on application, MIP Gate, MIP application, AHP Gate, AHP application, Case Record staging, Markdown rendering, and final checks.

### `templates/`

YAML templates for disciplined PMS case work.

The templates are not validators. They are structured artifacts for making case handling inspectable.

---

## Template Groups

### Core and Pre-Analysis

```text
pms_discipline_pre_analysis_template.yaml
pms_core_case_application_template.yaml
```

These templates prepare the case boundary, source status, claim ceiling, intended use, PMS Core application, non-capture, rival pressure, and correction conditions.

### Add-on Gate

```text
pms_discipline_addon_recommendation_gate_template.yaml
```

This template determines whether a supported add-on family is recommended, not recommended, scan-only, unsafe, or unclear.

It does not apply the add-on.

It does not authorize MIP or AHP.

### Add-on Application Templates

```text
pms_addon_anticipation_case_application_template.yaml
pms_addon_conflict_case_application_template.yaml
pms_addon_critique_case_application_template.yaml
pms_addon_eden_case_application_template.yaml
pms_addon_logic_case_application_template.yaml
pms_addon_sex_case_application_template.yaml
```

These templates apply exactly one selected add-on after checked Core and checked Add-on Gate output.

They preserve PMS Core, source status, claim ceiling, non-capture, rival pressure, and stop capability.

They do not apply MIP or AHP.

### MIP and AHP Gates

```text
pms_discipline_mip_gate_template.yaml
pms_discipline_ahp_gate_template.yaml
```

The MIP Gate determines whether downstream MIP review/application pressure is present.

The AHP Gate can only become relevant after checked MIP output exists.

Neither gate is an ordinary add-on.

### Case Record Stages

```text
pms_case_record_stage_1_artifact_index_template.yaml
pms_case_record_stage_2_layer_digest_extraction_template.yaml
pms_case_record_stage_3_full_case_record_integration_template.yaml
```

Case records are staged for inspectability.

They can preserve which artifacts existed, what each layer contributed, what was skipped, what was corrected, what remained unresolved, and what claim boundary applies.

They are not verdicts.

---

## Stop Capability

Stopping is a valid disciplined outcome.

A case may stop before add-on use, before MIP review, before MIP application, before AHP review, before AHP application, before Case Record integration, before Markdown rendering, or before publication-facing use.

A stopped case is not automatically incomplete. If the stop reason is explicit, stopping may be the correct disciplined result.

---

## Optional Orchestrator Tooling

A separate local orchestrator may be used to execute the PMS-DISCIPLINE prompt sequence, preserve route state, pass declared files, store checked artifacts, and prevent skipped or unavailable branches from being silently treated as present: [PMS-ORCHESTRATOR](https://github.com/tz-dev/PMS-ORCHESTRATOR).

PMS-ORCHESTRATOR also supports case-specific materials such as ZIP document packages, articles, reports, statistics, tables, notes, data files, and images. Materials can be added while creating or editing a case, and each material can carry a user-supplied description of its contents and purpose in the case.

Configured materials are copied into the local case folder and included in step #1 together with `PMS.yaml`. The reading order remains controlled:

1. Read `PMS.yaml` first.
2. Inspect the inventory of each supplied ZIP archive.
3. Read every accessible and relevant file contained in the archive.
4. Read the remaining standalone case-material files.
5. Identify inaccessible, unsupported, corrupted, encrypted, or otherwise unreadable content explicitly.

The orchestrator records material paths, descriptions, purposes, sizes, hashes, and local presence status. This metadata preserves provenance and file availability; it does not establish that a file was interpreted correctly or that its contents are true.

Changing the configured materials after step #1 has begun requires the dependent pipeline work to be reset and archived before the case is rerun with the changed material packet.

The orchestrator is tooling.

It is not PMS Base.

It is not PMS-DISCIPLINE theory.

It is not a validator.

It is not governance.

It is not a source of authority.

It is not a substitute for checked artifacts or human route confirmation.

Case materials are bounded input.

They are not PMS Base.

They are not templates.

They are not validation.

They are not checked artifacts merely because they were uploaded.

They are not evidence merely because they are locally present.

Repository cases generated through an orchestrator should be documented in the orchestrator repository and may reference this PMS-DISCIPLINE repository as the methodological discipline.

---

## Examples

Examples will be added after case generation.

```text
<!-- EXAMPLES_START -->

Placeholder for PMS-DISCIPLINE examples.

Suggested future entries:
- Core-only case
- Core + ANTICIPATION case
- Core + selected add-on + MIP case
- Core + MIP + AHP case
- Full routed case with Case Record stages

<!-- EXAMPLES_END -->
```

---

## Links and Resources

### PMS Core Theory and Model

| Category        | Resource                                                                                 | Description                                            |
| --------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Project website | [PMS Theory Site](https://pms-theory.netlify.app)                                        | Canonical PMS theory reference                         |
| GitHub repo     | [PMS Theory / Repository](https://github.com/tz-dev/Praxeological-Meta-Structure-Theory) | PMS grammar, theory texts, YAML/JSON model definitions |
| DOI             | [PMS Theory DOI](https://doi.org/10.5281/zenodo.17075154)                                | Archived reference version of the PMS base theory      |

### PMS Domain Lenses and Overlays

| Category    | Resource                                                       | Description                                                        |
| ----------- | -------------------------------------------------------------- | ------------------------------------------------------------------ |
| GitHub repo | [PMS-ANTICIPATION](https://github.com/tz-dev/PMS-ANTICIPATION) | Anticipatory praxis under uncertainty                              |
| GitHub repo | [PMS-CRITIQUE](https://github.com/tz-dev/PMS-CRITIQUE)         | Critique as interruption, recontextualization, and correction      |
| GitHub repo | [PMS-CONFLICT](https://github.com/tz-dev/PMS-CONFLICT)         | Conflict as stabilized incompatibility                             |
| GitHub repo | [PMS-EDEN](https://github.com/tz-dev/PMS-EDEN)                 | Drift from praxis to comparison, pseudo-symmetry, reciprocity loss |
| GitHub repo | [PMS-LOGIC](https://github.com/tz-dev/PMS-LOGIC)               | Structural responsibility, logical limits, post-moral effects      |
| GitHub repo | [PMS-SEX](https://github.com/tz-dev/PMS-SEX)                   | Sexuality as framed impulse, asymmetry, time, exit, and binding    |
| GitHub repo | [PMS-QC](https://github.com/tz-dev/PMS-QC)                     | PMS structural layer for quantum computing                         |

### PMS Downstream Applications and Architectures

| Category    | Resource                                                             | Description                                                                                                                                                                                                                                                                                                             |
| ----------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub repo | [PMS-AXIOM](https://github.com/tz-dev/PMS-AXIOM)                     | Cartography of classical closure-demands across the PMS stack                                                                                                                                                                                                                                                           |
| GitHub repo | [PMS-STACK](https://github.com/tz-dev/PMS-STACK)                     | Implementation-layer PMS architecture specification for abstract machine, virtual CPU, OS, runtime, language, security, networking, distributed systems, tooling, simulation, verification, boot, and cluster profiles ([book website](https://pms-stack.netlify.app) / [amazon](https://www.amazon.com/dp/B0G6G7V38P)) |
| GitHub repo | [PMS-RUST](https://github.com/tz-dev/PMS-RUST)                       | Executable PMS-STACK Evidence Spine: Rust kernel, REPL, validation, JSONL, vFS, AI bridge                                                                                                                                                                                                                               |
| GitHub repo | [PMS-EMERGENCE MODEL](https://github.com/tz-dev/PMS-EMERGENCE_MODEL) | Claim-disciplined developmental architecture for trace-backed emergence                                                                                                                                                                                                                                                 |
| GitHub repo | [PMS — UNDER LOAD](https://github.com/tz-dev/PMS---UNDER-LOAD)       | Structural self-critique of PMS under calibration, coverage, stack drift, publicness, and self-application                                                                                                                                                                                                              |

### MIP: Adjacent Praxeological Ecosystem

| Category | Resource | Description |
|---|---|---|
| GitHub repo | [Maturity-in-Practice Repository](https://github.com/tz-dev/Maturity-in-Practice) | Maturity in Practice model + attack surface hardening addon ([book website EN](https://maturity-in-practice.netlify.app) / [book website DE](https://reife-im-vollzug.netlify.app) / [amazon EN](https://www.amazon.com/dp/B0G4XBKNNR) / [amazon DE](https://www.amazon.de/dp/B0G4SPBDQD)) |
| Book website | [Maturity in Practice (EN)](https://maturity-in-practice.netlify.app) | English book website for *Maturity in Practice – A Praxeological Anthropology* |
| Book website | [Reife im Vollzug (DE)](https://reife-im-vollzug.netlify.app) | German book website for *Reife im Vollzug – Eine praxeologische Anthropologie* |
| Book on Amazon | [Maturity in Practice on Amazon](https://www.amazon.com/dp/B0G4XBKNNR) | Published English edition |
| Book on Amazon | [Reife im Vollzug on Amazon](https://www.amazon.de/dp/B0G4SPBDQD) | Published German edition |

### Interactive Assistants

| Category      | Resource                                                                                                                           | Description                                     |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| GPT assistant | [PMS Model Assistant](https://chatgpt.com/g/g-69358a2a4980819183da6a97893389cf-pms-model-assistant)                                | Interactive PMS.yaml exploration and validation |
| GPT assistant | [Maturity in Action](https://chat.openai.com/g/g-693460d3def48191ad08647301645a2e-maturity-in-action-a-praxeological-anthropology) | Applied praxeological anthropology assistant    |

---

## Use Notes

A disciplined PMS-DISCIPLINE run should preserve the following rules:

```text
Read PMS.yaml first.
For ZIP case materials, inspect the archive inventory before reading accessible contained files.
Treat supplied case materials as bounded input, not as PMS Base, validation, checked artifacts, or evidence by presence alone.
Do not treat topic cues as add-on authorization.
Do not treat template completion as validation.
Do not treat YAML as evidence.
Do not treat AI output as evidence.
Do not treat Core output as permission to publish.
Do not treat add-on output as MIP/AHP authorization.
Do not treat MIP/AHP as ordinary add-ons.
Do not carry unchecked artifacts forward.
Do not erase skipped branches.
Do not upgrade source status through fluency.
Do not convert structural readability into person verdicts.
```

---

## License

PMS-ORCHESTRATOR uses separate licenses for software and methodological content.

### Software

Unless otherwise stated, the application source code, tests, launchers, and application-specific configuration files are licensed under the Apache License, Version 2.0.

### Methodological Content

Original prompts, PMS-DISCIPLINE templates, methodological documentation, and repository examples are licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license unless a file states otherwise.

### External Resources

PMS Base, PMS add-ons, MIP, AHP, downloaded templates, and other resources originating from separate repositories retain their own copyright and license terms. Their presence in a local installation or in `source_manifest.json` does not relicense them under PMS-ORCHESTRATOR.

User-created cases, imported documents, uploaded case materials, and generated case outputs remain subject to the rights and responsibilities of their respective users and source owners. They are not automatically licensed under the repository licenses.

The complete license scope and both full license texts are contained in the repository `LICENSE` file. The application displays this file verbatim under **Help → About PMS-ORCHESTRATOR**.

---

## Final Boundary

PMS-DISCIPLINE makes PMS use more inspectable.

It does not make PMS use automatically correct.

It disciplines application, records limits, preserves correction, and keeps stop capability available.

Its central practical rule is simple:

```text
Correction before coherence.
Boundary before claim strength.
Checked artifact before continuation.
Stop capability before closure.
```
