---
name: getnote-knowledge-sprouter
description: Generate cross-knowledge "sprouts" from the user's Get笔记 knowledge bases and framework notes, producing new insights, questions, product ideas, and business opportunities in one continuously maintained sprout log. Use when the user asks to 发芽, 跨库关联, 关系生成, 新机会, 新想法, 定期外脑更新 after maintainer, or sprout from Get笔记 content; do not use for ordinary analysis, capture, or maintenance.
---

# Getnote Knowledge Sprouter

## Overview

Use this skill to generate new ideas from relationships across the user's Get笔记 knowledge system. This skill is not for answering one question or filing notes. It periodically connects KB cognition maps, cross-library frameworks, knowledge bases, evidence notes, AI回流 notes, and observation pools to produce new cognition, product ideas, commercial opportunities, and research questions.

Use `getnote-knowledge-maintainer` before this skill in periodic automation. Use `getnote-knowledge-analyzer` to deep-dive a sprout. Use `getnote-knowledge-capturer` to capture a matured sprout as a standalone note.

## Skill Collaboration

| Skill | Role |
|---|---|
| `getnote-knowledge-maintainer` | Owns KB maps, cross-library frameworks, governance log |
| `getnote-knowledge-analyzer` | Deep-dives individual sprouts with argumentative analysis |
| `getnote-knowledge-sprouter` | Cross-library sprouting; reads KB maps as primary collision surface |
| `getnote-knowledge-capturer` | Captures matured sprouts as standalone notes |

## Core Boundary

This skill may:

- Read the total index, KB cognition maps, cross-library framework notes, governance log, sprout log, and representative notes from knowledge bases.
- Generate cross-knowledge relationships.
- Identify high-connectivity nodes.
- Produce dual-track sprout cards: commercial/product-value sprouts and cognition/knowledge-collision sprouts.
- Interrogate and filter new and existing sprouts through a strict two-round review process.
- Mark whether P0/P1 sprouts may become framework-upgrade candidates for later maintainer review.
- Update the single sprout log note.
- Mark this round's additions and adjustments inline.
- Recommend analyzer/capturer/maintainer follow-up actions.

This skill must not:

- Replace maintainer's classification, KB map governance, or framework governance.
- Update framework notes directly unless the user explicitly asks for system-note synchronization.
- Capture arbitrary AI conversation outputs; use `getnote-knowledge-capturer`.
- Create many new notes by default.
- Scan local files or run Graphify by default.

## Required Confirmation

Before any write operation, present a short execution plan and expected impact, then wait for explicit user approval. Writes include `getnote save`, `getnote note update`, and `getnote kb add`.

## Single Sprout Log Rule

Default target note:

- `个人知识发芽日志｜跨库关联与新机会`

This is the single canonical sprout log. Each sprouting run updates this same note.

Create additional notes only when the user explicitly confirms that a mature sprout should become a standalone product, project, framework, or research note.

## Periodic Order

When the user asks for a periodic external-brain update:

```text
1. Run getnote-knowledge-maintainer first
2. Then run getnote-knowledge-sprouter
3. Report maintenance changes + new sprouts together
```

Reason: sprouts should build on the latest classified notes, updated frameworks, and refreshed observation pools.

## Routing Hierarchy

KB cognition maps and cross-library frameworks remain the primary sprouting surface. `文章精读与金句索引` is only a high-signal supplementary source.

```text
1. 发芽日志 → 看既有机会与验证状态
2. 总索引 → 发现库级认知地图路由、跨库框架体系、观察池
3. 库级认知地图 + 跨库任务框架 → 主碰撞面（优先于原始笔记采样）
4. 知识库代表笔记 → 补充地图未覆盖的素材
5. 治理日志 → 仅维护元数据（registry、lint、观察池），不读全文
6. 精读/金句索引 → 补充用户高关注素材
7. 生成发芽卡片
```

## 人读层与机器层分层

**人读层（发芽卡片正文）**

- `一句话价值`、`核心判断`、`为什么现在重要`、`关联逻辑` 用自然语言写，像机会简报而不是表单
- `使用方式` 写具体场景，不要只列空 bullet
- 卡片主体不出现 `拷问结果` 字段清单作为正文结构

**机器层（卡片末尾维护区）**

- `证据强度`、`证据缺口`、`验证问题`、`放弃条件`、`下一次复查`、`框架升级状态`
- `拷问结果` 全文
- `来源索引` 完整链接表
- 收纳在每张卡片底部的 `### 维护区` 下，或发芽日志 note 最末的 `## 维护区` 汇总

**聊天汇报**

- 先说本轮最值得看的 1-3 个发芽（人话）
- 再给 P0/P1 列表和统计

## Sprouting Workflow

1. Read the sprout log note.
2. Remove or downgrade previous `【本轮新增】` / `【本轮调整】` markers.
3. Read the total index; extract `库级认知地图路由` and cross-library framework list.
4. Read relevant `知识库认知地图｜【库名】` notes and core cross-library framework notes.
5. Sample representative knowledge-base notes only when KB maps do not cover a theme.
6. Read governance log only for maintenance metadata: observation pools, framework-upgrade candidates, lint pointers. Do not read the full governance log for精读/洞察 bodies.
7. **Supplement only**: read `文章精读与金句索引｜用户高关注认知` for user-curated deep-read judgments and golden-quote insights.
8. Extract:
   - high-connectivity themes across KB maps and frameworks
   - cross-domain pairings (especially KB map nodes that have not yet been promoted to cross-library frameworks)
   - repeated unresolved questions
   - commercializable methods
   - reusable workflows or skill candidates
   - investment/product/career implications
   - user deep-read article judgments and golden-quote insights from the supplementary reading index
9. Generate candidate sprouts in two tracks:
   - **Commercial/product-value track**: products, service packages, business models, customer scenarios, automation opportunities, monetizable assets.
   - **Cognition/knowledge-collision track**: thinking models, analysis frameworks, trend hypotheses, investment observation themes, career/life decision insights, framework corrections.
10. Attach source indexes to every candidate sprout: specific KB map cognition, specific note/article, specific framework node, prior sprout, or user-curated deep-read / golden-quote entry when relevant.
11. Run the first-round Interrogator review against all new candidates and selected existing sprouts.
12. Promote first-round pass items into the formal board.
13. Send failed-but-promising items into reconstruction: sharpen the core judgment, source path, value, use case, evidence gap, and validation action.
14. Run the second-round Interrogator review on reconstructed items.
15. Promote second-round pass items into the formal board; move remaining items to candidate pool or dropped area.
16. Add evidence strength, evidence gaps, abandonment conditions, and next review date to P0/P1 cards (in card maintenance zone).
17. For P0/P1 cards, set `框架升级状态` (in card maintenance zone).
18. Mark only this round's new or adjusted content.
19. Update the single sprout log (human-readable card bodies + maintenance zones).

## Dual-Track Sprouting

Each sprout must belong to one primary track.

### Commercial / Product-Value Track

Use this track when the sprout could become a product, solution, service package, workflow, monetizable knowledge asset, or business opportunity.

Each sprout must answer:

- Who has the problem?
- What painful or costly problem does it solve?
- Why might it be valid now?
- What user/customer scenario would test it?
- What is the lowest-cost validation action?
- What condition would make it not worth pursuing?

### Cognition / Knowledge-Collision Track

Use this track when the sprout creates a new thinking model, analysis framework, investment/trend hypothesis, decision lens, or correction to an existing framework.

Each sprout must answer:

- What does it change about how the user understands a topic?
- Which old cognition does it combine, challenge, or refine?
- What new question or framework does it create?
- What analysis, investment, career, or life decision could use it?
- What evidence or future observation would strengthen or falsify it?

## Source Index Rules

Every sprout must include a `来源索引` section.

- Cite concrete Get笔记 notes with full title and `note_id` whenever available.
- Cite concrete framework notes with full title, `note_id`, and the relevant node or cognition point.
- Cite specific articles or external sources with original title and link when used.
- Cite prior sprouts when a new sprout extends or challenges them.
- Do not invent note IDs, titles, links, or framework nodes.
- If concrete sources are missing, write `来源不足` and keep the sprout in candidate pool unless the user explicitly asks to explore it.

Source index examples:

```markdown
### 来源索引
- **库级地图**：[知识库认知地图｜【库名】](getnote://note_id)｜节点：...
- **知识库认知**：[完整笔记标题](getnote://note_id)｜相关认知：...
- **具体文章**：[完整文章标题](getnote://note_id)
- **框架节点**：[AI解决方案专家框架](getnote://NOTE_ID_AI_FRAMEWORK)｜节点：...
- **历史萌芽**：[个人知识发芽日志｜跨库关联与新机会](getnote://NOTE_ID_SPROUT_LOG)｜发芽 003：...
```

## Value Gate

Do not put low-value sprouts into the formal board.

A formal sprout must satisfy at least two of these conditions:

- Has a clear new judgment, not just a summary.
- Connects two or more concrete sources.
- Can guide an action, analysis, decision, or validation.
- Creates product, commercial, investment, cognitive, or framework value.
- States an evidence gap, risk, or falsification condition.
- Is not merely a restatement of an existing framework.

Items that do not pass the value gate go to `候选萌芽池` or `淘汰区`, with the reason stated.

## Framework Upgrade Signal

Sprouter does not create framework notes. It only marks whether a sprout may deserve later framework-upgrade review by `getnote-knowledge-maintainer`.

Use this field on every formal P0/P1 sprout:

```markdown
**框架升级状态**：观察中 / 候选 / 建议新建 / 已进入框架 / 暂不升级
```

Rules:

- **观察中**: promising theme, but evidence or use case is still thin.
- **候选**: connects multiple concrete sources and appears likely to require a dedicated frame if it continues.
- **建议新建**: has 10+ evidence notes, a real product/commercial/investment/decision scenario, or has appeared in P0/P1 across 2 consecutive sprout rounds.
- **已进入框架**: maintainer has already absorbed it into an existing framework.
- **暂不升级**: useful sprout, but not broad or durable enough to become a framework.

If a sprout is P0/P1 and the same theme has already appeared in prior P0/P1 rounds, explicitly mention this in `框架升级状态` or `验证问题` so maintainer can list it under `框架升级候选`.

Candidate examples for validating the rule, not hard-coded framework notes:

- `AI智能体定制与解决方案产品化框架`
- `AI算力产业链投资框架`
- `个人外脑与知识系统产品化框架`

## Interrogator Agent

The Interrogator is a strict internal reviewer for both new and existing sprouts. It should be harsh, objective, and skeptical.

It asks:

- **Creativity**: Is this more than a repackaging of existing notes? Does it create a new combination, lens, or question?
- **Value**: Can this change judgment, action, analysis, investment attention, or framework structure?
- **Commerciality**: If it is commercial/product-oriented, does it have a clear customer, pain, delivery form, validation path, and abandonment condition?
- **Source quality**: Are sources concrete, traceable, and sufficient for the claimed strength?
- **Usefulness**: Would the user actually use this in decisions, products, investing, or cognition?

### Two-Round Review

1. **First interrogation**
   - Pass: move to formal sprout board.
   - Fail but promising: reconstruct once.
   - Fail and weak: move to dropped area.

2. **Reconstruction**
   - Clarify the core judgment.
   - Strengthen the source index.
   - Make the value/use case more concrete.
   - Add evidence gap, validation action, and abandonment condition.

3. **Second interrogation**
   - Pass: move to formal sprout board.
   - Still incomplete but worth watching: move to candidate pool.
   - Still weak: move to dropped area.

### Interrogator Fields

Every formal or candidate sprout must include:

```markdown
### 拷问结果
- 第一次拷问：通过 / 重构后再审 / 淘汰
- 主要问题：
- 重构方向：
- 第二次拷问：通过 / 候选 / 淘汰 / 不适用
- 最终状态：正式萌芽 / 候选萌芽 / 淘汰
```

## Priority and Ordering

The sprout log is an opportunity board, not a chronological report. Put the most useful cards first.

Default order:

```text
本轮必看
→ P0 cards
→ P1 cards
→ P2 cards
→ P3 cards
→ relationship graph
→ high-connectivity nodes
→ suggested questions
→ archive / mature / dropped
→ version log
```

Priority definitions:

- **P0**: worth analyzing immediately; could become a product, project, or major decision.
- **P1**: worth validating soon; has clear evidence links and plausible output.
- **P2**: observe and enrich; promising but evidence is still thin.
- **P3**: parking lot; keep for later, do not actively pursue.

Within the same priority, put this round's `【本轮新增】` and `【本轮调整】` cards before older unchanged cards.

## Graphify-Inspired Presentation

Borrow Graphify's knowledge-graph logic, but express it in readable Get笔记 markdown:

- **Relationship graph**: show concept nodes and generated opportunities.
- **High-connectivity nodes**: identify concepts linking multiple knowledge bases.
- **Sprout cards**: one card per new idea/opportunity.
- **Suggested questions**: provide next questions for analyzer deep dives.
- **Evidence path**: point to frameworks or notes that support the sprout.

Do not require Graphify or local files in the MVP. Later, if the user provides Graphify outputs (`GRAPH_REPORT.md`, `graph.json`, `graph.html`) or a local folder, read them only after a plan and explicit approval.

## Sprout Log Format

Use this canonical structure. Card **bodies** are human-readable; machine fields go in `### 维护区` at the bottom of each card.

~~~markdown
# 个人知识发芽日志｜跨库关联与新机会

## 本轮必看

用 2-4 句说明本轮最值得关注的发芽，不要只列编号。

- P0：（一句话）
- P1：（一句话）

## 发芽卡片看板

### P0｜发芽 001｜标题【本轮新增/本轮调整】

**轨道**：商业化/产品价值 / 认知/知识碰撞

**一句话价值**：（人话，这张卡片值得看的理由）

**核心判断**：（新观点是什么，2-4 句）

**为什么现在重要**：（时机、变化、缺口）

**关联逻辑**：（哪些库级地图/框架/笔记碰撞出了这个想法，用叙述写）

**使用方式**
- 商业化/产品：……
- 分析/认知：……
- 投资/趋势：……

**可能产物**：……

### 维护区
- **证据强度**：强 / 中 / 弱 / 待验证
- **证据缺口**：……
- **验证问题**：……
- **放弃条件**：……
- **下一次复查**：YYYY-MM-DD
- **下一步动作**：……
- **框架升级状态**：观察中 / 候选 / 建议新建 / 已进入框架 / 暂不升级
- **状态**：观察中 / 待验证 / 已进入框架 / 已转项目 / 已放弃

**来源索引**
- **库级地图**：……
- **知识库认知**：……
- **框架节点**：……

**拷问结果**
- 第一次拷问：通过 / 重构后再审 / 淘汰
- 主要问题：……
- 第二次拷问：通过 / 候选 / 淘汰 / 不适用
- 最终状态：正式萌芽 / 候选萌芽 / 淘汰

## 候选萌芽池

- 候选标题：……
  - 未进入主看板原因：……
  - 下一步补强：……

## 跨库关系图

```text
高连接节点
├─ 连接：库级地图 / 跨库框架 / 主题
│  └─ 发芽：新认知 / 新产品 / 新机会
```

## 高连接节点

| 节点 | 连接范围 | 为什么重要 | 下一步 |
|---|---|---|---|

## 建议追问

- ……

## 成熟/归档/放弃区

- 已进入框架：
- 已转项目：
- 已放弃：

## 版本记录

### v0.1｜YYYY-MM-DD
- 本轮新增：……
- 本轮调整：……
~~~

Legacy report-style ordering is allowed only for old notes; new updates should use opportunity-board ordering.

## LLM Wiki Pattern

Karpathy's LLM Wiki pattern is relevant to sprouting:

- **Raw sources**: original Get笔记 notes and local files; do not rewrite them casually.
- **Wiki layer**: framework notes and sprout log; LLM-maintained, structured, cross-linked.
- **Schema**: skills and governance rules; tells the LLM how to maintain the system.
- **Index**: total index; content-oriented navigation.
- **Log**: governance log; chronological evolution and maintenance record.
- **Lint**: periodic checks for stale claims, contradictions, orphan concepts, missing links, and weak sprouts.

Sprouter should operate on the wiki layer, cite sources, and generate new relationship hypotheses without treating them as proven facts.

## Sprout Validation Rules

Every P0/P1 sprout must include:

- **Track**: commercial/product-value or cognition/knowledge-collision.
- **Source index**: concrete source notes, articles, framework nodes, or prior sprouts.
- **Core judgment**: the actual new claim or insight.
- **Evidence strength**: `强 / 中 / 弱 / 待验证`.
- **Evidence gaps**: what is missing before taking action.
- **Abandonment conditions**: what would make this sprout not worth pursuing.
- **Next review date**: when it should be checked again.
- **Interrogator result**: first-round and second-round review outcome.
- **Framework upgrade status**: `观察中 / 候选 / 建议新建 / 已进入框架 / 暂不升级`.

If these fields are missing, mark the sprout as incomplete and do not promote it above P2.

## Get笔记 Commands

- Read note: `getnote note <note_id> -o json`
- Search notes: `getnote search "<query>" --limit 10 -o json`
- Create sprout log if absent: `getnote save "<content>" --title "个人知识发芽日志｜跨库关联与新机会" -o json`
- Update sprout log: `getnote note update <note_id> --content "<content>" -o json`
- Add sprout log to knowledge base: `getnote kb add <topic_id> <note_id>`

Known system notes:

- `个人知识操作系统｜总索引` (`NOTE_ID_TOTAL_INDEX`)
- `AI解决方案专家框架` (`NOTE_ID_AI_FRAMEWORK`)
- `投资研究与风险收益框架` (`NOTE_ID_INVESTMENT_FRAMEWORK`)
- `个人知识系统治理日志` (`NOTE_ID_GOVERNANCE_LOG`)
- `个人知识发芽日志｜跨库关联与新机会` (`NOTE_ID_SPROUT_LOG`)

Supplementary index (not a framework entry point):

- `文章精读与金句索引｜用户高关注认知` (`NOTE_ID_ARTICLE_INDEX`)

Known knowledge bases:

- `【AI】AI工具` (`vnd1VVeY`)
- `【AI】AI Agent` (`VnW1RRR0`)
- `【AI】AI编程` (`G0P1EE4J`)
- `【投资】资产与市场` (`nrddMkx0`)
- `【汽车】云车机与智能座舱` (`0QWWMjKn`)
- `【行业】趋势与洞察` (`pn5LlleJ`)
- `【创业】商业与公司` (`zYq2VVQ0`)
- `【认知】思维与方法论` (`1n3lqq2Y`)
- `【团队】组织与管理` (`QJm7VVqY`)
- `【设计】体验与交互` (`6n1bllDY`)

## Output Rules

- Lead chat reports with human-readable "what's worth your attention this round" before P0/P1 lists.
- Be concise and conclusion-first in card bodies.
- Do not overstate sprouts as proven opportunities; mark assumptions and validation questions in the maintenance zone.
- Prefer product/business/cognition implications over generic summaries in card bodies.
- Keep sprout log card bodies readable for humans; put interrogator results, evidence strength, and source indexes in each card's `### 维护区`.
- If evidence is weak, mark the sprout as `观察中` instead of `待验证`.
