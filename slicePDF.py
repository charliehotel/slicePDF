# slicePDF.py

from pypdf import PdfReader, PdfWriter
import os
import math

def parse_ranges_manual(ranges_str, total_pages):
    """e.g. '1-10,11-20' → [(1, 10), (11, 20)]"""
    ranges = []
    # If empty input
    if not ranges_str.strip():
        raise ValueError("Range string is empty.")

    for part in ranges_str.split(','):
        if not part.strip():
            continue
        try:
            if '-' in part:
                start, end = map(int, part.strip().split('-'))
            else:
                # Single page case
                start = end = int(part.strip())
        except ValueError:
             raise ValueError(f"Invalid format in '{part}'. Expected 'start-end' or single page number.")
             
        if start < 1 or end > total_pages:
            raise ValueError(f"Invalid range: {start}-{end} (PDF has {total_pages} pages).")
        if start > end:
            raise ValueError(f"Start page ({start}) cannot be greater than end page ({end}).")
        ranges.append((start, end))
    return ranges

def parse_ranges_auto(part_str, total_pages):
    """e.g. '/3' → [(1, 25), (26, 50), (51, 74)]"""
    try:
        num_parts = int(part_str[1:])
    except ValueError:
        raise ValueError("Invalid auto-split format. Expected '/N' where N is a number.")
        
    if num_parts < 1:
        raise ValueError("The number of parts must be at least 1.")
    
    ranges = []
    base_size = total_pages // num_parts
    remainder = total_pages % num_parts
    
    current_start = 1
    
    for i in range(num_parts):
        # Distribute the remainder pages one by one to the first 'remainder' chunks
        size = base_size + 1 if i < remainder else base_size
        
        if size == 0:
            break # Should not happen if total_pages >= num_parts
            
        end = current_start + size - 1
        # Clamp end to total_pages just in case, though math ensures it fits exactly
        end = min(end, total_pages)
        
        ranges.append((current_start, end))
        current_start = end + 1
        
        if current_start > total_pages:
            break
            
    return ranges

def split_pdf(input_path, page_ranges, password=None):
    input_dir = os.path.dirname(input_path)
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    created_files = []

    # Open file fresh to ensure no stale handle issues
    reader = PdfReader(input_path)
    if reader.is_encrypted and password:
        reader.decrypt(password)
    
    total_pages = len(reader.pages)

    for i, (start, end) in enumerate(page_ranges, start=1):
        writer = PdfWriter()
        # Pages are 0-indexed in pypdf, but 1-indexed in UI
        added_count = 0
        for page_num in range(start - 1, end):
            if page_num < total_pages:
                writer.add_page(reader.pages[page_num])
                added_count += 1
        
        if added_count > 0:
            # Format: 'Base_1.pdf' or 'Base_2-4.pdf'
            if start == end:
                range_suffix = f"{start}"
            else:
                range_suffix = f"{start}-{end}"
                
            output_filename = f"{base_filename}_{range_suffix}.pdf"
            output_path = os.path.join(input_dir, output_filename)

            with open(output_path, "wb") as f:
                writer.write(f)
            
            print(f"✔ Saved: {output_path} ({start}–{end})")
            created_files.append(output_path)
            
    return created_files

def main():
    print("🔹 slicePDF CLI 🔹")

    reader = None
    input_path = ""
    password = None

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
    while True:
        print("✂ Enter page ranges to split:")
        print("→ Manual mode: 1-20,21-50,51-74")
        print("→ Auto mode: /3 (split into 3 equal parts)")
        range_input = input("Input: ").strip()

        try:
            if range_input.startswith("/"):
                page_ranges = parse_ranges_auto(range_input, total_pages)
            else:
                page_ranges = parse_ranges_manual(range_input, total_pages)
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    # Run split
    split_pdf(input_path, page_ranges, password=password)

if __name__ == "__main__":
    main()
