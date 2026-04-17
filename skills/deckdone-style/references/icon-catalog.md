# Icon Catalog — Semantic Mapping

Reference for Step 7 (Content Plan). Maps content themes and page zones to specific icon names from the bundled Tabler Icons set.

## Usage

During content planning, match each zone's semantic theme to an icon below. If no exact match exists, use the closest category. Every icon name must correspond to a file in `references/icons/{name}.svg`.

---

## By Content Theme

| Theme | Icon Name | Also Good For |
|-------|-----------|---------------|
| growth / revenue | trending-up | KPI, increase, improvement |
| decline / decrease | trending-down | loss, reduction, risk |
| strategy / plan | target | goals, focus, objective |
| team / collaboration | users-group | teamwork, group, collective |
| individual / person | user | personal, individual, member |
| leadership / management | crown | executive, authority, C-suite |
| technology / IT | code | software, engineering, dev |
| infrastructure | server | hardware, backend, hosting |
| data / database | database | storage, records, persistence |
| cloud / networking | cloud | internet, SaaS, remote |
| AI / machine learning | robot | automation, ML, intelligent |
| analytics / data viz | chart-bar | statistics, metrics, reporting |
| trends / time series | chart-line | progress, trajectory, forecast |
| pie / proportions | chart-pie | distribution, segments, share |
| communication | message | chat, messaging, dialog |
| email / outreach | mail | contact, newsletter, inbox |
| presentation / public speaking | presentation | slides, keynote, talk |
| announcement | megaphone | broadcast, promotion, alert |
| finance / budget | coin | money, cost, pricing |
| investment | chart-candle | trading, market, portfolio |
| receipt / billing | receipt | invoice, payment, transaction |
| process / workflow | list-check | steps, procedure, operations |
| settings / configuration | settings | preferences, options, control |
| refresh / update | refresh | reload, sync, retry |
| timeline / roadmap | clock | schedule, deadline, timing |
| schedule / calendar | calendar | date, event, planning |
| security / protection | shield | safety, compliance, guard |
| risk / warning | alert-triangle | caution, danger, attention |
| success / achievement | trophy | win, award, recognition |
| failure / error | x | cancel, reject, remove |
| approval / correct | check | confirm, validate, done |
| innovation / idea | rocket | launch, startup, breakthrough |
| learning / education | school | training, course, academy |
| knowledge / docs | book | documentation, manual, guide |
| creativity / design | pencil | edit, write, create |
| tool / utility | tool | build, fix, utility |
| speed / performance | bolt | fast, energy, power |
| growth / nature | leaf | eco, green, organic |
| energy / enthusiasm | flame | passion, hot, trending |
| celebration / milestone | stars | highlight, featured, premium |
| global / international | world | worldwide, global, earth |
| connection / link | link | URL, reference, association |
| download | download | import, retrieve, save |
| upload | upload | export, publish, deploy |
| search / find | search | query, lookup, discover |
| filter / refine | filter | narrow, sort, criteria |
| lock / privacy | lock | secure, private, restricted |
| unlock / open | lock-open | access, permission, granted |
| folder / organize | folder | directory, collection, group |
| copy / duplicate | copy | clone, replicate, backup |
| external / outbound | external-link | open, redirect, outside |
| arrow / direction | arrow-right | next, proceed, continue |
| expand / detail | chevron-right | drill-down, show-more, navigate |
| checklist | checklist | task-list, todo, validation |
| notification | bell | alert, remind, notify |
| heart / favorite | heart | like, love, endorse |
| star / rating | star | review, score, premium |
| flag / milestone | flag | marker, milestone, important |
| home / start | home | landing, dashboard, main |
| briefcase / business | briefcase | work, corporate, professional |
| question / help | help | support, FAQ, assistance |
| info / information | info-circle | details, about, context |
| plus / add | plus | create, new, insert |
| minus / remove | minus | delete, reduce, subtract |

---

## By Page Type Defaults

Icons that should be selected when no specific theme override is needed.

| Page Type | Default Icon |
|-----------|-------------|
| Cover | (match presentation topic from brief) |
| Agenda | list-check |
| Section Divider | (match section theme) |
| Content-Text | (none required) |
| Content-TwoCol | (none required) |
| Data-Chart | chart-bar |
| Quote | star |
| Timeline | clock |
| Comparison | scale (or chevron-right vs chevron-left) |
| Closing | flag |
| Composite-Diagram | (match diagram topic) |
| Pipeline-Flow | arrow-right |

---

## By Page Zone

Guidance for icon sizes in specific page positions.

| Zone Position | Icon Size | When to Use |
|---------------|-----------|-------------|
| Slide title prefix | 32–48pt | Always on Cover, Section Divider; optional elsewhere |
| Bullet point prefix | 16pt | Recommended for Content-Text and Content-TwoCol H2 items |
| Timeline event node | 24pt | Always; replaces text marker |
| Pipeline stage header | 32pt | Always; top of each stage card |
| Comparison column header | 24pt | Recommended for each side |
| Composite-Diagram subsystem | 20pt | Recommended for subsystem labels |
| Chart interpretation | 16pt | Optional; insight/lightbulb icon |

---

## Icon Naming Convention

All icon names use kebab-case matching the Tabler Icons outline set naming:
- Valid: `trending-up`, `chart-bar`, `list-check`
- Invalid: `TrendingUp`, `chart_bar`, `listcheck`

To verify an icon exists: check for `references/icons/{name}.svg` file.
To find new icons: browse https://tabler.io/icons (use outline style names).
