#!/usr/bin/env python3
"""Fail if the seeder's baseline-checklist.json drifts from the DATA constant
embedded in cxone-onboarding-checklist.html.

The tool's Markdown parser maps every mandatory item by `item:<section>-<index>`,
so the two copies must agree on section order, item order, and item text.
Run from anywhere: python3 scripts/check-baseline.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "cx-se-onboarding-checklist"
HTML = PLUGIN / "tool" / "cxone-onboarding-checklist.html"
JSON = PLUGIN / "skills" / "cxone-onboarding-seeder" / "references" / "baseline-checklist.json"


def extract_html_data(html: str):
    m = re.search(r"const DOCS = \"([^\"]+)\";", html)
    docs = m.group(1) if m else ""
    m = re.search(r"const DATA = (\[.*?\n\]);", html, re.S)
    if not m:
        sys.exit("could not find `const DATA = [...]` in the HTML")
    src = m.group(1)
    src = src.replace('DOCS+"', '"' + docs)            # DOCS+"x" -> "https://.../x"
    src = re.sub(r"\b(title|sub|items|t|l)\s*:", r'"\1":', src)  # quote keys
    src = re.sub(r",(\s*[\]}])", r"\1", src)           # trailing commas
    return json.loads(src)


def main() -> int:
    html_data = extract_html_data(HTML.read_text(encoding="utf-8"))
    json_data = json.loads(JSON.read_text(encoding="utf-8"))
    problems = []

    if len(html_data) != len(json_data):
        problems.append(f"section count: HTML has {len(html_data)}, JSON has {len(json_data)}")

    for i, (h, j) in enumerate(zip(html_data, json_data)):
        if h["title"] != j["title"]:
            problems.append(f"section {i} title: HTML '{h['title']}' vs JSON '{j['title']}'")
        if len(h["items"]) != len(j["items"]):
            problems.append(f"section {i} item count: HTML {len(h['items'])} vs JSON {len(j['items'])}")
        for k, (hi, ji) in enumerate(zip(h["items"], j["items"])):
            if hi["t"] != ji["t"]:
                problems.append(f"item {i}-{k} text differs:\n    HTML: {hi['t']}\n    JSON: {ji['t']}")
            if hi.get("l") != ji.get("l"):
                problems.append(f"item {i}-{k} link differs:\n    HTML: {hi.get('l')}\n    JSON: {ji.get('l')}")

    if problems:
        print("baseline-checklist.json is out of sync with the HTML tool:")
        for p in problems:
            print("  - " + p)
        print("\nFix: regenerate the JSON with  python3 scripts/check-baseline.py --write")
        return 1

    total = sum(len(s["items"]) for s in json_data)
    print(f"OK: {len(json_data)} sections, {total} mandatory items match between HTML and JSON")
    return 0


if __name__ == "__main__":
    if "--write" in sys.argv:
        data = extract_html_data(HTML.read_text(encoding="utf-8"))
        JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {JSON.relative_to(ROOT)} from the HTML DATA constant")
        sys.exit(0)
    sys.exit(main())
