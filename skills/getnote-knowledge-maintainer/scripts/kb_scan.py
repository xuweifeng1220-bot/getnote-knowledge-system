#!/usr/bin/env python3
"""Token-efficient KB scanner for getnote-knowledge-maintainer.

Modes (pick one):
  inventory   — note_id, title, tags, excerpt (cheap; clustering / delta prep)
  delta       — compare KB vs ledger JSON; output new/removed ids only
  read        — full excerpt for specific note_ids (stdin or --ids)
  deepen      — bootstrap/deepen: all notes with tiered excerpt (P0 longer)
  export-ledger — write ledger JSON from --nodes file or stdin JSON

Examples:
  kb_scan.py VnW1RRR0 inventory
  kb_scan.py VnW1RRR0 delta --ledger .maintainer/ledgers/VnW1RRR0.json
  kb_scan.py VnW1RRR0 read --ids NOTE_ID_SAMPLE_B,NOTE_ID_SAMPLE_A --excerpt 600
  kb_scan.py VnW1RRR0 deepen --p0-excerpt 800 --p2-excerpt 280
  kb_scan.py VnW1RRR0 export-ledger --ledger .maintainer/ledgers/VnW1RRR0.json --nodes nodes.json

Output: compact JSON on stdout (except deepen/inventory text when --format text).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

P0_TAG = "精读文章"
GOLD_MARK = "【金】"
MAP_PREFIX = "知识库认知地图"


def run_getnote(*args: str) -> dict[str, Any]:
    r = subprocess.run(["getnote", *args, "-o", "json"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or "getnote failed")
    return json.loads(r.stdout)


def list_kb_notes(topic_id: str) -> list[dict[str, Any]]:
    data = run_getnote("kb", topic_id, "--all")
    return data["data"]["notes"]


def fetch_note(nid: str) -> dict[str, Any]:
    data = run_getnote("note", str(nid))
    return data["data"]["note"]


def tag_names(tags: Any) -> list[str]:
    if not tags:
        return []
    if isinstance(tags, str):
        return [tags]
    if isinstance(tags, list):
        out = []
        for t in tags:
            if isinstance(t, dict):
                out.append(str(t.get("name", "")))
            else:
                out.append(str(t))
        return [x for x in out if x]
    return []


def is_p0(tags: list[str], content: str) -> bool:
    if P0_TAG in tags:
        return True
    if GOLD_MARK in (content or ""):
        return True
    if "【发现点】" in (content or ""):
        return True
    return False


def is_map_note(title: str) -> bool:
    return (title or "").startswith(MAP_PREFIX)


def excerpt(content: str, n: int) -> str:
    c = (content or "").strip().replace("\r\n", "\n")
    if len(c) <= n:
        return c
    return c[:n] + "…"


def cmd_inventory(topic_id: str, excerpt_len: int, fmt: str) -> None:
    notes = list_kb_notes(topic_id)
    rows = []
    for n in notes:
        nid = str(n["note_id"])
        title = n.get("title") or ""
        if is_map_note(title):
            rows.append({"id": nid, "title": title, "kind": "map", "skip": True})
            continue
        note = fetch_note(nid)
        content = note.get("content") or ""
        tags = tag_names(note.get("tags") or note.get("tag"))
        rows.append(
            {
                "id": nid,
                "title": title,
                "tags": tags,
                "p0": is_p0(tags, content),
                "excerpt": excerpt(content, excerpt_len),
                "chars": len(content),
            }
        )
    content_notes = [r for r in rows if not r.get("skip")]
    payload = {
        "topic_id": topic_id,
        "total": len(rows),
        "content_n": len(content_notes),
        "notes": rows,
    }
    if fmt == "text":
        print(f"TOTAL={len(rows)} CONTENT_N={len(content_notes)}")
        for r in rows:
            print(f"==== {r['id']} | {r['title']}")
            if r.get("skip"):
                print("  <MAP>")
                continue
            if r.get("tags"):
                print("  TAGS:", ",".join(r["tags"][:8]))
            if r.get("p0"):
                print("  P0: yes")
            print(r.get("excerpt", ""))
            print()
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def load_ledger(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def all_ledger_ids(ledger: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for ids_list in (ledger.get("nodes") or {}).values():
        for i in ids_list:
            ids.add(str(i))
    for item in ledger.get("ignored") or []:
        if isinstance(item, dict):
            ids.add(str(item.get("id", "")))
        else:
            ids.add(str(item))
    ids.discard("")
    return ids


def cmd_delta(topic_id: str, ledger_path: Path, fmt: str) -> None:
    ledger = load_ledger(ledger_path)
    notes = list_kb_notes(topic_id)
    current = {
        str(n["note_id"])
        for n in notes
        if not is_map_note(n.get("title") or "")
    }
    known = all_ledger_ids(ledger)
    new_ids = sorted(current - known)
    removed_ids = sorted(known - current)
    payload = {
        "topic_id": topic_id,
        "ledger": str(ledger_path),
        "ledger_N": ledger.get("N"),
        "current_n": len(current),
        "new": new_ids,
        "removed": removed_ids,
        "unchanged_n": len(current & known),
        "needs_full_read": new_ids,
    }
    if fmt == "text":
        print(f"CURRENT_N={len(current)} NEW={len(new_ids)} REMOVED={len(removed_ids)}")
        for nid in new_ids:
            print(f"  + {nid}")
        for nid in removed_ids:
            print(f"  - {nid}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_read(topic_id: str, ids: list[str], excerpt_len: int, fmt: str) -> None:
    rows = []
    for nid in ids:
        note = fetch_note(nid)
        content = note.get("content") or ""
        tags = tag_names(note.get("tags") or note.get("tag"))
        rows.append(
            {
                "id": nid,
                "title": note.get("title") or "",
                "tags": tags,
                "p0": is_p0(tags, content),
                "excerpt": excerpt(content, excerpt_len),
                "chars": len(content),
            }
        )
    payload = {"topic_id": topic_id, "read_n": len(rows), "notes": rows}
    if fmt == "text":
        for r in rows:
            print(f"==== {r['id']} | {r['title']}")
            if r["tags"]:
                print("  TAGS:", ",".join(r["tags"][:8]))
            print(r["excerpt"])
            print()
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_deepen(topic_id: str, p0_excerpt: int, p2_excerpt: int, fmt: str) -> None:
    notes = list_kb_notes(topic_id)
    rows = []
    for n in notes:
        nid = str(n["note_id"])
        title = n.get("title") or ""
        if is_map_note(title):
            continue
        note = fetch_note(nid)
        content = note.get("content") or ""
        tags = tag_names(note.get("tags") or note.get("tag"))
        p0 = is_p0(tags, content)
        lim = p0_excerpt if p0 else p2_excerpt
        rows.append(
            {
                "id": nid,
                "title": title,
                "tags": tags,
                "p0": p0,
                "excerpt": excerpt(content, lim),
                "chars": len(content),
            }
        )
    payload = {
        "topic_id": topic_id,
        "mode": "deepen",
        "content_n": len(rows),
        "p0_n": sum(1 for r in rows if r["p0"]),
        "notes": rows,
    }
    if fmt == "text":
        print(f"TOTAL_CONTENT={len(rows)} P0={payload['p0_n']}")
        for r in rows:
            print(f"==== {r['id']} | {r['title']}")
            if r["tags"]:
                print("  TAGS:", ",".join(r["tags"][:8]))
            if r["p0"]:
                print("  P0: yes")
            print(r["excerpt"])
            print()
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_export_ledger(
    topic_id: str,
    ledger_path: Path,
    nodes_path: Path | None,
    kb_name: str,
    map_note_id: str,
) -> None:
    if nodes_path:
        nodes_data = json.loads(nodes_path.read_text(encoding="utf-8"))
    else:
        nodes_data = json.load(sys.stdin)
    notes = list_kb_notes(topic_id)
    content_ids = [
        str(n["note_id"])
        for n in notes
        if not is_map_note(n.get("title") or "")
    ]
    mapped: set[str] = set()
    for ids in nodes_data.get("nodes", {}).values():
        for i in ids:
            mapped.add(str(i))
    for item in nodes_data.get("ignored") or []:
        mapped.add(str(item.get("id") if isinstance(item, dict) else item))
    mapped.discard("")
    ledger = {
        "topic_id": topic_id,
        "kb_name": kb_name or nodes_data.get("kb_name", ""),
        "map_note_id": map_note_id or nodes_data.get("map_note_id", ""),
        "last_maintained": nodes_data.get("last_maintained", ""),
        "N": len(content_ids),
        "M": len(mapped & set(content_ids)),
        "nodes": nodes_data.get("nodes", {}),
        "ignored": nodes_data.get("ignored", []),
        "unmapped": sorted(set(content_ids) - mapped),
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"written": str(ledger_path), "N": ledger["N"], "M": ledger["M"], "unmapped_n": len(ledger["unmapped"])}, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description="Token-efficient KB scanner for maintainer")
    p.add_argument("topic_id")
    p.add_argument(
        "mode",
        choices=["inventory", "delta", "read", "deepen", "export-ledger"],
    )
    p.add_argument("--ledger", type=Path, help="Ledger JSON path")
    p.add_argument("--ids", help="Comma-separated note_ids for read mode")
    p.add_argument("--excerpt", type=int, default=180, help="inventory/read default excerpt")
    p.add_argument("--p0-excerpt", type=int, default=800)
    p.add_argument("--p2-excerpt", type=int, default=280)
    p.add_argument("--format", choices=["json", "text"], default="json")
    p.add_argument("--nodes", type=Path, help="nodes JSON for export-ledger")
    p.add_argument("--kb-name", default="")
    p.add_argument("--map-note-id", default="")
    args = p.parse_args()

    if args.mode == "inventory":
        cmd_inventory(args.topic_id, args.excerpt, args.format)
    elif args.mode == "delta":
        if not args.ledger:
            sys.exit("--ledger required for delta")
        cmd_delta(args.topic_id, args.ledger, args.format)
    elif args.mode == "read":
        if not args.ids:
            sys.exit("--ids required for read")
        cmd_read(args.topic_id, [x.strip() for x in args.ids.split(",") if x.strip()], args.excerpt, args.format)
    elif args.mode == "deepen":
        cmd_deepen(args.topic_id, args.p0_excerpt, args.p2_excerpt, args.format)
    elif args.mode == "export-ledger":
        if not args.ledger:
            sys.exit("--ledger required for export-ledger")
        cmd_export_ledger(args.topic_id, args.ledger, args.nodes, args.kb_name, args.map_note_id)


if __name__ == "__main__":
    main()
