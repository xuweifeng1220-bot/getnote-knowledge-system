# Token-Efficient Maintenance

Use this reference on every maintainer run. Goal: **same coverage and map quality, fewer tokens in context**.

## Architecture

```text
governance log (anchor only)
→ kb_scan inventory/delta (script, compact JSON)
→ read bodies only for: new notes | P0 backlog | deepen scope
→ update map + ledger JSON
→ short maintenance report
```

Deterministic work stays in `scripts/kb_scan.py`. The model does clustering, judgment, and prose — not re-fetching unchanged notes.

## When to use which scan mode

| Situation | Mode | Read bodies? |
|---|---|---|
| Routine incremental (map already M=N) | `delta --ledger` | **Only** `new` ids (+ P0 backlog if unmapped) |
| New KB / 加深 / user asked 全量收口 | `deepen` | All notes, **tiered excerpt** (P0 800 / P2 280) |
| Re-cluster check without body change | `inventory --excerpt 180` | Metadata + short excerpt only |
| Targeted re-read after classification | `read --ids` | Listed ids only |

**Never** load a full-KB text dump (>30 notes × 900 chars) into a single model turn if `delta` shows zero new notes.

## Two-phase read protocol

1. **Phase 1 — cheap**: `inventory` or `delta` → titles, tags, p0 flag, 180-char excerpt.
2. **Phase 2 — expensive**: full `read` or longer excerpt **only** for notes that need classification, new sub-theme, or P0 processing.

Skip Phase 2 for notes already in ledger under the correct node unless user added `精读重检` or new `【金】` blocks.

## Ledger JSON (machine layer outside map body)

When a map reaches **M=N**, export ledger:

```bash
python3 scripts/kb_scan.py <topic_id> export-ledger \
  --ledger .maintainer/ledgers/<topic_id>.json \
  --nodes nodes.json
```

Store under workspace `.maintainer/ledgers/{topic_id}.json`. Map **维护区** keeps:

- `覆盖状态：全量已覆盖 M=N`
- `ledger_ref：.maintainer/ledgers/{topic_id}.json`
- **Per-node counts** (e.g. `A(17) B(8) …`) — not full id lists inline

Full note_id lists live in ledger JSON only. Incremental runs diff against ledger, not by re-parsing the map table.

## Excerpt tiers (deepen pass)

| Priority | Signal | Excerpt chars |
|---:|---|---:|
| P0 | tag `精读文章` or `【金】` in body | 800 |
| P2 | all other content notes | 280 |

P0 notes still need conclusion mapped into nodes; excerpt 800 is enough for clustering when combined with title/tags. Use full `getnote note` only when excerpt is ambiguous.

## Batching

- Do **one KB per agent stretch** when deepening; don't merge 9 KB dumps in one context.
- Within a KB deepen: if >40 notes, batch `read` in groups of 15–20 by emerging sub-theme.
- Re-scan at end: `getnote notes --all` filtered by timestamp — compare ids to processed set; don't re-read bodies.

## Maintenance report compression

Follow `token-efficient-automation` report rules:

| Status | Target length |
|---|---:|
| Incremental, no structural tasks | 150–350 words + tables |
| Partial completion / lint issues | 400–700 words |
| Full 加深 multi-KB | split per-KB reports or one summary + appendix |

**Include**: 执行口径, 七步检查表, 已完成/未完成, 待你执行任务.  
**Omit**: repeating static skill rules, full coverage id lists, unchanged map node prose, raw dump excerpts.

## Anti-patterns

- Title-only map bootstrap (quality ↓, tokens ↓ — forbidden)
- Full re-dump of 100+ note KB every weekly run when ledger delta is empty
- Pasting entire governance log or total index into context (read sections needed only)
- Duplicating all note_ids in map 维护区 **and** in chat report

## Script quick reference

```bash
# Cheap inventory
python3 scripts/kb_scan.py VnW1RRR0 inventory --format json

# Incremental: what's new since last ledger
python3 scripts/kb_scan.py VnW1RRR0 delta --ledger .maintainer/ledgers/VnW1RRR0.json

# Read only new notes
python3 scripts/kb_scan.py VnW1RRR0 read --ids NOTE_ID_SAMPLE_B --excerpt 600

# Bootstrap/deepen with tiered excerpts
python3 scripts/kb_scan.py VnW1RRR0 deepen --format text --p0-excerpt 800 --p2-excerpt 280
```

## Estimated savings (vs prior workflow)

| Step | Before | After |
|---|---|---|
| Incremental run (0 new notes) | Re-read map + optional full KB dump | delta JSON ~200 tokens |
| Incremental run (3 new notes) | Full KB dump 50k+ tokens | delta + 3× read ~3k tokens |
| Deepen 100-note KB | 100×900 char dump ~90k tokens | P0 full tier + P2 short ~35–45k tokens |
| Map maintenance zone | Inline 100+ ids in every map read | counts + ledger_ref ~500 tokens |

Quality preserved because: M=N verification uses ledger diff; P0 gets longer excerpt; judgment/clustering still model-owned.
