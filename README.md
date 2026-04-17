# DeckDone

**[English](README.en.md)** | 中文

面向 AI 编程工具（[opencode](https://opencode.ai)、Claude Code 等）的结构化演示文稿创建技能，专注于 15–40 页的大型、信息密集型 PPT 从零生成。

## 它做什么

DeckDone 通过 **4 阶段门控工作流** 编排整个 PPT 创建过程：

| 阶段 | 名称 | 做什么 |
|------|------|--------|
| 1 — 发现阶段 | 深度交互 | 确定目的、受众、叙事框架；收集素材；搭建大纲 |
| 2 — 设计阶段 | 逐页确认 | 分配页面类型、选择视觉风格、生成 HTML 线框图 |
| 3 — 内容阶段 | 轻量确认 | 为每页每个视觉区域撰写精确内容 |
| 4 — 实现阶段 | 批量执行 | 测试生成、批量 PPTX 生产、最终质量审查 |

每个阶段结束都设有**门控（Gate）**——用户确认交付物后方可推进，未确认则不进入下一阶段。

### 适用场景

- 构建**信息密集型演示文稿** — 年度经营计划、产品路线图、研发战略、技术架构评审
- 「**看图说话**」式演讲场景 — PPT 作为视觉辅助，演讲者对着画面讲述
- 厌倦了 AI 生成的「标题 + 3 个要点」千篇一律的演示文稿

### 设计原则

- **内容优先** — 先确定说什么，再决定怎么看
- **密度感知** — 专为每页 20–50+ 文本元素设计，而非简单要点页
- **优雅降级** — 最小依赖即可运行；可选技能（PDF、DOCX、XLSX）提升体验
- **跨会话连续** — 通过状态文件在多次 AI 对话间无缝续作

## 文件结构

```
deckdone/                              ← 仓库根目录
├── README.md                          # 说明文档（中文）
├── README.en.md                       # 说明文档（英文）
├── SETUP.md                           # 安装指南（AI 可读）
├── LICENSE                            # MIT
├── docs/                              # 设计文档
└── skills/
    └── deckdone/                      # 技能本体
        ├── SKILL.md                   # 核心工作流（~575 行）
        ├── references/
        │   ├── layout-patterns.md     # 12+ 页面类型及 HTML 骨架
        │   ├── narrative-frameworks.md # 6 种叙事框架 + 选择矩阵
        │   ├── audience-analysis.md   # 受众分析方法论
        │   ├── style-presets.md       # 18 套视觉风格预设
        │   ├── html-wireframe-guide.md # 线框图生成规范
        │   └── quality-checklist.md   # 各步骤验证清单
        └── scripts/
            ├── validate-content-plan.py # 内容计划结构验证器
            └── validate-html-slides.py  # HTML 幻灯片兼容性验证器
```

## 安装

### 方式 A：让 AI 工具自动安装（推荐）

DeckDone 包含 `SETUP.md` — 一份机器可读的安装指南。你可以让 AI 工具自动完成全部安装：

**第一步：** 先手动 clone DeckDone 到任意位置：

```bash
git clone https://github.com/anomalyco/deckdone.git
```

**第二步：** 在 AI 工具中开启新对话，发送以下指令：

```
请阅读 deckdone/SETUP.md 文件，按照其中的说明安装所有必需和可选依赖。
```

AI 会读取 `SETUP.md`，理解依赖关系图，并自动执行安装命令。

### 方式 B：opencode 项目级安装（仅当前项目可用）

如果只想在当前项目中使用 DeckDone，而不要全局安装：

```bash
# 在项目根目录下
mkdir -p .opencode/skills

# 安装 DeckDone 技能
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone
cp -r /tmp/deckdone/skills/deckdone .opencode/skills/deckdone

# 安装 pptx 技能（来自 anthropics/skills）
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/pptx .opencode/skills/pptx

# 运行时依赖仍需全局安装
npm install -g pptxgenjs playwright sharp react-icons
npx playwright install chromium
```

opencode 会自动加载项目目录下 `.opencode/skills/` 中的技能，仅对当前项目生效。

### 方式 C：手动全局安装

**前置条件：** Node.js 18+、Python 3.10+、opencode 或 Claude Code。

```bash
# 1. 安装 DeckDone 技能
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone
mkdir -p ~/.config/opencode/skills
cp -r /tmp/deckdone/skills/deckdone ~/.config/opencode/skills/deckdone

# 2. 安装必需的 pptx 技能（来自 anthropics/skills）
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/pptx ~/.config/opencode/skills/pptx

# 3. 安装运行时依赖
npm install -g pptxgenjs playwright sharp react-icons
npx playwright install chromium
```

**可选依赖**（同样来自 [anthropics/skills](https://github.com/anthropics/skills)，用于 PDF/DOCX/XLSX 内容提取和扩展样式）：

```bash
# 如果已 clone 过 anthropics/skills 则跳过这行
git clone https://github.com/anthropics/skills.git /tmp/anthropic-skills
cp -r /tmp/anthropic-skills/skills/pdf ~/.config/opencode/skills/pdf          # PDF 支持
pip install markitdown
cp -r /tmp/anthropic-skills/skills/docx ~/.config/opencode/skills/docx        # Word 文档支持
cp -r /tmp/anthropic-skills/skills/xlsx ~/.config/opencode/skills/xlsx        # 电子表格支持
cp -r /tmp/anthropic-skills/skills/theme-factory ~/.config/opencode/skills/theme-factory  # 扩展样式预设
```

### 验证安装

根据安装方式选择对应路径：

```bash
# 全局安装
python ~/.config/opencode/skills/deckdone/scripts/validate-content-plan.py --help

# 项目级安装
python .opencode/skills/deckdone/scripts/validate-content-plan.py --help
```

命令应正常输出使用说明，不报错。

## 快速开始

安装完成后，开启新对话，输入：

> 用 DeckDone 创建一个关于 [你的主题] 的演示文稿

AI 会加载技能并启动分阶段工作流 — 从目的、受众、核心信息开始逐步推进。

## 工作流示意

```
用户: "用 DeckDone 创建一份 FY26 研发计划演示文稿"
         │
  阶段 1: 发掘
  ├── 步骤 1: 简报 → 目的是什么？受众是谁？核心信息？
  ├── 步骤 2: 素材 → 收集源文档，提取关键数据
  └── 步骤 3: 大纲 → 搭建叙事骨架，估算页数
         │  （门控：用户确认大纲）
  阶段 2: 设计
  ├── 步骤 4: 页面类型 → 为每页分配布局类型
  ├── 步骤 5: 风格 → 选择视觉色板和字体
  └── 步骤 6: 线框图 → 生成 HTML 模拟稿（分批确认）
         │  （门控：用户确认所有线框图）
  阶段 3: 内容
  ├── 步骤 7: 内容计划 → 为每个区域撰写精确文本
  └── 步骤 8: 确认 → 用户审阅并修改
         │  （门控：用户确认内容）
  阶段 4: 实现
  ├── 步骤 9: 测试页面 → 每种布局类型生成一个样本
  ├── 步骤 10: 批量生成 → 分块生产所有页面
  └── 步骤 11: 最终审查 → 质量检查，输出 final.pptx
```

## 续作功能

如果对话在项目进行中中断，在新对话中输入：

> 继续我的 DeckDone 演示文稿

AI 会读取 `deckdone-state.md`，恢复上下文，从上次离开的步骤继续。

## 依赖一览

| 依赖 | 是否必需 | 用途 |
|------|---------|------|
| pptx skill | 是 | PPTX 生成引擎 |
| pptxgenjs | 是 | PowerPoint 库 |
| playwright | 是 | HTML 渲染 |
| sharp | 是 | 图标/渐变光栅化 |
| pdf skill | 否 | 从 PDF 提取文本 |
| docx skill | 否 | 从 Word 文档提取文本 |
| xlsx skill | 否 | 读取电子表格数据 |
| theme-factory skill | 否 | 扩展视觉预设 |

## 许可证

MIT
