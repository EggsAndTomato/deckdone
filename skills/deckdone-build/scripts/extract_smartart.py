"""
SmartArt Template Extractor — extracts all diagram templates from a PPTX.

Usage:
    python extract_smartart.py input.pptx output_dir/

Output:
    output_dir/
        index.md                      ← index of all extracted types
        INDEX_SHEET.svg               ← visual reference for AI selection
        Category_Type_LayoutName/      ← one folder per diagram
            data.xml
            layout.xml
            drawing.xml
            colors.xml
            quickStyle.xml
"""
import zipfile, re, os, shutil, json
from pathlib import Path
from collections import defaultdict

def extract(pptx_path, output_dir):
    """Extract all SmartArt diagram templates from a PPTX."""
    os.makedirs(output_dir, exist_ok=True)
    
    with zipfile.ZipFile(pptx_path, 'r') as z:
        names = sorted(z.namelist())
    
    # First pass: get slide titles for naming
    slide_texts = {}
    for name in names:
        m = re.match(r'ppt/slides/slide(\d+)\.xml', name)
        if m:
            slide_num = int(m.group(1))
            with zipfile.ZipFile(pptx_path, 'r') as z:
                slide_xml = z.read(name).decode()
                # Extract all text from slide shapes
                texts = re.findall(r'<a:t>([^<]*)</a:t>', slide_xml)
                slide_texts[slide_num] = ' '.join(t for t in texts if t.strip())[:80]
    
    # Group diagram files by index
    diag_files = defaultdict(dict)
    for name in names:
        m = re.match(r'ppt/diagrams/(data|layout|drawing|colors|quickStyle)(\d+)\.xml', name)
        if m:
            diag_files[int(m.group(2))][m.group(1)] = name
    
    # Process each diagram
    types = {}
    with zipfile.ZipFile(pptx_path, 'r') as z:
        for idx in sorted(diag_files.keys()):
            files = diag_files[idx]
            
            # Read layout.xml
            layout_xml = z.read(f'ppt/diagrams/layout{idx}.xml').decode()
            title = re.search(r'<dgm:title[^>]*val="([^"]*)"', layout_xml)
            unique_id = re.search(r'uniqueId="([^"]+)"', layout_xml)
            cat = re.search(r'<dgm:cat type="([^"]+)"', layout_xml)
            
            layout_name = title.group(1) if title and title.group(1) else ''
            uid = unique_id.group(1) if unique_id else ''
            category = cat.group(1) if cat else 'unknown'
            
            # Try to get name from drawing.xml text
            drawing_name = ''
            if 'drawing' in files:
                drawing_xml = z.read(f'ppt/diagrams/drawing{idx}.xml').decode()
                dtexts = re.findall(r'<a:t>([^<]+)</a:t>', drawing_xml)
                drawing_name = ' '.join(dtexts[:3]) if dtexts else ''
            
            name = layout_name or drawing_name or f'Diagram_{idx}'
            
            # Clean name
            name = name.strip()
            if not name or name.isspace():
                name = f'Diagram_{idx}'
            
            # Derive a safe folder name (truncated)
            safe_name = re.sub(r'[^\w\-]', '_', name).strip('_')[:40]
            cat_safe = re.sub(r'[^\w\-]', '_', category).strip('_')
            folder = f'{cat_safe}_{safe_name}_{idx}'
            folder_path = os.path.join(output_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            # Extract files
            for file_type, file_path in files.items():
                content = z.read(file_path)
                out_path = os.path.join(folder_path, f'{file_type}.xml')
                with open(out_path, 'wb') as f:
                    f.write(content)
            
            types[idx] = {
                'name': name, 'category': category, 'folder': folder,
                'uid': uid, 'slide_idx': None
            }
    
    # Map each diagram to which slide it appears on, and get slide-based name
    for name in names:
        m = re.match(r'ppt/slides/slide(\d+)\.xml', name)
        if m:
            slide_num = int(m.group(1))
            with zipfile.ZipFile(pptx_path, 'r') as z:
                slide_xml = z.read(name).decode()
                dgm_match = re.search(r'r:dm="rId(\d+)"', slide_xml)
                if dgm_match:
                    rid = dgm_match.group(1)
                    rels_name = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
                    if rels_name in names:
                        with zipfile.ZipFile(pptx_path, 'r') as z:
                            rels = z.read(rels_name).decode()
                            target = re.search(f'Id="rId{rid}"[^>]*Target="[^"]*data(\\d+)\\.xml"', rels)
                            if target:
                                diag_idx = int(target.group(1))
                                if diag_idx in types:
                                    types[diag_idx]['slide_idx'] = slide_num
                                    # Use slide text as name if layout name is empty
                                    if types[diag_idx]['name'] == f'Diagram_{diag_idx}':
                                        slide_text = slide_texts.get(slide_num, '')
                                        if slide_text:
                                            types[diag_idx]['name'] = slide_text[:60]
    
    # Write index
    index_lines = ['# SmartArt Template Index', '', f'Source: {os.path.basename(pptx_path)}', f'Total: {len(types)} types', '']
    for idx, info in sorted(types.items()):
        index_lines.append(f'## {info["name"]}')
        index_lines.append(f'- Category: `{info["category"]}`')
        index_lines.append(f'- Folder: `{info["folder"]}`')
        index_lines.append(f'- Slide: {info["slide_idx"] or "unknown"}')
        index_lines.append(f'- Layout URI: `{info["uid"]}`')
        index_lines.append('')
    
    with open(os.path.join(output_dir, 'index.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_lines))
    
    return types


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python extract_smartart.py <input.pptx> [output_dir]')
        sys.exit(1)
    
    pptx = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else pptx.replace('.pptx', '_templates')
    types = extract(pptx, out)
    
    # Print summary
    cats = defaultdict(list)
    for idx, info in sorted(types.items()):
        cats[info['category']].append(info['name'])
    
    print(f'Extracted {len(types)} SmartArt templates to: {out}')
    print()
    for cat, names in sorted(cats.items()):
        print(f'  [{cat}] ({len(names)} types)')
        for n in names:
            print(f'    - {n}')
