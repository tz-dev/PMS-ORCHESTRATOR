# PMS-ORCHESTRATOR

## A Human-Guided Runner for PMS-DISCIPLINE Case Work

**PMS-ORCHESTRATOR** is a service-independent desktop runner for structured PMS-DISCIPLINE case generation. It prepares the next prompt, shows the required files, stores the raw response, applies configured local YAML checks, keeps optional route decisions human-confirmed, and enforces an explicit PMS-DISCIPLINE Pre-Analysis pipeline stop.

The application does not connect to an AI service and does not treat attached files, YAML completion, or model output as evidence by presence alone.

> Structure the workflow, preserve the record, expose drift, and keep decisions human-confirmed.

---

![PMS-ORCHESTRATOR screenshot](img/screenshot.png)

---

## Main Case-Generation Flow

```text
PMS Base and optional case materials
→ Pre-Analysis
→ binding stop or PMS Core
→ optional PMS add-on
→ optional MIP
→ optional AHP
→ Case Record Stages 1–3
→ optional Iteration Handoff
→ optional Markdown article and/or separately bounded follow-up case
```

The runner guides one active step at a time. The user manually transfers prompts and outputs to the external AI service. No API key is required.

---

## Discipline Options Inside a Case

### Case packet and materials

Each case starts with:

```text
case title
case description or material
source status
intended use
```

Optional case materials can be attached, described, and assigned a purpose. Their presence does not upgrade them into evidence. Step #1 reads `PMS.yaml` first, then the configured case materials where accessible.


### Startup splash

At startup the runner shows `resources/splash.png` for five seconds. Click the splash to continue immediately. If the file is absent or cannot be loaded, the main window opens normally.

### Review mode

A case can run in **Full Review** or **Fast Mode**.

Full Review keeps the semantic AI check steps active:

```text
#3, #5, #7, #10, #12, #15, #17, #19, #21, #23, #25, #31
```

Fast Mode skips unfinished semantic review steps, forwards the direct output, and marks it as unchecked by user choice. It reduces calls and time while accepting higher semantic-drift risk.

### Discipline stop

The primary stop key is:

```yaml
scope_and_pipeline_disposition:
  pipeline_case_disposition: stop
```

The runner also recognizes the corresponding final-status stop fields and the configured mandatory person-near hard-stop combination.

In **Full Review**, a stop signal in step #2 opens a prominent warning but does not yet terminate the run. Step #3 remains mandatory and must confirm or correct the Pre-Analysis. A complete corrected Pre-Analysis YAML returned by step #3 takes precedence; when step #3 contains no corrected YAML, the saved step #2 YAML remains effective. If the effective checked result still contains a stop, the runner terminates before Core.

In **Fast Mode**, step #3 is skipped, so step #2 is evaluated immediately and a detected stop terminates the run at once.

A binding detected stop sets the run to `pipeline_stopped_by_pre_analysis`, locks Core and every later analysis step, and opens a modal status dialog. There is no continue-anyway action. The user may inspect the source output or reset the Pre-Analysis revision step; only a revised Pre-Analysis can reopen the pipeline.

This is a PMS-DISCIPLINE scope-control enforcement, not an autonomous optional route choice, person verdict, or truth validation.

### Local YAML validation

Local YAML validation is structural, not semantic. It can warn or block on malformed YAML, duplicate keys, missing keys, unexpected keys, shape mismatches, type mismatches, or invalid configured values. It does not decide whether a claim, route, interpretation, or conclusion is correct. Semantic review prompts receive the local result as authoritative for deterministic structure and should not repeat a full key-tree audit. A review response is treated as corrected YAML only when it is either a complete YAML document with the expected source-step root or contains exactly one fenced `yaml`/`yml` block with that root.

### Add-on route

After Core, the runner asks whether exactly zero or one PMS add-on should be used.

Supported add-ons:

```text
ANTICIPATION
CRITIQUE
CONFLICT
LOGIC
EDEN
SEX
```

Add-on selection follows structural burden, not surface vocabulary. A user override is preserved as user-requested, not as proof that the gate structurally recommended the add-on.

### MIP and AHP routes

MIP is downstream and non-add-on. Its runner route remains binary: `no_mip` skips steps #13–#19, while `use_mip` performs step #13 source reading and then the bounded case application in steps #14–#15. The nested source-reading and application fields in the MIP Gate refine the semantic recommendation; they do not create a source-reading-only runner route. AHP is available only after an actual checked MIP branch and remains a second-order analysis-quality overlay. AHP does not rescore MIP, activate D, upgrade evidence, or authorize stronger claims.

The MIP route dialog displays the overall MIP recommendation, the source-reading recommendation, and the case-application recommendation separately. Only the overall recommendation preselects the binary route. The nested decisions remain visible and are preserved in route provenance so reading guidance and application limits are not collapsed into one status.

### Case Record Stages 1–3

The Case Record stages preserve the run:

```text
#20 Stage 1 Artifact Index
#21 Stage 1 Check
#22 Stage 2 Layer Digest Extraction
#23 Stage 2 Check
#24 Stage 3 Full Record Integration
#25 Stage 3 Check
```

Stage 1 indexes actual selected or produced artifacts and route states. Stage 2 compresses layer-specific digests without changing the checked analysis. Stage 3 integrates the checked record without creating new substantive findings.

Stage #24 records the Stage 3 artifact's generation-time state, normally `ready_for_stage_3_output_check`. Stage #25 stores the separate semantic check result. Completing #25 does not retroactively make the original #24 lifecycle fields incorrect; only a concrete content defect warrants a corrected Stage 3 artifact.

MIP is not triggered merely because a constructed or hypothetical case could involve real persons if instantiated. Routine role/process coordination, deadline pressure, delay, or option-space reduction remains no-MIP when the case avoids person assessment, blame, dignity judgment, role-capacity evaluation, or stronger real-person use.

MIP may be recommended with limits when the checked case structure itself centers face/status loss, revision-capacity pressure, responsibility attribution, role-capacity pressure, dignity-in-practice pressure, reputational exposure, or consequential person-near transfer.

---

## Iteration Handoff

After checked Case Record Stage 3, step #26 prepares an optional **Iteration Handoff and Follow-up Preparation**.

```text
#26 Iteration Handoff and Follow-up Preparation
```

This is **not** Case Record Stage 4. It derives only from checked Stages 1–3 and runner metadata. It may identify current analytical depth, sufficiency for the original intended use, iteration value, urgency, follow-up targets, and material needed for a separately bounded future case.

It must not create new findings, preselect add-ons, preselect MIP/AHP, inherit claim authority, or treat prior analysis as evidence.

### User review inside step #26

Before step #26 completes, the runner opens the Iteration Handoff review window. The user sees:

```text
model recommendation
current analytical depth
sufficiency for original intended use
iteration urgency
urgency reasons
minimum follow-up coverage
proposed follow-up targets
```

For each proposed target, the user can:

```text
accept
refine
replace
split
merge
reject
annotate
```

The user can also add follow-up questions, case notes, chronology or trajectory notes, material-location notes, and a general handoff note.

The saved YAML keeps three layers separate:

```text
model proposal
user response
effective follow-up target
```

User notes guide future preparation. They do not become verified facts, current-case findings, evidence, operator activations, route authorization, or confirmation of the prior analysis.

### Post-handoff action

After step #26 is completed, the runner asks for the next controlled action:

```text
Create follow-up case now
Continue to article decision
Finish without article
Decide later
```

The same contextual action dialog can be reopened later with **Review Hand-off** in the toolbar or in the **Routes** menu. This allows a follow-up case to be created from an already completed handoff without resetting step #26 or pasting the handoff YAML again.

A follow-up case can be created only when the confirmed Iteration Handoff contains approved effective targets. The new case starts again at step #1 and must confirm its own boundary, source status, intended use, and material roles. It inherits context and lineage, not findings, routes, evidence status, claim ceiling, or claim authority.

---

## Optional Article Generation

Article generation begins only after the Iteration Handoff step.

```text
#27 Article Source Setup and Rendering Contract
#28 Base Markdown Case Article Draft
#29 Example Decision and Optional Example Generation
#30 Final Integrated Markdown Case Article
#31 Final Article Check and Conservative Patch
```

Two article profiles are available:

### Case article

A compact, standalone, case-specific article. It preserves the main structural movement, active-layer contributions, relevant rivals, limits, weakening conditions, reopening conditions, and a bounded iteration outlook when confirmed.

It avoids audit sprawl, repeated non-authority language, inactive-layer inventories, remote boundary catalogues, and separate operator paragraphs merely to prove every operator was considered.

### Full analysis article

A detailed, audit-rich narrative rendering of the checked analysis. It may include fuller provenance, route decisions, operator calibration, layer interaction, checked non-use records, extended boundaries, unresolved tensions, weakening and reopening conditions, and a fuller iteration outlook.

Both profiles preserve canonical PMS operator names and must not change the current case result, claim ceiling, source status, route state, or sufficiency assessment.

---

## Basic Use

1. Start the application.
2. Create a new case.
3. Enter title, case description/material, source status, and intended use.
4. Optionally add case materials.
5. Choose Full Review or Fast Mode.
6. Choose YAML validation behavior.
7. Complete the active steps by copying prompts to the AI service and pasting/importing outputs.
8. If Pre-Analysis records a pipeline stop, inspect or revise it; Core cannot be opened until the stop is removed. Otherwise confirm Add-on, MIP, AHP, and article routes when prompted.
9. Complete Case Record Stages 1–3.
10. Complete and review the Iteration Handoff.
11. Choose whether to create a follow-up case, continue to article generation, finish without article, or decide later.
12. When generating an article, choose `Case article` or `Full analysis article`.
13. When step #31 proposes exact minor patches, review the unified diff and choose whether to apply them; accepted patches are applied atomically after the original article is archived, and every completed decision is retained in the internal patch log.

Changing material or earlier analysis resets dependent work. Changing only the article profile resets article steps #27–#31. An approved Iteration Handoff remains independent of the article profile.

---

## Technical Documentation

Detailed implementation notes, storage layout, validation behavior, interface details, route handling, source manifests, project structure, and known boundaries are now kept in:

```text
TECHNICAL.md
```

---

## Claim and Authority Boundaries

PMS-ORCHESTRATOR is workflow software. It does not prove PMS, validate PMS Base, validate add-ons, validate MIP/AHP, turn YAML into evidence, turn model output into evidence, rank persons, make legal/clinical/forensic/HR conclusions, authorize publication, or make final case decisions.

A completed pipeline is a structured and reviewable record, not a truth certificate.

> Workflow completion is not epistemic authority.

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

## Citation

Suggested software citation:

> T. Zöller (2026): *PMS-ORCHESTRATOR — A Human-Guided Runner for PMS-DISCIPLINE Case Work*. Version 1.8.4. https://github.com/tz-dev/PMS-ORCHESTRATOR

Replace this entry with an archival citation or DOI when one becomes available.

---

## License

PMS-ORCHESTRATOR uses separate licenses for software and methodological content.

### Software

Unless a file states otherwise, the application source code, tests, runtime scripts, and application-specific configuration files are licensed under the Apache License, Version 2.0.

### Methodological content

Original prompts, PMS-DISCIPLINE templates, methodological documentation, and repository examples are licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license unless a file states otherwise.

### External resources

PMS Base, PMS add-ons, MIP, AHP, downloaded templates, and other resources originating from separate repositories retain their own copyright and license terms. Their presence in a local installation or in `source_manifest.json` does not relicense them under PMS-ORCHESTRATOR.

User-created cases, imported documents, case materials, and generated case outputs remain subject to the rights and responsibilities of their respective users and source owners. They are not automatically licensed under the repository licenses.

The complete scope notice and both full license texts are contained in the repository `LICENSE` file. The application displays that file verbatim under **Help → About PMS-ORCHESTRATOR**.

© 2026 T. Zöller
