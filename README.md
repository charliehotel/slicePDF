# slicePDF

**slicePDF** is a simple command-line tool to split a PDF file into multiple parts by custom page ranges or evenly-sized segments.


---

## 📦 Features

- ✅ Split PDF by custom ranges (e.g., `1-5,6-10`)
- ✅ Split PDF evenly by number of parts (e.g., `/3` for 3 parts)
- ✅ Handles encrypted PDFs with password
- ✅ Lightweight, no GUI required

---

## 🛠 Requirements

- Python 3.8+
- `pypdf` (See `requirements.txt`)

Install:

```bash
pip install -r requirements.txt
```

## 🚀 Usage
```bash
python slicePDF.py
```

You will be prompted to enter:

1. Input PDF file path
2. Page ranges, either:
  - Manual: `1-3,4-6,7-10`
  - Auto: `/3` to divide the PDF into 3 equal parts
The program saves output files as:
```python
yourfile_Part1.pdf
yourfile_Part2.pdf
...
```

## 📝 Example
```python
🔹 slicePDF CLI 🔹
📂 Enter path to input PDF file: /Users/you/Documents/report.pdf
📄 PDF loaded successfully. Total pages: 12

✂ Enter page ranges to split:
→ Manual mode: 1-4,5-8,9-12
→ Auto mode: /3 (split into 3 equal parts)
Input: /3

✔ Saved: report_Part1.pdf (1–4)
✔ Saved: report_Part2.pdf (5–8)
✔ Saved: report_Part3.pdf (9–12)
```
