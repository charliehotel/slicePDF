from pypdf import PdfReader, PdfWriter

# === 설정 ===
input_path = "/Users/charliehotel/Downloads/무제 폴더/한다 마사오;마츠다 마사유키_저작권법 코멘터리 3(제2판)(2015).pdf"  # 원본 PDF 경로
output_prefix = "output"  # 저장할 파일 이름 앞부분
page_ranges = [
    (1, 300),
    (301, 600),
    (601, 900),
    (901, 1075)
]  # (시작페이지, 끝페이지) 목록

# === 실행 ===
reader = PdfReader(input_path)

for i, (start, end) in enumerate(page_ranges, start=1):
    writer = PdfWriter()

    for page_num in range(start - 1, end):
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])

    output_path = f"/Users/charliehotel/Downloads/무제 폴더/{output_prefix}{i}.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"✔ 저장 완료: {output_path} ({start}–{end}페이지)")