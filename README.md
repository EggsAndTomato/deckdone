# DeckDone

**[English](README.en.md)** | 中文

面向 AI 编程工具（[opencode](https://opencode.ai)、Claude Code 等）的结构化演示文稿创建技能，专注于 15–40 页的大型、信息密集型 PPT 从零生成。

## 核心思路

把"说什么"和"看起来怎样"彻底分开：

- **Plan 阶段**（Steps 1-5）：只管内容和结构。最后一步用 HTML 线框图 + 浏览器实时刷新，让你边看边讨论内容，确认完毕后导出内容合同。
- **Build 阶段**（Steps 6-8）：只管视觉。选完风格后批量生成所有页面，每一步都锁定设计参数保证一致性。

中间用 markdown 文件衔接，Build 阶段零创意决策，机械执行 Plan 的产出。

## 适用场景

- 信息密集型演示文稿 — 年度经营计划、产品路线图、研发战略、技术架构评审
- 「看图说话」式演讲 — PPT 作为视觉辅助，演讲者对着画面讲述
- 厌倦了 AI 生成的「标题 + 3 个要点」千篇一律的演示文稿

## 工作流

```
用户: "用 DeckDone 创建一份 FY26 研发计划演示文稿"
         │
  Plan · 步骤 1: 简报 → 目的？受众？核心信息？
  Plan · 步骤 2: 素材 → 收集源文档，提取数据
  Plan · 步骤 3: 大纲 → 叙事骨架，估算页数
         │  ✓ 用户确认
  Plan · 步骤 4: 页面类型 → 为每页分配布局
  Plan · 步骤 5: 内容线框图 → 浏览器实时审阅，逐页确认内容
         │  ✓ 用户确认
  Build · 步骤 6: 风格 + 测试 → 选配色字体，生成测试页
  Build · 步骤 7: 批量生成 → 逐页 SVG 生成，质量审查
  Build · 步骤 8: 导出 → final.pptx + 演讲指南
```

每一步都有门控，用户不确认就不往下走。完成后如果需要改，Revision Mode 支持单页修改、全局换色、增删页面。

## 安装

```bash
git clone https://github.com/anomalyco/deckdone.git /tmp/deckdone
mkdir -p ~/.config/opencode/skills
cp -r /tmp/deckdone/skills/deckdone-plan ~/.config/opencode/skills/
cp -r /tmp/deckdone/skills/deckdone-build ~/.config/opencode/skills/
pip install python-pptx lxml
```

如果需要从 PDF/DOCX/XLSX 提取素材，额外安装 [anthropics/skills](https://github.com/anthropics/skills) 中的 pdf、docx、xlsx 技能。

## 快速开始

安装完成后，开启新对话：

> 用 DeckDone 创建一个关于 FY26 研发计划的演示文稿

AI 会从目的、受众、核心信息开始逐步推进。

## 续作

对话中断后，在新对话中输入：

> 继续我的 DeckDone 演示文稿

AI 会读取状态文件，从上次离开的步骤继续。

## 依赖

| 依赖 | 必需 | 用途 |
|------|------|------|
| python-pptx | 是 | PPTX 生成 |
| lxml | 是 | SVG 解析 |
| pdf skill | 否 | PDF 素材提取 |
| docx skill | 否 | Word 素材提取 |
| xlsx skill | 否 | 表格数据提取 |

## 许可证

MIT
