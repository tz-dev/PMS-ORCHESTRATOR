# PMS-ORCHESTRATOR

## A Human-Guided Runner for PMS-DISCIPLINE Case Work

**PMS-ORCHESTRATOR** is a service-independent desktop application for running structured PMS-DISCIPLINE case sessions step by step.

The application does not connect to an AI service, does not make autonomous route decisions, and does not treat generated output as evidence. It prepares the current prompt, shows the files required for that step, stores the raw response, applies deterministic local YAML checks where configured, and keeps the human user in control of every consequential branch.

Its operating principle is:

> Structure the workflow, preserve the record, expose drift, and keep decisions human-confirmed.

---

## What the Application Does

PMS-ORCHESTRATOR guides a case through a bounded analytical and article-generation pipeline:

```text
PMS Base
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
- Markdown preview;
- a maximized output reader;
- source and template availability checks;
- source and template downloads from one editable manifest.

---

![PMS-ORCHESTRATOR](img/screenshot.png)

---

## Design Principles

### Human control

The application never selects a consequential route by itself.

Gate outputs may preselect a route, but the user confirms or overrides:

- the selected PMS add-on;
- MIP use or non-use;
- AHP use or non-use;
- optional article generation.

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

---

## Implemented Pipeline

The guided workflow contains 30 steps.

### PMS Base and Core

```text
#1  Read PMS.yaml
#2  Apply Pre-Analysis Template
#3  Check Pre-Analysis YAML
#4  Apply PMS Core Case Application Template
#5  Check PMS Core Case Application YAML
```

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
#11 Apply MIP Gate Template
#12 Check MIP Gate YAML
#13 Read MIP YAML
#14 Apply MIP Case Application
#15 Check MIP Case Application YAML
#16 Apply AHP Gate Template
#17 Check AHP Gate YAML
#18 Apply AHP Module
#19 Check AHP Module Output YAML
```

AHP is available only after an actual MIP branch.

### Case Record

```text
#20 Apply Case Record Stage 1 Artifact Index
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

Archived material is stored under:

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
- a persistent timestamped status line.

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

The About view reads application metadata from `app_metadata.json` and displays the configured license file.

---

## Sources and Templates

The application expects local PMS, MIP/AHP, and PMS-DISCIPLINE YAML resources.

The editable root-level manifest is:

```text
source_manifest.json
```

It contains:

- PMS Base;
- six PMS add-on sources;
- MIP;
- the MIP AHP module;
- PMS-DISCIPLINE application templates;
- PMS-DISCIPLINE gate templates;
- PMS-DISCIPLINE Case Record templates.

`Check sources` reports each configured resource as:

```text
Present
Missing
```

The same dialog can download all configured resources.

Before replacing any existing file, the runner asks for confirmation.

Downloads are staged before replacement. A failed batch does not partially overwrite existing resources.

The manifest is intentionally editable so repository locations can be updated without changing application code.

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
- Fast Mode overrides;
- local validation handoffs;
- structural/semantic responsibility separation;
- runner-managed article shortcuts.

The manual PMS-DISCIPLINE prompt set and the application prompt resource serve different execution environments and should remain separate.

---

## Installation

### Requirements

- Windows with Python and Tkinter;
- PyYAML for local YAML validation.

Extract the project folder and start:

```text
start_orchestrator.bat
```

The launcher checks whether PyYAML is available and can install the dependency from:

```text
requirements.txt
```

Manual installation:

```text
py -3 -m pip install -r requirements.txt
```

Declining the installation still starts the application, but local YAML validation remains unavailable until PyYAML is installed.

---

## Basic Use

1. Start the application.
2. Create a new case.
3. Enter:
   - case title;
   - case material;
   - source status;
   - intended use.
4. Choose Full Review or Fast Mode.
5. Choose YAML validation behavior.
6. Open the current step.
7. Upload the listed files to the AI service.
8. Copy the rendered prompt.
9. Paste or import the AI response.
10. Review validation findings.
11. Save or complete the step.
12. Confirm routes when prompted.
13. Resume later by reopening the case folder.

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
├── prompts/
├── outputs/
├── exchanges/
├── validation/
└── history/
    └── route_revisions/
```

The case record preserves:

- user-entered case metadata;
- step state;
- route state;
- rendered prompts;
- raw outputs;
- validation reports;
- archived revisions.

---

## Project Structure

```text
PMS-ORCHESTRATOR/
├── README.md
├── LICENSE
├── app_metadata.json
├── requirements.txt
├── source_manifest.json
├── yaml_validation_manifest.json
├── start_orchestrator.bat
│
├── orchestrator/
│   ├── app.py
│   ├── app_metadata.py
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
│   └── test_core.py
│
└── cases/
```

The `cases/` directory contains user-generated work and should not be included in a clean release archive.

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
- Local YAML validation is structural rather than semantic.
- Template changes can cause older outputs to show findings under newer profiles.
- Fast Mode intentionally accepts greater semantic risk.
- Markdown Preview is a bounded desktop renderer, not a full browser engine.
- Resource availability does not prove that a source was selected, read, or applied.
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

> T. Zöller (2026): *PMS-ORCHESTRATOR — A Human-Guided Runner for PMS-DISCIPLINE Case Work.*

Replace this entry with the final repository or archival citation when available.

---

## License

See the repository `LICENSE` file.

The software license applies to the application code. PMS, PMS add-ons, PMS-DISCIPLINE templates, MIP, AHP, documentation, and downloaded source resources may carry their own licenses and attribution requirements.

© 2026 T. Zöller
