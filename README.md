# pdfsplit

A command-line tool to split PDF files into individual pages, page ranges, or chunks with customizable naming and output options.

## Installation

Install via PyPI:

```bash
pip install pdfsplit
```

This installs the `pdfsplit` command, along with dependencies (`PyPDF2`, `tqdm`).

## Usage

```bash
pdfsplit input.pdf [-p PAGES] [-g GRANULARITY] [-d DIRECTORY] [--prefix PREFIX] [--force] [-q] [--version]
```

### Options
- `input_pdf`: Path to the input PDF file (required).
- `-p, --pages PAGES`: Specify pages or ranges (e.g., `1,3,5-7,10-` for pages 1, 3, 5-7, and 10 to end).
- `-g, --granularity GRANULARITY`: Split into chunks of N pages (default: 1, used if no `--pages`).
- `-d, --directory DIRECTORY`: Output directory (default: current directory).
- `--prefix PREFIX`: Custom filename prefix (default: input PDF filename without extension).
- `--force`: Overwrite existing files without prompting.
- `-q, --quiet`: Suppress progress bar and non-error output.
- `--version`: Show version (1.0).
- `-h, --help`: Show help message.

### Examples
1. Split a 20-page PDF into single pages:
   ```bash
   pdfsplit document.pdf
   ```
   Creates: `document_page_01.pdf`, `document_page_02.pdf`, ..., `document_page_20.pdf`.

2. Split into 5-page chunks in `output/` directory:
   ```bash
   pdfsplit document.pdf -g 5 -d output
   ```
   Creates: `output/document_pages_01-05.pdf`, `output/document_pages_06-10.pdf`, etc.

3. Split specific pages/ranges with custom prefix:
   ```bash
   pdfsplit document.pdf -p 1,3,5-7,10- --prefix split -d split_pdfs
   ```
   Creates: `split_pdfs/split_page_01.pdf`, `split_pdfs/split_page_03.pdf`, `split_pdfs/split_pages_05-07.pdf`, `split_pdfs/split_pages_10-20.pdf`.

4. Quiet mode (no output):
   ```bash
   pdfsplit document.pdf -q
   ```

5. Force overwrite existing files:
   ```bash
   pdfsplit document.pdf --force
   ```

## Features
- Splits PDFs by individual pages, ranges, or chunks.
- Zero-padded filenames based on total pages (e.g., `01` for 20 pages, `001` for 200 pages).
- Progress bar for long operations (disabled with `-q`).
- Overwrite protection with interactive prompts (bypass with `--force`).
- Cross-platform (Linux, Windows, macOS) using `pathlib`.
- Specific exit codes for scripting (2: file not found, 3: invalid PDF, 4: empty PDF, 5: directory error, 6: invalid page spec).

## Dependencies
- Python 3.6+
- PyPDF2
- tqdm

## License
MIT License. See `LICENSE` file.

## Contributing
Issues and pull requests are welcome at [https://github.com/EdgeOfAssembly/pdfsplit](https://github.com/EdgeOfAssembly/pdfsplit).

## Author
EdgeOfAssembly (haxbox2000@gmail.com)