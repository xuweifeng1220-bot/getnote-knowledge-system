# Get 笔记知识系统 Skills

可通过 `npx skills add` 安装到 Codex、Claude Code、Cursor 等兼容 Agent 的公开 skill 仓库模板。

这是一套围绕 Get 笔记构建个人外脑的 4 个 Codex skills：

1. `getnote-knowledge-analyzer`：调用知识框架和证据笔记进行分析，只读不写。
2. `getnote-knowledge-capturer`：把经过确认的 AI 对话、方法和新知识回流到 Get 笔记。
3. `getnote-knowledge-maintainer`：定期整理新增笔记，更新知识库地图、框架、来源登记和治理日志。
4. `getnote-knowledge-sprouter`：跨知识库关联，生成经过两轮拷问的“萌芽”认知、产品机会和研究方向。

## 推荐使用顺序

日常分析：

```text
getnote-knowledge-analyzer
```

定期维护外脑：

```text
getnote-knowledge-maintainer -> getnote-knowledge-sprouter
```

需要把 AI 对话或成熟成果保存回 Get 笔记时：

```text
getnote-knowledge-capturer -> getnote-knowledge-maintainer
```

## 安装

发布到 GitHub 后，用户可以安装全部 skills：

```bash
npx skills add xuweifeng1220-bot/getnote-knowledge-system
```

也可以只安装一个 skill：

```bash
npx skills add xuweifeng1220-bot/getnote-knowledge-system --skill getnote-knowledge-analyzer
```

安装后重启对应 Agent。

如果不使用 `npx skills`，也可以手动复制：

将 `skills/` 下的 4 个目录复制到目标 Codex 的 skills 目录：

```bash
cp -R skills/getnote-knowledge-analyzer "$CODEX_HOME/skills/"
cp -R skills/getnote-knowledge-capturer "$CODEX_HOME/skills/"
cp -R skills/getnote-knowledge-maintainer "$CODEX_HOME/skills/"
cp -R skills/getnote-knowledge-sprouter "$CODEX_HOME/skills/"
```

如果目标环境没有设置 `CODEX_HOME`，请将其替换为实际的 Codex skills 目录。

## 使用前必须个性化

当前 skill 是从一个真实个人知识系统导出的，仍包含原知识系统的：

- 总索引、框架、治理日志和发芽日志标题；
- Get 笔记 `note_id` 和 `biji.com` 链接；
- 面向投资、AI 解决方案和个人外脑的示例内容。

具体配置方法见 [CONFIGURATION.md](CONFIGURATION.md)。接收者至少需要替换：

1. `Known framework notes` / `Known system notes`。
2. 总索引、治理日志、发芽日志等入口笔记的 `note_id`。
3. 个人知识库名称、框架名称和来源登记。
4. 仅属于原作者的案例、行业方向或示例链接。

不建议直接把当前 note_id 当作他人的入口，否则会把分析路由到原作者的知识库结构。

## 依赖

- Codex 或兼容的 skill 加载器。
- 已安装并登录的 Get 笔记 CLI：`getnote`。
- maintainer 使用的 `scripts/kb_scan.py` 需要 Python 3。

## 安全边界

本仓库不包含 Get 笔记 Key、Token、Cookie、密码或账号凭据。使用者必须在本机自行完成 Get 笔记登录。不要把任何密钥写入 `SKILL.md`、Git 仓库或公开 issue。

## 写入安全

这 4 个 skill 保留了写入前确认机制。尤其是新建框架、更新框架笔记、更新发芽日志和加入知识库，都应先展示计划和影响，获得用户确认后再执行。

## 目录结构

```text
skills/
├── getnote-knowledge-analyzer/
├── getnote-knowledge-capturer/
├── getnote-knowledge-maintainer/
│   ├── references/token-efficient-maintenance.md
│   └── scripts/kb_scan.py
└── getnote-knowledge-sprouter/
```
