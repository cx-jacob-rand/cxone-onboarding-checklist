# Checkmarx One Onboarding Checklist

Two pieces that work together to turn a customer's raw requirements into a
clickable, trackable onboarding checklist:

1. **`skills/cxone-onboarding-seeder`** — a Claude skill that reads a
   customer's requirements (notes, RFP excerpt, transcript, a list of asks)
   and generates a ready-to-load Markdown file.
2. **`tool/cxone-onboarding-checklist.html`** — a self-contained, no-build
   HTML app that renders that Markdown as an interactive 11-step onboarding
   checklist, tracks progress per customer, and exports a clean PDF.

The skill writes the file; the tool reads it. Nothing in this repo
contains customer data — it's just the skill and the viewer.

## Repo layout

```
skills/cxone-onboarding-seeder/
  SKILL.md                     # the skill's instructions
  references/baseline-checklist.json  # the 11-section baseline checklist data
tool/
  cxone-onboarding-checklist.html     # the interactive viewer/tool
```

---

## 1. The skill: `cxone-onboarding-seeder`

### What it does

Given a customer name and their raw requirements, the skill:

1. Reads the baseline 11-section checklist (`references/baseline-checklist.json`)
   — the same fixed sequence the tool renders (Pre-kickoff readiness →
   Tenant fundamentals → IAM → Applications & projects → Scanner config →
   Repo integration → CI/CD → Policy/gates → IDE plugins/Developer Assist →
   Reporting → Migration).
2. Extracts each distinct, actionable ask from the customer's notes and maps
   it to the section it actually belongs to.
3. **Checks feasibility for every mapped requirement** — searches Confluence,
   SharePoint, and checkmarx.com/docs.checkmarx.com to confirm whether
   Checkmarx One actually supports it, tagging each as `yes` / `no` /
   `unknown`, with a short note and a documentation link where one exists.
4. Writes a single `<customer-slug>.md` file in the exact schema the tool's
   parser expects (see [Markdown schema](#markdown-schema-shared-contract)
   below).

This is a **one-time seeding step** at kickoff — not meant to be re-run to
merge in new requirements later. New requirements after kickoff should be
added directly in the tool, via its own **"+ Add customer requirement"**
button in each section.

### How to use it

1. Make sure the skill is installed/available in your Claude session (it's a
   standard Claude Code / claude.ai skill — drop `skills/cxone-onboarding-seeder`
   into your skills directory, or install it however your setup loads skills).
2. In a conversation, give Claude:
   - the **customer name**, and
   - the **raw requirements** (pasted notes, a transcript excerpt, an RFP
     section, or just typed out verbally) — any format is fine.
3. Ask it to seed the checklist, e.g. *"seed the checklist for Acme Corp"*
   or *"turn these requirements into the onboarding checklist."*
4. Claude will report back: how many requirements it placed and where, the
   feasibility breakdown (Supported / Not supported / Needs verification —
   calling out the latter two by name), and anything it couldn't place.
5. It saves `<customer-slug>.md` (e.g. `acme-corp.md`) — load that into the
   tool directly, or drop it into a folder the tool is watching (see
   [Vault folder sync](#vault-folder-sync) below).

If the skill detects a seed file already exists for that customer, it asks
before overwriting rather than silently merging.

---

## 2. The tool: `cxone-onboarding-checklist.html`

A single HTML file — no server, no build step, no dependencies to install.
Open it directly in a browser (double-click, or `open tool/cxone-onboarding-checklist.html`).

### Core features

- **11-section checklist** matching `baseline-checklist.json`, with
  progress tracking per section and overall.
- **Per-customer state**, kept in the browser's `localStorage`, keyed by
  customer name — switch between customers without losing progress.
- **Load Markdown** — load a seed file produced by the skill (or any file
  following the same schema).
- **Save Markdown** — write the current state back out as a `.md` file,
  downloadable from the browser.
- **Connect folder…** (Chrome/Edge only, via the File System Access API) —
  point the tool at a local folder (e.g. an Obsidian vault) and it keeps that
  folder's Markdown files in sync automatically as you check items off, add
  notes, or add requirements — no manual Save needed. In unsupported
  browsers (Safari/Firefox), the tool falls back to manual Save/Load
  Markdown and says so in the status line.
- **+ Add customer requirement** (per section) — add new asks after kickoff
  without re-running the skill; you set the feasibility tag and optional
  link/note yourself.
- **Feasibility tags** — customer-requirement items show a Supported /
  Not supported / Needs verification indicator, an optional documentation
  link (rendered as a clean clickable hostname), and an optional prose note.
- **Internal notes** — private, per-item notes (click to add) that are never
  included in the PDF export.
- **Export PDF** — a clean, shareable PDF snapshot of current progress.

### Typical workflow

1. Run the skill to seed `<customer>.md` (or start from scratch in the tool).
2. Open the tool, click **Connect folder…** and point it at the folder
   holding your seed files (recommended), or just **Load Markdown** the file
   directly.
3. Work the checklist during onboarding — check items off, add notes, add
   new requirements as they come up.
4. Changes write back to the same Markdown file (automatically if a folder
   is connected, otherwise via **Save Markdown**) — so the `.md` file is
   always the source of truth, and the browser's `localStorage` is just a
   local cache.
5. **Export PDF** whenever you need a leave-behind or status snapshot.

---

## Markdown schema (shared contract)

Both the skill and the tool depend on this exact structure — the tool's
parser is regex-based, so deviating from it (wrong section numbers, missing
HTML comments, blank lines in the wrong place) will cause items to not load
or not match correctly.

```markdown
---
customer: <Customer Name>
updated: <ISO 8601 timestamp>
tool: cxone-onboarding-checklist
---

# Checkmarx One Onboarding — <Customer Name>

## 0. Pre-kickoff readiness

- [ ] <mandatory item text, verbatim from baseline-checklist.json> <!-- item:0-0 -->
- [x] <a customer requirement> <!-- item:custom-a1b2c3 feasible:yes link:https://docs.checkmarx.com/... -->
  > **Feasibility:** <prose note, no URL in it>

## 1. Tenant & account fundamentals
...
```

Key rules:

- All **11 sections** (`## 0.` through `## 10.`) must be present, in order,
  even if empty of customer items.
- **Mandatory items** come first in each section, tagged
  `<!-- item:<section>-<index> -->`, matching `baseline-checklist.json`
  exactly (0-indexed on both axes).
- **Customer-requirement items** come after, tagged
  `<!-- item:custom-<id> feasible:<yes|no|unknown> -->`, with an optional
  `link:<full https:// URL>` token.
- A feasibility note, when present, is the **very next line** after its item
  (no blank line in between): `  > **Feasibility:** <note>`.
- Checkbox state (`[ ]` / `[x]`) reflects completion, not feasibility.

See `skills/cxone-onboarding-seeder/SKILL.md` for the full generation rules.
