# Release Notes

## v0.2 (2026-01-17)
*Current Release*

### Major Improvements
- **Robust File Handling**: Completely rewritten file access logic. The splitter now creates a fresh file handle for each output operation. This resolves intermittent issues with blank pages or stale file buffers.
- **Smarter Auto-Split**: Improved the automatic splitting algorithm (`/N` mode). It now uses modulo arithmetic to distribute pages as evenly as possible (e.g., 16 pages into 5 parts becomes 4, 3, 3, 3, 3), ensuring the exact requested number of files is generated.
- **Descriptive Filenames**: Output files are now named with their specific page ranges (e.g., `MyDoc_1-3.pdf`, `MyDoc_4.pdf`) instead of generic part numbers (`Part1`, `Part2`), making it easier to identify contents.

### Bug Fixes
- Fixed a logic error where `Auto Split` could produce fewer files than requested due to rounding.
- Fixed variable scope issues for password handling in the CLI `main` loop.
- Improved error handling to be more graceful (raising exceptions instead of immediate exit), allowing for better integration with other tools (like the new GUI).

---

## v0.1 (Initial Release - 2025-08-15)

### Features
- **CLI Interface**: Simple command-line tool for quick PDF splitting.
- **Manual Mode**: Support for separating specific page ranges (e.g., `1-5, 8, 11-15`).
- **Auto Mode**: Support for splitting a PDF into N equal parts.
- **Encryption Support**: Handles password-protected PDF files.
- **Core Library**: Built on `pypdf` for reliable PDF processing.
