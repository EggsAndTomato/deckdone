"""
SmartArt Template Injector — copies complete diagram templates into a PPTX.

Usage:
    from smartart_inject import inject
    inject('input.pptx', 'output.pptx', slide_index=0, template_name='pyramid1')

The injector works by:
    1. Scanning the template library to build a name→folder mapping
    2. Copying all 5 XML files (data, layout, drawing, colors, quickStyle) into the PPTX
    3. Adding Content_Types entries for all 5 files
    4. Adding 5 relationships to the target slide's rels
    5. Adding a graphicFrame to the target slide's XML

Uses the complete drawing.xml from the template library — no minimal layout XML,
no URI-based layout references. This ensures WPS can render the diagram.
"""

import zipfile, re, os
from pathlib import Path
from collections import defaultdict
from io import BytesIO
from typing import Optional

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / 'templates' / 'smartart'

# ── SmartArt Color Schemes ──
# Maps DeckDone style-preset "vibe" to SmartArt color scheme URIs.
# AI selects the best match based on the user's chosen style preset.

SMARTART_COLOR_SCHEMES = {
    # Vibrant multi-color
    'colorful':    'urn:microsoft.com/office/officeart/2005/8/colors/colorful1',
    'colorful1':   'urn:microsoft.com/office/officeart/2005/8/colors/colorful1',
    'colorful2':   'urn:microsoft.com/office/officeart/2005/8/colors/colorful2',
    'colorful3':   'urn:microsoft.com/office/officeart/2005/8/colors/colorful3',
    # Accent-based (single color family)
    'accent1':     'urn:microsoft.com/office/officeart/2005/8/colors/accent1',
    'accent1_2':   'urn:microsoft.com/office/officeart/2005/8/colors/accent1_2',
    'accent1_3':   'urn:microsoft.com/office/officeart/2005/8/colors/accent1_3',
    # Dark themes
    'dark1':       'urn:microsoft.com/office/officeart/2005/8/colors/dark1',
    'dark2':       'urn:microsoft.com/office/officeart/2005/8/colors/dark2',
}

def _lighten(hex_color, pct):
    """Lighten a hex color by percentage (0-100)."""
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, int(r + (255 - r) * pct / 100))
    g = min(255, int(g + (255 - g) * pct / 100))
    b = min(255, int(b + (255 - b) * pct / 100))
    return f'{r:02X}{g:02X}{b:02X}'

def _darken(hex_color, pct):
    """Darken a hex color by percentage (0-100)."""
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = max(0, int(r * (1 - pct / 100)))
    g = max(0, int(g * (1 - pct / 100)))
    b = max(0, int(b * (1 - pct / 100)))
    return f'{r:02X}{g:02X}{b:02X}'

# Style-preset → recommended SmartArt color scheme + drawing color mapping
# Maps schemeClr references in drawing.xml to actual hex colors from style-presets
# accent4/accent5/accent6 are auto-derived via _lighten/_darken from accent1/2/3
STYLE_TO_SMARTART_COLOR = {
    # Corporate/professional
    'Corporate Blue': ('accent1_2', {
        'accent1': '1B365D',  # Primary
        'accent2': '2E5C8A',  # Secondary
        'accent3': 'E8A838',  # Accent
        'accent4': '5F728D',  # lighten(accent1, 30%)
        'accent5': '6C8CAD',  # lighten(accent2, 30%)
        'accent6': 'B9862C',  # darken(accent3, 20%)
    }),
    'Steel Gray': ('accent1', {
        'accent1': '2D3436',  # Primary
        'accent2': '636E72',  # Secondary
        'accent3': '0984E3',  # Accent
        'accent4': '6C7072',  # lighten(accent1, 30%)
        'accent5': '91999C',  # lighten(accent2, 30%)
        'accent6': '0769B5',  # darken(accent3, 20%)
    }),
    'Navy Gold': ('accent1_2', {
        'accent1': '1B2838',  # Primary
        'accent2': '2C3E50',  # Secondary
        'accent3': 'D4AF37',  # Accent
        'accent4': '5F6873',  # lighten(accent1, 30%)
        'accent5': '6B7784',  # lighten(accent2, 30%)
        'accent6': 'A98C2C',  # darken(accent3, 20%)
    }),
    'Arctic Blue': ('accent1_2', {
        'accent1': '2980B9',  # Primary
        'accent2': '3498DB',  # Secondary
        'accent3': 'E67E22',  # Accent
        'accent4': '69A6CE',  # lighten(accent1, 30%)
        'accent5': '70B6E5',  # lighten(accent2, 30%)
        'accent6': 'B8641B',  # darken(accent3, 20%)
    }),
    'Dark Carbon': ('dark1', {
        'accent1': '1A1A2E',  # Primary
        'accent2': '16213E',  # Secondary
        'accent3': '0F3460',  # Accent
        'accent4': '5E5E6C',  # lighten(accent1, 30%)
        'accent5': '5B6377',  # lighten(accent2, 30%)
        'accent6': '0C294C',  # darken(accent3, 20%)
        'lt1': '0A0A14',     # Background
        'dk1': 'E0E0E0',     # Text
    }),
    'Clean White': ('accent1', {
        'accent1': '333333',  # Primary
        'accent2': '666666',  # Secondary
        'accent3': '0066CC',  # Accent
        'accent4': '707070',  # lighten(accent1, 30%)
        'accent5': '939393',  # lighten(accent2, 30%)
        'accent6': '0051A3',  # darken(accent3, 20%)
    }),
    'Royal Indigo': ('accent1_2', {
        'accent1': '4B0082',  # Primary
        'accent2': '6A0DAD',  # Secondary
        'accent3': 'FFD700',  # Accent
        'accent4': '814CA7',  # lighten(accent1, 30%)
        'accent5': '9655C5',  # lighten(accent2, 30%)
        'accent6': 'CCAC00',  # darken(accent3, 20%)
    }),
    # Warm/creative
    'Sunset Warmth': ('colorful1', {
        'accent1': 'E76F51',  # Primary
        'accent2': 'F4A261',  # Secondary
        'accent3': '264653',  # Accent
        'accent4': 'EE9A85',  # lighten(accent1, 30%)
        'accent5': 'F7BD90',  # lighten(accent2, 30%)
        'accent6': '1E3842',  # darken(accent3, 20%)
    }),
    'Ocean Teal': ('colorful2', {
        'accent1': '0D7377',  # Primary
        'accent2': '14A3A8',  # Secondary
        'accent3': 'FF6B35',  # Accent
        'accent4': '559D9F',  # lighten(accent1, 30%)
        'accent5': '5ABEC2',  # lighten(accent2, 30%)
        'accent6': 'CC552A',  # darken(accent3, 20%)
    }),
    'Forest Green': ('colorful2', {
        'accent1': '2D6A4F',  # Primary
        'accent2': '40916C',  # Secondary
        'accent3': 'D4A373',  # Accent
        'accent4': '6C9683',  # lighten(accent1, 30%)
        'accent5': '79B298',  # lighten(accent2, 30%)
        'accent6': 'A9825C',  # darken(accent3, 20%)
    }),
    'Terracotta Earth': ('colorful2', {
        'accent1': 'A0522D',  # Primary
        'accent2': 'CD853F',  # Secondary
        'accent3': '2E4057',  # Accent
        'accent4': 'BC856C',  # lighten(accent1, 30%)
        'accent5': 'DCA978',  # lighten(accent2, 30%)
        'accent6': '243345',  # darken(accent3, 20%)
    }),
    'Warm Sand': ('colorful2', {
        'accent1': 'C19A6B',  # Primary
        'accent2': 'DEB887',  # Secondary
        'accent3': '8B4513',  # Accent
        'accent4': 'D3B897',  # lighten(accent1, 30%)
        'accent5': 'E7CDAB',  # lighten(accent2, 30%)
        'accent6': '6F370F',  # darken(accent3, 20%)
    }),
    # Bold/impact
    'Midnight Purple': ('colorful3', {
        'accent1': '2D1B69',  # Primary
        'accent2': '5B3E96',  # Secondary
        'accent3': 'FFB627',  # Accent
        'accent4': '6C5F96',  # lighten(accent1, 30%)
        'accent5': '8C77B5',  # lighten(accent2, 30%)
        'accent6': 'CC911F',  # darken(accent3, 20%)
    }),
    'Cherry Red': ('colorful1', {
        'accent1': 'C0392B',  # Primary
        'accent2': 'E74C3C',  # Secondary
        'accent3': '2C3E50',  # Accent
        'accent4': 'D2746A',  # lighten(accent1, 30%)
        'accent5': 'EE8176',  # lighten(accent2, 30%)
        'accent6': '233140',  # darken(accent3, 20%)
    }),
    'Crimson Elite': ('colorful3', {
        'accent1': '8B0000',  # Primary
        'accent2': 'B22222',  # Secondary
        'accent3': 'FFD700',  # Accent
        'accent4': 'AD4C4C',  # lighten(accent1, 30%)
        'accent5': 'C96464',  # lighten(accent2, 30%)
        'accent6': 'CCAC00',  # darken(accent3, 20%)
    }),
    'Electric Neon': ('dark2', {
        'accent1': '00D2FF',  # Primary
        'accent2': '7A2FCD',  # Secondary
        'accent3': 'FF0080',  # Accent
        'accent4': '4CDFFF',  # lighten(accent1, 30%)
        'accent5': 'A16DDC',  # lighten(accent2, 30%)
        'accent6': 'CC0066',  # darken(accent3, 20%)
        'lt1': '0A0A0A',     # Background
        'dk1': 'EAEAEA',     # Text
    }),
    # Soft/approachable
    'Teal Coral': ('colorful2', {
        'accent1': '5EA8A7',  # Primary
        'accent2': '3D8B8A',  # Secondary
        'accent3': 'FF6F61',  # Accent
        'accent4': '8EC2C1',  # lighten(accent1, 30%)
        'accent5': '77ADAD',  # lighten(accent2, 30%)
        'accent6': 'CC584D',  # darken(accent3, 20%)
    }),
    'Sage Serenity': ('accent1_3', {
        'accent1': '7D8A6E',  # Primary
        'accent2': 'A3B18A',  # Secondary
        'accent3': 'D4C5A9',  # Accent
        'accent4': 'A4AD99',  # lighten(accent1, 30%)
        'accent5': 'BEC8AD',  # lighten(accent2, 30%)
        'accent6': 'A99D87',  # darken(accent3, 20%)
    }),
    # ── Layout template color schemes (6 entries) ──
    'teal_medical': ('colorful2', {
        'accent1': '0D7377',  # Teal
        'accent2': '5EA8A7',  # Light Teal
        'accent3': 'FF6B35',  # Coral
        'accent4': '559D9F',  # lighten(accent1, 30%)
        'accent5': '8EC2C1',  # lighten(accent2, 30%)
        'accent6': 'CC552A',  # darken(accent3, 20%)
    }),
    'tech_blue': ('colorful2', {
        'accent1': '0078D7',  # Tech Blue
        'accent2': '106EBE',  # Darker Blue
        'accent3': 'E1EFFF',  # Light Blue
        'accent4': '4CA0E3',  # lighten(accent1, 30%)
        'accent5': '5799D1',  # lighten(accent2, 30%)
        'accent6': 'B4BFCC',  # darken(accent3, 20%)
    }),
    'smart_red': ('colorful2', {
        'accent1': 'DE3545',  # Smart Red-Orange
        'accent2': 'C12D3B',  # Darker Red
        'accent3': 'FF6B6B',  # Light Red
        'accent4': 'E7717C',  # lighten(accent1, 30%)
        'accent5': 'D36C75',  # lighten(accent2, 30%)
        'accent6': 'CC5555',  # darken(accent3, 20%)
    }),
    'dark_neon': ('dark1', {
        'accent1': '00D2FF',  # Cyan
        'accent2': '7A2FCD',  # Purple
        'accent3': 'FF0080',  # Neon Pink
        'accent4': '4CDFFF',  # lighten(accent1, 30%)
        'accent5': 'A16DDC',  # lighten(accent2, 30%)
        'accent6': 'CC0066',  # darken(accent3, 20%)
        'lt1': '0A0A14',     # Background
        'dk1': 'EAEAEA',     # Text
    }),
    'organic_warm': ('colorful2', {
        'accent1': '2D6A4F',  # Forest Green
        'accent2': '7D8A6E',  # Sage
        'accent3': 'D4A373',  # Warm Gold
        'accent4': '6C9683',  # lighten(accent1, 30%)
        'accent5': 'A4AD99',  # lighten(accent2, 30%)
        'accent6': 'A9825C',  # darken(accent3, 20%)
    }),
    'exhibit': ('colorful2', {
        'accent1': '1A1A1A',  # Dark base
        'accent2': 'D4AF37',  # Gold accent
        'accent3': 'C9A84C',  # Light Gold
        'accent4': '5E5E5E',  # lighten(accent1, 30%)
        'accent5': 'E0C773',  # lighten(accent2, 30%)
        'accent6': 'A0863C',  # darken(accent3, 20%)
    }),
}


def get_color_scheme_uri(style_name: str = None) -> str:
    """Get the SmartArt color scheme URI for a given style preset name."""
    if style_name and style_name in STYLE_TO_SMARTART_COLOR:
        scheme_key = STYLE_TO_SMARTART_COLOR[style_name][0]
    else:
        scheme_key = 'accent1_2'
    return SMARTART_COLOR_SCHEMES.get(scheme_key, SMARTART_COLOR_SCHEMES['accent1_2'])


def get_style_color_map(style_name: str = None) -> dict:
    """Get the scheme→hex color mapping for drawing.xml replacement."""
    if style_name and style_name in STYLE_TO_SMARTART_COLOR:
        return STYLE_TO_SMARTART_COLOR[style_name][1]
    return {}


def inject_theme(pptx_path: str, output_path: str = None,
                 colors: dict = None, style_name: str = None):
    """Override PPTX theme accent colors. Affects ALL SmartArt in the deck.

    Args:
        pptx_path: Path to PPTX file (modified in-place if output_path is None).
        output_path: Optional output path.
        colors: Dict of {accent_slot: hex_color}, e.g. {'accent1': 'E76F51', ...}.
        style_name: DeckDone style preset name (fills colors from STYLE_TO_SMARTART_COLOR).
    """
    if output_path is None:
        output_path = pptx_path
    
    if colors is None and style_name:
        colors = get_style_color_map(style_name)
    
    if not colors:
        return  # nothing to change

    with zipfile.ZipFile(pptx_path, 'r') as z:
        entries = {name: z.read(name) for name in z.namelist()}

    theme_path = 'ppt/theme/theme1.xml'
    if theme_path not in entries:
        return  # no theme to modify

    theme_xml = entries[theme_path].decode('utf-8')
    for slot, hex_color in colors.items():
        if slot.startswith('accent'):
            theme_xml = re.sub(
                f'(<a:{slot}>)\\s*<a:srgbClr val="[^"]*"\\s*/>\\s*(</a:{slot}>)',
                f'\\1<a:srgbClr val="{hex_color}"/></a:{slot}>',
                theme_xml
            )
        else:
            # Handle lt1, dk1 etc. — may use <a:srgbClr> or <a:sysClr>
            theme_xml = re.sub(
                f'(<a:{slot}>)\\s*<a:sysClr val="[^"]*"\\s*/>\\s*(</a:{slot}>)',
                f'\\1<a:srgbClr val="{hex_color}"/></a:{slot}>',
                theme_xml
            )
            theme_xml = re.sub(
                f'(<a:{slot}>)\\s*<a:srgbClr val="[^"]*"\\s*/>\\s*(</a:{slot}>)',
                f'\\1<a:srgbClr val="{hex_color}"/></a:{slot}>',
                theme_xml
            )
    entries[theme_path] = theme_xml.encode('utf-8')

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted(entries.keys()):
            z.writestr(name, entries[name])


def _build_colors_xml(scheme_uri: str) -> str:
    """Build a minimal colors.xml for a given color scheme."""
    scheme_name = scheme_uri.split('/')[-1]
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<dgm:colorsDef xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"\n'
        f'               uniqueId="{scheme_uri}">\n'
        f'  <dgm:title lang="" val="{scheme_name}"/>\n'
        '  <dgm:desc lang="" val=""/>\n'
        '</dgm:colorsDef>'
    )
DIAGRAM_NS = 'http://schemas.openxmlformats.org/drawingml/2006/diagram'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

_TYPE_CLASSES = {
    'data': ('data', 'dgmData', 'application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml'),
    'layout': ('layout', 'dgmLayout', 'application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml'),
    'drawing': ('drawing', 'dgmDrawing',
                'application/vnd.ms-office.drawingml.diagramDrawing+xml'),
    'colors': ('colors', 'dgmColors',
               'application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml'),
    'quickStyle': ('quickStyle', 'dgmQuickStyle',
                   'application/vnd.openxmlformats-officedocument.drawingml.diagramQuickStyle+xml'),
}

_REL_TYPES = {
    'data': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramData',
    'layout': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout',
    'quickStyle': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramQuickStyle',
    'colors': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramColors',
    'drawing': 'http://schemas.microsoft.com/office/2007/relationships/diagramDrawing',
}

_GRAPHICFRAME_REFS = {
    'data': 'dm',
    'layout': 'lo',
    'quickStyle': 'qs',
    'colors': 'cs',
}

_REQUIRED_FILES = ('data.xml', 'layout.xml', 'drawing.xml', 'colors.xml', 'quickStyle.xml')


def _discover_templates() -> dict:
    """Scan the template directory and build a mapping from logical name -> folder path.

    Returns a dict where keys are short names (uniqueId slug, e.g. 'pyramid1', 'cycle2',
    'gear') and category-prefixed names (e.g. 'pyramid/basic', 'cycle/basic').
    Values are Path objects pointing to template folders.
    """
    mapping = {}
    if not TEMPLATE_DIR.is_dir():
        return mapping

    for folder in sorted(TEMPLATE_DIR.iterdir()):
        if not folder.is_dir():
            continue
        layout_file = folder / 'layout.xml'
        if not layout_file.exists():
            continue

        layout_xml = layout_file.read_text(encoding='utf-8')

        uid_match = re.search(r'uniqueId="([^"]+)"', layout_xml)
        cat_match = re.search(r'<dgm:cat\s+type="([^"]+)"', layout_xml)
        if not uid_match:
            continue

        uid = uid_match.group(1)
        slug = uid.split('/')[-1] if uid else folder.name
        # strip +Icon suffix
        slug = slug.replace('+Icon', '').strip()
        category = cat_match.group(1) if cat_match else 'unknown'

        # deduplicate: first template wins
        if slug not in mapping:
            mapping[slug] = folder

        cat_slug = f'{category}/{slug}'
        if cat_slug not in mapping:
            mapping[cat_slug] = folder

    return mapping


_TEMPLATE_MAP = None


def get_template_map() -> dict:
    """Return the cached template name → folder mapping (lazy-init)."""
    global _TEMPLATE_MAP
    if _TEMPLATE_MAP is None:
        _TEMPLATE_MAP = _discover_templates()
    return _TEMPLATE_MAP


def _find_next_diagram_index(existing_names: list) -> int:
    """Find the next available diagram index across all file types.

    Scans ppt/diagrams/ entries in the ZIP for existing diagram<N>.xml files
    and returns N+1.
    """
    max_idx = 0
    for name in existing_names:
        m = re.match(r'ppt/diagrams/(?:data|layout|drawing|colors|quickStyle)(\d+)\.xml', name)
        if m:
            idx = int(m.group(1))
            if idx > max_idx:
                max_idx = idx
    return max_idx + 1


def _find_next_shape_id(slide_xml: str) -> int:
    """Find the next available shape ID in the slide XML."""
    ids = [int(m) for m in re.findall(r'<p:cNvPr[^>]*\s+id="(\d+)"', slide_xml)]
    max_id = max(ids) if ids else 0
    return max_id + 1


def _find_next_rid(rels_xml: str) -> int:
    """Find the next available relationship ID in the rels XML."""
    rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels_xml)]
    max_rid = max(rids) if rids else 0
    return max_rid + 1


def _add_content_types(content_types_xml: str, diagram_index: int) -> str:
    """Add diagram content type entries to [Content_Types].xml."""
    entries = []
    for file_type, (prefix, _, ct) in _TYPE_CLASSES.items():
        part_name = f'/ppt/diagrams/{prefix}{diagram_index}.xml'
        entry = f'<Override PartName="{part_name}" ContentType="{ct}"/>'
        entries.append(entry)

    # insert before closing </Types>
    if '</Types>' not in content_types_xml:
        return content_types_xml
    new_xml = content_types_xml.replace('</Types>', ''.join(entries) + '</Types>')
    return new_xml


def _add_slide_rels(rels_xml: str, diagram_index: int) -> tuple:
    """Add 5 diagram relationships to the slide rels XML.

    Returns (new_rels_xml, rid_map) where rid_map maps file_type to 'rId<N>'.
    """
    next_rid = _find_next_rid(rels_xml)
    rid_map = {}
    rel_entries = []

    # Must be in this order for deterministic output
    for file_type in ('data', 'layout', 'quickStyle', 'colors', 'drawing'):
        rid = next_rid
        next_rid += 1
        rid_str = f'rId{rid}'
        rid_map[file_type] = rid_str

        prefix = _TYPE_CLASSES[file_type][0]
        rel_type = _REL_TYPES[file_type]
        target = f'../diagrams/{prefix}{diagram_index}.xml'
        rel_entries.append(
            f'<Relationship Id="{rid_str}" Type="{rel_type}" Target="{target}"/>'
        )

    if '</Relationships>' not in rels_xml:
        return rels_xml, rid_map

    new_xml = rels_xml.replace('</Relationships>', ''.join(rel_entries) + '</Relationships>')
    return new_xml, rid_map


def _add_graphic_frame(slide_xml: str, shape_id: int, rid_map: dict) -> str:
    """Add a graphicFrame element to the slide XML using the diagram relationships.

    The graphicFrame is placed at a reasonable default position on the slide.
    rid_map maps: data→rId, layout→rId, quickStyle→rId, colors→rId
    """
    ref_attrs = []
    for file_type, attr_name in _GRAPHICFRAME_REFS.items():
        if file_type in rid_map:
            ref_attrs.append(f'r:{attr_name}="{rid_map[file_type]}"')

    ref_attrs_str = ' '.join(ref_attrs)

    graphic_frame = (
        '<p:graphicFrame>'
        '<p:nvGraphicFramePr>'
        f'<p:cNvPr id="{shape_id}" name="Diagram {shape_id}"/>'
        '<p:cNvGraphicFramePr/>'
        '<p:nvPr/>'
        '</p:nvGraphicFramePr>'
        '<p:xfrm>'
        '<a:off x="2011680" y="1280160"/>'
        '<a:ext cx="8128000" cy="4857750"/>'
        '</p:xfrm>'
        '<a:graphic>'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/diagram">'
        f'<dgm:relIds xmlns:dgm="{DIAGRAM_NS}" xmlns:r="{REL_NS}" {ref_attrs_str}/>'
        '</a:graphicData>'
        '</a:graphic>'
        '</p:graphicFrame>'
    )

    if '</p:spTree>' not in slide_xml:
        return slide_xml

    return slide_xml.replace('</p:spTree>', graphic_frame + '</p:spTree>')


def inject(pptx_path: str, output_path: str, slide_index: int,
           template_name: str, color_scheme_uri: str = None,
           texts: list = None) -> Optional[str]:
    """Inject a SmartArt template into a PPTX slide.

    Args:
        pptx_path: Path to source PPTX file.
        output_path: Path for the output PPTX.
        slide_index: 0-based index of the target slide.
        template_name: Either a short name (e.g. 'pyramid1', 'cycle2', 'gear1')
                       or a category-prefixed name (e.g. 'pyramid/pyramid1').
        color_scheme_uri: Optional SmartArt color scheme URI. If not provided,
                          uses the template's default colors.
                          Get from get_color_scheme_uri(style_name).
        style_name: Optional DeckDone style preset name (e.g. 'Corporate Blue').
                    When provided, replaces schemeClr references in drawing.xml
                    with actual hex colors from the style preset.

    Returns:
        The diagram index string (e.g. 'dgmData5') or None on failure.
    """
    tm = get_template_map()
    if not tm:
        raise FileNotFoundError(f'Template directory not found: {TEMPLATE_DIR}')

    template_folder = tm.get(template_name)
    if template_folder is None:
        available = ', '.join(sorted(tm.keys())[:20])
        raise ValueError(
            f'Unknown template: {template_name}. '
            f'Available names include: {available}...'
        )

    # Verify all 5 required files exist
    for fname in _REQUIRED_FILES:
        if not (template_folder / fname).exists():
            raise FileNotFoundError(f'Missing {fname} in template folder: {template_folder}')

    # Read source PPTX
    with zipfile.ZipFile(pptx_path, 'r') as z:
        entries = {name: z.read(name) for name in z.namelist()}

    names = sorted(entries.keys())

    # Find next diagram index
    diag_idx = _find_next_diagram_index(names)

    # Target slide paths
    slide_entry = f'ppt/slides/slide{slide_index + 1}.xml'
    slide_rels_entry = f'ppt/slides/_rels/slide{slide_index + 1}.xml.rels'
    content_types_entry = '[Content_Types].xml'

    if slide_entry not in entries:
        raise ValueError(f'Slide {slide_index} not found in {pptx_path}')

    # Process slide XML
    slide_xml = entries[slide_entry].decode('utf-8')
    shape_id = _find_next_shape_id(slide_xml)

    # Process slide rels
    if slide_rels_entry in entries:
        rels_xml = entries[slide_rels_entry].decode('utf-8')
    else:
        rels_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'
        )

    new_rels_xml, rid_map = _add_slide_rels(rels_xml, diag_idx)
    new_slide_xml = _add_graphic_frame(slide_xml, shape_id, rid_map)

    # Process Content_Types
    if content_types_entry in entries:
        ct_xml = entries[content_types_entry].decode('utf-8')
    else:
        ct_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>'
        )
    new_ct_xml = _add_content_types(ct_xml, diag_idx)

    # Copy template files into entries
    for fname in _REQUIRED_FILES:
        file_type = fname.replace('.xml', '')
        prefix = _TYPE_CLASSES[file_type][0]
        dst_name = f'ppt/diagrams/{prefix}{diag_idx}.xml'
        entries[dst_name] = (template_folder / fname).read_bytes()

    # Inject text content into data.xml
    if texts:
        data_dst = f'ppt/diagrams/{_TYPE_CLASSES["data"][0]}{diag_idx}.xml'
        data_xml = entries[data_dst].decode('utf-8')
        slot_count = len(re.findall(r'<dgm:t>.*?</dgm:t>', data_xml, re.DOTALL))
        flat = _flatten_texts(texts)
        if len(flat) > slot_count:
            import warnings
            warnings.warn(
                f'Template "{template_name}" has {slot_count} text slots but '
                f'{len(flat)} texts provided. Extra texts will be dropped.'
            )
        data_xml = _inject_text_into_data(data_xml, texts)
        entries[data_dst] = data_xml.encode('utf-8')

    # Override colors and data if color scheme URI specified
    if color_scheme_uri:
        colors_dst = f'ppt/diagrams/{_TYPE_CLASSES["colors"][0]}{diag_idx}.xml'
        entries[colors_dst] = _build_colors_xml(color_scheme_uri).encode('utf-8')
        data_dst = f'ppt/diagrams/{_TYPE_CLASSES["data"][0]}{diag_idx}.xml'
        data_xml = entries[data_dst].decode('utf-8')
        data_xml = re.sub(r'csTypeId="[^"]*"', f'csTypeId="{color_scheme_uri}"', data_xml)
        entries[data_dst] = data_xml.encode('utf-8')

    # Ensure we have a diagrams directory placeholder
    if 'ppt/diagrams/' not in entries:
        entries['ppt/diagrams/'] = b''

    # Update entries with modified XML
    entries[slide_entry] = new_slide_xml.encode('utf-8')
    entries[slide_rels_entry] = new_rels_xml.encode('utf-8')
    entries[content_types_entry] = new_ct_xml.encode('utf-8')

    # Write output — read source into memory, modify, write
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted(entries.keys()):
            z.writestr(name, entries[name])

    diagram_tag = _TYPE_CLASSES['data'][1]
    return f'{diagram_tag}{diag_idx}'


def _flatten_texts(texts: list) -> list:
    """Flatten hierarchical texts into ordered list matching data model node order."""
    result = []
    for item in texts:
        if isinstance(item, dict):
            result.append(item.get('text', ''))
            for child in item.get('children', []):
                result.append(child if isinstance(child, str) else child.get('text', ''))
        else:
            result.append(str(item))
    return result


def _inject_text_into_data(data_xml: str, texts: list) -> str:
    """Inject text content into data.xml <dgm:t> elements.
    
    Matches node-type <dgm:t> elements positionally with flattened texts list.
    Replaces existing <a:t> text or inserts new <a:r> for empty nodes.
    """
    flat = _flatten_texts(texts)
    if not flat:
        return data_xml
    
    parts = []
    last_end = 0
    text_idx = 0
    
    for m in re.finditer(r'<dgm:t>(.*?)</dgm:t>', data_xml, re.DOTALL):
        inner = m.group(1)
        if text_idx >= len(flat):
            break
        
        text = flat[text_idx]
        text_idx += 1
        
        # Check if there's existing <a:t> with content — replace it
        existing_t = re.search(r'<a:t>([^<]*)</a:t>', inner)
        if existing_t:
            new_inner = inner[:existing_t.start()] + f'<a:t>{_xml_escape(text)}</a:t>' + inner[existing_t.end():]
        else:
            # No existing text — insert new <a:r> before </a:p> or after <a:p>
            new_inner = re.sub(
                r'(<a:endParaRPr[^/]*/>)',
                f'\\1<a:r><a:rPr lang="zh-CN" dirty="0"/><a:t>{_xml_escape(text)}</a:t></a:r>',
                inner,
                count=1
            )
            # Fallback: if no endParaRPr, insert at first <a:p>
            if new_inner == inner:
                new_inner = re.sub(
                    r'(<a:p>)',
                    f'\\1<a:r><a:rPr lang="zh-CN" dirty="0"/><a:t>{_xml_escape(text)}</a:t></a:r>',
                    inner,
                    count=1
                )
        
        parts.append(data_xml[last_end:m.start()])
        parts.append(f'<dgm:t>{new_inner}</dgm:t>')
        last_end = m.end()
    
    parts.append(data_xml[last_end:])
    return ''.join(parts)


def _xml_escape(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def list_templates() -> list:
    """Return sorted list of available template names."""
    return sorted(get_template_map().keys())
