#!/usr/bin/env python3
"""Extracts text from PDFs. Handles image-type PDFs by rendering pages as PNG."""

import argparse
import os
import sys


def check_deps():
    missing = []
    try:
        import pypdf
    except ImportError:
        missing.append("pypdf")
    try:
        import pypdfium2 as pdfium
    except ImportError:
        missing.append("pypdfium2")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(2)


def load_pdf(filepath):
    try:
        from pypdf import PdfReader

        reader = PdfReader(filepath)
        return reader
    except Exception as e:
        encrypted = "encrypt" in str(e).lower() or "password" in str(e).lower()
        if encrypted:
            print(f"Error: PDF appears to be encrypted/protected: {filepath}")
            print("Please provide a decrypted copy of this PDF.")
            sys.exit(1)
        print(f"Error reading PDF: {e}")
        sys.exit(1)


def get_page_text(reader, page_num):
    try:
        page = reader.pages[page_num]
        text = page.extract_text()
        return text.strip() if text else ""
    except Exception:
        return ""


def classify_pages(reader):
    total = len(reader.pages)
    page_types = {}

    if total <= 50:
        for i in range(total):
            text = get_page_text(reader, i)
            page_types[i] = "text" if len(text) > 20 else "image"
    else:
        sample_indices = [0, total // 4, total // 2, 3 * total // 4, total - 1]
        sample_indices = sorted(set(i for i in sample_indices if i < total))
        samples = {i: get_page_text(reader, i) for i in sample_indices}
        all_text = all(len(samples[i]) > 20 for i in sample_indices)
        all_image = all(len(samples[i]) <= 20 for i in sample_indices)

        if all_text:
            for i in range(total):
                page_types[i] = "text"
        elif all_image:
            for i in range(total):
                page_types[i] = "image"
        else:
            for i in range(total):
                text = get_page_text(reader, i)
                page_types[i] = "text" if len(text) > 20 else "image"

    return page_types


def extract_text_pages(reader, page_types, output_dir):
    text_pages = [i for i, t in page_types.items() if t == "text"]
    if not text_pages:
        return []

    written = []
    for page_num in text_pages:
        text = get_page_text(reader, page_num)
        filename = f"{page_num + 1:02d}-page-{page_num + 1:03d}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Page {page_num + 1}\n\n{text}\n")
        written.append(filename)
    return written


def render_image_pages(filepath, page_types, output_dir):
    import pypdfium2 as pdfium

    image_pages = [i for i, t in page_types.items() if t == "image"]
    if not image_pages:
        return []

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    pdf = pdfium.PdfDocument(filepath)
    rendered = []

    for page_num in image_pages:
        page = pdf[page_num]
        bitmap = page.render(scale=200 / 72)
        pil_img = bitmap.to_pil()
        img_filename = f"page-{page_num + 1:03d}.png"
        img_path = os.path.join(images_dir, img_filename)
        pil_img.save(img_path)
        rendered.append((page_num + 1, img_filename))

    pdf.close()
    return rendered


def write_manifest(source_name, total_pages, rendered, output_dir):
    manifest_path = os.path.join(output_dir, "image-pdf-manifest.md")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"# Image PDF Extraction Manifest\n\n")
        f.write(f"## Source: {source_name}\n")
        f.write(f"## Total Pages: {total_pages}\n")
        f.write(f"## Status: Images rendered, awaiting AI visual extraction\n\n")
        f.write(f"## Instructions for AI Agent\n")
        f.write(f"For each page image below, use visual recognition to extract:\n")
        f.write(f"- All text content (headings, body text, labels, data)\n")
        f.write(f"- Table structures (rows, columns, values)\n")
        f.write(f"- Chart/graph descriptions (type, data points, trends)\n")
        f.write(f"- Image descriptions (diagrams, photos)\n\n")
        f.write(f"## Pages\n")
        for page_num, img_filename in rendered:
            f.write(f"- Page {page_num}: images/{img_filename}\n")
    return manifest_path


def write_index(source_name, page_types, text_files, manifest_path, output_dir):
    index_path = os.path.join(output_dir, "00-index.md")
    text_count = sum(1 for t in page_types.values() if t == "text")
    image_count = sum(1 for t in page_types.values() if t == "image")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# Source Index\n\n")
        f.write(f"- Source: {source_name}\n")
        f.write(f"- Total pages: {len(page_types)}\n")
        f.write(f"- Text pages: {text_count}\n")
        f.write(f"- Image pages: {image_count}\n")
        if text_files:
            f.write(f"- Text files: {', '.join(text_files)}\n")
        if manifest_path:
            f.write(f"- Image manifest: image-pdf-manifest.md\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs; render image-type pages as PNG for AI visual extraction"
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument(
        "--output",
        "-o",
        default="materials",
        help="Output directory (default: materials/)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for image rendering (default: 200)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.pdf_file):
        print(f"Error: File not found: {args.pdf_file}")
        sys.exit(2)

    check_deps()

    source_name = os.path.basename(args.pdf_file)
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    reader = load_pdf(args.pdf_file)
    page_types = classify_pages(reader)
    total = len(reader.pages)

    text_count = sum(1 for t in page_types.values() if t == "text")
    image_count = sum(1 for t in page_types.values() if t == "image")

    print(f"PDF: {source_name}")
    print(f"Total pages: {total}")
    print(f"Text pages: {text_count}")
    print(f"Image pages: {image_count}")

    text_files = []
    manifest_path = None

    if text_count > 0:
        print(f"\nExtracting text from {text_count} page(s)...")
        text_files = extract_text_pages(reader, page_types, output_dir)
        print(f"  Wrote {len(text_files)} text file(s)")

    if image_count > 0:
        print(f"\nRendering {image_count} image page(s) as PNG...")
        rendered = render_image_pages(args.pdf_file, page_types, output_dir)
        print(f"  Rendered {len(rendered)} image(s)")
        manifest_path = write_manifest(source_name, total, rendered, output_dir)
        print(f"  Manifest: {manifest_path}")

    write_index(source_name, page_types, text_files, manifest_path, output_dir)
    print(f"\nDone. Output in: {output_dir}/")


if __name__ == "__main__":
    main()
