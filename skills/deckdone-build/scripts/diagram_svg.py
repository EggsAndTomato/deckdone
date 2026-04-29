#!/usr/bin/env python3
"""Pure SVG diagram generators — 14 diagram types outputting SVG strings.

Usage:
    from diagram_svg import draw_diagram, DIAGRAM_FUNCTIONS
    svg_text = draw_diagram('pyramid', data, style)

Every function returns a self-contained, fully-valid SVG string compliant with
svg-constraints.md for conversion through svg_to_pptx.
"""

import math

# ---------------------------------------------------------------------------
# Default style
# ---------------------------------------------------------------------------
DEFAULT_STYLE = {
    'primary': '#1B365D',
    'secondary': '#2E5C8A',
    'accent': '#0D7377',
    'bg': '#FFFFFF',
    'text': '#1A1A1A',
    'text_light': '#636E72',
    'text_muted': '#999999',
    'border': '#CCCCCC',
    'white': '#FFFFFF',
    'accent_light': '#0D7377',
}

# ---------------------------------------------------------------------------
# SVG canvas dimensions
# ---------------------------------------------------------------------------
CANVAS_W = 1280
CANVAS_H = 720


def _resolve_style(user_style=None):
    """Merge user style with defaults."""
    if user_style is None:
        return dict(DEFAULT_STYLE)
    merged = dict(DEFAULT_STYLE)
    merged.update(user_style)
    return merged


# ---------------------------------------------------------------------------
# SVG utility helpers
# ---------------------------------------------------------------------------

def _rrect_path(x, y, w, h, r):
    """Return an SVG path d-string for a rounded rectangle (clockwise)."""
    if r > w / 2:
        r = w / 2
    if r > h / 2:
        r = h / 2
    if r <= 0:
        return f'M{x},{y} h{w} v{h} h{-w} Z'
    return (
        f'M{x + r},{y} '
        f'h{w - 2 * r} '
        f'a{r},{r} 0 0 1 {r},{r} '
        f'v{h - 2 * r} '
        f'a{r},{r} 0 0 1 {-r},{r} '
        f'h{-w + 2 * r} '
        f'a{r},{r} 0 0 1 {-r},{-r} '
        f'v{-h + 2 * r} '
        f'a{r},{r} 0 0 1 {r},{-r} Z'
    )


def _text_element(x, y, text, font_family='Arial', font_size='14',
                  fill='#1A1A1A', text_anchor='start', font_weight='normal',
                  fill_opacity=None, letter_spacing=None):
    """Build a single <text> element string."""
    attrs = [
        f'x="{x}"', f'y="{y}"',
        f'font-family="{font_family}"',
        f'font-size="{font_size}"',
        f'fill="{fill}"',
        f'text-anchor="{text_anchor}"',
        f'font-weight="{font_weight}"',
    ]
    if fill_opacity is not None:
        attrs.append(f'fill-opacity="{fill_opacity}"')
    if letter_spacing is not None:
        attrs.append(f'letter-spacing="{letter_spacing}"')
    # Escape XML entities in text
    safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'<text {" ".join(attrs)}>{safe_text}</text>'


def _build_defs(style):
    """Build the <defs> block with gradients and drop-shadow filters."""
    prim = style.get('primary', '#1B365D')
    sec = style.get('secondary', '#2E5C8A')
    acc = style.get('accent', '#0D7377')

    lines = []
    lines.append('    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">')
    lines.append('      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>')
    lines.append('    </filter>')
    lines.append('    <filter id="lightShadow" x="-10%" y="-10%" width="120%" height="120%">')
    lines.append('      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.08"/>')
    lines.append('    </filter>')
    lines.append('    <filter id="iconDrop" x="-20%" y="-20%" width="140%" height="140%">')
    lines.append('      <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#000000" flood-opacity="0.15"/>')
    lines.append('    </filter>')
    # Gradients
    lines.append(f'    <linearGradient id="gradPrimary" x1="0%" y1="0%" x2="100%" y2="100%">')
    lines.append(f'      <stop offset="0%" style="stop-color:{prim};stop-opacity:1"/>')
    lines.append(f'      <stop offset="100%" style="stop-color:' + _darken_hex(prim, 0.85) + f';stop-opacity:1"/>')
    lines.append(f'    </linearGradient>')
    lines.append(f'    <linearGradient id="gradSecondary" x1="0%" y1="0%" x2="100%" y2="100%">')
    lines.append(f'      <stop offset="0%" style="stop-color:{sec};stop-opacity:1"/>')
    lines.append(f'      <stop offset="100%" style="stop-color:' + _darken_hex(sec, 0.85) + f';stop-opacity:1"/>')
    lines.append(f'    </linearGradient>')
    lines.append(f'    <linearGradient id="gradAccent" x1="0%" y1="0%" x2="100%" y2="100%">')
    lines.append(f'      <stop offset="0%" style="stop-color:{acc};stop-opacity:1"/>')
    lines.append(f'      <stop offset="100%" style="stop-color:' + _darken_hex(acc, 0.85) + f';stop-opacity:1"/>')
    lines.append(f'    </linearGradient>')
    # Vertical gradient for pyramid
    lines.append(f'    <linearGradient id="gradAccentV" x1="0%" y1="0%" x2="0%" y2="100%">')
    lines.append(f'      <stop offset="0%" style="stop-color:{acc};stop-opacity:1"/>')
    lines.append(f'      <stop offset="100%" style="stop-color:{prim};stop-opacity:1"/>')
    lines.append(f'    </linearGradient>')
    # Arrowhead marker
    lines.append('    <marker id="arrowRight" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">')
    lines.append(f'      <path d="M0,0 L10,4 L0,8 Z" fill="{acc}"/>')
    lines.append('    </marker>')
    lines.append('    <marker id="arrowLeft" markerWidth="10" markerHeight="8" refX="2" refY="4" orient="auto">')
    lines.append(f'      <path d="M10,0 L0,4 L10,8 Z" fill="{acc}"/>')
    lines.append('    </marker>')
    return '\n'.join(lines)


def _lighten_hex(hex_color, factor=0.7):
    """Return a lighter hex string."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f'#{r:02X}{g:02X}{b:02X}'


def _darken_hex(hex_color, factor=0.7):
    """Return a darker hex string."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f'#{r:02X}{g:02X}{b:02X}'


# ---------------------------------------------------------------------------
# Title bar — shared across diagrams
# ---------------------------------------------------------------------------

def add_title_bar(style, title, subtitle=None):
    """Return SVG elements for a page title bar with accent underline."""
    acc = style.get('accent', '#0D7377')
    txt = style.get('text', '#1A1A1A')
    light = style.get('text_light', '#636E72')
    parts = []
    parts.append(f'    <!-- Title Bar -->')
    parts.append(_text_element(60, 58, title, font_size='26',
                               fill=txt, font_weight='bold'))
    if subtitle:
        parts.append(_text_element(60, 82, subtitle, font_size='14',
                                   fill=light, font_weight='normal'))
    # Accent underline bar
    parts.append(f'    <rect x="60" y="94" width="80" height="3" fill="{acc}"/>')
    # Thin full-width line
    parts.append(f'    <line x1="60" y1="104" x2="1220" y2="104" '
                 f'stroke="{style.get("border", "#CCCCCC")}" stroke-width="1" stroke-opacity="0.5"/>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 1: Pyramid
# ======================================================================

def draw_pyramid(data, style):
    """Pyramid diagram with horizontal stacked bands, decreasing width.

    data = {'title': str, 'subtitle': str,
            'layers': [{'label': str, 'items': [str], 'color_role': str}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    layers = data.get('layers', [])
    n = len(layers)
    if n == 0:
        layers = [{'label': 'Layer 1', 'items': ['Item 1'], 'color_role': 'accent'},
                  {'label': 'Layer 2', 'items': ['Item 2'], 'color_role': 'secondary'},
                  {'label': 'Layer 3', 'items': ['Item 3'], 'color_role': 'primary'}]
        n = len(layers)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    top_y = 130
    total_h = 540
    max_w = 900
    min_w = 280
    center_x = 640

    layer_h = total_h / n - 8
    color_map = {
        'primary': s.get('primary', '#1B365D'),
        'secondary': s.get('secondary', '#2E5C8A'),
        'accent': s.get('accent', '#0D7377'),
    }
    color_ramp_default = [color_map['accent'], color_map['secondary'], color_map['primary']]

    for i, layer in enumerate(layers):
        t = i / max(n - 1, 1)
        w = max_w - (max_w - min_w) * t
        y = top_y + i * (total_h / n)
        role = layer.get('color_role', 'accent' if i == 0 else 'secondary' if i < n - 1 else 'primary')
        fill = color_map.get(role, color_ramp_default[min(i, len(color_ramp_default) - 1)])

        x = center_x - w / 2
        parts.append(f'    <!-- Layer {i + 1}: {layer.get("label", "")} -->')
        parts.append(f'    <rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" '
                     f'height="{layer_h:.0f}" fill="{fill}" filter="url(#cardShadow)"/>')
        # Label
        label_y = y + layer_h * 0.4
        parts.append(_text_element(center_x, label_y, layer.get('label', ''),
                                   font_size='18', fill=s['white'],
                                   text_anchor='middle', font_weight='bold'))
        # Items
        for j, item in enumerate(layer.get('items', [])):
            item_y = y + layer_h * 0.4 + 24 + j * 22
            if item_y < y + layer_h - 14:
                parts.append(_text_element(center_x, item_y, f'• {item}',
                                           font_size='12', fill=s['white'],
                                           text_anchor='middle', fill_opacity='0.85'))
    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 2: Hub-and-Spoke
# ======================================================================

def draw_hub_spoke(data, style):
    """Hub-and-spoke with center circle and branch cards at corners.

    data = {'title': str, 'subtitle': str,
            'center': {'label': str},
            'branches': [{'label': str, 'items': [str]}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    center_label = data.get('center', {}).get('label', 'Hub')
    branches = data.get('branches', [])
    if not branches:
        branches = [{'label': 'Branch 1', 'items': ['Item']},
                    {'label': 'Branch 2', 'items': ['Item']},
                    {'label': 'Branch 3', 'items': ['Item']},
                    {'label': 'Branch 4', 'items': ['Item']}]
    n = len(branches)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    hub_cx, hub_cy = 640, 370
    hub_r = 72

    # Corner card positions (top-left, top-right, bottom-left, bottom-right)
    base_positions = [
        (80, 130, 320, 210),
        (880, 130, 320, 210),
        (80, 420, 320, 210),
        (880, 420, 320, 210),
    ]
    # For 2 branches, use left and right centered
    if n <= 2:
        base_positions = [
            (80, 270, 320, 220),
            (880, 270, 320, 220),
        ]

    # Decorative rings
    parts.append(f'    <circle cx="{hub_cx}" cy="{hub_cy}" r="160" fill="none" '
                 f'stroke="{s["border"]}" stroke-width="1" stroke-dasharray="6,4" stroke-opacity="0.4"/>')
    parts.append(f'    <circle cx="{hub_cx}" cy="{hub_cy}" r="100" fill="none" '
                 f'stroke="{s["border"]}" stroke-width="1" stroke-dasharray="4,3" stroke-opacity="0.3"/>')

    # Center hub
    parts.append(f'    <!-- Center Hub -->')
    parts.append(f'    <circle cx="{hub_cx}" cy="{hub_cy}" r="{hub_r}" '
                 f'fill="url(#gradAccent)" filter="url(#cardShadow)"/>')
    parts.append(f'    <circle cx="{hub_cx}" cy="{hub_cy}" r="{hub_r - 18}" '
                 f'fill="none" stroke="{s["white"]}" stroke-width="1.5" stroke-opacity="0.3"/>')
    # Word-wrap center label if needed
    label_words = center_label.split()
    if len(label_words) > 2:
        mid = len(label_words) // 2
        line1 = ' '.join(label_words[:mid])
        line2 = ' '.join(label_words[mid:])
        parts.append(_text_element(hub_cx, hub_cy - 8, line1, font_size='16',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))
        parts.append(_text_element(hub_cx, hub_cy + 14, line2, font_size='16',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))
    else:
        parts.append(_text_element(hub_cx, hub_cy + 5, center_label, font_size='16',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))

    branch_colors = [s.get('accent', '#0D7377'), s.get('secondary', '#2E5C8A'),
                     s.get('primary', '#1B365D'), s.get('accent', '#0D7377')]

    for idx, branch in enumerate(branches):
        if idx >= len(base_positions):
            break
        bx, by, bw, bh = base_positions[idx]
        bc = branch_colors[min(idx, len(branch_colors) - 1)]
        blabel = branch.get('label', '')
        bitems = branch.get('items', [])

        # Card
        parts.append(f'    <!-- Branch {idx + 1}: {blabel} -->')
        path = _rrect_path(bx, by, bw, bh, 12)
        parts.append(f'    <path d="{path}" fill="{s["white"]}" '
                     f'stroke="{bc}" stroke-width="2" filter="url(#cardShadow)"/>')
        # Accent left bar
        parts.append(f'    <rect x="{bx}" y="{by}" width="5" height="{bh}" fill="{bc}"/>')
        # Title
        parts.append(_text_element(bx + 20, by + 30, blabel, font_size='16',
                                   fill=s['text'], text_anchor='start', font_weight='bold'))
        # Items
        for j, item in enumerate(bitems):
            iy = by + 58 + j * 22
            if iy < by + bh - 10:
                parts.append(_text_element(bx + 20, iy, f'• {item}', font_size='12',
                                           fill=s['text_light'], text_anchor='start'))

        # Connector from hub to card center
        ccx = bx + bw / 2
        ccy = by + bh / 2
        dx = ccx - hub_cx
        dy = ccy - hub_cy
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            # Start from edge of hub ring
            sx = hub_cx + dx * hub_r / dist
            sy = hub_cy + dy * hub_r / dist
            # End at card edge
            ex = ccx - dx * (bw / 2 + 6) / dist
            ey = ccy - dy * (bh / 2 + 6) / dist
            parts.append(f'    <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                         f'stroke="{bc}" stroke-width="2" stroke-opacity="0.3" stroke-dasharray="5,4"/>')
            # Thick background line
            parts.append(f'    <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                         f'stroke="{bc}" stroke-width="5" stroke-opacity="0.06"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 3: Dual-Gears
# ======================================================================

def draw_dual_gears(data, style):
    """Two large circles with items beside each and synergy arrow between.

    data = {'title': str, 'subtitle': str,
            'left': {'label': str, 'items': [str]},
            'right': {'label': str, 'items': [str]},
            'arrow_label': str}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    left = data.get('left', {'label': 'Left', 'items': []})
    right = data.get('right', {'label': 'Right', 'items': []})
    arrow_label = data.get('arrow_label', 'Synergy')

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    l_cx, l_cy = 360, 390
    r_cx, r_cy = 920, 390
    gear_r = 88

    # Left gear
    parts.append(f'    <!-- Left Gear -->')
    l_dark = _darken_hex(s.get('secondary', '#2E5C8A'), 0.9)
    parts.append(f'    <circle cx="{l_cx}" cy="{l_cy}" r="{gear_r}" '
                 f'fill="url(#gradSecondary)" filter="url(#cardShadow)"/>')
    parts.append(f'    <circle cx="{l_cx}" cy="{l_cy}" r="{gear_r - 14}" '
                 f'fill="none" stroke="{s["white"]}" stroke-width="1.5" stroke-opacity="0.25"/>')
    parts.append(_text_element(l_cx, l_cy + 5, left.get('label', ''), font_size='16',
                               fill=s['white'], text_anchor='middle', font_weight='bold'))
    # Left items
    for j, item in enumerate(left.get('items', [])):
        iy = 180 + j * 30
        parts.append(_text_element(60, iy, f'• {item}', font_size='13',
                                   fill=s['text_light'], text_anchor='start'))

    # Right gear
    parts.append(f'    <!-- Right Gear -->')
    parts.append(f'    <circle cx="{r_cx}" cy="{r_cy}" r="{gear_r}" '
                 f'fill="url(#gradAccent)" filter="url(#cardShadow)"/>')
    parts.append(f'    <circle cx="{r_cx}" cy="{r_cy}" r="{gear_r - 14}" '
                 f'fill="none" stroke="{s["white"]}" stroke-width="1.5" stroke-opacity="0.25"/>')
    parts.append(_text_element(r_cx, r_cy + 5, right.get('label', ''), font_size='16',
                               fill=s['white'], text_anchor='middle', font_weight='bold'))
    # Right items
    for j, item in enumerate(right.get('items', [])):
        iy = 180 + j * 30
        parts.append(_text_element(900, iy, f'• {item}', font_size='13',
                                   fill=s['text_light'], text_anchor='start'))

    # Synergy arrow/label between gears
    parts.append(f'    <!-- Synergy Arrow -->')
    arrow_y = 320
    parts.append(f'    <line x1="{l_cx + gear_r + 15}" y1="{arrow_y}" '
                 f'x2="{r_cx - gear_r - 15}" y2="{arrow_y}" '
                 f'stroke="{s["accent"]}" stroke-width="2" '
                 f'marker-end="url(#arrowRight)" marker-start="url(#arrowLeft)"/>')
    parts.append(_text_element(640, arrow_y - 10, arrow_label, font_size='13',
                               fill=s['accent'], text_anchor='middle', font_weight='bold'))
    # Gear teeth hints
    inner_r = gear_r - 6
    outer_r = gear_r + 6
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        for cx, cy, fill_col in [(l_cx, l_cy, s.get('secondary', '#2E5C8A')),
                                  (r_cx, r_cy, s.get('accent', '#0D7377'))]:
            x1 = cx + inner_r * math.cos(rad)
            y1 = cy + inner_r * math.sin(rad)
            x2 = cx + outer_r * math.cos(rad)
            y2 = cy + outer_r * math.sin(rad)
            parts.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                         f'stroke="{fill_col}" stroke-width="3" stroke-opacity="0.3"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 4: Tension-Triangle
# ======================================================================

def draw_tension_triangle(data, style):
    """Three nodes at triangle vertices with connector lines and edge labels.

    data = {'title': str, 'subtitle': str,
            'nodes': [{'label': str}],
            'edges': [{'from': int, 'to': int, 'label': str}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])

    if len(nodes) < 3:
        nodes = [{'label': 'Speed'}, {'label': 'Quality'}, {'label': 'Cost'}]
    if not edges:
        edges = [{'from': 0, 'to': 1, 'label': 'Trade-off'},
                 {'from': 1, 'to': 2, 'label': 'Tension'},
                 {'from': 2, 'to': 0, 'label': 'Balance'}]

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    # Triangle vertex positions
    top = (640, 160)
    bl = (220, 560)
    br = (1060, 560)
    positions = [top, bl, br]
    node_r = 40

    primary = s.get('primary', '#1B365D')

    # Draw edges
    for edge in edges:
        f_idx = edge.get('from', 0)
        t_idx = edge.get('to', 0)
        if 0 <= f_idx < 3 and 0 <= t_idx < 3:
            x1, y1 = positions[f_idx]
            x2, y2 = positions[t_idx]
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                ratio = (node_r + 6) / dist
                sx = x1 + dx * ratio
                sy = y1 + dy * ratio
                ex = x2 - dx * ratio
                ey = y2 - dy * ratio
            else:
                sx, sy, ex, ey = x1, y1, x2, y2
            parts.append(f'    <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                         f'stroke="{primary}" stroke-width="2" stroke-opacity="0.4"/>')
            # Edge label at midpoint
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2 - 8
            lx = mx + (mx - 640) * 0.05
            ly = my + (my - 360) * 0.05
            parts.append(_text_element(lx, ly, edge.get('label', ''), font_size='13',
                                       fill=primary, text_anchor='middle', font_weight='bold',
                                       fill_opacity='0.7'))

    # Draw nodes
    for i, node in enumerate(nodes):
        if i >= 3:
            break
        nx, ny = positions[i]
        parts.append(f'    <!-- Node {i + 1}: {node.get("label", "")} -->')
        parts.append(f'    <circle cx="{nx}" cy="{ny}" r="{node_r}" '
                     f'fill="{s["accent"]}" filter="url(#cardShadow)"/>')
        parts.append(_text_element(nx, ny + 5, node.get('label', ''),
                                   font_size='15', fill=s['white'],
                                   text_anchor='middle', font_weight='bold'))
        # Label below node
        label_y = ny + node_r + 22
        if label_y < 700:
            parts.append(_text_element(nx, label_y, node.get('label', ''),
                                       font_size='13', fill=s['text'],
                                       text_anchor='middle', font_weight='bold'))

    # Center icon
    ccx, ccy = 640, 420
    parts.append(f'    <circle cx="{ccx}" cy="{ccy}" r="20" '
                 f'fill="{s["primary"]}" filter="url(#iconDrop)"/>')
    parts.append(_text_element(ccx, ccy + 6, '\u25B2', font_size='16',
                               fill=s['white'], text_anchor='middle'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 5: Bubble-Matrix
# ======================================================================

def draw_bubble_matrix(data, style):
    """2x2 quadrant grid with sized bubbles and takeaway bar.

    data = {'title': str, 'subtitle': str,
            'x_axis': str, 'y_axis': str,
            'quadrants': {'top_left': str, 'top_right': str,
                          'bottom_left': str, 'bottom_right': str},
            'bubbles': [{'label': str, 'x': float, 'y': float, 'size': str}],
            'takeaway': str}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    x_axis = data.get('x_axis', '')
    y_axis = data.get('y_axis', '')
    quadrants = data.get('quadrants', {})
    bubbles = data.get('bubbles', [])
    takeaway = data.get('takeaway', '')

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    gx, gy = 180, 130
    gw, gh = 960, 490
    mid_x = gx + gw / 2
    mid_y = gy + gh / 2
    grid_rc = s.get('border', '#CCCCCC')

    # Grid box
    parts.append(f'    <rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" '
                 f'fill="none" stroke="{grid_rc}" stroke-width="1.5" stroke-opacity="0.5"/>')
    # Cross lines
    parts.append(f'    <line x1="{gx}" y1="{mid_y:.0f}" x2="{gx + gw}" y2="{mid_y:.0f}" '
                 f'stroke="{grid_rc}" stroke-width="1" stroke-dasharray="6,4" stroke-opacity="0.35"/>')
    parts.append(f'    <line x1="{mid_x:.0f}" y1="{gy}" x2="{mid_x:.0f}" y2="{gy + gh}" '
                 f'stroke="{grid_rc}" stroke-width="1" stroke-dasharray="6,4" stroke-opacity="0.35"/>')

    # Top-right quadrant highlight
    highlight_w = gw / 2
    highlight_h = gh / 2
    acc_light = s.get('accent_light', s.get('accent', '#0D7377'))
    parts.append(f'    <rect x="{mid_x:.0f}" y="{gy}" width="{highlight_w:.0f}" '
                 f'height="{highlight_h:.0f}" fill="{acc_light}" fill-opacity="0.06"/>')

    # Quadrant labels
    q_tl = quadrants.get('top_left', quadrants.get('q1', ''))
    q_tr = quadrants.get('top_right', quadrants.get('q2', ''))
    q_bl = quadrants.get('bottom_left', quadrants.get('q3', ''))
    q_br = quadrants.get('bottom_right', quadrants.get('q4', ''))
    parts.append(_text_element(gx + 10, gy + 20, q_tl, font_size='12',
                               fill=s['text_light'], text_anchor='start', fill_opacity='0.7'))
    parts.append(_text_element(mid_x + 10, gy + 20, q_tr, font_size='12',
                               fill=s['text_light'], text_anchor='start', fill_opacity='0.7'))
    parts.append(_text_element(gx + 10, gy + gh - 8, q_bl, font_size='12',
                               fill=s['text_light'], text_anchor='start', fill_opacity='0.7'))
    parts.append(_text_element(mid_x + 10, gy + gh - 8, q_br, font_size='12',
                               fill=s['text_light'], text_anchor='start', fill_opacity='0.7'))

    # Axis labels
    if x_axis:
        parts.append(_text_element(mid_x, gy + gh + 24, x_axis, font_size='13',
                                   fill=s['text_light'], text_anchor='middle', font_weight='bold'))
    if y_axis:
        parts.append(_text_element(gx - 80, mid_y, y_axis, font_size='13',
                                   fill=s['text_light'], text_anchor='middle', font_weight='bold',
                                   letter_spacing='2'))
        # Vertical axis arrow
        parts.append(f'    <line x1="{gx - 20}" y1="{mid_y + 40}" x2="{gx - 20}" y2="{mid_y - 40}" '
                     f'stroke="{s["text_light"]}" stroke-width="1.5" stroke-opacity="0.3"/>')
        parts.append(f'    <polygon points="{gx - 20},{mid_y - 45} {gx - 25},{mid_y - 35} '
                     f'{gx - 15},{mid_y - 35}" fill="{s["text_light"]}" fill-opacity="0.3"/>')
    # Horizontal axis arrow
    parts.append(f'    <line x1="{gx - 40}" y1="{gy + gh + 16}" x2="{gx + gw + 40}" y2="{gy + gh + 16}" '
                 f'stroke="{s["text_light"]}" stroke-width="1.5" stroke-opacity="0.3"/>')
    parts.append(f'    <polygon points="{gx + gw + 45},{gy + gh + 16} {gx + gw + 35},{gy + gh + 11} '
                 f'{gx + gw + 35},{gy + gh + 21}" fill="{s["text_light"]}" fill-opacity="0.3"/>')

    # Bubbles
    size_map = {'small': 22, 'medium': 38, 'large': 55}
    for bubble in bubbles:
        bx = float(bubble.get('x', 0.5))
        by = float(bubble.get('y', 0.5))
        bsize = str(bubble.get('size', 'medium')).lower()
        bz = size_map.get(bsize, 30)
        label = bubble.get('label', '')

        cx = gx + gw * bx
        cy = gy + gh * (1.0 - by)
        parts.append(f'    <!-- Bubble: {label} -->')
        parts.append(f'    <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{bz}" '
                     f'fill="{s["secondary"]}" stroke="{s["secondary"]}" '
                     f'stroke-width="1" filter="url(#lightShadow)" fill-opacity="0.7"/>')
        parts.append(_text_element(cx, cy + 4, label, font_size='11',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))

    # Takeaway bar
    if takeaway:
        by = 650
        path = _rrect_path(80, by, 1120, 40, 8)
        parts.append(f'    <path d="{path}" fill="{s["accent"]}" fill-opacity="0.1" '
                     f'stroke="{s["accent"]}" stroke-width="1" stroke-opacity="0.3"/>')
        parts.append(_text_element(100, by + 26, takeaway, font_size='14',
                                   fill=s['text'], text_anchor='start', font_weight='bold'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 6: Staircase
# ======================================================================

def draw_staircase(data, style):
    """Ascending stair blocks with numbered badges and dashed connectors.

    data = {'title': str, 'subtitle': str,
            'steps': [{'label': str, 'items': [str]}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    steps = data.get('steps', [])
    if not steps:
        steps = [{'label': f'Step {i + 1}', 'items': [f'Item {i + 1}']} for i in range(4)]

    n = len(steps)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    step_w = 200
    step_h = 110
    start_x = 80
    base_y = 610
    shift_x = 240
    shift_y = 120

    color_ramp = [s.get('accent', '#0D7377'), s.get('secondary', '#2E5C8A'),
                  s.get('primary', '#1B365D'),
                  _darken_hex(s.get('primary', '#1B365D'), 0.8)]

    for i, step in enumerate(steps):
        x = start_x + i * shift_x
        y = base_y - (n - i) * shift_y + shift_y

        fill = color_ramp[min(i, len(color_ramp) - 1)]

        parts.append(f'    <!-- Step {i + 1}: {step.get("label", "")} -->')
        parts.append(f'    <rect x="{x:.0f}" y="{y:.0f}" width="{step_w}" '
                     f'height="{step_h}" fill="{fill}" filter="url(#cardShadow)"/>')
        # Step label
        parts.append(_text_element(x + step_w / 2, y + 28, step.get('label', ''),
                                   font_size='14', fill=s['white'],
                                   text_anchor='middle', font_weight='bold'))
        # Items
        for j, item in enumerate(step.get('items', [])):
            iy = y + 55 + j * 20
            if iy < y + step_h - 8:
                parts.append(_text_element(x + step_w / 2, iy, f'• {item}',
                                           font_size='11', fill=s['white'],
                                           text_anchor='middle', fill_opacity='0.85'))

        # Numbered badge
        badge_cx = x + step_w / 2
        badge_cy = y - 14
        parts.append(f'    <circle cx="{badge_cx:.0f}" cy="{badge_cy:.0f}" r="16" '
                     f'fill="{s["accent"]}" filter="url(#iconDrop)"/>')
        parts.append(_text_element(badge_cx, badge_cy + 5, str(i + 1), font_size='14',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))

        # Dashed connector to next step
        if i < n - 1:
            nx = x + step_w
            ny = y - shift_y
            parts.append(f'    <line x1="{x + step_w:.0f}" y1="{y + step_h / 2:.0f}" '
                         f'x2="{nx:.0f}" y2="{ny + step_h / 2:.0f}" '
                         f'stroke="{s["border"]}" stroke-width="1.5" '
                         f'stroke-dasharray="5,5" stroke-opacity="0.4"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 7: Split-Comparison
# ======================================================================

def draw_split_comparison(data, style):
    """Two-panel comparison with vertical divider and bulleted items.

    data = {'title': str, 'subtitle': str,
            'left': {'label': str, 'items': [str]},
            'right': {'label': str, 'items': [str]}}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    left = data.get('left', {'label': 'Before', 'items': ['Item A', 'Item B']})
    right = data.get('right', {'label': 'After', 'items': ['Item X', 'Item Y']})

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    divider_x = 640
    secondary = s.get('secondary', '#2E5C8A')
    accent = s.get('accent', '#0D7377')

    # Vertical divider
    parts.append(f'    <line x1="{divider_x}" y1="130" x2="{divider_x}" y2="660" '
                 f'stroke="{s["border"]}" stroke-width="2" stroke-opacity="0.5"/>')

    # Left header
    left_label = left.get('label', '')
    parts.append(_text_element(340, 150, left_label, font_size='22',
                               fill=secondary, text_anchor='middle', font_weight='bold'))
    # Accent underline
    parts.append(f'    <rect x="250" y="160" width="180" height="3" '
                 f'fill="{secondary}" fill-opacity="0.5"/>')

    # Left items as cards
    left_items = left.get('items', [])
    sec_light = _lighten_hex(secondary, 0.6)
    for j, item in enumerate(left_items):
        iy = 195 + j * 58
        if iy > 650:
            break
        path = _rrect_path(80, iy, 520, 48, 8)
        parts.append(f'    <path d="{path}" fill="{sec_light}" '
                     f'stroke="{secondary}" stroke-width="1" fill-opacity="0.12"/>')
        parts.append(f'    <rect x="80" y="{iy}" width="5" height="48" fill="{secondary}" fill-opacity="0.3"/>')
        parts.append(_text_element(100, iy + 30, f'• {item}', font_size='14',
                                   fill=s['text'], text_anchor='start'))

    # Right header
    right_label = right.get('label', '')
    parts.append(_text_element(940, 150, right_label, font_size='22',
                               fill=accent, text_anchor='middle', font_weight='bold'))
    parts.append(f'    <rect x="850" y="160" width="180" height="3" '
                 f'fill="{accent}" fill-opacity="0.5"/>')

    # Right items as cards
    right_items = right.get('items', [])
    acc_light = _lighten_hex(accent, 0.6)
    for j, item in enumerate(right_items):
        iy = 195 + j * 58
        if iy > 650:
            break
        path = _rrect_path(680, iy, 520, 48, 8)
        parts.append(f'    <path d="{path}" fill="{acc_light}" '
                     f'stroke="{accent}" stroke-width="1" fill-opacity="0.12"/>')
        parts.append(f'    <rect x="680" y="{iy}" width="5" height="48" fill="{accent}" fill-opacity="0.3"/>')
        parts.append(_text_element(700, iy + 30, f'• {item}', font_size='14',
                                   fill=s['text'], text_anchor='start'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 8: Data-Card-Grid
# ======================================================================

def draw_data_card_grid(data, style):
    """Grid of metric cards with large value numbers.

    data = {'title': str, 'subtitle': str,
            'layout': str (e.g. '2x2', '1x4', '3x2'),
            'cards': [{'label': str, 'value': str, 'unit': str}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    cards = data.get('cards', [])
    layout = data.get('layout', '2x2')

    if not cards:
        cards = [{'label': 'Metric', 'value': '100', 'unit': '%'} for _ in range(4)]

    # Determine grid dimensions
    if layout == '1x4':
        cols, rows = min(len(cards), 4), 1
    elif layout == '3x2':
        cols, rows = 3, 2
    else:
        cols, rows = 2, min(2, (len(cards) + 1) // 2)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    margin_x = 60
    margin_y = 130
    gap = 20
    avail_w = CANVAS_W - 2 * margin_x - (cols - 1) * gap
    avail_h = 530 - (rows - 1) * gap
    card_w = avail_w / cols
    card_h = avail_h / rows

    for idx, card in enumerate(cards):
        col = idx % cols
        row = idx // cols
        if row >= rows:
            break

        x = margin_x + col * (card_w + gap)
        y = margin_y + row * (card_h + gap)
        value_text = str(card.get('value', ''))
        unit_text = card.get('unit', '')
        label_text = card.get('label', '')

        # Rounded card background
        rpath = _rrect_path(x, y, card_w, card_h, 12)
        parts.append(f'    <!-- Card {idx + 1}: {label_text} -->')
        parts.append(f'    <path d="{rpath}" fill="{s["white"]}" '
                     f'stroke="{s["primary"]}" stroke-width="1.5" filter="url(#cardShadow)"/>')
        # Accent top bar
        parts.append(f'    <path d="{_rrect_path(x, y, card_w, 6, 6)}" '
                     f'fill="{s["accent"]}" fill-opacity="0.7"/>')
        # Large value
        parts.append(_text_element(x + card_w / 2, y + card_h * 0.4 + 8, value_text,
                                   font_size='38', fill=s['accent'],
                                   text_anchor='middle', font_weight='bold'))
        # Unit
        if unit_text:
            parts.append(_text_element(x + card_w / 2, y + card_h * 0.62, unit_text,
                                       font_size='13', fill=s['text_light'],
                                       text_anchor='middle'))
        # Label
        parts.append(_text_element(x + card_w / 2, y + card_h * 0.82, label_text,
                                   font_size='14', fill=s['text'],
                                   text_anchor='middle', font_weight='bold'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 9: Layered-Architecture
# ======================================================================

def draw_layered_architecture(data, style):
    """Horizontal stacked blocks with layer labels and nested subcomponents.

    data = {'title': str, 'subtitle': str,
            'layers': [{'label': str, 'subcomponents': [{'label': str}]}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    layers = data.get('layers', [])
    if not layers:
        layers = [{'label': 'Presentation', 'subcomponents': [{'label': 'Web'}, {'label': 'Mobile'}]},
                  {'label': 'Application', 'subcomponents': [{'label': 'API'}, {'label': 'Services'}]},
                  {'label': 'Data', 'subcomponents': [{'label': 'DB'}, {'label': 'Cache'}]}]

    n = len(layers)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    start_y = 130
    total_h = 530
    layer_h = total_h / n - 10
    left_w = 200
    right_x = 280
    right_w = 940
    gap = 10

    color_ramp = [
        s.get('secondary', '#2E5C8A'),
        s.get('primary', '#1B365D'),
        s.get('primary', '#1B365D'),
        s.get('primary', '#1B365D'),
    ]

    for i, layer in enumerate(layers):
        y = start_y + i * (layer_h + gap)
        fill = color_ramp[min(i, len(color_ramp) - 1)]

        # Layer label block (left)
        lbw = left_w
        parts.append(f'    <!-- Layer {i + 1}: {layer.get("label", "")} -->')
        parts.append(f'    <rect x="60" y="{y:.0f}" width="{lbw}" height="{layer_h:.0f}" '
                     f'fill="{fill}" filter="url(#lightShadow)"/>')
        parts.append(_text_element(60 + lbw / 2, y + layer_h / 2 + 5,
                                   layer.get('label', ''), font_size='14',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))

        # Subcomponents
        subcomponents = layer.get('subcomponents', [])
        sub_n = len(subcomponents)
        if sub_n == 0:
            continue
        sub_gap = 15
        sub_w = (right_w - (sub_n - 1) * sub_gap) / sub_n
        for j, sub in enumerate(subcomponents):
            sx = right_x + j * (sub_w + sub_gap)
            sy = y + 8
            sh = layer_h - 16
            light_fill = _lighten_hex(fill, 0.5)
            rpath = _rrect_path(sx, sy, sub_w, sh, 8)
            parts.append(f'    <path d="{rpath}" fill="{light_fill}" '
                         f'stroke="{fill}" stroke-width="1" fill-opacity="0.9"/>')
            parts.append(_text_element(sx + sub_w / 2, sy + sh / 2 + 5,
                                       sub.get('label', ''), font_size='13',
                                       fill=s['white'], text_anchor='middle', font_weight='bold'))
        # Layer connector arrow
        if i < n - 1:
            ay = y + layer_h + gap / 2
            parts.append(f'    <line x1="400" y1="{ay}" x2="400" y2="{ay + gap / 2}" '
                         f'stroke="{fill}" stroke-width="1.5" stroke-opacity="0.3"/>')
            parts.append(f'    <polygon points="396,{ay + gap / 2 - 4} 400,{ay + gap / 2 + 2} '
                         f'404,{ay + gap / 2 - 4}" fill="{fill}" fill-opacity="0.3"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 10: Filter-Funnel
# ======================================================================

def draw_filter_funnel(data, style):
    """Centered trapezoids of decreasing width, with labels and items.

    data = {'title': str, 'subtitle': str,
            'layers': [{'label': str, 'items': [str], 'width': float}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    layers = data.get('layers', [])
    if not layers:
        layers = [
            {'label': 'Stage 1', 'items': ['All leads (100%)'], 'width': 1.0},
            {'label': 'Stage 2', 'items': ['Qualified (70%)'], 'width': 0.7},
            {'label': 'Stage 3', 'items': ['Engaged (40%)'], 'width': 0.4},
            {'label': 'Stage 4', 'items': ['Converted (25%)'], 'width': 0.25},
        ]

    n = len(layers)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    center_x = 640
    top_y = 140
    total_h = 520
    gap = 8
    layer_h = total_h / n - gap
    max_w = 800
    min_w = 200

    # Gradient colors for funnel
    grad_stops = [
        _lighten_hex(s.get('accent', '#0D7377'), 0.5),
        _lighten_hex(s.get('secondary', '#2E5C8A'), 0.4),
        s.get('secondary', '#2E5C8A'),
        s.get('primary', '#1B365D'),
    ]

    for i, layer in enumerate(layers):
        w_top = max_w * (layer.get('width', 1.0 - i / max(n, 1) * 0.25))
        if i < n - 1:
            next_w = max_w * (layers[i + 1].get('width', 1.0 - (i + 1) / max(n, 1) * 0.25))
        else:
            next_w = w_top * 0.6

        y_top = top_y + i * (layer_h + gap)
        y_bottom = y_top + layer_h

        fill = grad_stops[min(i, len(grad_stops) - 1)]
        text_color = s.get('text', '#1A1A1A') if i == 0 else s['white']

        # Trapezoid path
        x1 = center_x - w_top / 2
        x2 = center_x + w_top / 2
        x3 = center_x + next_w / 2
        x4 = center_x - next_w / 2

        parts.append(f'    <!-- Funnel layer {i + 1}: {layer.get("label", "")} -->')
        path_d = f'M{x1:.0f},{y_top:.0f} L{x2:.0f},{y_top:.0f} L{x3:.0f},{y_bottom:.0f} L{x4:.0f},{y_bottom:.0f} Z'
        parts.append(f'    <path d="{path_d}" fill="{fill}" filter="url(#cardShadow)"/>')
        # Label
        ly = y_top + layer_h * 0.4
        parts.append(_text_element(center_x, ly, layer.get('label', ''),
                                   font_size='15', fill=text_color,
                                   text_anchor='middle', font_weight='bold'))
        # Items
        for j, item in enumerate(layer.get('items', [])):
            iy = ly + 22 + j * 22
            if iy < y_bottom - 8:
                parts.append(_text_element(center_x, iy, f'• {item}',
                                           font_size='12', fill=text_color,
                                           text_anchor='middle',
                                           fill_opacity=None if text_color == s['white'] else '0.85'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 11: Overlapping-Spheres
# ======================================================================

def draw_overlapping_spheres(data, style):
    """2-3 overlapping circles (Venn-style) with intersection labels.

    data = {'title': str, 'subtitle': str,
            'circles': [{'label': str}],
            'overlap_labels': {'0_1': str, '0_2': str, '1_2': str, '0_1_2': str}}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    circles = data.get('circles', [])
    overlap_labels = data.get('overlap_labels', {})

    if len(circles) < 2:
        circles = [{'label': 'Area A'}, {'label': 'Area B'}]

    n_circles = len(circles)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    fills = [
        s.get('secondary', '#2E5C8A'),
        s.get('accent', '#0D7377'),
        s.get('primary', '#1B365D'),
    ]

    if n_circles == 2:
        r = 140
        c1_x, c1_y = 480, 400
        c2_x, c2_y = 800, 400

        parts.append(f'    <circle cx="{c1_x}" cy="{c1_y}" r="{r}" '
                     f'fill="{fills[0]}" stroke="{fills[0]}" stroke-width="2" '
                     f'fill-opacity="0.35" filter="url(#lightShadow)"/>')
        parts.append(f'    <circle cx="{c2_x}" cy="{c2_y}" r="{r}" '
                     f'fill="{fills[1]}" stroke="{fills[1]}" stroke-width="2" '
                     f'fill-opacity="0.35" filter="url(#lightShadow)"/>')

        parts.append(_text_element(c1_x - r * 0.5, c1_y - 20,
                                   circles[0].get('label', ''),
                                   font_size='18', fill=s['text'],
                                   text_anchor='middle', font_weight='bold'))
        parts.append(_text_element(c2_x + r * 0.5, c2_y - 20,
                                   circles[1].get('label', ''),
                                   font_size='18', fill=s['text'],
                                   text_anchor='middle', font_weight='bold'))

        # Overlap label
        overlap = overlap_labels.get('0_1', '')
        if overlap:
            parts.append(_text_element((c1_x + c2_x) / 2, 400,
                                       overlap, font_size='14',
                                       fill=s.get('primary', '#1B365D'),
                                       text_anchor='middle', font_weight='bold'))
    else:
        # 3 circles in triangle arrangement
        r = 120
        cx, cy_center = 640, 390
        positions = [
            (cx, cy_center - 100),
            (cx - 130, cy_center + 70),
            (cx + 130, cy_center + 70),
        ]
        for i in range(min(3, n_circles)):
            px, py = positions[i]
            fill = fills[min(i, len(fills) - 1)]
            parts.append(f'    <circle cx="{px}" cy="{py}" r="{r}" '
                         f'fill="{fill}" stroke="{fill}" stroke-width="2" '
                         f'fill-opacity="0.35" filter="url(#lightShadow)"/>')
            # Label offset from circle center
            if i == 0:
                lx, ly = px, py - r - 30
            elif i == 1:
                lx, ly = px - r - 40, py + 30
            else:
                lx, ly = px + r + 40, py + 30
            parts.append(_text_element(lx, ly, circles[i].get('label', ''),
                                       font_size='16', fill=s['text'],
                                       text_anchor='middle', font_weight='bold'))

        center_label = overlap_labels.get('0_1_2', '')
        if center_label:
            parts.append(_text_element(cx, cy_center + 5, center_label,
                                       font_size='14', fill=s.get('primary', '#1B365D'),
                                       text_anchor='middle', font_weight='bold'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 12: Iterative-Cycle
# ======================================================================

def draw_iterative_cycle(data, style):
    """Steps at 90° intervals around center, with arrow connectors.

    data = {'title': str, 'subtitle': str,
            'steps': [{'label': str}],
            'center_label': str}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    steps = data.get('steps', [])
    center_label = data.get('center_label', 'Cycle')

    if not steps:
        steps = [{'label': 'Plan'}, {'label': 'Do'}, {'label': 'Check'}, {'label': 'Act'}]

    n = len(steps)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    cx, cy = 640, 400
    radius = 210
    node_r = 38
    step_colors = [s.get('accent', '#0D7377'), s.get('secondary', '#2E5C8A'),
                   s.get('primary', '#1B365D'),
                   _darken_hex(s.get('primary', '#1B365D'), 0.8)]

    # Decorative rings
    parts.append(f'    <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
                 f'stroke="{s["border"]}" stroke-width="1.5" stroke-dasharray="8,5" stroke-opacity="0.35"/>')

    positions = []
    for i in range(n):
        angle = -math.pi / 2 + 2 * math.pi * i / n
        nx = cx + radius * math.cos(angle)
        ny = cy + radius * math.sin(angle)
        positions.append((nx, ny))

    # Arrow connectors using path arcs
    for i in range(n):
        x1, y1 = positions[i]
        x2, y2 = positions[(i + 1) % n]
        # Compute mid-angle for curved path
        angle1 = -math.pi / 2 + 2 * math.pi * i / n
        angle2 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        mid_angle = (angle1 + angle2) / 2
        # Handle wrap-around
        if angle2 < angle1:
            mid_angle += math.pi
        arrow_r = radius - node_r - 8
        ax1 = cx + arrow_r * math.cos(angle1 + 0.12)
        ay1 = cy + arrow_r * math.sin(angle1 + 0.12)
        ax2 = cx + arrow_r * math.cos(angle2 - 0.12)
        ay2 = cy + arrow_r * math.sin(angle2 - 0.12)
        # Quadratic curve for curved arrow
        mid_px = cx + (radius + 30) * math.cos(mid_angle)
        mid_py = cy + (radius + 30) * math.sin(mid_angle)
        sc = step_colors[min(i, len(step_colors) - 1)]
        parts.append(f'    <path d="M{ax1:.0f},{ay1:.0f} Q{mid_px:.0f},{mid_py:.0f} {ax2:.0f},{ay2:.0f}" '
                     f'fill="none" stroke="{sc}" stroke-width="2" stroke-opacity="0.35"/>')
        # Arrowhead
        parts.append(f'    <polygon points="{ax2:.0f},{ay2:.0f} {ax2 - 6:.0f},{ay2 + 4:.0f} '
                     f'{ax2 - 6:.0f},{ay2 - 4:.0f}" fill="{sc}" fill-opacity="0.35" '
                     f'transform="rotate({math.degrees(angle2)},{ax2:.0f},{ay2:.0f})"/>')

    # Nodes
    for i, step in enumerate(steps):
        nx, ny = positions[i]
        sc = step_colors[min(i, len(step_colors) - 1)]
        parts.append(f'    <!-- Step {i + 1}: {step.get("label", "")} -->')
        parts.append(f'    <circle cx="{nx:.0f}" cy="{ny:.0f}" r="{node_r}" '
                     f'fill="{sc}" filter="url(#cardShadow)"/>')
        parts.append(_text_element(nx, ny + 5, str(i + 1), font_size='16',
                                   fill=s['white'], text_anchor='middle', font_weight='bold'))
        # Label outside
        angle = -math.pi / 2 + 2 * math.pi * i / n
        lx = cx + (radius + 70) * math.cos(angle)
        ly = cy + (radius + 70) * math.sin(angle) + 5
        parts.append(_text_element(lx, ly, step.get('label', ''), font_size='14',
                                   fill=s['text'], text_anchor='middle', font_weight='bold'))

    # Center circle
    parts.append(f'    <circle cx="{cx}" cy="{cy}" r="50" '
                 f'fill="url(#gradPrimary)" filter="url(#cardShadow)"/>')
    parts.append(_text_element(cx, cy + 5, center_label, font_size='14',
                               fill=s['white'], text_anchor='middle', font_weight='bold'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 13: Bridge-Gap
# ======================================================================

def draw_bridge_gap(data, style):
    """Left current-state box, right future-state box, bridge in middle.

    data = {'title': str, 'subtitle': str,
            'current': {'label': str, 'items': [str]},
            'future': {'label': str, 'items': [str]},
            'bridge': {'label': str, 'items': [str]},
            'gap_analysis': str}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    current = data.get('current', {'label': 'Current State', 'items': ['Point A', 'Point B']})
    future = data.get('future', {'label': 'Future State', 'items': ['Point X', 'Point Y']})
    bridge = data.get('bridge', {'label': 'Bridge', 'items': ['Step 1', 'Step 2']})
    gap_analysis = data.get('gap_analysis', '')

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    # Current state (left)
    cbx, cby, cbw, cbh = 60, 140, 350, 440
    secondary = s.get('secondary', '#2E5C8A')
    parts.append(f'    <!-- Current State -->')
    parts.append(f'    <rect x="{cbx}" y="{cby}" width="{cbw}" height="{cbh}" '
                 f'fill="{secondary}" filter="url(#cardShadow)"/>')
    parts.append(_text_element(cbx + cbw / 2, cby + 35, current.get('label', ''),
                               font_size='18', fill=s['white'],
                               text_anchor='middle', font_weight='bold'))
    parts.append(f'    <line x1="{cbx + 30}" y1="{cby + 50}" x2="{cbx + cbw - 30}" '
                 f'y2="{cby + 50}" stroke="{s["white"]}" stroke-width="1" stroke-opacity="0.3"/>')
    for j, item in enumerate(current.get('items', [])):
        iy = cby + 75 + j * 32
        parts.append(_text_element(cbx + 25, iy, f'• {item}', font_size='13',
                                   fill=s['white'], text_anchor='start', fill_opacity='0.9'))

    # Future state (right)
    fbx, fby, fbw, fbh = 870, 140, 350, 440
    accent = s.get('accent', '#0D7377')
    parts.append(f'    <!-- Future State -->')
    parts.append(f'    <rect x="{fbx}" y="{fby}" width="{fbw}" height="{fbh}" '
                 f'fill="{accent}" filter="url(#cardShadow)"/>')
    parts.append(_text_element(fbx + fbw / 2, fby + 35, future.get('label', ''),
                               font_size='18', fill=s['white'],
                               text_anchor='middle', font_weight='bold'))
    parts.append(f'    <line x1="{fbx + 30}" y1="{fby + 50}" x2="{fbx + fbw - 30}" '
                 f'y2="{fby + 50}" stroke="{s["white"]}" stroke-width="1" stroke-opacity="0.3"/>')
    for j, item in enumerate(future.get('items', [])):
        iy = fby + 75 + j * 32
        parts.append(_text_element(fbx + 25, iy, f'• {item}', font_size='13',
                                   fill=s['white'], text_anchor='start', fill_opacity='0.9'))

    # Bridge (center card)
    bbx, bby, bbw, bbh = 440, 180, 400, 320
    bridge_label = bridge.get('label', 'Bridge')
    parts.append(f'    <!-- Bridge -->')
    brpath = _rrect_path(bbx, bby, bbw, bbh, 12)
    parts.append(f'    <path d="{brpath}" fill="{s["white"]}" '
                 f'stroke="{accent}" stroke-width="2" filter="url(#cardShadow)"/>')
    # Bridge header bar
    parts.append(f'    <rect x="{bbx}" y="{bby}" width="{bbw}" height="40" '
                 f'fill="{accent}" fill-opacity="0.12"/>')
    parts.append(_text_element(bbx + bbw / 2, bby + 27, bridge_label,
                               font_size='16', fill=s['text'],
                               text_anchor='middle', font_weight='bold'))
    for j, item in enumerate(bridge.get('items', [])):
        iy = bby + 60 + j * 28
        parts.append(_text_element(bbx + 25, iy, f'• {item}', font_size='13',
                                   fill=s['text_light'], text_anchor='start'))

    # Arrows from current -> bridge -> future
    arrow_y = 300
    parts.append(f'    <line x1="{cbx + cbw + 5}" y1="{arrow_y}" '
                 f'x2="{bbx - 5}" y2="{arrow_y}" stroke="{accent}" stroke-width="2" '
                 f'marker-end="url(#arrowRight)"/>')
    parts.append(f'    <line x1="{bbx + bbw + 5}" y1="{arrow_y}" '
                 f'x2="{fbx - 5}" y2="{arrow_y}" stroke="{accent}" stroke-width="2" '
                 f'marker-end="url(#arrowRight)"/>')

    # Gap analysis card
    if gap_analysis:
        gy = 610
        grpath = _rrect_path(120, gy, 1040, 60, 10)
        parts.append(f'    <!-- Gap Analysis -->')
        parts.append(f'    <path d="{grpath}" fill="{s["white"]}" '
                     f'stroke="{s["border"]}" stroke-width="1.5" filter="url(#lightShadow)"/>')
        parts.append(f'    <rect x="120" y="{gy}" width="5" height="60" fill="{accent}" fill-opacity="0.6"/>')
        parts.append(_text_element(145, gy + 21, 'Gap Analysis', font_size='14',
                                   fill=s['text'], text_anchor='start', font_weight='bold'))
        parts.append(_text_element(145, gy + 42, gap_analysis, font_size='12',
                                   fill=s['text_light'], text_anchor='start'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram 14: Timeline
# ======================================================================

def draw_timeline_diagram(data, style):
    """Horizontal timeline with event nodes, dates above and descriptions below.

    data = {'title': str, 'subtitle': str,
            'events': [{'date': str, 'desc': str}]}
    """
    s = _resolve_style(style)
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')
    events = data.get('events', [])
    if not events:
        events = [{'date': '2020', 'desc': 'Foundation'},
                  {'date': '2021', 'desc': 'Launch'},
                  {'date': '2022', 'desc': 'Growth'},
                  {'date': '2023', 'desc': 'Scale'},
                  {'date': '2024', 'desc': 'Expand'}]

    n = len(events)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
                 f'width="{CANVAS_W}" height="{CANVAS_H}">')
    parts.append('  <defs>')
    parts.append(_build_defs(s))
    parts.append('  </defs>')
    parts.append(f'  <rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="{s["bg"]}"/>')
    parts.append(add_title_bar(s, title, subtitle))

    line_y = 400
    line_x1 = 140
    line_x2 = 1140
    accent = s.get('accent', '#0D7377')

    # Main timeline
    parts.append(f'    <line x1="{line_x1}" y1="{line_y}" x2="{line_x2}" y2="{line_y}" '
                 f'stroke="{accent}" stroke-width="3" stroke-opacity="0.6"/>')

    spacing = (line_x2 - line_x1) / max(n - 1, 1)
    node_r = 16

    for i, event in enumerate(events):
        nx = line_x1 + spacing * i

        # Node (circle)
        parts.append(f'    <!-- Event {i + 1}: {event.get("date", "")} -->')
        parts.append(f'    <circle cx="{nx:.1f}" cy="{line_y}" r="{node_r}" '
                     f'fill="{accent}" filter="url(#iconDrop)"/>')
        parts.append(f'    <circle cx="{nx:.1f}" cy="{line_y}" r="{node_r - 6}" '
                     f'fill="{s["bg"]}" stroke="{accent}" stroke-width="1.5" stroke-opacity="0.5"/>')

        # Date above
        dy = line_y - node_r - 30
        # Connector line to date
        parts.append(f'    <line x1="{nx:.1f}" y1="{line_y - node_r}" '
                     f'x2="{nx:.1f}" y2="{dy + 24}" '
                     f'stroke="{accent}" stroke-width="1" stroke-opacity="0.3"/>')
        parts.append(_text_element(nx, dy, event.get('date', ''),
                                   font_size='14', fill=accent,
                                   text_anchor='middle', font_weight='bold'))

        # Description below
        ey = line_y + node_r + 28
        parts.append(f'    <line x1="{nx:.1f}" y1="{line_y + node_r}" '
                     f'x2="{nx:.1f}" y2="{ey - 4}" '
                     f'stroke="{accent}" stroke-width="1" stroke-opacity="0.2"/>')
        # Truncate long descriptions
        desc = event.get('desc', '')
        max_chars = 35
        if len(desc) > max_chars * 2:
            # Two-line split
            mid = len(desc) // 2
            parts.append(_text_element(nx, ey, desc[:mid].strip(),
                                       font_size='12', fill=s['text_light'],
                                       text_anchor='middle'))
            parts.append(_text_element(nx, ey + 18, desc[mid:].strip(),
                                       font_size='12', fill=s['text_light'],
                                       text_anchor='middle'))
        else:
            parts.append(_text_element(nx, ey, desc,
                                       font_size='12', fill=s['text_light'],
                                       text_anchor='middle'))

    parts.append('</svg>')
    return '\n'.join(parts)


# ======================================================================
# Diagram dispatch table
# ======================================================================

DIAGRAM_FUNCTIONS = {
    'pyramid': draw_pyramid,
    'hub_spoke': draw_hub_spoke,
    'dual_gears': draw_dual_gears,
    'tension_triangle': draw_tension_triangle,
    'bubble_matrix': draw_bubble_matrix,
    'staircase': draw_staircase,
    'split_comparison': draw_split_comparison,
    'data_card_grid': draw_data_card_grid,
    'layered_architecture': draw_layered_architecture,
    'filter_funnel': draw_filter_funnel,
    'overlapping_spheres': draw_overlapping_spheres,
    'iterative_cycle': draw_iterative_cycle,
    'bridge_gap': draw_bridge_gap,
    'timeline_diagram': draw_timeline_diagram,
}


def draw_diagram(diagram_type, data=None, style=None):
    """Dispatch to the correct diagram SVG renderer.

    Args:
        diagram_type: str key into DIAGRAM_FUNCTIONS.
        data: dict with type-specific content keys.
        style: optional dict with style overrides (hex color strings).

    Returns:
        SVG string ready for svg_to_pptx conversion.

    Raises:
        KeyError: if diagram_type is not registered.
    """
    func = DIAGRAM_FUNCTIONS.get(diagram_type)
    if func is None:
        raise KeyError(
            f"Unknown diagram type '{diagram_type}'. "
            f"Available: {', '.join(sorted(DIAGRAM_FUNCTIONS.keys()))}"
        )
    resolved_style = _resolve_style(style)
    return func(data or {}, resolved_style)
