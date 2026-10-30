---
name: "cxone-onboarding-seeder"
description: Seeds a per-customer Checkmarx One onboarding checklist Markdown from raw customer requirements, feasibility-checked against Confluence, SharePoint, and docs. Use for 'seed the checklist for [customer]' or POV onboarding asks.
---

# Checkmarx One Onboarding Seeder

Turns a customer's raw requirements into a ready-to-load Markdown file for the `cxone-onboarding-checklist.html` tool (the interactive onboarding checklist that ships in this plugin under `tool/`). The output is a single `.md` file that the user either drops into the folder the tool is connected to, or loads via the tool's **Load Markdown** button.

This is a **one-time seeding step**, meant to run once per customer at or just before kickoff. It is not meant to be re-run later to merge in new requirements — if the user wants to add more requirements after the fact, that's what the tool's own **+ Add customer requirement** button (inside each section) is for. If a seed file for this customer already exists (you find `<customer-slug>.md` in the target folder, or the user mentions or shares one), ask whether they want to overwrite it before proceeding — don't silently merge.

## Prerequisites

- **Research sources.** Feasibility checks (Step 3) search Confluence and SharePoint first. In Claude Code that means the Atlassian and Microsoft 365 connectors are configured; in claude.ai it means those connectors are enabled for the conversation. If neither is available, say so up front and research from docs.checkmarx.com and checkmarx.com only — and expect more items to land in `unknown`.
- **A place to write the file.** See Step 5. Ask once if it isn't obvious.

## What you need before starting

1. **The customer name.** If not given, ask.
2. **The raw requirements.** Pasted text, a transcript excerpt, an RFP/discovery doc, or a verbal list the user types out. Take whatever form it comes in — don't make the user reformat it first.

If either is missing, ask for it rather than guessing — a seed file with the wrong customer name or missing requirements undermines the whole point (showing the customer exactly what was done for them).

## Step 1: Read the baseline structure

Read `references/baseline-checklist.json`, which sits next to this SKILL.md. It's the exact same 11-section array (`title`, `sub`, `items[].t`, `items[].l`) baked into the tool's `DATA` constant — sections `0` through `10`:

0. Pre-kickoff readiness
1. Tenant & account fundamentals
2. Identity & access management
3. Applications & project structure
4. Scanner configuration
5. Code repository integration & baseline scan
6. CI/CD pipeline integration
7. Policy, break-build gates & notifications
8. IDE plugins / Developer Assist rollout
9. Reporting & executive visibility
10. Migration (if replacing legacy CxSAST)

These section indices (`0`–`10`) are what you'll place each customer requirement under. Do not invent new sections, rename these, or change their order — the tool's rendering and progress math depend on these exact 11 sections existing with these exact indices.

## Step 2: Extract and map each requirement

Read through the customer's raw requirements and pull out each distinct, actionable ask. A few things worth knowing:

- **Granularity**: split compound asks into separate items when they'd plausibly be checked off independently (e.g. "needs SSO via Okta and wants break-build off for the pilot repo" → two items, one for section 2, one for section 7). Don't split a single coherent ask into fragments just to pad the count.
- **Mapping logic**: match the requirement's topic to the closest-fitting section by what it's actually about, not by keyword-matching alone. "Needs GitHub Enterprise Server on-prem" → section 5 (repo integration), even though it also touches firewall/network concerns that section 0 covers generically — the specific repo ask belongs with repo integration.
- **Ambiguous or cross-cutting asks**: if something genuinely could fit two sections, pick the one where the work actually gets done (e.g., "wants IaC scanning enabled" is a scanner-config ask → section 4, not section 1, even though it's configured at the tenant level).
- **Non-actionable items**: if the customer notes are more like context/background than an actionable requirement ("they're migrating off GitLab self-hosted next year"), don't manufacture a checklist item for it — mention it to the user in your reply instead, so they can decide whether and where it belongs.
- **Truly unplaceable items**: if something doesn't fit any of the 11 sections at all (rare — most account/platform asks do fit somewhere), say so explicitly in your reply rather than forcing it into the nearest section. Let the user decide.

Keep each item's wording as a clear, concise, checkable action — written in the same register as the tool's existing mandatory items (e.g. "Configure SAML SSO via Okta for all CxOne users" rather than a verbatim quote from notes).

## Step 3: Confirm feasibility for every requirement

This is the part that gives the checklist its proof-of-value: don't just place the requirement, verify whether Checkmarx One can actually do it. For each requirement you mapped in Step 2:

1. **Search for it.** Check Confluence and SharePoint first (product capability docs, competitive positioning pages, feature matrices — many of these questions have already been answered for past deals). Fall back to public documentation at docs.checkmarx.com and checkmarx.com for anything not covered internally. Use whatever search tools are available in this conversation; don't answer from general knowledge of the product when Checkmarx One is involved.
2. **Classify each requirement as one of:**
   - **`yes`** — confirmed supported. You found a clear doc or page describing the capability as it's being asked about.
   - **`no`** — confirmed *not* supported, deprecated, or explicitly out of scope for Checkmarx One. State plainly why, and link documentation if any exists that confirms the gap (a doc saying what *is* supported instead is fine evidence here, even if it doesn't explicitly say "this isn't supported").
   - **`unknown`** — you searched and couldn't find a clear answer either way. Don't force this to `yes` or `no` just to avoid the ambiguous bucket — a wrong "yes" is worse than an honest "needs verification," since this file becomes a customer-facing record of what was promised.
3. **Write a short note for every item that isn't a clean, unqualified `yes`** (and feel free to add one for `yes` items too if there's a useful caveat, like a minimum plan tier or version requirement). The note is prose only — explain what you found or didn't, and for `no` items suggest the closest alternative if one exists (e.g. "Not supported as a native feature; the equivalent workflow is X"). **Do not put the URL inside this prose note.** The tool has a separate structured field for the documentation link (see Step 4) and renders it as its own clickable line with a clean hostname label — a URL buried in the note text either won't render as a link at all, or renders ugly and redundant next to the real link field.
4. **Decide the note's audience.** Every note is either **Internal** (default; shown only inside the tool, never in the PDF leave-behind) or **Customer-facing** (included in the PDF). Seeded notes are almost always Internal, because they record what you found while verifying — pricing tiers, early-access programs, things to confirm with product. Only mark a note Customer-facing when it's wording you'd be comfortable handing to the customer as-is.
5. **Whenever you have a supporting or refuting documentation link, capture it as a full URL** (always starting with `https://` — never a bare domain like `docs.checkmarx.com/...`) to go in the structured link field.
6. If you genuinely cannot research something (no indexed source at all, and the topic isn't public-facing), mark it `unknown` and say so in your reply rather than silently leaving it unexamined — the whole point is that nothing meant to represent "yes, we can do this" goes out without a check.

## Step 4: Generate the Markdown

Each customer-requirement item needs a short unique id (4–8 lowercase alphanumeric characters, e.g. `a1b2c3`) — generate these yourself, make sure none collide within the file.

Follow this exact schema. The tool's parser is regex-based and depends on this structure precisely:

```
---
customer: <Customer Name>
updated: <ISO 8601 timestamp, e.g. 2026-10-02T00:00:00.000Z>
tool: cxone-onboarding-checklist
---

# Checkmarx One Onboarding — <Customer Name>

## 0. Pre-kickoff readiness

- [ ] Confirm license / entitlement scope matches what's being piloted or demoed (which scanners, how many repos/apps) <!-- item:0-0 -->
- [ ] Confirm firewall / IP allowlist requirements, especially for self-hosted SCM, on-prem tools, or locked-down networks <!-- item:0-1 -->
- [ ] If repos are self-hosted or not internet-accessible, confirm whether IP-based repo configuration is needed instead of hostname resolution <!-- item:0-2 -->
- [ ] Identify who owns each access decision on the customer's side (SSO/IAM admin, repo admin, security lead) so the kickoff isn't stalled waiting on the right person <!-- item:0-3 -->

## 1. Tenant & account fundamentals

- [ ] Complete initial admin login <!-- item:1-0 -->
- [ ] Review global account settings (scanner defaults, AI Assist, domain management) <!-- item:1-1 -->
- [ ] <a customer requirement mapped here, if any> <!-- item:custom-a1b2c3 feasible:yes link:https://docs.checkmarx.com/en/34965-xxxxx-example.html -->
  > **Note (Internal):** Supported natively on [plan tier] — confirm the customer's entitlement includes it before kickoff.

[... continue through section 10 ...]
```

Rules that matter:

- **Every mandatory item from `baseline-checklist.json` must appear, in order, under its section**, each tagged `<!-- item:i-j -->` where `i` is the section index and `j` is the item's position within that section's `items` array (both 0-indexed) — exactly matching the JSON. These always start unchecked (`[ ]`) for a fresh seed. Do not add doc links inline in the Markdown text itself — the tool supplies those separately; just reproduce the item's `t` text verbatim. Mandatory items don't carry `feasible`/`link` tags — they're the platform's own setup steps, not asks to verify.
- **Customer-requirement items go after the mandatory items in their section**, each tagged `<!-- item:custom-<id> feasible:<yes|no|unknown> -->` (the literal `custom-` prefix is how the parser tells the two kinds apart; the `feasible:` token carries your Step 3 verdict). These also start unchecked.
- **When you have a documentation link, append a `link:` token to the same comment**: `<!-- item:custom-<id> feasible:<status> link:<full https:// URL> -->`. Always the complete URL with scheme — never a bare domain like `docs.checkmarx.com/...`. This is a separate structured field from the prose note below, and the tool renders it as its own clickable line with a clean hostname label — don't also repeat the URL inside the prose note.
- **Immediately below any customer-requirement line that has a note**, add one line: `  > **Note (Internal):** <your prose note, no URL in it>` — or `  > **Note (Customer-facing):** ...` if you decided in Step 3 that it's safe to show the customer. Two leading spaces, then the blockquote marker. This must be the line directly after the item (no blank line between), or the tool's parser won't associate it with the right item. Only add this line when you have something worth saying — a clean `yes` with nothing noteworthy doesn't need one. A `link:` with no accompanying note is fine; let the link stand on its own.
- **Multi-line notes** continue on following lines as `  > <more text>` (two spaces, blockquote marker), directly under the first note line.
- **Don't emit the tool's other tokens.** The tool itself also writes `expected:YYYY-MM-DD` / `done:YYYY-MM-DD` date tokens, `hidden:true` markers, `> **Internal Notes:**` blocks, and section-level `> **Notes (Internal):**` blocks as the user works the checklist. A fresh seed has none of those — leave them out. (If you ever load an older file that uses `> **Feasibility:**`, the tool still reads it and treats it as an Internal note, but don't write that legacy form.)
- **Sections with no mapped customer requirements** just contain their mandatory items and nothing else — don't force an empty customer-requirement line.
- **Every one of the 11 sections must be present** as a `## N. Title` heading, even if nothing customer-specific landed there, so the tool can render the full sequence.
- Use the exact section titles from the JSON (`## 0. Pre-kickoff readiness`, etc.) — the heading number is what the parser reads to know which section it's in.
- Leave a blank line between sections for readability; it doesn't affect parsing either way (but don't put a blank line between a custom item and its note — see above).

## Step 5: Deliver it

1. Name the file `<customer-slug>.md` where the slug is the customer name lowercased, non-alphanumeric runs collapsed to single hyphens, no leading/trailing hyphens (e.g. "Thundercrest Fizzwidget Corp" → `thundercrest-fizzwidget-corp.md`). This must match exactly what the tool itself would generate from that customer name, since the tool's own save/load logic keys off the same slug function.
2. **Where to write it:**
   - **Claude Code:** if the current working directory (or a folder the user named) already holds checklist files — Markdown files whose frontmatter contains `tool: cxone-onboarding-checklist` — write there; that's the folder the tool is connected to. Otherwise ask the user once for their checklist folder. Check for an existing `<customer-slug>.md` before writing and confirm before overwriting.
   - **claude.ai:** produce the file as a downloadable attachment.
3. In your reply, tell the user plainly:
   - How many customer-requirement items you placed, and in which sections (a quick list — section name → count is enough, not a full re-print of every item).
   - **The feasibility breakdown**: how many came back Supported, how many Not supported, how many Needs verification — and call out the Not-supported and Needs-verification ones by name, since those are the ones the user will want to address with the customer directly rather than discover later.
   - Anything you deliberately left out (non-actionable context, or genuinely unplaceable asks) and why.
   - That the tool picks the file up automatically if it's in the connected folder (the file appears under **Saved checklists**), or they can load it directly with **Load Markdown**.

Don't silently drop requirements you weren't confident about placing — flag them and let the user redirect you rather than guessing wrong on something that'll be shown back to the customer as proof of what was addressed. The same goes double for feasibility: an unverified "yes" is the one mistake this skill exists to prevent.
