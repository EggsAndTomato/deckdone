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
           template_name: str) -> Optional[str]:
    """Inject a SmartArt template into a PPTX slide.

    Args:
        pptx_path: Path to source PPTX file.
        output_path: Path for the output PPTX.
        slide_index: 0-based index of the target slide.
        template_name: Either a short name (e.g. 'pyramid1', 'cycle2', 'gear1')
                       or a category-prefixed name (e.g. 'pyramid/pyramid1').

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


def list_templates() -> list:
    """Return sorted list of available template names."""
    return sorted(get_template_map().keys())
