# Changelog

## [1.0.1] — 2026-10-30

### Changed
- Shortened both skill descriptions to the marketplace's 30-word limit.
- Added `contrib/marketplace-pr.patch`, a ready-to-apply patch for CheckmarxDev/cx-plugin-marketplace.

## [1.0.0] — 2026-10-30

### Added
- Packaged the `cxone-onboarding-seeder` skill and the `cxone-onboarding-checklist.html` tool as one Claude Code plugin.
- `cxone-onboarding-tool` skill: opens the bundled HTML tool from Claude Code.
- `scripts/check-baseline.py`: fails if the skill's `baseline-checklist.json` drifts from the checklist data embedded in the HTML.
- `scripts/build-claude-ai-skill.sh`: zips the seeder skill for upload to claude.ai.

### Changed
- Seeder now writes notes in the tool's current schema (`Note (Internal)` / `Note (Customer-facing)`, `Internal Notes`) instead of the legacy `Feasibility:` form.
- Seeder documents the Confluence and SharePoint connector prerequisites and where to save the output.
- Removed personal workspace references from the skill instructions.
