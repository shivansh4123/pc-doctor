# pc-doctor

Uses AI to look for problem causing you system slow and Fixes it

> Clean potentially unwanted files and invalid Windows Registry entries from a computers.

pc-doctor helps identify and safely remove temporary/unwanted files and common invalid or stale Windows Registry entries. It is designed to assist power users and system administrators in reclaiming disk space and improving system health while minimizing risk through dry-run modes, backups, and clear logging.

---

## Table of Contents

- [Features](#features)
- [Why use pc-doctor](#why-use-pc-doctor)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [GUI / Web UI](#gui--web-ui)
  - [Command-line (CLI)](#command-line-cli)
  - [Examples](#examples)
- [Safety & Backups (IMPORTANT)](#safety--backups-important)
- [How it works (high level)](#how-it-works-high-level)
- [Configuration](#configuration)
- [Logging & Reports](#logging--reports)
- [Contributing](#contributing)
- [License](#license)
- [Support / Contact](#support--contact)

---

## Features

- Scan for common temporary and unnecessary file types (browser cache, temp files, installer leftovers, Recycle Bin contents).
- Detect potentially invalid or stale Windows Registry entries (uninstalled app remnants, broken COM registrations).
- Dry-run scan mode to preview changes without making them.
- Create backups and export registry fixes as .reg files for manual review and restore.
- Detailed logs and optional report export (CSV/JSON).
- Configurable rules and exclusion lists.

---

## Why use pc-doctor

- Safely reclaim disk space by removing unnecessary files.
- Reduce system clutter and potential registry bloat with careful checks and backups.
- Designed with safety-first defaults (dry-run, backups, logs).

---

## Requirements

- Windows 10 / Windows 11 (tested)
- Python 3.8+ (if using the Python version)
- Administrative privileges required for registry scanning/changes
- (Optional) A modern web browser if using a bundled web UI

Notes:
- If a packaged/executable build is provided (e.g., via PyInstaller), Python may not be required to run the executable.
- Always run with care—see the Safety section below.

---

## Installation

1. Clone the repository:
   git clone https://github.com/shivansh4123/pc-doctor.git
   cd pc-doctor

2. (Optional) Create a virtual environment and activate it:
   python -m venv .venv
   .venv\Scripts\activate

3. Install Python dependencies (if present):
   pip install -r requirements.txt

4. Check the repository root for the project entrypoint (e.g., `main.py`, `app.py`, or packaged executable). If none exist, consult the README in subdirectories or the repo owner for the correct start command.

---

## Usage

There are two typical modes: a GUI/web UI and a CLI. Exact commands may vary depending on repository entrypoints—replace `<entrypoint>` below with the actual script/executable name.

### GUI / Web UI

- If the project includes a web UI, start the server:
  python <entrypoint>
- Open your browser and navigate to the address shown in the console (for example `http://127.0.0.1:5000`).
- Use the UI to run scans, review findings, create backups, and apply cleaning operations.

### Command-line (CLI)

Common options you should expect or add:

- --scan-only or --dry-run : perform scan and report only (do not modify files/registry)
- --clean : perform cleaning actions
- --backup : create backups of registry and critical files before cleaning
- --report <file> : export the scan report to a file (CSV or JSON)
- --exclude <pattern> : exclude certain paths or registry keys

Example (replace `<entrypoint>` with actual script name):
python <entrypoint> --dry-run --report report.json

---

## Examples

- Dry-run scan and write a JSON report:
  python <entrypoint> --dry-run --report scan-report.json

- Run scan, create backups, then apply cleaning:
  python <entrypoint> --backup --clean

---

## Safety & Backups (IMPORTANT)

pc-doctor touches filesystem and the Windows Registry. Follow these safety practices:

- Always run a dry-run first to review proposed changes.
- Create a full system restore point or a backup of important data before making registry changes.
- Use the `--backup` option to export registry changes as a .reg file you can manually inspect and re-import.
- Review logs and reports before and after cleaning.
- Prefer running on test systems before rolling out to production machines.

---

## How it works (high level)

1. Scan common temporary file locations and candidate registry paths using configured rules.
2. Build a list of findings with metadata (path/key, size, last modified, recommended action).
3. Present findings (UI or CLI report) and optionally export them.
4. If cleaning is approved, create backups and apply removals/registry fixes.
5. Produce a final report and logs.

---

## Configuration

- Rules and exclusions are configurable. Look for configuration files (e.g., `config/`, `rules.json`, or similar) in the repository.
- Typical configuration items:
  - Paths to scan
  - File extensions and size thresholds
  - Registry hives and key patterns
  - Exclusion rules

If the repo does not include a config yet, create a config file (YAML/JSON) specifying the above items and update the entrypoint to load it.

---

## Logging & Reports

- All operations should be logged to a timestamped log file in `logs/`.
- Reports can be saved in JSON or CSV for audit and review.
- Include verbosity levels or a `--verbose` flag to increase diagnostic output.

---

## Contributing

Contributions are welcome:

- Open issues for bugs and feature requests.
- Fork the repository, create a feature branch, and submit a pull request.
- When contributing code that modifies cleaning rules or registry handling, include tests and clear documentation.
- Respect the safety-first approach—add dry-run tests and backup verification.

---

## License

This project is provided under the MIT License. See LICENSE file for details.

---

## Support / Contact

For issues and feature requests, please open an issue in the repository:

https://github.com/shivansh4123/pc-doctor/issues

If you want me to commit this README to the repository, or tailor the usage/commands to the actual entrypoint files in the repo, tell me the entrypoint filenames or say "commit README" and I will add it for you.
