---
name: getnote-knowledge-maintainer
description: Maintain the user's Get笔记 knowledge system by scanning recent or unfiled notes, classifying them into knowledge bases, updating framework notes, and recording framework evolution. Runs on any cadence (Codex automation or manual); scan window is always since last maintenance, not a fixed schedule. Uses kb_scan.py + ledger JSON for token-efficient incremental runs after M=N bootstrap. Distinguishes incremental maintenance (default) vs full closure; reports mandatory 已完成/未完成 and seven-step closure checklist; ends with in-run note re-scan. Outputs 待你执行任务 for structural writes. Use when the user asks to整理新增笔记, 归档, 更新知识框架, 迭代知识系统, or maintain Get笔记 content; do not use for ordinary analysis questions.
---

# Getnote Knowledge Maintainer

## Overview

Use this skill to perform periodic Get笔记 maintenance: classify new notes, review captured AI回流 notes, maintain per-knowledge-base cognition maps, update cross-library task frameworks, and record changes in the governance log. Do not perform open-ended business or investment analysis; use `getnote-knowledge-analyzer` for analysis. Do not capture new AI outputs; use `getnote-knowledge-capturer` for回流. Do not generate cross-knowledge sprouts; use `getnote-knowledge-sprouter` after maintenance.

## Skill Collaboration

| Skill | Role |
|---|---|
| `getnote-knowledge-capturer` | Ingestion gate; writes human-readable notes |
| `getnote-knowledge-maintainer` | Owns KB maps, cross-library frameworks, governance log, source registry |
| `getnote-knowledge-analyzer` | Read-only; routes through KB maps + frameworks for argumentative analysis |
| `getnote-knowledge-sprouter` | Read-only on KB maps; uses them as cross-library collision surface |

## Maintenance Scope

This skill may:

- Read all or recent Get笔记 notes.
- Review older captured notes marked `待 maintainer 复核`, `#AI回流`, or `#待框架复核`.
- Create knowledge bases when a confirmed topic requires one.
- Add notes to knowledge bases.
- Create and update per-knowledge-base cognition maps (`知识库认知地图｜【库名】`).
- Update cross-library task framework notes and the governance log.

This skill must not:

- Delete notes.
- Rewrite original source/evidence notes.
- Create AI回流 notes from the current conversation.
- Mix in deep advisory analysis beyond maintenance summary.
- Leave classified notes with cognitive value unaccounted for (must land in KB map, cross-library framework, observation pool, or explicit no-value disposition).
- Automatically create new knowledge bases without explicit user confirmation.
- Automatically create new cross-library task framework notes without explicit user confirmation.
- Execute structural tasks (new KB / new KB map for new KB / cross-library framework create or major adjust) without the user explicitly asking to run them — **propose only, user executes**.

## 维护触发模式（用户确认偏好）

Maintainer has **no fixed schedule** in the skill. The user triggers it via:

- **Codex automation** on whatever cadence they configure (weekly, monthly, or other)
- **Manual** `/getnote-knowledge-maintainer` anytime

Do not assume weekly or monthly in reports, plans, or logic. Use **time since last maintenance** only.

```text
Codex 自动化（任意周期）/ 用户手动触发
→ maintainer 读 + 梳理 + 诊断
→ 扫描窗口 = 自上次治理日志维护记录以来（见下方）
→ 输出「待你执行任务」：结构性变更只提示，不自动执行
→ 用户说「执行待办 N」后再写入
```

### 扫描窗口（唯一的时间锚点）

**Do not hard-code weekly, monthly, or N-day intervals.**

| 场景 | 扫描什么 |
|---|---|
| **常规维护**（任意触发间隔） | 自 **上次治理日志 maintainer 版本行** 以来：新增/未归档笔记、未处理的 AI回流、未登记的精读/金句 |
| **精读/金句 backlog** | 不受时间限制：凡带 `精读文章` / `【金】...【金】` 且未登记或未进库级地图的，**一律扫** |
| **库级地图 bootstrap / 加深** | **该库全部笔记正文**（见 `库级地图内容扫描协议`），不只标题 |
| **无新笔记的一次运行** | 仍跑：Lint、库级地图密度检查、待你执行任务队列、精读/金句遗漏对账 |

Last-run anchor: read governance log for the latest maintainer version entry (e.g. `v1.7｜YYYY-MM-DD`); if missing, treat unregistered sources in source registry as the backlog.

**Primary deliverable** (any cadence): maintenance report with **`待你执行任务`** right after 一句话总结, plus mandatory **`已完成 / 未完成`** closure checklist (see **执行口径与闭环规则**).

## 执行口径与闭环规则

Maintainer 必须区分 **做了什么** 与 **是否闭环**。默认运行是增量维护；全量收口只有用户明确要求或七步链路全部满足时才可宣称完成。

### 两种执行口径（不可混用表述）

| 口径 | 触发 | 扫描范围 | 允许使用的完成表述 |
|---|---|---|---|
| **增量维护**（默认） | 常规 automation / 手动 `/getnote-knowledge-maintainer`；用户说「执行吧」但未说「全量/加深/整理全部」 | 自上次治理日志锚点以来的新增/未归档 + P0 精读/金句 backlog + Lint | **不得**写「全库梳理完成」「地图已全部加深」「归档已全部完成」。应写「本轮增量维护已执行 / 部分完成」并标明范围 |
| **全量收口** | 用户明确说「整理全部」「深度维护」「执行全部加深」「全量收口」；或单库「执行加深库级地图｜【库名】」 | 指定库/全库全文扫描、历史 backlog 清零、七步链路逐项验收 | 仅当 **七步闭环链路** 全部满足，才可写「本轮梳理完成」；否则必须写「部分完成」 |

**反模式（禁止）**：
- 只做了 2 篇新笔记增量 + 1 库加深，却汇报「维护完成」「地图已达标」
- 把「Tier B 已写入 N 条」等同于「归档/标签/地图/索引/金句已全部同步」
- 用阶段性进度回答用户「是否完成 XXX」——必须按 **最严格闭环口径** 回答（见下）

### 七步闭环链路（「本轮梳理完成」的唯一条件）

只有以下 **全部** 满足，才可在汇报中使用 **「本轮梳理完成」**；任一步未完成 → 必须使用 **「部分完成」** 并列出剩余项：

```text
1. 新增归档     — 扫描窗口内所有应归档笔记已 kb add 或明确判定无认知价值/ignored
2. 标签复核     — 见下方「标签」广义定义；无应归类而未承接的笔记
3. 库级地图承接 — 每条有认知价值的已归档笔记，已在对应 KB map 有节点/案例/无价值标注
4. 跨库框架/观察池承接 — 够门槛的已升级/登记观察池；Tier C 待办不算已完成
5. 总索引/治理日志同步 — 总索引路由、治理日志版本行、source registry 与本轮写入一致
6. 精读/金句对账 — 所有 `精读文章` / `【金】...【金】` 与索引 03/04/05 零遗漏
7. 运行中新增复扫 — 收尾二次扫描，无执行期间新增漏网（见下）
```

汇报时在 **一句话总结** 中必须点明本轮是 **「梳理完成」** 还是 **「部分完成」**，并引用上表缺了哪几步。

### 「标签」的广义定义（回答用户问「打标签了吗」）

用户问「是否完成打标签/标签处理」时，**不要**狭义理解为是否改写了 Get笔记原生 `tag` 字段。

**标签完成** = 以下治理动作均已到位、且无遗漏：

| 维度 | 完成标准 |
|---|---|
| **正确归类** | 笔记已进入正确知识库，或 explicit `无认知价值` / `ignored` |
| **正确承接** | 有认知价值的笔记已在 Layer 1（KB map）或 Layer 2（跨库框架）或 Layer 3（观察池/精读登记）有记录 |
| **用户高关注信号** | `精读文章`、`【金】...【金】`、`#AI回流` / 待复核 已按 skill 规则处理或列入未完成 |
| **无遗漏治理** | 零遗漏对账通过；不存在「已归档但未进地图/框架/观察池/无价值说明」 |

回答模板：「标签/归类：**已完成 / 部分完成 / 未完成** ——（按上表逐项说明，缺什么写什么）」

### 用户追问「是否完成 XXX」的严格回答规则

当用户问是否完成 **归档 / 标签 / 地图 / 索引 / 金句同步**（任一或组合）时：

1. **按七步链路逐项验收**，不用「本轮做了哪些写入」代替验收
2. **默认最严格口径**：有 backlog、有 Tier A/C 待办、有历史遗漏 → 答 **未完成** 或 **部分完成**，并列出剩余项
3. **不得**用「已归档 2 篇」「已更新 3 张地图」暗示全流程已完成
4. 分项简表（汇报中建议固定出现）：

| 检查项 | 状态 | 说明 |
|---|---|---|
| 归档 | ✅ / ⚠️ / ❌ | |
| 标签/归类承接 | ✅ / ⚠️ / ❌ | 广义标签，非仅 tag 字段 |
| 库级地图 | ✅ / ⚠️ / ❌ | 增量 vs 加深范围写清 |
| 跨库框架/观察池 | ✅ / ⚠️ / ❌ | |
| 总索引/治理日志 | ✅ / ⚠️ / ❌ | |
| 精读/金句对账 | ✅ / ⚠️ / ❌ | |
| 运行中新增复扫 | ✅ / ⚠️ / ❌ | |

### 运行期间新增笔记二次复扫（默认收尾步骤）

**每次 maintainer 运行结束前必须执行**，不可省略：

1. 记录本轮 **开始时刻** 或 **开始时的最新 note 时间戳/治理日志锚点**
2. 完成 Tier B/A 写入、治理日志草稿后，**再次**执行：
   - `getnote notes --all` 或等价方式，拉取自锚点以来 **全部** 笔记
   - 对比本轮已处理 note_id 列表
3. 若发现 **执行期间新增** 且落入扫描窗口的笔记：
   - **默认**：纳入本轮继续处理（归档 → 地图 → registry → 对账）
   - 若上下文/配额不允许当场处理：写入 **未完成**「运行中新增漏扫：note_id 列表」，**不得**宣称梳理完成
4. 复扫通过（0 条未处理新增）后，才可在第 7 步标 ✅

### 汇报强制结构：已完成 vs 未完成

维护报告 **必须** 在「一句话总结」之后、「待你执行任务」之前（或紧随其后）单列两节，**不能只列已做动作**：

```markdown
## 已完成（本轮实际闭环范围）
- 执行口径：增量维护 / 全量收口 / 单库加深｜【库名】
- 已闭环步骤：（从七步链路中列出本轮真正完成的步骤）
- 已处理笔记：（note_id + 一句话处置）

## 未完成（剩余项，必须显式列出）
- 未闭环步骤：（从七步链路中列出缺项及原因）
- 待下轮 / 待用户执行：（Tier A/C、加深队列、精读 backlog 等）
- 运行中新增复扫：（通过 / 发现 N 条待处理）
```

若本轮为 **部分完成**，一句话总结首句必须含 **「部分完成」** 及最主要缺项，禁止仅用积极措辞描述已做部分。

## 写入分级（Write Tiers）

| 层级 | 操作 | 默认行为 |
|---|---|---|
| **Tier A — 结构性** | 新建知识库；新建库级认知地图（针对**新**库）；新建跨库框架；跨库框架大改/拆分/合并 | **只提议，不写入**；列入 `待你执行任务`，等用户明确说执行 |
| **Tier B — 日常维护** | 笔记归档到已有库；已有库级地图增量更新；精读/金句登记；source registry；治理日志指针；观察池计数 | 可先出计划；**用户未反对时可执行 Tier B**，或用户说「日常部分直接做」时执行 |
| **Tier C — 跨库框架微调** | 在已有跨库框架中新增/强化/降级单个节点（非新建框架、非拆分） | 列入 `待你执行任务` **或** 与用户确认后执行；默认与 Tier A 一样先提示 |

User preference: **Tier A 必须提示；用户自己来触发执行。** When in doubt, prompt rather than write.

## Required Confirmation

Before **Tier A** or **Tier C** writes, present the task in `待你执行任务` and wait until the user explicitly asks to execute that task (e.g. 「执行待办 1」「新建这个知识库」「按方案更新投资框架」).

Before **Tier B** batch writes, a short execution plan is enough unless the user has asked for suggest-only mode.

Writes include `getnote save`, `getnote note update`, `getnote kb create`, and `getnote kb add`.

## User Collaboration Signals

The user marks high-attention content with lightweight tags and inline anchors. Maintainer must treat these signals as **first-class scan targets**, not optional extras after ordinary classification.

### 精读文章

- User tag: `精读文章` via Get笔记 native tags; do not require a literal `#` in the tag field
- Optional re-review tag: `精读重检`
- User may add `精读文章` **after** earlier maintenance already archived the note; do not skip it because it is old or already classified
- Detection rule: any note tagged `精读文章` enters the deep-read queue when:
  - it is absent from the governance log `文章精读登记表`, or
  - it carries `精读重检`, or
  - it contains new `【金】...【金】` blocks not yet registered in `洞察/发现点池`
- Do not rewrite the article body during deep-read processing
- Default output location: `文章精读与金句索引｜用户高关注认知` note (`NOTE_ID_ARTICLE_INDEX`), not the article header
- Governance log keeps only a pointer and sync metadata; do not append full精读/洞察 bodies into the governance log
- Optional, only after user approval: append a short `## Maintainer精读沉淀｜YYYY-MM-DD` block at the **end** of the original note

### 发现点 / 金句锚定

Use one **symmetric** bookend marker so mobile marking stays fast, humans can spot golden quotes easily, and extraction stays reliable:

```text
【金】被锚定的句子或段落【金】
```

Rules:

- Always use the **same** marker `【金】` at both the start and the end
- `【金】` means 金句 / 发现点; humans should read it as a highlighted quote
- Do not require the `精读文章` tag before adding a golden-quote anchor
- Do not use blockquotes, bold-only marking, or asymmetric wrappers as the primary format
- The wrapped content may be one sentence or multiple paragraphs
- The user may add new wrappers anytime, including on notes already archived or already deep-read
- Extract every complete `【金】...【金】` block during maintenance
- Legacy support: still extract older `【发现点】...【/发现点】` blocks if present, but recommend `【金】...【金】` for all new marking
- Do not rewrite or remove the user's wrappers in the original note
- Do **not** require an extra note tag such as `金句` or `发现点`; the paired body anchor is sufficient
- Do **not** full-scan all archived notes looking for implicit golden quotes
- Find candidate notes via `getnote search "【金】"` first, then cross-check `洞察/发现点池`
- Deep-read only notes with unregistered `【金】...【金】` blocks
- `精读文章` and `【金】` are independent: either, both, or only one may be present

Mobile-friendly examples:

```markdown
【金】未来公司的增长，往往会先体现在验证周期和良率数据上。【金】

【金】
第一段观点。
第二段补充。
【金】
```

Mobile shortcut tip: set a text replacement such as `jj` -> `【金】`, then paste it before and after the selected text.

### 沉淀去向

| 用户动作 | Maintainer 默认沉淀位置 | 何时进入库级地图 | 何时进入跨库框架 |
|---|---|---|---|
| 普通新笔记 | 归档到知识库 + 对应 `知识库认知地图｜【库名】` | 带来该库任何新认知、方法、案例或判断时（低门槛） | 改变跨库任务判断、方法、案例或风险认知时 |
| `精读文章` tag | `文章精读与金句索引｜用户高关注认知` → 03｜文章精读索引 | 同时更新相关库级地图 | 当文章改变了跨库任务判断、方法、案例或风险认知时 |
| `【金】...【金】` | 同上 → 04｜洞察/金句池 | 同时更新相关库级地图 | 当发现点可复用、可观察、可改变跨库分析方式时 |
| 高价值案例 | 相关库级地图 + 跨库框架节点 | 默认进入库级地图 | 符合 High-Value Case Extraction 规则时 |

Do not create one standalone summary note per article or per discovery point by default. Use the rolling indexes unless the user explicitly asks for a separate note.

### 总索引同步

Whenever maintainer creates or materially updates the reading index or KB maps, also update `个人知识操作系统｜总索引` sections `用户高关注内容路由` and `库级认知地图路由`, and add a one-line sync record in `个人知识系统治理日志`.

The total index section `库级认知地图路由` must list for each KB:

- knowledge base name and topic_id
- map note title and note ID
- one-line purpose (what cognition this library holds)
- when analyzer should route here
- related cross-library frameworks (if nodes were promoted)

The reading index note must state:

- user marking rules: tag `精读文章`; golden quotes use `【金】...【金】`
- section locations: 03 精读索引 / 04 洞察金句池 / 05 登记表
- when analyzer should route there
- when sprouter should treat them as high-signal cross-connect material
- link to `[NOTE_ID_ARTICLE_INDEX｜文章精读与金句索引｜用户高关注认知](https://biji.com/note/NOTE_ID_ARTICLE_INDEX)`

### 遗漏防护

At the end of each maintenance run, cross-check:

- all notes tagged `精读文章` against `文章精读登记表`
- all `【金】...【金】` blocks against `洞察/发现点池`
- report any user-marked item that remains unprocessed

## 库级认知地图（Knowledge-Base Cognition Map）

Each known knowledge base must have exactly one cognition map note:

- Title pattern: `知识库认知地图｜【库名】` (e.g. `知识库认知地图｜【投资】资产与市场`)
- One map per KB; do not split one KB into multiple maps
- Maps are **owned by maintainer**; `getnote-knowledge-analyzer` and `getnote-knowledge-sprouter` read them but do not update them

### Purpose

A KB map is the **low-threshold cognition layer** for that knowledge base. It answers: "What have I actually learned in this library?" Cross-library task frameworks (AI解决方案、投资研究, etc.) sit **above** KB maps and handle task-specific judgment across domains.

### When to update a KB map

Update the relevant KB map when a note brings **any** of:

- a new judgment or conclusion within that KB's domain
- a reusable method, checklist, or indicator
- a meaningful case or example
- a risk, boundary, or counterexample
- a golden quote or insight tied to that KB

**No 3/5/10 note threshold for adding a node.** One note with cognitive value is enough for an incremental update.

### KB map density standards（易读 ≠ 过薄）

A KB map must be **human-readable and sufficiently dense** to represent what the library actually contains. Do not collapse a 50–100 note library into 3–5 generic slogans.

**Minimum coverage by library size** (bootstrap or major deepening pass):

| 库内笔记数 | 认知全貌树：一级主题分支 | 认知节点详述 | 代表案例 |
|---:|---:|---:|---:|
| 1–15 | 3–5 | 每个分支至少 1 段详述 | 1–2 |
| 16–40 | 5–8 | 8–12 个节点有详述 | 2–4 |
| 41–70 | 8–12 | 12–20 个节点有详述 | 3–6 |
| 70+ | 10–15 | 20–30+ 个节点有详述 | 5–8 |

**How to build density without becoming unreadable**:

1. **Thematic clustering**: group notes into 8–15 sub-themes (e.g. AI Agent 库 → OpenClaw / Loop / 企业落地 / PRD / 多Agent协作 / Token策略 …), not one node per note.
2. **Each sub-theme node** needs: 一句话结论 + 为什么这么说（2–3 句）+ 什么时候用 + 边界 + **至少 1 条代表证据链接**。
3. **认知全貌树** shows the full sub-theme structure; **认知节点详述** expands the most important 60–80% of nodes (not only top 5).
4. **代表案例** picks cases that change future judgment, with links — not duplicate every note title.
5. **维护区节点索引** should list **all** mapped nodes with evidence links, even if正文详述略短 — this is the machine layer for analyzer drill-down.

**Anti-patterns (do not do this)**:

- 5 nodes summarizing 97 notes with no sub-structure
- Generic labels like「行业趋势」「工具应用」with no specific conclusions
- Bootstrap from **titles only** without reading full note bodies per 库级地图内容扫描协议
- Copying cross-library framework content instead of library-specific cognition

**Bootstrap vs deepening**:

- **Bootstrap** (first map): follow **库级地图内容扫描协议** — read all KB notes in full, P0 精读/金句 first, then cluster into sub-themes.
- **Deepening pass** (existing thin map): same full-KB content scan; expand toward density table; list unmapped 精读/金句 explicitly in gap analysis.
- **Incremental update** (after map meets density minimum): full read of new notes since last run + P0 精读/金句 backlog in that KB.

If a map is below minimum density for its note count, list **`待办｜加深库级地图｜【库名】`** in 待你执行任务 with gap analysis (current nodes vs target, unmapped note themes).

### 库级地图内容扫描协议（KB Map Content Scan）

When **creating**, **deepening**, or **materially revising** a KB cognition map, **do not rely on note titles alone**. Read note **bodies** via `getnote note <note_id>` (or full KB pull + per-note read).

**Scan scope for bootstrap / 加深 pass**:

1. `getnote kb <topic_id> --all` → list every note in the library
2. Read **full content** of each note (all notes in that KB for bootstrap/deepening; not a title-only sample)
3. Cross-check `文章精读与金句索引｜用户高关注认知` for entries belonging to this KB

**Priority order within the KB** (read and map these first, with extra weight in the cognition tree):

| 优先级 | 识别方式 | 维护要求 |
|---:|---|---|
| P0 | Get笔记标签 `精读文章` | 必须进入库级地图对应子主题；同步检查精读索引 03；核心结论写入节点详述 |
| P0 | 正文 `【金】...【金】`（含 legacy `【发现点】`） | 必须进入库级地图 + 洞察池；金句本身或提炼结论写入节点 |
| P1 | `#AI回流` / maintainer 待复核 | 读全文，提取可复用认知 |
| P2 | 其余库内笔记 | 读全文，聚类进子主题 |

**Clustering after full read**: group by sub-theme using content (not title keywords alone). Each sub-theme node must cite evidence from notes actually read.

**Routine maintenance** (between bootstrap/deepening): at minimum read **full body** of every **new** note since last run + re-scan all P0 精读/金句 in that KB if not yet reflected in the map.

**Anti-pattern**: generating a KB map from `getnote kb --all` titles only, or reading fewer than all notes during a 加深 pass when user requested full library coverage.

### 全量覆盖账（Full-Coverage Ledger）— 认知地图的硬性验收

核心原则：**认知地图 = 对该库全量内容的一次性梳理，不是抽样。** 一张地图只有在「每条笔记都被账目接住」后，才能标为 `全量已覆盖`。

**覆盖账规则**：

1. bootstrap 或加深一张地图时，先取 `getnote kb <topic_id> --all` 得到 **完整 note_id 全集 N**。
2. 逐条读全文后，**每一个 note_id 必须有归宿**，二选一：
   - 归入某个 **认知子主题节点**（记录它支撑哪个节点），或
   - 明确标 **`无认知价值 / 重复 / ignored`** 并写一句原因。
3. 不允许「读了几条、抽出几个主题」就收工——**未归位的 note_id 一条都不能剩**（除非列入未完成并说明原因）。
4. 覆盖率 = 已归位笔记数 / N。**只有 = N（100%）时**，该地图才可称 `全量已覆盖 / 加深完成`；否则是 `部分覆盖 M/N`，必须进 `未完成` 与 2b 加深队列。
5. 覆盖账落在地图 **维护区** 的「全量覆盖账」表，供后续增量维护对账。

**子主题密度**：仍遵循 KB map density standards（按库大小定分支/详述数）。全量覆盖解决「有没有漏」，密度标准解决「够不够厚」，两者都要满足才算加深完成。

**加深完成后转增量**：一张地图达成 100% 覆盖并满足密度下限后，后续每轮只需：
- 读该库自上次锚点以来的 **新增笔记**，逐条归位并更新覆盖账（N 增大、M 同步增大）；
- 重扫该库未登记的 P0 精读/金句；
- 不需要再全库重读（除非用户要求「重检 / 全量收口」或库结构大改）。

**验收提问**：回答「这个库的地图梳理完整吗」时，用覆盖账口径——报 `M/N` 与未归位清单，不能用「抽了几个主题」代替。

### Token-efficient execution（默认，不影响质量）

Read `references/token-efficient-maintenance.md` before every run. Use `scripts/kb_scan.py` — **do not** paste full-KB text dumps into context when ledger delta is empty.

| 场景 | 做法 |
|---|---|
| **增量维护**（地图已 M=N） | `kb_scan delta --ledger .maintainer/ledgers/{topic_id}.json` → 仅对 `new` + 未映射 P0 做 `read` |
| **加深 / bootstrap** | `kb_scan deepen`（P0 excerpt 800 / P2 excerpt 280）；一库一批，>40 篇再分子批 |
| **聚类预检** | `kb_scan inventory --excerpt 180`（不读全文） |
| **M=N 后维护区** | 正文保留详述；**维护区**用 `ledger_ref` + 各节点 **计数**，完整 note_id 列表只存 ledger JSON |

**禁止**：增量轮次对 30+ 笔记库做 900 字/篇全量 dump；零新增时仍重读全库正文。

**汇报压缩**：增量且无结构性待办 → 150–350 词 + 七步表；不重复贴覆盖账 id 清单。

### KB map structure (human-readable body)

```markdown
# 知识库认知地图｜【库名】

> 一句话主线：这个库最核心的认知是什么

## 认知全貌

```text
【库名】
├─ 主线判断：...
├─ 关键认知节点【本轮新增/本轮调整】
│  ├─ 节点A：一句话结论
│  │  ├─ 为什么这么说
│  │  ├─ 什么时候用
│  │  ├─ 什么时候不适用
│  │  └─ 代表证据：[note_id｜完整标题](https://biji.com/note/note_id)
│  └─ ...
└── 与跨库框架的衔接
    └─ 哪些节点已升级到跨库框架、哪些仍留在此库
```

## 认知节点详述

（用自然语言段落写清每个节点的结论、推导、用法、边界；不要写成表单）

## 代表案例

（讲清楚背景、关键变量、可复用认知；案例本身是人话，不是字段清单）

---

## 维护区

（机器层元数据收纳于此，正文不出现）

### 库信息
- 知识库：【库名】
- topic_id：
- 最后维护：YYYY-MM-DD
- 笔记计数 N / 节点计数
- 覆盖状态：全量已覆盖 M=N ｜ 部分覆盖 M/N

### 全量覆盖账（机器层）
> 目标：M=N。每个 note_id 要么进某节点，要么标无价值/重复/ignored。未归位清单必须为空才算加深完成。

**M=N 后（增量默认）** — 紧凑格式，完整 id 列表存 ledger JSON，不重复堆在地图里：

```markdown
- ledger_ref：.maintainer/ledgers/{topic_id}.json
- 覆盖摘要：A(17) B(8) C(2) …｜ignored(0)｜M=N=101
- 未归位：无
```

**加深进行中 / 部分覆盖** — 仍用明细表直到 M=N：

| 子主题节点 | 承接的 note_id（可多条） |
|---|---|
| 节点A | |
| 无认知价值/重复/ignored | note_id｜原因 |
| **未归位（待下轮）** | note_id｜原因（非空即 部分覆盖） |

### 节点索引（机器层）
| 节点 | 框架关系 | 证据强度 | 来源 note_id | 最后复核 |
|---|---|---|---|---|

### 升级候选
- 已达 3 篇同主题 → 观察池
- 已达 5 篇同主题 → 考虑并入跨库框架节点
- 已达 10 篇或出现真实任务场景 → 提议独立跨库框架
```

### KB map bootstrap

On the first substantial maintenance run after this rule is active:

1. Read `个人知识操作系统｜总索引` section `库级认知地图路由` (create if missing after user approval).
2. For each known knowledge base, check whether `知识库认知地图｜【库名】` exists.
3. If missing, propose creating it using **KB map density standards** and **库级地图内容扫描协议** — full note bodies, P0 精读/金句 first.
4. Batch creation requires explicit user approval; present density target (node count, sub-themes) per KB in the plan.
5. After creation, register each map in total index `库级认知地图路由` and governance log source registry.

**If maps already exist but are below density minimum** (e.g. bootstrap used title-only summaries): schedule a **加深 pass** — either as Tier B when user says 「加深库级地图」, or as 待你执行任务 with per-KB gap table.

Known KB → map title mapping:

| Knowledge base | Map title |
|---|---|
| `【AI】AI工具` | `知识库认知地图｜【AI】AI工具` |
| `【AI】AI Agent` | `知识库认知地图｜【AI】AI Agent` |
| `【AI】AI编程` | `知识库认知地图｜【AI】AI编程` |
| `【投资】资产与市场` | `知识库认知地图｜【投资】资产与市场` |
| `【汽车】云车机与智能座舱` | `知识库认知地图｜【汽车】云车机与智能座舱` |
| `【行业】趋势与洞察` | `知识库认知地图｜【行业】趋势与洞察` |
| `【创业】商业与公司` | `知识库认知地图｜【创业】商业与公司` |
| `【认知】思维与方法论` | `知识库认知地图｜【认知】思维与方法论` |
| `【团队】组织与管理` | `知识库认知地图｜【团队】组织与管理` |
| `【设计】体验与交互` | `知识库认知地图｜【设计】体验与交互` |

KB maps are discovered dynamically from total index `库级认知地图路由`; the table above is the canonical naming convention, not a hard-coded note ID list.

## 三层承接漏斗

Replace the old binary "archive vs framework" logic with three explicit layers. Every scanned note with cognitive value must land in exactly one primary disposition (plus optional secondary promotions).

```text
Layer 1 — 库级认知地图（低门槛，默认承接层）
  → 单篇笔记带来该库新认知即更新
  → 接住绝大多数笔记，避免"归档即黑洞"

Layer 2 — 跨库任务框架（高门槛，任务型升级层）
  → 沿用 3/5/10 升级诊断与 Framework Upgrade Diagnosis
  → 处理跨库、跨场景的判断、方法、案例

Layer 3 — 观察池 / 精读登记表（线索层）
  → 主题未成认知、仅计数或待观察
  → 精读文章 / 金句索引在此登记，再按需升入 Layer 1 或 2
```

Disposition rules per note:

| Note value | Layer 1 KB map | Layer 2 cross-library framework | Layer 3 observation |
|---|---|---|---|
| 带来库内新认知 | **必须更新** | 若够跨库门槛则同时升级 | 主题未成认知时先入观察池 |
| 仅归档、无认知价值 | 跳过 | 跳过 | 标记 `无认知价值` 并说明原因 |
| 精读文章 / 金句 | 更新相关库级地图 | 若改变跨库判断则升级 | 登记表必选 |

Do **not** use "仅归档不入框架" as a silent default. If a note has cognitive value, it must appear in a KB map.

## 零遗漏对账

At the end of every maintenance run, reconcile:

```text
本轮扫描笔记数
= 进库级地图
+ 进跨库框架（可与库级地图重叠）
+ 进观察池/精读登记
+ 明确判定无认知价值
+ 待下轮处理（必须列出原因）
```

Any note that is "classified but unaccounted" — archived to a KB without a KB map update and without explicit no-value disposition — is a **miss** and must appear in the maintenance report under `未表态笔记` and **`未完成`** closure section.

Merge this check with `遗漏防护`, LLM Wiki Lint `Orphan nodes`, and **七步闭环链路** step 2–3.

## 人读层与机器层分层

Shared principle across the getnote-knowledge series (see also `getnote-knowledge-capturer` "Write for Humans").

**人读层（正文，默认呈现给用户）**

- 结论、推理、认知、案例
- 自然语言段落和会说话的认知树
- 不出现 `证据强度：`、`框架关系：`、`01｜02｜` 编号模块作为正文结构

**机器层（维护区，收纳在 note 末尾）**

- `证据强度`、`框架关系`、计数表、节点索引、登记表元数据
- 用 `---` 分隔后放在 `## 维护区` 下
- 框架 note、库级地图、精读索引、发芽日志均遵循此规则

**聊天汇报**

- 先说人话结论（本次最重要的认知变化）
- 再给统计表和处理明细（机器层）

When updating framework notes or KB maps, write the human-readable body first; append or update the maintenance zone last.

## Framework Update Rules

- Keep framework notes readable for humans and callable for AI.
- Treat known framework notes as startup entry points, not a hard-coded complete framework list.
- At the beginning of each substantial maintenance run, read `个人知识操作系统｜总索引` and `个人知识系统治理日志` to discover the latest framework list, source registry, observation pools, and framework-upgrade candidates.
- Preserve an XMind-style full-map section for whole-system visibility, then use Markdown sections for detailed reading.
- Every major framework note should include (in human-readable body):
  - **一句话记忆点**: one bold, memorable conclusion.
  - **全貌关系图**: an XMind-like plain-text tree with key conclusions, not just a directory.
  - **推导链路**: why the conclusion follows.
  - **关键认知节点**: each node needs conclusion, derivation, usage method, boundary/risk, and evidence — written as readable prose, not form fields.
  - **AI下钻路径**: how to retrieve evidence notes for deeper analysis.
- Put `证据强度`, `框架关系`, node index tables, and sync metadata in the note's `## 维护区` at the end; do not scatter them through the human-readable body.
- Mark updates inline with `【本轮新增】` and `【本轮调整】`; do not create a separate update module just for highlights.
- Before a new framework iteration, remove or downgrade the previous round's `【本轮新增】` / `【本轮调整】` markers, then mark only the current round.
- Evidence must use complete note titles and clickable links: `[note_id｜完整标题](https://biji.com/note/note_id)`.
- Important claims in the maintenance zone should carry evidence strength: `强 / 中 / 弱 / 待验证`.
- Important claims should include source links, counterexample status, and last reviewed date when practical in the maintenance zone.
- **Always update the relevant KB map first** when a note brings domain cognition; promote to cross-library framework only when the content changes cross-domain task judgment.
- Do not skip KB map updates because content is "not framework-worthy yet."
- Do not lose high-quality cases. When a note contains a case that reveals a reusable cognition, indicator, reversal signal, or analysis method, extract the case into the relevant KB map and cross-library framework when applicable.
- New framework creation is a structural write. The skill may recommend a new framework, but must not create it until the user explicitly approves the title, target knowledge base, purpose, and initial content.
- After a user confirms a new framework, creation is not complete until the framework is registered back into the system entry points: total index, governance log/source registry, and analyzer routing guidance.

## Framework Upgrade Diagnosis

During every maintenance run, diagnose whether growing themes should remain in observation, be absorbed into an existing framework, or be proposed as an independent framework.

Check:

- Whether a theme has entered the observation pool across multiple rounds.
- Whether there are **3+** notes on the same theme.
- Whether there are **5+** evidence notes on the same theme.
- Whether there are **10+** evidence notes, or a real product, business, investment, career, project, or delivery scenario.
- Whether the theme has appeared in the sprout log as P0/P1 for **2 consecutive rounds**.
- Whether an existing framework is becoming bloated because one theme contains multiple different task types.
- Whether the theme has a clear use case: productization, investment research, career decision, project delivery, business validation, or reusable cognition.

Decision rules:

- **3 same-theme notes**: add to observation pool.
- **5 same-theme notes**: add or strengthen a node under an existing framework.
- **10 same-theme notes**, or one real output/commercial/investment/decision scenario: propose whether to create an independent framework.
- **2 consecutive P0/P1 sprout rounds**: list the theme in `框架升级候选`.
- **3+ same-type nodes under one existing framework**, especially when they serve different task types: recommend splitting into a specialized framework.
- **Weak evidence or no real action scenario**: keep in observation pool; do not recommend creation yet.

When proposing a new framework, include the proposed title, trigger reason, evidence count, current host KB map/framework/log, suggested knowledge base, and recommended next action. Do not run `getnote save` until the user confirms.

## 新知识库检测（New Knowledge Base Detection）

During **every** maintenance run (any automation cadence or manual trigger), after scanning new notes, check whether any theme deserves a **new knowledge base** — not only whether it fits existing 10 KBs.

### Suggest a new KB when at least two of these hold

- **5+ notes** on a theme that repeatedly misfits every existing KB (wrong shelf, mixed retrieval, forced classification).
- **Distinct domain** with its own vocabulary, evidence chain, and future retrieval need (e.g. 跨境出海、医疗、订阅源专题 — if volume grows).
- **Recurring user action scene**: investment, delivery, product, career, or research where the user would naturally search this topic alone.
- **Observation pool** has carried the theme for **2+ maintenance rounds** with growing note count.
- **Sprout P0/P1** or cross-library pressure suggests a dedicated library would reduce noise in an existing KB.

### Do not suggest a new KB when

- Notes fit cleanly into an existing KB and its cognition map.
- Only **1–2** notes on the theme (use observation pool + existing KB).
- Theme is a **subtopic** of an existing cross-library framework, not a new material domain.
- Splitting would duplicate nodes already in a KB map or cross-library framework.

### New KB proposal must include

```markdown
### 待办｜新建知识库｜【建议库名】
- **触发原因**：
- **证据笔记**：（note_id + 标题，至少 3 条，建议 5+）
- **与现有库冲突**：为什么不宜放在【现有库名】
- **建议描述**：（一句话库用途）
- **连带待办**：新建 `知识库认知地图｜【建议库名】`（Tier A，需一并确认）
- **建议动作**：用户回复「执行新建知识库」后，maintainer 执行 kb create + KB map + 总索引路由
```

Creating a new KB is **always Tier A**: propose first, execute only after user confirmation.

## 待你执行任务（Structural Task Queue）

Every maintenance report must include this section **near the top** (after 一句话总结). Group tasks by type; user executes by referencing task id or description.

### Task type 1 — 新建知识库

See **新知识库检测** above. One card per candidate KB.

### Task type 2 — 新建库级认知地图（针对新库）

When task type 1 is approved, **always** bundle or follow with:

```markdown
### 待办｜新建库级地图｜知识库认知地图｜【库名】
- **前置**：知识库已创建（或与本待办同时执行）
- **初始主线**：（1 句）
- **初始节点**：（3–5 个，来自已有证据笔记）
- **维护区**：空模板即可
- **同步**：总索引 `库级认知地图路由` + 治理日志登记
- **建议动作**：用户回复「执行新建库级地图」
```

For **existing** KBs missing a map, list as Tier A until bootstrap is done. For **existing thin maps**, list **`待办｜加深库级地图`** with density gap. After a map meets density minimum, **incremental updates** on subsequent runs are Tier B.

### Task type 2b — 加深库级认知地图（已有库，内容过薄 / 未全量覆盖）

When note count ≫ mapped nodes (see density table) **或 覆盖账 M<N**, propose:

```markdown
### 待办｜加深库级地图｜【库名】
- **当前状态**：笔记数 N / 已映射节点 Y（低于密度下限 Z）
- **覆盖状态**：全量覆盖 M/N（当前 bootstrap 多为抽样，M≈少数）
- **未覆盖子主题**：（从 **全文扫描** 聚类得出，列 5–10 条；标注含多少 精读/金句）
- **P0 未进地图的精读/金句**：（note_id 列表）
- **拟新增分支**：（认知全貌树增量）
- **扫描计划**：该库共 N 篇 → 加深 pass **必须 M=N**（全量覆盖账逐条归位），不得抽样收工
- **建议动作**：用户回复「执行加深库级地图｜【库名】」或「执行全部加深」
```

**加深 pass 完成判定**：覆盖账 M=N（无未归位 note_id）**且** 满足密度下限。任一不满足 → 仍是 `部分覆盖`，进 `未完成`。

Bundled with task type 2 only when the KB is **new**. Existing KBs use 2b.

### Task type 3 — 新建或调整跨库框架

**新建跨库框架** — use Framework Upgrade Diagnosis thresholds; include:

```markdown
### 待办｜新建跨库框架｜【建议标题】
- **触发原因**：
- **证据数量**：
- **解决什么问题**：
- **建议宿主知识库**：
- **初始节点草案**：
- **建议动作**：用户回复「执行新建跨库框架」
```

**调整跨库框架** — include:

```markdown
### 待办｜调整跨库框架｜【框架名】
- **调整类型**：强化 / 反驳 / 补充 / 新增节点 / 降级 / 拆分建议 / 合并建议
- **触发笔记**：
- **拟改内容摘要**：（人话，附草案片段）
- **是否影响库级地图**：哪些 KB map 节点同步升级或标注已晋升
- **建议动作**：用户回复「执行框架调整 X」
```

**减少 / 收缩** — never auto-delete. Propose: downgrade claim, merge nodes, move back to KB map only, or mark 观察中/暂不升级. User confirms before write.

### Empty queue

If no structural tasks: write `本轮无结构性待办；日常维护已处理 / 已列入 Tier B 计划。`

### User execution phrases

When the user says any of: `执行待办`, `执行第 N 条`, `新建这个知识库`, `按方案更新框架`, `执行全部待办` — run only the confirmed tasks from the latest report, then append governance log sync record.

## KB Map Registration

When creating or materially updating a KB cognition map, perform synchronized system updates (same discipline as cross-library framework registration):

1. **Create or update the KB map note** using the KB map structure above (human body + maintenance zone).
2. **Add it to the target knowledge base** via `getnote kb add`.
3. **Update `个人知识操作系统｜总索引` section `库级认知地图路由`**:
   - KB name, map title, note ID, one-line purpose
   - Question types that should route analyzer to this map
   - Link to related cross-library frameworks when nodes have been promoted
4. **Update governance log / source registry** with map creation or material change, evidence count, last reviewed date.
5. **Record analyzer routing guidance**: which domains and question types should read this map before or alongside cross-library frameworks.

If any synchronized update fails, report partial state and recommend repair.

## New Framework Registration

When the user explicitly confirms creating a new framework note, perform the creation as one coordinated system update. Do not create an isolated framework note.

Required synchronized updates:

1. **Create the new framework note**
   - Use the XMind-style framework format.
   - Include one-sentence memory point, full-map tree, core derivation chain, key cognition nodes, evidence links, evidence strength, boundaries/risks, and AI drill-down protocol.

2. **Add it to the target knowledge base**
   - Use the knowledge base suggested in the approved plan.
   - If a new knowledge base is needed, ask for separate confirmation before `getnote kb create`.

3. **Update `个人知识操作系统｜总索引`**
   - Add the new framework to the core framework list or relevant section.
   - State what problem it handles and when analyzer should call it.
   - Link the new framework with full title and note ID.
   - Cross-link from relevant `库级认知地图路由` entries when the framework absorbs promoted nodes.

4. **Update `个人知识系统治理日志` and Source Registry**
   - Record why the framework was created.
   - Link the evidence notes, prior observation pool, and sprout cards it absorbs.
   - Record framework relationship and last reviewed date.

5. **Record analyzer routing guidance**
   - In the total index and/or governance log, write the question types that should route to this framework.
   - If the framework becomes a long-term stable core entry, consider later adding it to this skill's Known framework notes and analyzer's Known framework notes. Do not do that by default during initial creation.

If any synchronized update fails, report the partial state clearly and recommend a repair step. The goal is that a new framework is discoverable by future `getnote-knowledge-analyzer` runs through the total index and governance log.

Use current real cases only as validation examples, not as hard-coded framework notes:

- `AI智能体定制与解决方案产品化框架`
- `AI算力产业链投资框架`
- `个人外脑与知识系统产品化框架`

## High-Value Case Extraction

When maintaining frameworks, actively identify and extract high-value cases from notes. A high-value case is not merely an example; it changes how the user should analyze future companies, industries, products, or decisions.

Extract a case when it contains at least one of:

- **Reversal signal**: a non-leader, challenger, or second-tier company shows early signs of surpassing the incumbent.
- **Early expression of future growth**: operating metrics, validation speed, delivery speed, customer adoption, gross margin, or yield improvements appear before the market fully recognizes the growth path.
- **Core variable shift**: the basis of competition changes, such as cost advantage giving way to delivery speed, efficiency, data assets, process knowledge, or ecosystem fit.
- **Counter-consensus indicator**: the winning factor is not the obvious industry-leader advantage.
- **Reusable analysis method**: the case can become a checklist, indicator, or framework node.

For each high-value case, extract into human-readable prose in the KB map / framework body. Use this structure in the **维护区** or as an internal drafting template — do not paste raw form fields into the human-readable body:

```markdown
### 案例｜完整案例标题
- **案例来源**：[note_id｜完整标题](https://biji.com/note/note_id)
- **案例背景**：
- **关键变量**：
- **反常识点**：
- **可复用认知**：
- **可观察指标**：
- **适用边界**：
- **框架关系**：支撑 / 反驳 / 补充 / 案例 / 风险 / 方法
```

Investment cases should be especially checked for:

- **非龙头反超信号**: the beneficiary may be a challenger that adapted to the new competition variable earlier than the incumbent.
- **早期经营表征**: validation cycle, delivery speed, customer certification, utilization rate, gross margin, yield database, order conversion, or supply-chain bottleneck position may signal future stock performance before full earnings release.
- **技术路线反转**: a different process route, architecture, or accumulated database can become the real moat.
- **利润弹性窗口**: early profitability improvement may come from demand pull, localization, utilization ramp, or technical leadership, but may decay once the product becomes standardized.

Validation example:

- `[NOTE_ID_EXAMPLE_HBM｜国产存储芯片赶超路径与行业逻辑深度研报](https://biji.com/note/NOTE_ID_EXAMPLE_HBM)` contains the HBM case where SK Hynix used MR-MUF, ten years of process accumulation, and a digital yield database to pass NVIDIA validation earlier than Samsung. The reusable cognition is: **future company growth may be expressed early through operating and validation signals; the beneficiary may be a challenger that beats the incumbent when the industry's key competition variable changes.**

## Source Registry Rules

Maintain a lightweight source registry inside the governance log unless a standalone registry note is later created.

Track important sources with:

- `note_id`
- full title
- source type: raw note / AI回流 / framework / sprout / local file / 精读文章 / 发现点摘录
- knowledge base
- processing status: unprocessed / classified / kb-map-updated / framework-reviewed / sprout-reviewed / deep-read-pending / deep-read-done / insight-extracted / no-cognitive-value / ignored
- framework relationship: 支撑 / 反驳 / 补充 / 案例 / 风险 / 方法
- linked frameworks or sprout cards
- last reviewed date

Use the registry to avoid repeated processing and to identify source material that has never entered a KB map, cross-library framework, or sprout.

## LLM Wiki Health Check / Lint

During periodic maintenance, run a light lint pass:

- **Evidence gaps**: key claims without source links or with only weak evidence.
- **Counterexample gaps**: high-confidence claims with no recorded counterexamples or failure conditions.
- **Stale claims**: time-sensitive claims not reviewed recently.
- **Orphan nodes**: knowledge-base themes or notes with cognitive value but no KB map entry, observation-pool entry, or cross-library framework link
- **KB map gaps**: known knowledge bases missing `知识库认知地图｜【库名】`
- **KB map under-density**: note count vs mapped node count below **KB map density standards** table — flag for 待办｜加深库级地图
- **KB map stale**: no update in 90+ days despite new notes
- **Broken/weak links**: incomplete note titles, missing note IDs, or non-clickable evidence.
- **Sprout drift**: P0/P1 sprouts with no validation action, no evidence gap, or no next review date.
- **Framework pressure**: themes that repeatedly appear in observation pools, sprout P0/P1 cards, or framework subnodes but still lack an independent frame.
- **User-flag misses**: notes tagged `精读文章` or containing `【金】...【金】` that are not yet in `文章精读登记表` or `洞察/发现点池`
- **Retroactive tag drift**: older archived notes newly tagged `精读文章` but still treated as ordinary evidence only

Report lint findings separately from ordinary classification results.

## Get笔记 Commands

- List knowledge bases: `getnote kbs -o json`
- List notes: `getnote notes --all -o json`
- Read note: `getnote note <note_id> -o json`
- Update plain-text framework notes: `getnote note update <note_id> --content "<content>"`
- Create knowledge base: `getnote kb create "<name>" --desc "<desc>" -o json`
- Add notes to knowledge base: `getnote kb add <topic_id> <note_id...>`

Known framework notes:

- `个人知识操作系统｜总索引` (`NOTE_ID_TOTAL_INDEX`)
- `AI解决方案专家框架` (`NOTE_ID_AI_FRAMEWORK`)
- `投资研究与风险收益框架` (`NOTE_ID_INVESTMENT_FRAMEWORK`)
- `个人知识系统治理日志` (`NOTE_ID_GOVERNANCE_LOG`)
- `文章精读与金句索引｜用户高关注认知` (`NOTE_ID_ARTICLE_INDEX`)

Known framework notes are startup anchors only. The current framework inventory and KB map registry should be discovered from the total index (`库级认知地图路由` + core framework list), governance log, and source registry during maintenance.

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

## Deep-Read and Insight Extraction

When processing `精读文章` or `【金】...【金】`, use these templates in the governance log.

### 文章精读卡

```markdown
### 精读｜完整文章标题
- **原文**：[note_id｜完整标题](https://biji.com/note/note_id)
- **精读触发**：精读文章 / 精读重检 / 新增金句
- **核心问题**：这篇文章在回答什么
- **核心结论**：1-3 条可复用判断
- **推导链路**：作者如何论证
- **可复用方法/指标**：
- **边界/反例**：
- **关联框架**：
- **框架关系**：支撑 / 反驳 / 补充 / 案例 / 风险 / 方法
- **证据强度**：强 / 中 / 弱 / 待验证
- **精读日期**：YYYY-MM-DD
```

### 发现点摘录卡

```markdown
### 洞察｜一句概括
- **原文锚点**：「被【金】...【金】包裹的原文」
- **来源**：[note_id｜完整标题](https://biji.com/note/note_id)
- **发现点**：这句话真正新在哪里
- **可复用场景**：以后何时调用
- **可观察指标**：
- **关联框架/主题**：
- **框架关系**：支撑 / 反驳 / 补充 / 案例 / 风险 / 方法
- **证据强度**：强 / 中 / 弱 / 待验证
- **摘录日期**：YYYY-MM-DD
```

## Maintenance Workflow

### Standard run (default — any Codex automation cadence or manual)

0. **Token gate**: For each KB with M=N ledger, run `kb_scan delta` first; skip body reads if `new` is empty (still process P0/金句 backlog).
1. Read `个人知识操作系统｜总索引` and `个人知识系统治理日志`; discover framework list, `库级认知地图路由`, observation pools, upgrade candidates, and **last maintenance timestamp** (no assumed interval).
2. Check KB map coverage and **density vs note count**; flag thin maps as 待办｜加深库级地图.
3. **Scan all new/unfiled notes since last maintenance run** (per governance log anchor):
   - include AI回流待复核、精读、金句 backlog (P0, no time limit)
4. Cross-check精读/金句 index vs user flags and vs KB maps.
5. Classify each new note → suggested KB (existing or propose new KB).
6. **Tier B** (if user allows): archive, KB map incremental updates (full read of new notes),精读/金句登记, registry, 零遗漏对账.
7. **Tier A/C** (always): 新知识库检测 + Framework Upgrade Diagnosis + KB map density lint → `待你执行任务`.
8. Update governance log pointer (counts, version line, lint summary).
9. **运行期间新增笔记二次复扫**（默认收尾，不可省略）：再次拉取扫描窗口内笔记，处理或登记执行期间新增；未处理则不得宣称七步闭环完成.
10. **七步闭环验收**：逐项对照归档/标签承接/地图/框架/索引/精读金句/复扫；确定「梳理完成」或「部分完成」.
11. Report: **一句话总结（含完成度）→ 已完成 / 未完成 → 待你执行任务 →** rest.

### Full run (整理全部 / 深度维护 / 加深库级地图)

Same as standard run, plus:

- retroactive 精读/金句 user flags
- **deepening pass** on thin KB maps per **库级地图内容扫描协议** (full KB note bodies, P0 first)
- full lint on all KB maps / cross-library frameworks

Full run **still does not auto-equate to「本轮梳理完成」** unless user scope covers all backlog **and** **七步闭环链路**全部验收通过（含运行中新增复扫）。单库加深只闭环该库范围内的步骤 3 及相关对账，不得外推为全库完成。

### Legacy numbered steps (when executing approved writes)

1. Read total index and governance log.
2. Check KB map coverage.
3. Scan user high-attention signals.
4. Cross-check精读/金句 index.
5. Scan recent and unfiled notes.
6. Scan AI回流 maintenance signals.
7. Classify notes into knowledge bases.
8. Layer 1 — Update relevant KB map.
9. Process `精读文章`.
10. Process `【金】...【金】`.
11. Layer 2 — Identify cross-library framework updates.
12. Layer 3 — Observation pool / registry.
13. Mark `无认知价值` where applicable.
14. Clear captured-note maintenance signals.
15. Update governance log and indexes (when executing writes).
16. Update total index sections when maps/frameworks changed.
17. Update source registry and lint.
18. Read sprout log P0/P1 `框架升级状态`.
19. Produce `框架升级候选` in 待你执行任务.
20. User-flag miss check.
21. 零遗漏对账.
22. **运行期间新增笔记二次复扫**.
23. **七步闭环验收**（梳理完成 vs 部分完成）.
24. Report (human-readable first; **已完成 / 未完成** mandatory).

## Periodic External-Brain Update

When the user asks for a regular/periodic external-brain update, run maintenance first, then recommend or trigger `getnote-knowledge-sprouter` if the user requested the combined flow:

```text
maintainer
→ classify new notes
→ update KB maps (Layer 1)
→ review AI回流 notes
→ update cross-library frameworks and governance log (Layer 2)
→ sprouter reads the refreshed system
→ sprouter updates the single sprout log
```

This skill itself does not generate sprouts; it prepares the knowledge system for sprouting.

## XMind-Style Framework Format

Maintain framework notes with an XMind-like full-map plus readable Markdown detail:

```text
中心主题
├─ 目标：本框架解决什么真实问题
├─ 核心矛盾：最重要的冲突或约束
├─ 判断主线：前提 → 中间逻辑 → 结论
├─ 关键认知节点【本轮新增/本轮调整】
│  ├─ 节点A：一句话关键结论
│  │  ├─ 推导：为什么成立
│  │  ├─ 使用：遇到什么问题时怎么用
│  │  ├─ 边界/风险：什么时候失效
│  │  └─ 证据：[note_id｜完整标题](https://biji.com/note/note_id)
└── AI下钻路径
    ├── 方法证据
    ├── 案例证据
    ├── 风险证据
    └── 反例证据
```

## New Topic Rules

- 3 notes on the same new theme: add to observation pool.
- 5 notes: add a node under an existing framework.
- 10 notes or a real output scenario: propose a new framework note.
- 2 consecutive P0/P1 sprout appearances: list as a framework-upgrade candidate.
- If a theme still lacks real action scenes or has weak evidence, keep it in the observation pool and do not propose creation.
- 3 strong counterexamples against a judgment: rewrite or downgrade that judgment.

## Maintenance Report Template

Lead with human-readable conclusions; put statistics after.

```markdown
**一句话总结**
用 2-3 句说明：本轮新笔记概况、最重要认知变化、有没有结构性待办。
**必须**标明：**梳理完成** 或 **部分完成**（缺哪几步写哪几步）。默认增量维护不得写「全量完成」。

## 已完成（本轮实际闭环范围）

> 只写本轮真正验收通过的项；与下方「七步闭环检查」一致。

- **执行口径**：增量维护 / 全量收口 / 单库加深｜【库名】
- **已闭环步骤**：（从七步链路勾选）
- **已处理笔记**：（note_id｜标题 → 归档库 → 地图/框架/观察池/无价值）

### 七步闭环检查（严格口径）

| 检查项 | 状态 | 说明 |
|---|---|---|
| 1. 新增归档 | ✅ / ⚠️ / ❌ | |
| 2. 标签/归类承接 | ✅ / ⚠️ / ❌ | 广义标签，非仅 tag 字段 |
| 3. 库级地图承接 | ✅ / ⚠️ / ❌ | |
| 4. 跨库框架/观察池 | ✅ / ⚠️ / ❌ | |
| 5. 总索引/治理日志 | ✅ / ⚠️ / ❌ | |
| 6. 精读/金句对账 | ✅ / ⚠️ / ❌ | |
| 7. 运行中新增复扫 | ✅ / ⚠️ / ❌ | |

## 未完成（剩余项，必须显式列出）

> 不能只汇报已做动作；无剩余项时写「无」并说明为何可称梳理完成。

- **未闭环步骤**：
- **待下轮 / 待用户执行**：
- **运行中新增漏扫**：（note_id 列表，或「复扫通过」）

## 待你执行任务

> 结构性变更只提示，不自动执行。回复「执行待办 N」或「执行全部待办」后 maintainer 再写入。

### 1｜新建知识库
（无则写「无」）
| # | 建议库名 | 触发原因 | 证据篇数 | 建议动作 |
|---:|---|---|---:|---|
| | | | | 执行新建知识库 |

### 2｜新建库级认知地图（新库配套）
| # | 库名 | 初始主线 | 目标节点数 | 前置 | 建议动作 |
|---:|---|---|---:|---|---|
| | | | | 待办1完成后 | 执行新建库级地图 |

### 2b｜加深库级认知地图（已有库过薄）
| # | 库名 | 笔记数 | 当前节点 | 目标节点 | 未覆盖子主题摘要 | 建议动作 |
|---:|---|---:|---:|---:|---|---|
| | | | | | | 执行加深库级地图 |

### 3｜新建或调整跨库框架
| # | 类型 | 框架 | 触发原因 | 建议动作 |
|---:|---|---|---|---|
| | 新建/强化/反驳/拆分… | | | 执行框架调整 |

**本轮无结构性待办**：（若三类皆无，写一句说明）

---

**库级地图变化（Tier B 已执行 / 拟执行）**
- 【库名】：新增/调整了哪些认知节点（人话，不是表格堆砌）
- ...

**跨库框架变化**
- 被强化：
- 被削弱/反驳：
- 新增节点：
- 观察池：

**未表态笔记（零遗漏对账）**
| 笔记 | 归档库 | 未处理原因 | 建议下轮动作 |
|---|---|---|---|
| | | | |

---

**处理统计**
| 项目 | 数量 |
|---|---:|
| 新增/待处理笔记 | |
| 已归档 | |
| 进库级地图 | |
| 进跨库框架 | |
| 进观察池/精读登记 | |
| 明确无认知价值 | |
| 未表态笔记 | |
| 精读文章处理 | |
| 发现点摘录 | |
| 用户标注未处理 | |

**精读文章**
| 文章 | 触发原因 | 核心结论 | 进入库级地图 | 进入跨库框架 | 登记位置 |
|---|---|---|---|---|---|
| | | | | | |

**发现点摘录**
| 洞察摘要 | 原文锚点 | 来源 | 可复用场景 | 进入库级地图 | 进入跨库框架 |
|---|---|---|---|---|---|
| | | | | | |

**高价值案例提炼**
| 案例 | 来源 | 可复用认知 | 可观察指标 | 应进入库级地图 | 应进入跨库框架 |
|---|---|---|---|---|---|
| | | | | | |

**框架升级候选**
| 候选框架 | 触发原因 | 证据数量 | 当前承接位置 | 建议动作 |
|---|---|---:|---|---|
| | | | | |

**Source Registry / Lint**
- 新增登记来源：
- 证据缺口：
- 反例缺口：
- 过时判断：
- 孤立节点 / KB地图缺口：
- 弱发芽：

**下一步建议**
- ...
```
