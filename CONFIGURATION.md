# 配置说明

这 4 个 skills 是通用工作流模板，不能直接使用原作者的 Get 笔记入口。安装后需要把 `SKILL.md` 中的占位符替换为自己的笔记入口。

## 必填入口

至少配置以下 5 类笔记：

| 占位符 | 用途 |
|---|---|
| `NOTE_ID_TOTAL_INDEX` | 个人知识系统总索引 |
| `NOTE_ID_AI_FRAMEWORK` | AI、产品或解决方案框架 |
| `NOTE_ID_INVESTMENT_FRAMEWORK` | 投资研究框架；不做投资研究时可删除 |
| `NOTE_ID_GOVERNANCE_LOG` | 维护与框架变更日志 |
| `NOTE_ID_SPROUT_LOG` | 唯一的跨库发芽日志 |

## 配置步骤

1. 在 Get 笔记中创建或确定上述入口笔记。
2. 获取每条笔记的 `note_id`。
3. 在 4 个 `SKILL.md` 中搜索 `NOTE_ID_`。
4. 将占位符替换成真实 `note_id`。
5. 将示例中的个人框架名称和示例案例替换成自己的内容。
6. 保留 `https://biji.com/note/<note_id>` 或 `getnote://<note_id>` 的链接格式。
7. 运行一次只读分析，确认路由到了自己的入口笔记。
8. 再运行 maintainer；任何写入动作都应经过确认。

## Get 笔记 CLI

自行安装并登录 `getnote`，然后确认以下命令可用：

```bash
getnote kbs -o json
getnote search "测试" --limit 3 -o json
getnote note <note_id> -o json
```

不要把登录信息、Key、Token 或 Cookie 放进本仓库。

## 最小验证顺序

```text
analyzer（只读验证入口）
capturer（需要写入时先确认）
maintainer（增量维护）
sprouter（维护完成后运行）
```
