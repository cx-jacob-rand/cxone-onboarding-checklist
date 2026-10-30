# Checkmarx One Onboarding Checklist

A Claude Code plugin for SEs and CSMs running a Checkmarx One POV or onboarding. Two parts that share one Markdown file per customer:

1. **The seeder skill** reads a customer's raw requirements (discovery notes, an RFP excerpt, a call transcript) and writes a checklist Markdown file. Every customer ask is placed in the right step of the 11-step onboarding sequence and checked against Confluence, SharePoint, and docs.checkmarx.com for whether Checkmarx One can actually do it.
2. **The HTML tool** renders that file as an interactive checklist, tracks progress per customer, syncs changes back to the Markdown, and exports a customer-facing PDF.

Nothing in this repo contains customer data. Customer files live wherever you point the tool.

## Install

```bash
claude plugin marketplace add cx-jacob-rand/cxone-onboarding-checklist
claude plugin install cx-se-onboarding-checklist@cxone-onboarding-checklist
```

Then in Claude Code: *"open the onboarding checklist"* to launch the tool, or *"seed the checklist for Acme Corp"* with the customer's notes to generate a file.

**claude.ai users:** upload `dist/cxone-onboarding-seeder.zip` (build it with `scripts/build-claude-ai-skill.sh`) under Settings → Capabilities → Skills, and download the HTML tool from [`plugins/cx-se-onboarding-checklist/tool/`](plugins/cx-se-onboarding-checklist/tool/cxone-onboarding-checklist.html).

## Repo layout

```
.claude-plugin/marketplace.json          # makes this repo installable as a marketplace
plugins/cx-se-onboarding-checklist/      # the plugin (drop-in for CheckmarxDev/cx-plugin-marketplace)
  .claude-plugin/plugin.json
  skills/cxone-onboarding-seeder/        # SKILL.md + references/baseline-checklist.json
  skills/cxone-onboarding-tool/          # opens the HTML tool
  tool/cxone-onboarding-checklist.html   # the tracker
  README.md, CHANGELOG.md, CODEOWNERS
scripts/check-baseline.py                # fails if the JSON drifts from the HTML's checklist data
scripts/build-claude-ai-skill.sh         # zips the seeder skill for claude.ai
contrib/marketplace-pr.patch             # ready-to-apply PR for CheckmarxDev/cx-plugin-marketplace
```

See the [plugin README](plugins/cx-se-onboarding-checklist/README.md) for the workflow, prerequisites, and the Markdown contract.

## The tool at a glance

- 11 fixed sections, from pre-kickoff readiness through migration, each with Checkmarx documentation links.
- Per-customer state. Switch between customers from **Saved checklists**.
- **Connect folder…** (Chrome/Edge): the tool reads and writes Markdown files in a folder you choose. Browser storage is only a cache.
- **Save Markdown** / **Load Markdown** for other browsers.
- Customer requirements carry a Supported / Not supported / Needs verification tag, a doc link, and a note marked Internal or Customer-facing.
- Internal notes and expected/done dates per item. Internal notes never reach the PDF.
- Hide sections or items that don't apply to a customer.
- **Export PDF** for the leave-behind.

## Maintaining

The checklist content lives in two places that must agree: the `DATA` constant in the HTML and `baseline-checklist.json` in the skill. After editing either:

```bash
python3 scripts/check-baseline.py            # report drift
python3 scripts/check-baseline.py --write    # regenerate the JSON from the HTML
```

Bump `version` in `plugin.json` and add a `CHANGELOG.md` entry with each release.

## Publishing to the internal marketplace

The `plugins/cx-se-onboarding-checklist` directory follows the layout of `CheckmarxDev/cx-plugin-marketplace`. To publish there:

1. Copy the directory into that repo's `plugins/`.
2. Add this entry to its `.claude-plugin/marketplace.json`:
   ```json
   { "name": "cx-se-onboarding-checklist",
     "description": "Seed and run a per-customer Checkmarx One onboarding checklist: Claude writes the Markdown, the bundled HTML tool tracks it.",
     "source": "./plugins/cx-se-onboarding-checklist" }
   ```
3. Add a row to its README table and a line to `.github/CODEOWNERS`.
4. Open a PR.

Or apply the prepared patch, which does steps 1 to 3 in one commit:

```bash
git -C <marketplace-clone> checkout -b add-cx-se-onboarding-checklist && git -C <marketplace-clone> am <this-repo>/contrib/marketplace-pr.patch
```

That org requires the corporate VPN, forking is disabled, and pushing a branch needs write access from the marketplace owners listed in its `.github/CODEOWNERS`.
