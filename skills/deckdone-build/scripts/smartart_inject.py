"""
SmartArt Diagram Injection for python-pptx PPTX

Key insight from MarpToPptx (https://github.com/jongalloway/MarpToPptx/pull/162):
- layout1.xml only needs a uniqueId pointing to Microsoft's built-in layout URI
- PowerPoint/WPS loads the full layout definition from its own internal resources
- drawing.xml is NOT needed — PowerPoint regenerates it on first open

Zero dependencies beyond Python stdlib (zipfile + xml.etree).

Usage:
    from smartart_inject import SmartArtInjector
    inj = SmartArtInjector()
    inj.inject(pptx_path, output_path, slide_index, 'pyramid', items)
"""

import zipfile
import re
import shutil

# ── Built-in SmartArt Layout URI Registry ──

LAYOUT_URIS = {
    # Process / Flow
    'process':        'urn:microsoft.com/office/officeart/2005/8/layout/process1',
    'chevron':        'urn:microsoft.com/office/officeart/2005/8/layout/chevron1',
    'staircase':      'urn:microsoft.com/office/officeart/2005/8/layout/stepUpProcess1',
    'timeline':       'urn:microsoft.com/office/officeart/2005/8/layout/process1',
    
    # Cycle
    'cycle':          'urn:microsoft.com/office/officeart/2005/8/layout/cycle1',
    'radial':         'urn:microsoft.com/office/officeart/2005/8/layout/cycle6',
    'radial-cycle':   'urn:microsoft.com/office/officeart/2005/8/layout/cycle5',
    
    # Hierarchy
    'hierarchy':      'urn:microsoft.com/office/officeart/2005/8/layout/hierarchy2',
    'org-chart':      'urn:microsoft.com/office/officeart/2005/8/layout/hierarchy1',
    
    # Relationship
    'venn':           'urn:microsoft.com/office/officeart/2005/8/layout/relationship1',
    'gear':           'urn:microsoft.com/office/officeart/2005/8/layout/relationship5',
    'equation':       'urn:microsoft.com/office/officeart/2005/8/layout/relationship6',
    'converging':     'urn:microsoft.com/office/officeart/2005/8/layout/relationship3',
    'opposing-arrows':'urn:microsoft.com/office/officeart/2005/8/layout/opposingArrows1',
    
    # Matrix
    'matrix':         'urn:microsoft.com/office/officeart/2005/8/layout/matrix1',
    'titled-matrix':  'urn:microsoft.com/office/officeart/2005/8/layout/matrix2',
    'grid-matrix':    'urn:microsoft.com/office/officeart/2005/8/layout/matrix3',
    
    # Pyramid
    'pyramid':        'urn:microsoft.com/office/officeart/2005/8/layout/pyramid1',
    'segmented-pyramid': 'urn:microsoft.com/office/officeart/2005/8/layout/pyramid4',
    
    # List
    'vlist':          'urn:microsoft.com/office/officeart/2005/8/layout/vList5',
    'vbullet':        'urn:microsoft.com/office/officeart/2005/8/layout/vList1',
    
    # Funnel
    'funnel':         'urn:microsoft.com/office/officeart/2005/8/layout/funnel1',
}

# Friendly names for layout XML title
LAYOUT_NAMES = {
    k: k.replace('-', ' ').title() for k in LAYOUT_URIS
}
LAYOUT_NAMES.update({
    'vlist': 'Vertical Block List',
    'staircase': 'Step Up Process',
    'venn': 'Basic Venn',
    'matrix': 'Basic Matrix',
    'pyramid': 'Basic Pyramid',
})

# ── DeckDone Diagram Type → SmartArt Layout Mapping ──

DIAGRAM_TO_SMARTART = {
    'Pyramid':             'pyramid',
    'Hub-and-Spoke':       'radial',
    'Dual-Gears':          'gear',
    'Tension-Triangle':    'converging',
    'Bubble-Matrix':       'matrix',
    'Staircase':           'staircase',
    'Split-Comparison':    'opposing-arrows',
    'Data-Card-Grid':      'vlist',
    'Layered-Architecture': 'hierarchy',
    'Filter-Funnel':       'funnel',
    'Overlapping-Spheres': 'venn',
    'Iterative-Cycle':     'cycle',
    'Bridge-and-Gap':      'equation',
}

# Standard page dimensions (16:9)
SLIDE_WIDTH_EMU = 12192000   # 13.333 inches
SLIDE_HEIGHT_EMU = 6858000   # 7.5 inches

# Default diagram position/size
DEFAULT_X = 500000            # 0.5 inch from left
DEFAULT_Y = 900000            # 1.0 inch from top (below title)
DEFAULT_CX = 8600000          # 9.5 inch width
DEFAULT_CY = 5400000          # 6.0 inch height


class SmartArtInjector:
    """Inject SmartArt diagrams into PPTX files via direct OOXML manipulation."""

    def __init__(self):
        pass

    @staticmethod
    def get_layout_key(diagram_type):
        """Map DeckDone diagram type to SmartArt layout key."""
        return DIAGRAM_TO_SMARTART.get(diagram_type, 'process')

    def inject(self, pptx_path, output_path, slide_index, diagram_type, items,
               x=DEFAULT_X, y=DEFAULT_Y, cx=DEFAULT_CX, cy=DEFAULT_CY):
        """
        Inject a SmartArt diagram into a slide.

        Args:
            pptx_path: Source PPTX file
            output_path: Output PPTX file
            slide_index: 0-based slide index
            diagram_type: DeckDone diagram type (e.g., 'Pyramid', 'Hub-and-Spoke')
            items: List of dicts with 'text' and optional 'children' list
            x, y, cx, cy: Position and size in EMUs
        """
        layout_key = self.get_layout_key(diagram_type)
        shutil.copy(pptx_path, output_path)
        self._inject_inplace(output_path, slide_index, layout_key, items, x, y, cx, cy)

    def _inject_inplace(self, pptx_path, slide_index, layout_key, items,
                        x, y, cx, cy):
        """Inject into a PPTX file in-place (destructive)."""
        # Read all entries
        with zipfile.ZipFile(pptx_path, 'r') as zin:
            entries = {name: zin.read(name) for name in zin.namelist()}

        # Find next diagram number
        existing = entries.keys()
        diag_num = 1
        while f'ppt/diagrams/data{diag_num}.xml' in existing:
            diag_num += 1

        # Add diagram parts
        entries.update(self._build_diagram_parts(diag_num, layout_key, items))

        # Update Content_Types
        entries['[Content_Types].xml'] = self._update_content_types(
            entries['[Content_Types].xml'].decode('utf-8'), diag_num
        ).encode('utf-8')

        # Update slide relationships
        rels_path = f'ppt/slides/_rels/slide{slide_index + 1}.xml.rels'
        rels, rids = self._update_slide_rels(entries, rels_path, diag_num)
        entries[rels_path] = rels.encode('utf-8')

        # Update slide XML with graphicFrame
        slide_path = f'ppt/slides/slide{slide_index + 1}.xml'
        entries[slide_path] = self._add_graphic_frame(
            entries[slide_path].decode('utf-8'),
            slide_index, diag_num, rids, x, y, cx, cy
        ).encode('utf-8')

        # Write output
        with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for name, data in entries.items():
                zout.writestr(name, data)

    def _build_diagram_parts(self, diag_num, layout_key, items):
        """Build all 4 diagram XML parts."""
        uri = LAYOUT_URIS.get(layout_key, LAYOUT_URIS['process'])
        name = LAYOUT_NAMES.get(layout_key, layout_key)
        return {
            f'ppt/diagrams/data{diag_num}.xml':
                self._build_data_xml(items).encode('utf-8'),
            f'ppt/diagrams/layout{diag_num}.xml':
                self._build_layout_xml(uri, name).encode('utf-8'),
            f'ppt/diagrams/quickStyle{diag_num}.xml':
                self._build_style_xml().encode('utf-8'),
            f'ppt/diagrams/colors{diag_num}.xml':
                self._build_colors_xml().encode('utf-8'),
        }

    @staticmethod
    def _build_data_xml(items):
        """Build data model XML with node hierarchy."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<dgm:dataModel xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram">',
            '  <dgm:ptLst>',
            '    <dgm:pt modelId="0" type="doc"/>',
        ]
        next_id = 10
        connections = []

        for i, item in enumerate(items):
            text = item.get('text', '')
            children = item.get('children', [])
            node_id = next_id
            next_id += 10
            lines.append(f'    <dgm:pt modelId="{node_id}" type="node"/>')
            cxn_id = next_id
            next_id += 10
            connections.append(
                f'    <dgm:cxn modelId="{cxn_id}" type="parOf" '
                f'srcId="0" destId="{node_id}" srcOrd="{i}" destOrd="0"/>'
            )
            for j, child in enumerate(children):
                child_id = next_id
                next_id += 10
                lines.append(f'    <dgm:pt modelId="{child_id}" type="node"/>')
                cxn_id = next_id
                next_id += 10
                connections.append(
                    f'    <dgm:cxn modelId="{cxn_id}" type="parOf" '
                    f'srcId="{node_id}" destId="{child_id}" srcOrd="{j}" destOrd="0"/>'
                )

        lines.append('  </dgm:ptLst>')
        lines.append('  <dgm:cxnLst>')
        lines.extend(connections)
        lines.append('  </dgm:cxnLst>')
        lines.append('</dgm:dataModel>')
        return '\n'.join(lines)

    @staticmethod
    def _build_layout_xml(uri, name):
        """Build minimal layout XML referencing a built-in SmartArt layout."""
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<dgm:layoutDef xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"\n'
            f'               uniqueId="{uri}" minVer="12.0">\n'
            f'  <dgm:title lang="" val="{name}"/>\n'
            '  <dgm:desc lang="" val=""/>\n'
            '  <dgm:layoutNode name="root">\n'
            '    <dgm:varLst/>\n'
            '  </dgm:layoutNode>\n'
            '</dgm:layoutDef>'
        )

    @staticmethod
    def _build_style_xml():
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<dgm:styleDef xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"\n'
            '              uniqueId="urn:microsoft.com/office/officeart/2005/8/quickstyle/ps1">\n'
            '  <dgm:title lang="" val="Simple"/>\n'
            '  <dgm:desc lang="" val=""/>\n'
            '</dgm:styleDef>'
        )

    @staticmethod
    def _build_colors_xml():
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<dgm:colorsDef xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"\n'
            '               uniqueId="urn:microsoft.com/office/officeart/2005/8/colors/accent1_2">\n'
            '  <dgm:title lang="" val="Accent 1-2"/>\n'
            '  <dgm:desc lang="" val=""/>\n'
            '</dgm:colorsDef>'
        )

    @staticmethod
    def _update_content_types(ct_xml, diag_num):
        """Add diagram part overrides to Content_Types.xml."""
        parts = [
            (f'/ppt/diagrams/data{diag_num}.xml',
             'application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml'),
            (f'/ppt/diagrams/layout{diag_num}.xml',
             'application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml'),
            (f'/ppt/diagrams/quickStyle{diag_num}.xml',
             'application/vnd.openxmlformats-officedocument.drawingml.diagramQuickStyle+xml'),
            (f'/ppt/diagrams/colors{diag_num}.xml',
             'application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml'),
        ]
        for part_name, content_type in parts:
            entry = f'<Override PartName="{part_name}" ContentType="{content_type}"/>'
            if entry not in ct_xml:
                ct_xml = ct_xml.replace('</Types>', f'  {entry}\n</Types>')
        return ct_xml

    @staticmethod
    def _update_slide_rels(entries, rels_path, diag_num):
        """Add diagram relationships to the slide's .rels file."""
        if rels_path in entries:
            rels = entries[rels_path].decode('utf-8')
        else:
            rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
                    '</Relationships>')

        rids = re.findall(r'rId(\d+)', rels)
        next_rid = max(int(r) for r in rids) + 1 if rids else 1

        rid_map = {
            'data': next_rid,
            'layout': next_rid + 1,
            'style': next_rid + 2,
            'colors': next_rid + 3,
        }
        target_map = {
            'data': ('../diagrams/data{}.xml',
                     'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramData'),
            'layout': ('../diagrams/layout{}.xml',
                       'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout'),
            'style': ('../diagrams/quickStyle{}.xml',
                       'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramQuickStyle'),
            'colors': ('../diagrams/colors{}.xml',
                       'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramColors'),
        }

        new_rels = ''
        for key in ['data', 'layout', 'style', 'colors']:
            target_template, rel_type = target_map[key]
            rid = rid_map[key]
            new_rels += (
                f'  <Relationship Id="rId{rid}" Type="{rel_type}" '
                f'Target="{target_template.format(diag_num)}"/>\n'
            )

        rels = rels.replace('</Relationships>', new_rels + '</Relationships>')
        return rels, rid_map

    @staticmethod
    def _add_graphic_frame(slide_xml, slide_index, diag_num, rids,
                           x, y, cx, cy):
        """Add a graphicFrame element to the slide XML."""
        shape_id = 100 + slide_index * 100 + diag_num
        frame = (
            '\n  <p:graphicFrame'
            ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            ' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
            ' xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram">\n'
            '    <p:nvGraphicFramePr>\n'
            f'      <p:cNvPr id="{shape_id}" name="Diagram {diag_num}"/>\n'
            '      <p:cNvGraphicFramePr>\n'
            '        <a:graphicFrameLocks noGrp="1"/>\n'
            '      </p:cNvGraphicFramePr>\n'
            '      <p:nvPr/>\n'
            '    </p:nvGraphicFramePr>\n'
            '    <p:xfrm>\n'
            f'      <a:off x="{x}" y="{y}"/>\n'
            f'      <a:ext cx="{cx}" cy="{cy}"/>\n'
            '    </p:xfrm>\n'
            '    <a:graphic>\n'
            '      <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/diagram">\n'
            f'        <dgm:relIds r:dm="rId{rids["data"]}" r:lo="rId{rids["layout"]}" '
            f'r:qs="rId{rids["style"]}" r:cs="rId{rids["colors"]}"/>\n'
            '      </a:graphicData>\n'
            '    </a:graphic>\n'
            '  </p:graphicFrame>'
        )
        return slide_xml.replace('</p:spTree>', frame + '\n</p:spTree>')
