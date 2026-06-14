# EPUB Fixer - Vietnamese Punctuation Spacing Corrector

A Python command-line tool (CLI) that automatically fixes missing spaces after punctuation marks (such as `. , : ; ! ? " ) } ]`) in Vietnamese EPUB files.

The tool is optimized to preserve HTML structure and ignores common exceptions, such as:
- Domain names, URLs, and emails (e.g., `google.com`, `user@email.com`)
- Decimals and hierarchical numbers (e.g., `3.14`, `1.2.3`, `1,000`)
- Common abbreviations (e.g., `Tp.HCM`, `PGS.TS.`, `ThS.`, `U.S.A`)

## Requirements

Ensure you have Python installed on your computer. Install the required libraries by running:

```bash
pip install beautifulsoup4 lxml
```
*(Note: If you run into PEP 668 externally-managed-environment errors on macOS/Homebrew, you can use a virtual environment: `python3 -m venv .venv && source .venv/bin/activate && pip install beautifulsoup4 lxml` or use the `--break-system-packages` flag).*

## Usage

Simply copy and run the following command in your terminal, replacing the paths with your files:

**Syntax:**
```bash
python3 epub_fixer.py <path_to_input_epub> <path_to_output_epub>
```

**Example:**
```bash
python3 epub_fixer.py input.epub output.epub
```

*Note: If your filenames contain spaces, wrap them in double quotes (e.g., `"my book.epub"`).*

## How It Works

1. Unzips the original EPUB file.
2. Extracts the `mimetype` file and ensures it is kept uncompressed (stored mode).
3. Scans all content source files (`.html`, `.xhtml`, `.htm`) and parses their DOM using `BeautifulSoup` with the `xml` parser.
4. Identifies text nodes (skipping tag names/attributes) and applies regex pattern matching to add a space after punctuation if it is immediately followed by a word/number.
5. Re-compresses everything back into a fully compliant EPUB file.

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

If you encounter bugs or have feature requests, please open an Issue.

## License

This project is licensed under the [MIT License](LICENSE).
