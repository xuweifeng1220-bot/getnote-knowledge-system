---
name: getnote-knowledge-capturer
description: Capture high-value AI conversation outputs, pasted text, specified files, or specified notes back into Get笔记 as human-readable knowledge notes. Use when the user asks to 回流, 沉淀, 保存到Get笔记, capture, or turn an AI-generated insight/framework/method/skill design into a durable note; do not use for ordinary analysis or framework maintenance.
---

# Getnote Knowledge Capturer

## Overview

Use this skill to turn valuable AI-generated content or user-specified material into **human-readable** Get笔记 knowledge assets.

This skill is the external-brain **ingestion gate**: it decides what is worth saving, drafts a readable note after user confirmation, and writes it to the correct knowledge base.

- Use `getnote-knowledge-analyzer` for analysis.
- Use `getnote-knowledge-maintainer` for classification, source registry, framework updates, and maintenance metadata.
- Use `getnote-knowledge-sprouter` for cross-knowledge sprouts after maintenance.

## First Principle: Write for Humans, Not for AI

The saved note is a **reading artifact** for the user future self, not a schema dump for downstream agents.

This principle is shared across the getnote-knowledge series. `getnote-knowledge-maintainer`, `getnote-knowledge-analyzer`, and `getnote-knowledge-sprouter` also separate **人读层** (body) from **机器层** (maintenance zone at note end). Capturer is the ingestion entry point for human-readable content.

Default posture:

- Lead with **what was learned**, not how the note was processed.
- Prefer flowing sections over numbered maintenance modules (`01｜维护信号`, `04｜来源与引用谱系`, etc.).
- Put **主体内容、主要认知、推导逻辑、有价值要点** in the note body.
- Do **not** fill the note with provenance forms, evidence-strength checklists, or maintainer workflow fields unless the user explicitly asks.

Downstream skills already own the machine-oriented work:

| Concern | Owner skill |
|---|---|
| 库级认知地图、来源登记、引用谱系、证据强度 | `getnote-knowledge-maintainer` |
| 框架关系、纳入跨库框架、治理日志 | `getnote-knowledge-maintainer` |
| 跨库发芽、机会卡片 | `getnote-knowledge-sprouter` |
| 基于库级地图与框架的论证式分析 | `getnote-knowledge-analyzer` |

Capturer may mention source in **one short line** at the end (book title, conversation topic, file name). Do not expand into a full lineage section in the saved note.

## Core Boundary

This skill may:

- Capture the current conversation's high-value output.
- Capture user-pasted text.
- Capture a user-specified local file only after a plan and explicit approval.
- Capture or update a user-specified Get笔记 note.
- Create a new Get笔记 note for a new topic.
- Update an existing captured note for the same continuing topic.
- Add lightweight tags such as `#AI回流`, `#读书笔记`, or topic tags.
- Recommend later `maintainer` processing in the **confirmation chat only**.

This skill must not:

- Automatically scan local files.
- Automatically scan all Get笔记 notes.
- Update framework notes directly.
- Classify all recent notes or maintain knowledge bases in bulk.
- Save the full raw chat by default.
- Rewrite source/evidence notes unless the user explicitly asks to update that note.
- Write maintainer-only metadata blocks into the saved note by default.

## Required Confirmation

Before any write operation, present a short human-readable preview:

- Suggested action: new note or update existing note.
- Target title.
- Suggested knowledge base.
- Draft content to write (the actual reading experience).

Wait for explicit user approval before calling `getnote save`, `getnote note update`, or `getnote kb add`.

Do **not** require the user to review source-lineage forms, evidence-strength tables, or maintainer checklists before writing. Those belong in chat only when genuinely uncertain.

## Input Modes

1. **Current conversation capture**: capture the useful conclusions from the ongoing thread.
2. **Pasted content capture**: capture text the user provides directly.
3. **Specified file capture**: read a named local file only after plan and approval.
4. **Specified note capture/update**: read or update a Get笔记 note only after plan and approval.

Default behavior: do not scan local files or all Get笔记 notes.

## New Note vs Existing Note

Default rule: update an existing captured note for the same continuing topic; create a new note only when the topic clearly forks.

Update an existing note when:

- The same framework, method, skill, project, book, or judgment is being refined.
- The new content changes the latest conclusion, usage method, boundary, or main body.
- Future retrieval would naturally search for the same title/topic.

Create a new note when:

- The object of analysis changes.
- The use case changes.
- The knowledge-base ownership changes.
- The new topic deserves independent retrieval.

When unsure, ask the user to confirm the target note instead of silently creating duplicates.

Search before creating: `getnote search "<topic> #AI回流" --limit 10 -o json`

## Capture Note Format

Use this default structure. Section order may adapt to content type, but always keep the note **readable as a standalone article**.

```markdown
# 标题

> 一句话说明这篇笔记是什么、解决什么问题。（可选）

## 核心结论

1-3 段或 3-5 条 bullet。先给最重要的新认知，让读者 30 秒内知道值不值得继续读。

## 推导链路

说明「为什么得到上面的结论」：
- 前提 / 背景
- 关键逻辑步骤
- 最终判断

用自然语言写，不要写成表单。

## 原文摘录

保留关键原文、定义、金句、反直觉判断。
不保存完整闲聊、确认语和重复推导。

金句优先使用对称锚定，便于 maintainer 后续抽取：

【金】关键原句或段落【金】

## 主体内容

沉淀下来的**主体材料**：框架、章节梳理、方法步骤、对比表、法则清单、案例要点等。
这是笔记最长的部分，也是未来最常回看的部分。

按内容类型组织，例如：
- 书籍 / 长文：章节要点、核心观点、速查表
- 方法 / skill：步骤、原则、示例
- 分析 / 判断：对象、结论、论据、风险

## 使用场景

以后遇到什么问题、做什么决策时，应该回来读这篇笔记。

## 适用边界

什么时候不能直接套用；哪些结论依赖特定市场、时期、对象或前提。

---

来源：<书名 / 对话主题 / 文件名 / Get笔记 note_id>（一行即可）
#AI回流 #主题标签
```

### What Goes Where

**Must be in the saved note**

- 核心结论
- 推导链路
- 原文摘录 / 金句
- 主体内容（章节、方法、表格、清单等）
- 使用场景
- 适用边界

**Optional in the saved note**

- 与主流/旧认知的对比表
- 速查清单（如「20 条法则」）
- 本地化/落地提示（若对用户有价值）
- 一行来源说明
- 少量 tags

**Do not put in the saved note by default**

- `01｜维护信号`
- `04｜来源与引用谱系`
- 证据强度 / 来源完整度表单
- `05｜后续动作`
- `06｜版本记录`
- `状态：待 maintainer 复核`
- `#待框架复核`

If the user explicitly wants provenance or maintenance blocks, add them only after confirmation.

### Content-Type Adaptations

Keep the same human-readable spine; adjust **主体内容** only.

**书籍 / 长文梳理**

- 核心观点
- 分章/分部分要点
- 速查清单或对照表
- 保留金句摘录 + 推导链路

**方法 / 框架 / skill 设计**

- 原则
- 步骤
- 示例
- 边界

**分析 / 投资 / 产品判断**

- 对象
- 结论
- 论据
- 风险与反例

**对话沉淀**

- 先写结论，再写论证，最后写可执行要点
- 不要把聊天记录贴进正文

## Raw Text Policy

Do not save the full conversation by default.

Use:

- **原文摘录** for key phrases, definitions, or decisions.
- **主体内容** for structured knowledge the user will reread.
- **核心结论 / 推导链路** for reusable judgment.

Save full raw text only when the user explicitly asks, or when exact wording has legal, investment, project, or evidence value.

## Tags and Maintainer Handoff

Default tags on saved notes:

- `#AI回流` — provenance marker for maintainer scans
- one or two topic tags, e.g. `#读书笔记`, `#投资`, `#方法`

Do **not** require `#待框架复核` in the note body. Maintainer discovers AI回流 notes through tags, knowledge-base placement, and periodic scans.

In the confirmation chat after a successful write, you may briefly say:

- suggested knowledge base
- whether maintainer review may be useful (maintainer will update the relevant `知识库认知地图｜【库名】` and promote to cross-library frameworks when thresholds are met)

Keep that out of the note unless the user asks.

## Get笔记 Commands

- Create note: `getnote save "<content>" --title "<title>" -o json`
- Read note: `getnote note <note_id> -o json`
- Update note: `getnote note update <note_id> --content "<content>" -o json`
- Add note to knowledge base: `getnote kb add <topic_id> <note_id>`
- List knowledge bases: `getnote kbs -o json`
- Search existing captured notes: `getnote search "<topic> #AI回流" --limit 10 -o json`

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

## Capture Report Template

Use this in chat before writing. It is for confirmation, not for copying into the note.

```markdown
**拟沉淀笔记**
- 方式：新建 / 更新
- 标题：
- 知识库：
- 更新理由（若更新）：

**读者会先看到什么**
- 核心结论：（1-2 句）
- 主体内容包含：（如：章节梳理 + 20 条法则 + 对照表）

**拟写入正文预览**
（直接贴将要写入 Get笔记 的正文，或其主要部分）
```

## Quality Bar

Before presenting the draft or writing:

1. Would a human reread this note in 3 months and still understand the main point?
2. Is the **主体内容** substantial enough, not just a summary skin over empty metadata?
3. Are conclusion and derivation separated clearly?
4. Are golden quotes wrapped with `【金】...【金】` when they matter?
5. Did you avoid turning the note into an AI processing form?

If the conversation produced both a long梳理 and reusable judgment, include **both** — not one at the expense of the other.

## Reference Example

The preferred shape is close to a good book note:

1. 核心结论
2. 推导链路
3. 原文摘录（金句）
4. 全书/全文主体梳理
5. 使用场景 + 适用边界
6. 一行来源 + tags

Not:

1. 维护信号
2. 原文摘录
3. 二次整理
4. 来源与引用谱系
5. 后续动作
6. 版本记录
