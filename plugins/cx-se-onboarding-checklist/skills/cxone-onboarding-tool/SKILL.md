---
name: "cxone-onboarding-tool"
description: Opens the bundled Checkmarx One onboarding checklist HTML tool, or copies it to a folder. Use when the user asks to open, find, or view the onboarding checklist tool.
---

# Open the onboarding checklist tool

The interactive checklist lives in this plugin at `${CLAUDE_PLUGIN_ROOT}/tool/cxone-onboarding-checklist.html`. It is a single self-contained HTML file; nothing to install or build.

## Open it

Run:

```bash
open "${CLAUDE_PLUGIN_ROOT}/tool/cxone-onboarding-checklist.html"
```

(On Linux use `xdg-open`; on Windows use `start`.)

Then tell the user, in one or two lines:

- Click **Connect folder…** (Chrome or Edge) and pick the folder holding their checklist Markdown files. Every file there appears under **Saved checklists**, and every change writes straight back to the file.
- On Safari or Firefox the folder API isn't available, so use **Load Markdown** and **Save Markdown** instead.

## Copy it somewhere

If the user wants the file in a shared or synced location (OneDrive, a team folder), copy it rather than editing the plugin's copy:

```bash
cp "${CLAUDE_PLUGIN_ROOT}/tool/cxone-onboarding-checklist.html" "<destination>/"
```

Point out that the copy will not update when the plugin updates, so they should re-copy after `claude plugin update`.

## Don't

- Don't edit the HTML inside the plugin directory. Changes belong in the source repo so the seeder's `baseline-checklist.json` stays in sync (the repo has a check script for that).
- Don't try to publish the HTML as a hosted page. The folder-sync feature needs the File System Access API, which sandboxed hosting blocks.
