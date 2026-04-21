# Layout Skeleton Format — ASCII Wireframe Conventions

Reference for layout skeleton generation and review. Used during layout planning to communicate page structure before HTML wireframing.

---

## 1. ASCII Box Drawing Characters

### Character Set

| Purpose | Characters | Notes |
|---------|-----------|-------|
| Single-line corners | `┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘` | Inner zones, standard containers |
| Single-line edges | `│ ─` | Vertical and horizontal borders |
| Double-line corners | `╔ ╗ ╚ ╝` | Outer container only (Composite-Diagram) |
| Double-line edges | `║ ═` | Outer container borders |
| Arrow connectors | `→` | Pipeline-Flow stage separators |
| T-junctions | `┬ ┴ ├ ┤ ┼` | Multi-zone splits |

### Diagram Constraints

- **Max diagram width:** 72 characters (including borders).
- **Max diagram height:** 20 rows per page template.
- Use monospace alignment — assume all characters are equal width.
- Pad zone content with spaces to maintain box alignment.
- Every diagram must be a closed rectangle (no open edges).

---

## 2. Zone Label Syntax

Each zone inside an ASCII box uses this format:

```
[type] Content summary (weight)
```

### Fields

| Field | Required | Values |
|-------|----------|--------|
| type | Yes | `title`, `subtitle`, `body`, `bullet-list`, `data-table`, `chart-area`, `image-area`, `quote`, `timeline-item`, `comparison-col`, `icon-grid`, `label` |
| Content summary | Yes | Noun phrase, max 80 chars. Describes intent, not exact copy. |
| weight | Yes | `primary`, `secondary`, `auxiliary` |

### Examples

```
[title] Q3 revenue results (primary)
[bullet-list] Three growth drivers with supporting data (secondary)
[chart-area] Bar chart — revenue by region (primary)
[label] Confidential — internal use only (auxiliary)
[comparison-col] Option B features and trade-offs (secondary)
```

### Multi-line Zones

When a zone spans multiple rows, repeat the type and weight on the first line, then continue content with indent:

```
[body] Key findings from user research study spanning (secondary)
       three geographic markets and 500 participants
```

---

## 3. Overview Table Schema

Every layout skeleton set must include a summary table:

```markdown
| # | Type | Title | Key Content | Zones |
|---|------|-------|-------------|-------|
| 1 | Cover | Q3 Strategy Review | Annual performance summary | 3 |
| 2 | Agenda | Today's Topics | Four discussion areas | 5 |
| 3 | Section Divider | Market Overview | Section break | 2 |
```

### Column Rules

- **#**: Page number, sorted sequentially.
- **Type**: Must match a valid page type from `layout-types.md`.
- **Title**: Slide title text.
- **Key Content**: Max 60 chars. Summarizes the single most important message.
- **Zones**: Total zone count for the page.

---

## 4. Per-Page-Type Default Layouts

### 4.1 Cover — 3 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│         [title] Presentation title — max 60 chars (primary)      │
│                                                                  │
│       [subtitle] Supporting tagline or date (secondary)          │
│                                                                  │
│              [label] Author or event name (auxiliary)            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Agenda — 5 Zones (Two-Column Grid)

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Agenda or session overview (primary)                     │
├─────────────────────────────┬────────────────────────────────────┤
│ [bullet-list]               │ [bullet-list]                      │
│ Section 1 name + page ref   │ Section 3 name + page ref          │
│ (secondary)                 │ (secondary)                        │
├─────────────────────────────┼────────────────────────────────────┤
│ [bullet-list]               │ [bullet-list]                      │
│ Section 2 name + page ref   │ Section 4 name + page ref          │
│ (secondary)                 │ (secondary)                        │
└─────────────────────────────┴────────────────────────────────────┘
```

### 4.3 Section Divider — 2 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                                                                  │
│    [title] Section title — max 40 chars (primary)                │
│                                                                  │
│    [body] Brief section description or context (secondary)       │
│                                                                  │
│                                                                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.4 Content-Text — 3–7 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Page topic — max 60 chars (primary)                      │
├──────────────────────────────────────────────────────────────────┤
│ [bullet-list] First key point with context (secondary)           │
│ [bullet-list] Second key point with context (secondary)          │
│ [bullet-list] Third key point with context (secondary)           │
│ [bullet-list] Fourth key point with context (secondary)          │
│ [bullet-list] Fifth key point with context (secondary)           │
├──────────────────────────────────────────────────────────────────┤
│ [label] Source or footnote (auxiliary)                           │
└──────────────────────────────────────────────────────────────────┘
```

### 4.5 Content-TwoCol — 4–6 Zones, 50/50 Split

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Page topic — max 60 chars (primary)                      │
├───────────────────────────────┬──────────────────────────────────┤
│ [bullet-list]                │ [bullet-list]                     │
│ Left column heading and      │ Right column heading and          │
│ supporting points            │ supporting points                 │
│ (secondary)                  │ (secondary)                       │
│                              │                                   │
│ [body]                       │ [body]                            │
│ Additional context or        │ Additional context or             │
│ detail for left side         │ detail for right side             │
│ (secondary)                  │ (secondary)                       │
├───────────────────────────────┴──────────────────────────────────┤
│ [label] Source or footnote (auxiliary)                           │
└──────────────────────────────────────────────────────────────────┘
```

### 4.6 Data-Chart — 4 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Chart title and takeaway (primary)                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [chart-area] Chart type — subject measured across dims (primary)│
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ [body] One-line interpretation of the data (secondary)           │
├──────────────────────────────────────────────────────────────────┤
│ [label] Data source and date (auxiliary)                         │
└──────────────────────────────────────────────────────────────────┘
```

### 4.7 Quote — 2 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                                                                  │
│    [quote] Inspirational or authoritative quotation text          │
│    spanning up to 180 characters maximum length (primary)        │
│                                                                  │
│                                                                  │
│           [body] Attribution — speaker name, role (secondary)    │
│                                                                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.8 Timeline — 3–9 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Timeline title and scope (primary)                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐         │
│  │[timeline│   │[timeline│   │[timeline│   │[timeline│         │
│  │-item]   │───│-item]   │───│-item]   │───│-item]   │         │
│  │Q1 event │   │Q2 event │   │Q3 event │   │Q4 event │         │
│  │date +   │   │date +   │   │date +   │   │date +   │         │
│  │desc     │   │desc     │   │desc     │   │desc     │         │
│  │(sec.)   │   │(sec.)   │   │(sec.)   │   │(sec.)   │         │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Max 6 events horizontal, 8 events vertical. Vertical layout stacks events with connecting `│` lines between them.

### 4.9 Comparison — 3–4 Zones, 50/50 Split

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Comparison title — what is being compared (primary)      │
├─────────────────────────────┬────────────────────────────────────┤
│ [comparison-col]            │ [comparison-col]                   │
│ Option A heading            │ Option B heading                   │
│ (secondary)                 │ (secondary)                        │
├─────────────────────────────┼────────────────────────────────────┤
│ [body] Criteria 1: value A  │ [body] Criteria 1: value B         │
│ (secondary)                 │ (secondary)                        │
├─────────────────────────────┼────────────────────────────────────┤
│ [body] Criteria 2: value A  │ [body] Criteria 2: value B         │
│ (secondary)                 │ (secondary)                        │
├─────────────────────────────┴────────────────────────────────────┤
│ [label] Assessment note or methodology (auxiliary)               │
└──────────────────────────────────────────────────────────────────┘
```

Max 6 criteria rows. Each row is a pair of `[body]` zones.

### 4.10 Closing — 3 Zones

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                                                                  │
│    [title] Key takeaway or call to action (primary)              │
│                                                                  │
│    [body] Supporting message or next steps detail (secondary)    │
│                                                                  │
│                                                                  │
│              [label] Contact info or date (auxiliary)            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.11 Composite-Diagram — 3–15 Zones, Double-Line Outer

Uses `╔ ╗ ╚ ╝ ║ ═` for the outer container and `┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘ │ ─` for inner zones. Max 3 nesting levels.

**Realistic example — Microservice architecture with 2 subsystems:**

```
╔══════════════════════════════════════════════════════════════════╗
║ [title] System architecture overview (primary)                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║ ┌─── API Gateway (3 components) ──────────────────────────────┐ ║
║ │ [body]         │ [body]            │ [body]                  │ ║
║ │ Auth service   │ Rate limiter      │ Route dispatcher        │ ║
║ │ (secondary)    │ (secondary)       │ (secondary)             │ ║
║ └────────────────┴──────────────────┴─────────────────────────┘ ║
║                                                                  ║
║ ┌─── Core Services (4 components) ─────────────────────────────┐ ║
║ │  ┌──────────────┐  ┌──────────────┐                          │ ║
║ │  │ [body]       │  │ [body]       │                          │ ║
║ │  │ User service │  │ Order service│                          │ ║
║ │  │ (secondary)  │  │ (secondary)  │                          │ ║
║ │  └──────────────┘  └──────────────┘                          │ ║
║ │  ┌──────────────┐  ┌──────────────┐                          │ ║
║ │  │ [body]       │  │ [body]       │                          │ ║
║ │  │ Payment svc  │  │ Notification │                          │ ║
║ │  │ (secondary)  │  │ (secondary)  │                          │ ║
║ │  └──────────────┘  └──────────────┘                          │ ║
║ └──────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Nesting level rules:**
- Level 1 (double-line `╔╗╚╝║═`): Outer page container — always present.
- Level 2 (single-line `┌┬┐├┼┤└┴┘│─`): Subsystem or major group — labeled with subsystem name + component count.
- Level 3 (single-line, lighter grouping): Individual components — labeled with `[body]` zone per component.

### 4.12 Pipeline-Flow — 3–13 Zones, Arrow Connectors

Uses `→` between stages. Max 6 stages per row, max 2 rows.

```
┌──────────────────────────────────────────────────────────────────┐
│ [title] Pipeline or process title (primary)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│ │[body]    │   │[body]    │   │[body]    │   │[body]    │      │
│ │ Stage 1  │──→│ Stage 2  │──→│ Stage 3  │──→│ Stage 4  │      │
│ │ name and │   │ name and │   │ name and │   │ name and │      │
│ │ desc     │   │ desc     │   │ desc     │   │ desc     │      │
│ │(secondary│   │(secondary│   │(secondary│   │(secondary│      │
│ └──────────┘   └──────────┘   └──────────┘   └──────────┘      │
│                                                                  │
│ ┌──────────┐   ┌──────────┐                                     │
│ │[body]    │   │[body]    │                                     │
│ │ Stage 5  │──→│ Stage 6  │                                     │
│ │ name and │   │ name and │                                     │
│ │ desc     │   │ desc     │                                     │
│ │(secondary│   │(secondary│                                     │
│ └──────────┘   └──────────┘                                     │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ [label] Process owner or SLA reference (auxiliary)               │
└──────────────────────────────────────────────────────────────────┘
```

**Arrow connector rules:**
- Place `──→` (3 chars: 2 horizontal lines + arrow) between horizontally adjacent stages.
- Between rows, use vertical alignment — first stage of row 2 connects below last stage of row 1.
- Leave at least 3 spaces of padding between stage boxes and arrows.

---

## 5. Content Summary Writing Guidelines

### Rules

1. **Use noun phrases**, not full sentences. Write "Q3 revenue by region", not "This chart shows Q3 revenue by region".
2. **Max 80 characters** per content summary line. If intent cannot fit, split into a multi-line zone.
3. **Describe intent, not exact copy.** Write "Three growth drivers with supporting data", not "bullet 1: markets grew 15%".
4. **Chart areas include type + subject.** Write "Bar chart — revenue by region", "Pie chart — market share by segment", "Line chart — monthly active users over 12 months".
5. **Composite sub-zones include subsystem name + component count.** Write "API Gateway (3 components)", "Data Layer (2 components)".
6. **Avoid generic labels.** Do not write "text goes here" or "content TBD". Every zone must communicate what it represents.
7. **Timeline events use date + short description.** Write "Q1 2025 — Product launch in 3 markets", not "Event 1".
8. **Comparison cells use criteria + value.** Write "Pricing: $29/mo", not "value".
9. **Pipeline stages use action verb + object.** Write "Build artifact from source", not "Step 1".
10. **Auxiliary zones state their purpose.** Write "Source — World Bank 2025 report", not "footer text".
