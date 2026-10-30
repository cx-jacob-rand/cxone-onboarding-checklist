# cx-se-onboarding-checklist

Seed and run a per-customer Checkmarx One onboarding checklist. Claude writes the Markdown from the customer's requirements; the bundled HTML tool renders it, tracks progress, and exports a PDF leave-behind.

## Install

From the internal marketplace (once merged):

```bash
claude plugin install cx-se-onboarding-checklist@cx-plugin-marketplace
```

From this repo directly:

```bash
claude plugin marketplace add cx-jacob-rand/cxone-onboarding-checklist
claude plugin install cx-se-onboarding-checklist@cxone-onboarding-checklist
```

## Contents

| Path | What it is |
|------|------------|
| `skills/cxone-onboarding-seeder/` | The seeder skill. Turns raw customer asks into a checklist `.md`, with every ask feasibility-checked against Confluence, SharePoint, and docs.checkmarx.com. |
| `skills/cxone-onboarding-tool/` | Opens the bundled HTML tool from Claude Code (`open the onboarding checklist`). |
| `tool/cxone-onboarding-checklist.html` | The interactive tracker. Single file, no build, no server. |

## Workflow

1. **Seed.** In Claude Code, from the folder where you keep checklist files: *"seed the checklist for Acme Corp"* and paste the discovery notes. Claude writes `acme-corp.md` and reports what it placed, what's supported, and what needs verification.
2. **Open the tool.** *"open the onboarding checklist"*, or double-click the HTML file. Click **Connect folder…** and pick that same folder. Every file there shows up under **Saved checklists**.
3. **Work it.** Check items off, add notes (Internal or Customer-facing), add new asks with **+ Add customer requirement**, set expected and done dates. Every change writes back to the `.md` file.
4. **Hand off.** **Export PDF** produces the leave-behind. Internal notes never appear in it.

## Prerequisites

- **Connectors.** Feasibility research uses the Atlassian (Confluence) and Microsoft 365 (SharePoint) connectors. Without them the skill falls back to public docs and more items land in "needs verification".
- **Browser.** Folder sync needs Chrome or Edge (File System Access API). Safari and Firefox work with **Save Markdown** / **Load Markdown**.

## Markdown contract

The skill and the tool share one schema. The full rules are in the [seeder skill](skills/cxone-onboarding-seeder/SKILL.md); the short version:

```markdown
---
customer: Acme Corp
updated: 2026-10-30T00:00:00.000Z
tool: cxone-onboarding-checklist
---

# Checkmarx One Onboarding — Acme Corp

## 0. Pre-kickoff readiness

- [ ] <baseline item text, verbatim> <!-- item:0-0 -->
- [ ] <customer ask> <!-- item:custom-a1b2c3 feasible:yes link:https://docs.checkmarx.com/... -->
  > **Note (Internal):** <prose, no URL>
```

The baseline items the skill emits (`references/baseline-checklist.json`) must match the `DATA` constant inside the HTML exactly, because the tool maps items by `item:<section>-<index>`. The repo's `scripts/check-baseline.py` enforces that.
