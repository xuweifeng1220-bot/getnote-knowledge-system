---
name: getnote-knowledge-analyzer
description: Analyze business, product, investment, career, or cognition questions using the user's Get笔记 knowledge frameworks and evidence notes. Use when the user asks to call, search, analyze, reason from, or synthesize Get笔记 content, but is not asking to organize new notes or update the framework system.
---

# Getnote Knowledge Analyzer

## Overview

Use this skill to answer user questions by routing through KB cognition maps and cross-library framework notes, then drilling into evidence notes with explicit reasoning. Do not classify new notes, create knowledge bases, update framework notes or KB maps, or capture new AI output; use `getnote-knowledge-maintainer` for maintenance and `getnote-knowledge-capturer` for knowledge回流.

## Skill Collaboration

| Skill | Role |
|---|---|
| `getnote-knowledge-maintainer` | Owns KB maps, cross-library frameworks, governance log |
| `getnote-knowledge-analyzer` | Read-only; argumentative analysis using KB maps + frameworks + evidence |
| `getnote-knowledge-capturer` | Captures reusable analysis output when user asks |
| `getnote-knowledge-sprouter` | Cross-library sprouting; not used during ordinary analysis |

## Operating Principles

- Default to KB cognition maps and cross-library framework notes as entry points, not raw full-note search.
- Choose maps and frameworks automatically; never require the user to name a framework or knowledge base.
- Start with `个人知识操作系统｜总索引` for dynamic discovery of `库级认知地图路由`, framework list, and routing rules unless the user asks for a very narrow known framework or provides a specific note ID.
- Treat known framework notes as fallback anchors, not the complete framework list.
- KB maps (`知识库认知地图｜【库名】`) are the **domain cognition layer**; cross-library task frameworks are the **task judgment layer** above them.
- Use raw Get笔记 evidence only after the relevant KB map and/or framework is identified.
- Separate **已有证据**, **推断**, and **待验证假设** in outputs.
- Separate **强证据判断**, **弱证据推断**, and **待验证假设** when the answer depends on framework claims.
- Prefer concise, conclusion-first Chinese responses with critical risk framing.
- Treat KB maps and framework notes as the user's cognition map: extract key conclusions, derivation chains, usage methods, boundaries, and evidence links before answering.
- Use complete note titles when citing evidence; prefer clickable Get笔记 links in the form `[note_id｜完整标题](https://biji.com/note/note_id)`.
- Do not surface framework routing mechanics unless the user asks; the normal answer should feel like direct analysis.
- If the analysis produces a reusable new judgment, framework, method, or skill design, suggest that the user may call `getnote-knowledge-capturer`; do not write it automatically.
- When relevant, search for high-value cases inside KB maps, frameworks, and evidence notes, then convert them into reusable indicators or checklists for the current question.
- `文章精读与金句索引` is a **supplementary** user-curated layer only. It never replaces KB-map and framework-first routing through the total index.

## Routing Hierarchy

Always follow this order; do not skip KB map / framework routing because精读/金句 exists:

```text
1. 总索引 → 发现库级认知地图路由、跨库框架体系、观察池、路由规则
2. 库级认知地图 → 提取该领域的认知主线、节点、代表证据
3. 跨库任务框架 → 提取跨域判断主线、认知节点、下钻路径
4. 证据笔记 → 按地图/框架链接或搜索读取 3-8 篇原始笔记
5. 精读/金句索引（可选补充）→ 仅当问题涉及用户标过的文章/金句，或地图/框架证据偏薄时
6. 广域搜索（最后手段）→ 仍无覆盖时再 search Get笔记
```

`文章精读与金句索引｜用户高关注认知` saves token versus reading the full governance log, but it is **not** the cognition entry point. KB maps and cross-library framework notes remain the primary cognition maps.

## Framework Router

Default routing process:

1. Read `个人知识操作系统｜总索引`.
2. Extract `库级认知地图路由`, framework list, framework purposes, routing guidance, observation pools, and user high-attention routing if relevant.
3. Identify which knowledge base(s) the question belongs to; read the corresponding `知识库认知地图｜【库名】` note(s).
4. Choose the best cross-library framework or framework combination for the user's question.
5. If the total index points to a newer specialized framework, prefer that specialized framework and use the older broad framework as context.
6. Read the routed KB map(s) and framework note(s); extract judgments, derivation chains, usage methods, and evidence drill-down paths.
7. Read 3-8 relevant evidence notes linked from the map/framework or found by targeted search.
8. **Only if relevant or if evidence is thin**: read matching entries from `文章精读与金句索引｜用户高关注认知`, then open linked source notes.
9. If no listed map or framework fits, search Get笔记 for likely themes and state whether this may be an observation topic or missing KB map / framework.
10. Run the **推理引擎层** before composing the final answer.

Fallback anchors by intent:

- **AI automation / Agent / product solution / customer delivery / AI PM**: read `知识库认知地图｜【AI】AI Agent` or `【AI】AI工具`, then `AI解决方案专家框架`, unless the total index has a more specific map/framework.
- **Stocks / assets / valuation / macro / industry investing / company analysis**: read `知识库认知地图｜【投资】资产与市场`, then `投资研究与风险收益框架`, unless the total index has a more specific map/framework.
- **Overall knowledge system / current thinking / cognition map**: read `个人知识操作系统｜总索引`.
- **Maintenance rules / source registry / framework upgrade status**: read `个人知识系统治理日志`.
- **User-curated deep-read articles / golden quotes** (supplementary only, after map/framework routing): read `文章精读与金句索引｜用户高关注认知` (`NOTE_ID_ARTICLE_INDEX`).
- **No obvious map or framework fits**: search Get笔记 first, identify likely themes, then explain which KB map or cross-library framework is missing or should become an observation topic.

## Get笔记 Commands

Use the existing getnote skills/CLI:

- List knowledge bases: `getnote kbs -o json`
- Search notes: `getnote search "<query>" --limit 10 -o json`
- Read note: `getnote note <note_id> -o json`
- Read knowledge-base notes: `getnote kb <topic_id> --all -o json`

Known framework notes:

- `个人知识操作系统｜总索引` (`NOTE_ID_TOTAL_INDEX`)
- `AI解决方案专家框架` (`NOTE_ID_AI_FRAMEWORK`)
- `投资研究与风险收益框架` (`NOTE_ID_INVESTMENT_FRAMEWORK`)
- `个人知识系统治理日志` (`NOTE_ID_GOVERNANCE_LOG`) - read for maintenance rules and source registry only; do not update it.

Supplementary index (not a framework entry point):

- `文章精读与金句索引｜用户高关注认知` (`NOTE_ID_ARTICLE_INDEX`) - read only after framework routing when user-curated articles or golden quotes are relevant

Known framework notes are startup anchors only. KB maps and newly created frameworks should be discovered from the total index (`库级认知地图路由` + core framework list) and governance log after maintainer registers them.

## 推理引擎层（Reasoning Layer）

After reading KB maps, frameworks, and evidence — and **before** composing the final answer — run this internal reasoning pass. The user should experience the output as reasoned analysis, not a retrieved summary.

### Step 1 — 立论点

State the actual decision or judgment the user needs:

- What is the real question behind the surface question?
- What would count as a useful answer vs. an information dump?

### Step 2 — 多源交叉

Cross-read relevant KB maps and cross-library frameworks:

- Do they **mutually reinforce** the same conclusion?
- Do they **conflict**? If so, which source is more domain-specific or better evidenced?
- Are there cognition nodes in a KB map that have **not yet been promoted** to a cross-library framework but are directly relevant?

### Step 3 — 正反压测

Do not only collect supporting evidence:

- What would **refute** the emerging conclusion?
- What **counterexamples** exist in the user's notes?
- What **boundary conditions** make the conclusion fail?
- If only supportive evidence was found, lower confidence explicitly.

### Step 4 — 显式补链

Make inference jumps visible:

- List the steps from **已有证据** to **当前结论**
- Mark which steps are direct evidence vs. inference
- Identify the **weakest link** in the chain — the step most likely to be wrong

### Step 5 — 可执行判断

End with something the user can act on:

- A decision, position, checklist, validation question, or explicit "insufficient evidence — do not act yet"
- For investment/product decisions: invalidation conditions and what to watch next

Do not skip this layer for "simple" questions. Even narrow questions benefit from at least Steps 1, 3, and 5.

## 人读层与机器层分层

**人读层（默认输出给用户）**

- 论证式自然语言：论点、支撑、反驳、推理跳跃、结论与行动
- 不说"根据框架"、"根据库级地图" unless user asks
- 证据引用嵌入叙述，不用表单字段

**机器层（仅在用户要求结构化输出或维护场景时使用）**

- 证据强度分级、来源清单、路由记录
- 放在回答末尾的简短 `证据与置信度` 段，或完全省略

Default analysis answers are **人读层 only**.

## Analysis Workflow

1. Identify the user's actual decision problem: solution, investment, career, cognition, or unclear.
2. Read the total index unless the user supplied a specific note/framework ID or the question is intentionally narrow.
3. Route to relevant `知识库认知地图｜【库名】` note(s) via `库级认知地图路由`.
4. Route dynamically to the most relevant cross-library framework note(s).
5. Read the routed KB map(s) and framework note(s).
6. Extract cognition mainlines, XMind-style maps, core judgments, derivation chains, usage methods, evidence indexes, and AI drill-down protocols.
7. Read 3-8 relevant evidence notes by ID or search query; use complete titles and clickable note links in citations.
8. If the question may benefit from user-curated material, read matching entries from `文章精读与金句索引｜用户高关注认知`, then open the linked source notes.
9. If evidence is thin, search adjacent notes, tagged `精读文章` notes, or notes containing `【金】...【金】` before forming a strong conclusion.
10. Run the **推理引擎层** (立论点 → 多源交叉 → 正反压测 → 显式补链 → 可执行判断).
11. Compose the answer using the **论证式输出模板** below.

## High-Value Case Usage

When analyzing investments, companies, industries, products, or business opportunities, look for cases that reveal reusable signals rather than treating them as anecdotes.

In investment and company analysis, explicitly check:

- **Non-leader catch-up**: is a challenger adapting faster than the incumbent because the industry's key competition variable changed?
- **Early growth expression**: are validation speed, delivery speed, customer certification, utilization rate, gross margin, yield, order conversion, or ecosystem fit already signaling future growth before full earnings confirmation?
- **Competition-variable shift**: has the basis of advantage moved from cost/scale to efficiency, delivery, digital yield, process knowledge, software, ecosystem access, or customer validation?
- **Technical route reversal**: is a previously non-mainstream route becoming superior under new demand constraints?
- **Profitability window**: is the profit uplift driven by demand pull, localization, utilization ramp, or technical leadership, and how long might it last before standardization or price war?

Use cases in narrative form when helpful; avoid empty form shells:

```markdown
**可复用案例**

[案例名] 的关键启示是……（2-3 句人话）

映射到当前问题：……
最值得盯的指标：……
若出现……则此案例逻辑失效。
```

Reference example:

- `[NOTE_ID_EXAMPLE_HBM｜国产存储芯片赶超路径与行业逻辑深度研报](https://biji.com/note/NOTE_ID_EXAMPLE_HBM)`: SK Hynix surpassed Samsung in the HBM window because MR-MUF, accumulated process knowledge, and a digital yield database fit the new competition variable: rapid GPU-linked delivery and validation efficiency. The reusable signal is that future stock or company performance may be expressed early through operating indicators before it is fully obvious in headline leadership.

## Evidence Strength

Classify conclusions by evidence strength:

- **强证据判断**: multiple source notes, direct evidence, clear counterexample handling, and stable framework support.
- **中等证据判断**: one or two relevant notes plus a coherent framework inference, but limited cases or weak counterexamples.
- **弱证据推断**: plausible synthesis from adjacent frameworks, but thin direct evidence.
- **待验证假设**: useful idea, opportunity, or hypothesis that needs new evidence before acting.

When evidence is weak, lower the confidence explicitly and provide validation questions instead of definitive advice.

## 论证式输出模板

Default answer structure (人读层). Adapt section depth to question complexity; omit empty sections.

```markdown
## 核心判断

1-3 句直接回答用户问题。先给结论，不要先铺背景。

## 为什么这么说

用自然语言写推导链：从已有认知和证据出发，如何得到上面的判断。
引用关键证据时嵌入叙述，附 Get笔记 链接。

## 反面与风险

什么证据或情况会推翻上述判断？当前最薄弱的一环是什么？

## 推理跳跃说明

（当推断成分较多时必填）
- 已有证据直接支持的部分：……
- 我替你补的推理步骤：……
- 最脆弱的一步：……

## 可执行建议

现在可以做什么 / 不应做什么 / 下一步该验证什么。
投资或花钱类问题须写明失效条件。

## 可复用案例或指标

（可选）与当前问题真正相关的案例或观察指标。
```

Do **not** default to the old extractive template (`核心结论` + `证据强度` + `证据支撑` as parallel form fields). Those belong in the optional machine layer below.

### Optional machine layer (end of answer, only when useful)

```markdown
---
**证据与置信度**：强证据判断 / 中等证据判断 / 弱证据推断 / 待验证假设
**主要来源**：[note_id｜标题](链接)（最多 5 条）
```

## XMind-Style Output

When the user asks for structure or cognition maps, output an XMind-like plain-text tree, not Mermaid:

```text
中心主题
├── 一级结论：一句话方便记忆
│   ├── 推导：为什么成立
│   ├── 边界：什么时候成立
│   ├── 风险：什么时候失效
│   └── 证据：笔记ID｜标题
└── 下一层逻辑
    ├── ...
```

## Output Rules

- Default to the **论证式输出模板**; write like a sharp analyst, not a retrieval bot.
- Do not say "based on a framework" or "based on KB map" unless useful; make routing invisible in normal use.
- If evidence is weak, say so directly in `核心判断` or `反面与风险`, not only in a strength label.
- Do not present sprout-log opportunities as proven facts; treat them as hypotheses until analyzer reads evidence and validates assumptions.
- If the question implies spending or investment decisions, include risk-reward, transaction cost, and invalidation conditions in `可执行建议`.
- Do not update any Get笔记 note under this skill.
- Do not classify new notes, maintain knowledge bases, update KB maps, refresh update markers, or edit framework notes; those actions belong to `getnote-knowledge-maintainer`.
- Do not capture AI-generated outputs into Get笔记; that belongs to `getnote-knowledge-capturer`.
- When answering from a large KB map or framework, compress into decision-relevant branches instead of dumping the whole note.
