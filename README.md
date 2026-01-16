# slicePDF

**slicePDF** is a simple, robust command-line tool to split a PDF file into multiple parts by custom page ranges or evenly-sized segments.

---

## 📦 Features

- ✅ **Manual Split**: Split PDF by custom ranges (e.g., `1-5,6-10`) or single pages (`1, 5, 10`).
- ✅ **Auto Split**: Split PDF evenly by number of parts (e.g., `/3` for 3 parts).
    - *Improved in v0.2*: Distributes pages as evenly as possible (e.g., 16 pages / 5 parts → 4, 3, 3, 3, 3).
- ✅ **Descriptive Filenames**: Output files are named based on their content (e.g., `doc_1-4.pdf`, `doc_5.pdf`).
- ✅ **Secure**: Handles password-protected PDFs.
- ✅ **Robust**: Fresh file handling ensures no blank pages or stale buffers.

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

1. **Input PDF file path**
2. **Page ranges**, either:
  - Manual: `1-3,4-6,7-10`
  - Auto: `/3` to divide the PDF into 3 equal parts

The program saves output files in the same directory using the format:
```text
OriginalName_1-3.pdf
OriginalName_4-6.pdf
...
```

## 📝 Example
```text
🔹 slicePDF CLI 🔹
📂 Enter path to input PDF file: /Users/you/Documents/report.pdf
📄 PDF loaded successfully. Total pages: 12

✂ Enter page ranges to split:
→ Manual mode: 1-4,5-8,9-12
→ Auto mode: /3 (split into 3 equal parts)
Input: /3

✔ Saved: /Users/you/Documents/report_1-4.pdf (1–4)
✔ Saved: /Users/you/Documents/report_5-8.pdf (5–8)
✔ Saved: /Users/you/Documents/report_9-12.pdf (9–12)
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
