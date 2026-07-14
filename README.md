# PMS-ORCHESTRATOR

## A Human-Guided Runner for PMS-DISCIPLINE Case Work

**PMS-ORCHESTRATOR** is a service-independent desktop application for running structured PMS-DISCIPLINE case sessions step by step.

The application does not connect to an AI service, does not make autonomous route decisions, and does not treat generated output or supplied files as evidence merely because they are present. It prepares the current prompt, shows the files required for that step, stores the raw response, applies deterministic local YAML checks where configured, and keeps the human user in control of every consequential branch.

Its operating principle is:

> Structure the workflow, preserve the record, expose drift, and keep decisions human-confirmed.

---

![PMS-ORCHESTRATOR screenshot](img/screenshot.png)

---

## What the Application Does

PMS-ORCHESTRATOR guides a case through a bounded analytical and article-generation pipeline:

```text
PMS Base and optional case materials
→ Pre-Analysis
→ PMS Core
→ optional PMS add-on
→ optional MIP
→ optional AHP
→ Case Record Stages 1–3
→ optional Markdown article
```

The runner supports:

- one active step at a time;
- exact prompt rendering from the internal prompt resource;
- case creation and editing with multiline source-status and intended-use fields;
- case-specific supporting materials;
- temporary material selection while a new case is being created;
- file lists for the current step;
- manual copy to an external AI service;
- manual paste or import of the response;
- raw output preservation;
- resumable cases;
- human-confirmed Add-on, MIP, AHP, and article routes;
- optional semantic AI review steps;
- deterministic local YAML validation;
- persisted validation reports and finding handoffs;
- reset and route-revision archives;
- material-revision archives;
- Markdown preview;
- a maximized output reader;
- source and template availability checks;
- source and template downloads from one editable manifest;
- consistent light and dark themes across the main window and dialogs.

---

## Design Principles

### Human control

The application never selects a consequential route by itself.

Gate outputs may preselect a route, but the user confirms or overrides:

- the selected PMS add-on;
- MIP use or non-use;
- AHP use or non-use;
- optional article generation.

The runner also does not infer that a supplied material is true, relevant, complete, or evidentiary merely because it was attached to a case.

### Service independence

The runner has no built-in AI provider connection.

The user:

1. copies the rendered prompt;
2. uploads the listed files to an AI service;
3. pastes or imports the response;
4. reviews and completes the step.

No API key is required.

### Raw-output preservation

Responses are stored as received. The application does not silently rewrite model output.

Corrections remain visible through:

- review-step outputs;
- local validation reports;
- route records;
- reset archives;
- material-revision archives;
- case history.

### Structural validation without semantic authority

Local YAML validation checks structure, not meaning.

It can detect:

- invalid YAML;
- duplicate keys;
- missing keys;
- unexpected keys;
- mapping/list shape mismatches;
- basic type mismatches;
- explicitly allowed values.

It does not determine whether an interpretation, claim, route, score, boundary, or conclusion is correct.

### Visible and correctable drift

The runner does not assume that model drift can be eliminated.

Instead, it keeps drift:

- visible;
- bounded;
- persisted;
- transferable to the next relevant prompt;
- correctable without erasing provenance.

A green check indicates completion without unresolved local YAML findings. A yellow check indicates completion with findings retained in the record.

### Materials remain bounded input

Case materials may inform the case, but their presence does not upgrade their status.

A material is not automatically:

- PMS Base;
- a PMS add-on;
- MIP or AHP;
- a template;
- validation;
- a checked artifact;
- evidence;
- proof of a claim.

Descriptions and purposes entered by the user are orientation metadata. They are not independent evidence or validation.

---

## Implemented Pipeline

The guided workflow contains 30 steps.

### PMS Base, case materials, and Core

```text
#1  Read PMS.yaml and Optional Case Materials
#2  Apply Pre-Analysis Template
#3  Check Pre-Analysis YAML
#4  Apply PMS Core Case Application Template
#5  Check PMS Core Case Application YAML
```

Step #1 always reads `PMS.yaml` first. Configured case materials are then read where accessible. Case analysis does not begin during this reading step.

### PMS add-on routing and application

```text
#6  Apply Add-on Recommendation Gate Template
#7  Check Add-on Recommendation Gate YAML
#8  Read Selected PMS Add-on YAML
#9  Apply Selected PMS Add-on Case Application Template
#10 Check Selected PMS Add-on Case Application YAML
```

Supported add-on families:

```text
ANTICIPATION
CRITIQUE
CONFLICT
LOGIC
EDEN
SEX
```

Exactly zero or one add-on is applied in a run.

### MIP and AHP

```text
#11 Apply PMS-DISCIPLINE MIP Gate Template
#12 Check MIP Gate YAML
#13 Read MIP YAML
#14 Apply MIP Case Application
#15 Check MIP Case Application YAML
#16 Apply PMS-DISCIPLINE AHP Gate Template
#17 Check AHP Gate YAML
#18 Apply AHP Module
#19 Check AHP Module Output YAML
```

MIP is a downstream non-add-on layer.

AHP is available only after an actual checked MIP branch. It is a second-order analysis-quality overlay and does not rescore MIP, activate D, upgrade evidence, or authorize stronger claims.

### Case Record

```text
#20 Apply PMS-DISCIPLINE Case Record Stage 1 Artifact Index
#21 Check Stage 1 Artifact Index
#22 Apply Stage 2 Layer Digest Extraction
#23 Check Stage 2
#24 Apply Stage 3 Full Record Integration
#25 Check Stage 3
```

The Case Record pipeline separates:

- artifact inventory;
- layer-level digest extraction;
- full-record integration.

Stage 1 also receives a runner-generated case-material inventory with exact case-relative paths, descriptions, purposes, hashes, sizes, and presence status.

Stage 3 integrates checked or explicitly unchecked prior artifacts without creating new substantive analysis.

### Optional Markdown article

```text
#26 Article Source Setup and Rendering Contract
#27 Base Markdown Case Article Draft
#28 Example Decision and Optional Example Generation
#29 Final Integrated Markdown Case Article
#30 Final Article Check and Conservative Patch
```

When step #28 returns an unambiguous no-example decision, the runner copies the base article to the final-article path without an unnecessary rewrite. The final conservative review remains available when semantic review steps are enabled.

---

## Case Materials

PMS-ORCHESTRATOR supports case-specific supporting material such as:

```text
ZIP document packages
PDF and DOCX documents
Markdown and plain-text notes
CSV and spreadsheet files
JSON and YAML data
articles, reports, statistics, and tables
images
other user-selected files
```

ZIP is recommended when several related files belong together.

### Adding materials

Materials can be added from:

- `Add materials…` while creating a new case;
- `Add materials…` in the Edit Case dialog;
- `Add materials` in the main toolbar.

The button in the New Case dialog is available immediately. A title does not have to be entered before files can be selected.

The material manager supports multiple file selection. For each material, the user can enter:

- a description of its contents;
- its purpose in the case.

Duplicate filenames are handled safely. A later file does not silently overwrite an existing material with the same name.

### Materials in a new case

Files selected while creating a new case remain temporary until the case is saved.

After the user selects `Save`:

1. the case folder is created;
2. the selected files are copied into the case;
3. `materials.json` is written;
4. step #1 is rendered with the saved material inventory.

Cancelling the New Case dialog creates no case and copies no pending material files.

### Reading order in step #1

The controlled reading order is:

```text
1. Read PMS.yaml carefully and completely.
2. For each supplied ZIP archive, inspect the archive inventory first.
3. Read every accessible and relevant file contained in the archive.
4. Read every remaining standalone case-material file.
5. Identify inaccessible, unsupported, corrupted, encrypted, or otherwise unreadable content explicitly.
```

The runner lists each configured material with:

- material identifier;
- original filename;
- case-relative path;
- description;
- purpose;
- local presence status;
- SHA-256;
- file size.

The model must not claim that a missing or inaccessible material was read.

### Material changes and reset behavior

Changing the material set, description, or purpose changes the step #1 input packet.

After step #1 has begun, saving such a change requires a reset from step #1. The runner warns the user before it:

- archives dependent prompts and outputs;
- archives validation reports;
- archives route records;
- restarts the pipeline from step #1.

The attached material files remain part of the case. Pipeline resets do not delete them.

Removed or replaced material states are archived under the case history.

---

## Full Review and Fast Mode

Each case can run with semantic AI review steps enabled or disabled.

### Full Review

The semantic review steps remain active:

```text
#3, #5, #7, #10, #12, #15, #17, #19, #21, #23, #25, #30
```

These steps review:

- semantic field use;
- claim boundaries;
- route and source consistency;
- contradictions;
- over-triggering;
- safe correction of known structural findings.

### Fast Mode

Unfinished semantic review steps are skipped.

The runner then:

- forwards the corresponding direct output;
- marks it as `unchecked_by_user_choice`;
- never relabels it as checked or certified;
- keeps route decisions human-confirmed;
- preserves local YAML findings;
- passes unresolved findings to the next active prompt.

Fast Mode reduces model calls and time, but accepts a higher risk of semantic drift.

---

## Local YAML Validation

Local validation is configured per case:

```text
Validate generated YAML locally
On structural findings: warn | block
```

### Warn mode

The application shows findings and asks for confirmation before completion.

### Block mode

Structural findings must be corrected before the step can be completed.

### Corrected YAML in review steps

A semantic review step may return a complete corrected YAML document.

When the entire review output is one parseable YAML mapping or sequence, the runner can validate it against the reviewed source step's profile.

Examples:

```text
#3  uses the profile of #2
#5  uses the profile of #4
#7  uses the profile of #6
#10 uses the profile of #9
```

The same inheritance applies through MIP, AHP, and the Case Record stages.

Mixed prose plus YAML is not treated as corrected YAML.

### Persisted findings and handoff

Validation reports are stored under:

```text
cases/<case-id>/validation/
```

An unresolved report can be inserted into the next relevant prompt as a runner-generated handoff.

This handoff is:

- authoritative only for deterministic structural findings;
- not case evidence;
- not semantic review;
- not permission to invent missing content.

When corrected YAML validates cleanly, the original report remains in the history but is marked as resolved by the correcting step.

---

## Route Handling

Routes are saved independently for:

- selected add-on;
- MIP;
- AHP;
- article generation.

Changing a saved route archives and resets only dependent work.

Archived route revisions are stored under:

```text
cases/<case-id>/history/route_revisions/
```

Upstream work remains preserved unless the changed route makes it dependent.

Skipped branches remain visible in later Case Record stages as skipped, not applicable, rejected, not recommended, scan-only, unsafe, unresolved, or otherwise bounded by the recorded route.

---

## Interface

### Main workflow

The main window contains:

- the pipeline navigator;
- current-step title and status;
- files required for the selected step;
- rendered prompt;
- raw prompt view;
- AI service output editor;
- Markdown preview where applicable;
- YAML validation status;
- route review controls;
- `Add materials`;
- `Check sources`;
- a persistent timestamped status line.

### Case dialogs

The New Case and Edit Case dialogs contain:

- case title;
- case description or material;
- multiline source status;
- multiline intended use;
- semantic-review setting;
- local-YAML-validation setting;
- case-material controls where applicable.

The Case Materials dialog provides:

- multiple file selection;
- file type and size display;
- content description;
- purpose in the case;
- removal of selected entries;
- save or cancel controls.

The dialogs use the active application theme.

### Escape key

`Esc` closes the following dialogs without saving their current edits:

```text
New case
Edit case
Case materials
```

In the output reader, `Esc` leaves full-screen mode first and closes the reader when it is not full-screen.

### Direct mouse actions

- Right-click in the prompt area copies the raw prompt.
- Right-click in the output area pastes clipboard text into the raw output editor.

### Markdown Raw / Preview

Prompts open in Preview by default and can be switched to Raw.

Markdown outputs also support:

```text
Raw | Preview
```

Saving, completion, copying, and validation always operate on the raw text.

### Output reader

`Open output reader` opens a maximized, read-only view.

It supports:

- YAML syntax colors;
- Markdown Raw / Preview;
- plain-text reading;
- search and result highlighting;
- line-wrap toggle;
- Copy;
- Select All;
- Close Reader;
- `F11` full-screen toggle;
- `Esc` to leave full-screen mode or close the reader.

### Help menu

The application includes:

```text
Help
├── PMS-ORCHESTRATOR Guide
├── Keyboard and mouse controls
├── Open project folder
├── Open GitHub repository
└── About PMS-ORCHESTRATOR
```

The About view reads application metadata from `app_metadata.json` and displays the configured `LICENSE` file verbatim.

---

## Sources and Templates

The application expects local PMS, MIP/AHP, and PMS-DISCIPLINE YAML resources.

The editable root-level manifest is:

```text
source_manifest.json
```

The current manifest covers:

- PMS Base;
- six PMS add-on sources;
- MIP;
- the MIP AHP module;
- PMS-DISCIPLINE application templates;
- PMS-DISCIPLINE gate templates;
- PMS-DISCIPLINE Case Record templates.

This is a combined manifest containing 9 source files and 14 templates.

`Check sources` reports each configured resource as:

```text
Present
Missing
```

The same dialog can download all configured resources.

Before replacing any existing file, the runner asks for confirmation.

Downloads are staged before replacement. A failed batch does not partially overwrite existing resources.

The manifest is intentionally editable so repository locations can be updated without changing application code.

Case materials are not resource-manifest entries. They belong to individual cases.

---

## Internal Prompt Resource

The app-specific prompt sequence is stored at:

```text
resources/Prompts and Instructions.md
```

This file is required by the application.

It is not identical to the manual PMS-DISCIPLINE prompt document. The app-specific resource contains runner-only instructions such as:

- dynamic manifests;
- exact case-relative output paths;
- case-material reading instructions;
- Fast Mode overrides;
- local validation handoffs;
- structural/semantic responsibility separation;
- runner-managed article shortcuts.

The manual PMS-DISCIPLINE prompt set and the application prompt resource serve different execution environments and should remain separate.

---

## Installation

### Requirements

- Python 3;
- Tkinter;
- PyYAML for local YAML validation.

From the project root, install PyYAML when needed:

```text
py -3 -m pip install PyYAML
```

On systems where the Python command is `python`:

```text
python -m pip install PyYAML
```

Start the application from the project root:

```text
py -3 run_orchestrator.py
```

or:

```text
python run_orchestrator.py
```

The application can start without PyYAML, but local YAML validation remains unavailable until the dependency is installed.

---

## Basic Use

1. Start the application.
2. Create a new case.
3. Enter:
   - case title;
   - case description or material;
   - source status;
   - intended use.
4. Optionally add case materials and describe their contents and purpose.
5. Choose Full Review or Fast Mode.
6. Choose YAML validation behavior.
7. Save the case.
8. Open the current step.
9. Upload the listed files to the AI service.
10. Copy the rendered prompt.
11. Paste or import the AI response.
12. Review validation findings.
13. Save or complete the step.
14. Confirm routes when prompted.
15. Resume later by reopening the case folder.

---

## Case Storage

Each case is stored in its own folder.

A typical case contains:

```text
cases/<case-id>/
├── case.json
├── session.json
├── route.json
├── mip_route.json
├── ahp_route.json
├── article_route.json
├── materials.json
├── materials/
├── prompts/
├── outputs/
├── exchanges/
├── validation/
└── history/
    ├── route_revisions/
    └── material_revisions/
```

`materials.json` uses a separate material-manifest schema and records:

- material identifiers;
- original filenames;
- stored paths;
- descriptions;
- purposes;
- sizes;
- SHA-256 hashes;
- added and updated timestamps.

The case record preserves:

- user-entered case metadata;
- step state;
- route state;
- case-material metadata;
- rendered prompts;
- raw outputs;
- validation reports;
- archived route and material revisions.

---

## Project Structure

```text
PMS-ORCHESTRATOR/
├── README.md
├── LICENSE
├── app_metadata.json
├── run_orchestrator.py
├── source_manifest.json
├── yaml_validation_manifest.json
│
├── img/
│   └── screenshot.png
│
├── orchestrator/
│   ├── __init__.py
│   ├── app.py
│   ├── app_metadata.py
│   ├── case_materials.py
│   ├── dialogs.py
│   ├── gate_reader.py
│   ├── platform_utils.py
│   ├── prompt_source.py
│   ├── registry.py
│   ├── source_manager.py
│   ├── storage.py
│   ├── ui_views.py
│   └── yaml_validator.py
│
├── resources/
│   └── Prompts and Instructions.md
│
├── pms/
│   ├── PMS.yaml
│   └── PMS-*.yaml
│
├── mip/
│   ├── MIP - Maturity in Practice.yaml
│   └── MIP - Maturity in Practice - AHP Module.yaml
│
├── templates/
│   └── *.yaml
│
├── tests/
│   ├── test_core.py
│   ├── test_review_validation.py
│   └── test_ui_views.py
│
└── cases/
```

The `cases/` directory contains user-generated work. It should normally be excluded from a clean public release unless a case is intentionally supplied as an anonymized example.

---

## Claim and Authority Boundaries

PMS-ORCHESTRATOR is workflow software.

It does not:

```text
prove PMS
validate PMS Base
validate a PMS add-on
validate MIP or AHP
turn YAML into evidence
turn AI output into source evidence
turn a supplied file into evidence by presence alone
diagnose or rank persons
make legal or forensic conclusions
authorize publication
authorize implementation
make final case decisions
```

A completed pipeline is a structured and reviewable record, not a truth certificate.

The controlling rule is:

> Workflow completion is not epistemic authority.

---

## Known Boundaries

- AI-service behavior remains outside the application's control.
- Files must still be uploaded manually to the selected AI service.
- The runner cannot guarantee that an AI service can open every supplied format or archive entry.
- Local YAML validation is structural rather than semantic.
- Template changes can cause older outputs to show findings under newer profiles.
- Fast Mode intentionally accepts greater semantic risk.
- Markdown Preview is a bounded desktop renderer, not a full browser engine.
- Resource availability does not prove that a source was selected, read, or applied.
- Case-material presence does not prove truth, relevance, completeness, or evidentiary status.
- User-supplied material descriptions and purposes are orientation metadata.
- MIP and AHP remain separate analytical layers with their own limits.
- AHP does not rescore or authorize MIP output.
- Human review remains necessary for consequential use.

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

> T. Zöller (2026): *PMS-ORCHESTRATOR — A Human-Guided Runner for PMS-DISCIPLINE Case Work*. Version 1.5. https://github.com/tz-dev/PMS-ORCHESTRATOR

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
