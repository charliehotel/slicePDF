# slicePDF.py

from pypdf import PdfReader, PdfWriter
import os
import math

def parse_ranges_manual(ranges_str, total_pages):
    """e.g. '1-10,11-20' → [(1, 10), (11, 20)]"""
    try:
        ranges = []
        for part in ranges_str.split(','):
            start, end = map(int, part.strip().split('-'))
            if start < 1 or end > total_pages:
                raise ValueError(f"Invalid range: {start}-{end} (PDF has {total_pages} pages).")
            if start > end:
                raise ValueError(f"Start page ({start}) cannot be greater than end page ({end}).")
            ranges.append((start, end))
        return ranges
    except Exception as e:
        print(f"❌ Range parsing error: {e}")
        exit(1)

def parse_ranges_auto(part_str, total_pages):
    """e.g. '/3' → [(1, 25), (26, 50), (51, 74)]"""
    try:
        num_parts = int(part_str[1:])
        if num_parts < 1:
            raise ValueError("The number of parts must be at least 1.")
        ranges = []
        chunk_size = math.ceil(total_pages / num_parts)
        for i in range(num_parts):
            start = i * chunk_size + 1
            end = min((i + 1) * chunk_size, total_pages)
            ranges.append((start, end))
        return ranges
    except Exception as e:
        print(f"❌ Auto split parsing error: {e}")
        exit(1)

def split_pdf(reader, input_path, page_ranges):
    total_pages = len(reader.pages)
    input_dir = os.path.dirname(input_path)
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    for i, (start, end) in enumerate(page_ranges, start=1):
        writer = PdfWriter()
        for page_num in range(start - 1, end):
            if page_num < total_pages:
                writer.add_page(reader.pages[page_num])

        output_filename = f"{base_filename}_Part{i}.pdf"
        output_path = os.path.join(input_dir, output_filename)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"✔ Saved: {output_path} ({start}–{end})")

if __name__ == "__main__":
    print("🔹 slicePDF CLI 🔹")

    reader = None
    input_path = ""

    # File path validation and open
    while True:
        input_path = input("📂 Enter path to input PDF file: ").strip().strip("'\"")
        if not os.path.isfile(input_path):
            print(f"❌ File not found: {input_path}\nPlease try again.\n")
            continue

        try:
            reader = PdfReader(input_path)
        except Exception as e:
            print(f"❌ Failed to open PDF: {e}")
            continue

        if reader.is_encrypted:
            print("🔐 This PDF is encrypted.")
            try:
                password = input("🔑 Enter password (or press Enter to try without one): ").strip()
                success = reader.decrypt(password)
                if success == 0:
                    print("❌ Incorrect password or unable to decrypt.\n")
                    continue
                else:
                    print("✅ Decryption successful.")
            except Exception as e:
                print(f"❌ Decryption error: {e}")
                continue

        total_pages = len(reader.pages)
        print(f"📄 PDF loaded successfully. Total pages: {total_pages}\n")
        break

    # Range input (manual or auto)
    print("✂ Enter page ranges to split:")
    print("→ Manual mode: 1-20,21-50,51-74")
    print("→ Auto mode: /3 (split into 3 equal parts)")
    range_input = input("Input: ").strip()

    if range_input.startswith("/"):
        page_ranges = parse_ranges_auto(range_input, total_pages)
    else:
        page_ranges = parse_ranges_manual(range_input, total_pages)

    # Run split
    split_pdf(reader, input_path, page_ranges)
