# RepoXray

> **X-ray vision for your local Git repository.**

RepoXray is an offline-first Python command-line tool for quickly understanding a local codebase. It inventories the repository, detects languages, identifies large files, builds a compact tree, checks local Git state, looks for likely sensitive material, and calculates a transparent health score.

It is intentionally small: no cloud account, API key, database, Docker daemon, background service, or runtime third-party dependency is required.

```text
╭──────────────────────────────────────────────────────────╮
│                         RepoXray                         │
│           X-ray vision for your Git repository           │
╰──────────────────────────────────────────────────────────╯

Repository       /work/my-project
Files            147
Directories      23
Size             4.8 MB

Languages
─────────
Python           ██████████████        71.0%  (41 files)
TypeScript       █████                 23.0%  (18 files)
CSS              █                      6.0%  (4 files)

Repo Health
───────────
87/100
✓ README found (+12)
✓ No obvious secrets found (+5)
⚠ No tests directory found
```

## What it does

- Scans a local directory recursively and reports file count, directory count, total size, hidden files, ignored paths, extensions, and largest files.
- Detects common languages from file extensions and shows a byte-weighted percentage breakdown.
- Renders a deliberately bounded tree so a large repository does not overwhelm the terminal.
- Highlights files at or above the large-file threshold (5 MiB by default).
- Checks files locally for likely API keys, tokens, password assignments, private keys, and sensitive filenames without exposing detected values.
- Reads local Git metadata when available: branch, working tree cleanliness, commit count, and `origin` remote URL.
- Produces a transparent heuristic health score from 0 to 100.
- Emits a complete JSON document for scripts, CI jobs, or other local automation.

## Tech stack

| Area | Choice | Why |
| --- | --- | --- |
| Language | Python 3.9+ | Portable standard-library CLI implementation. |
| CLI parsing | `argparse` | Built into Python; no dependency needed. |
| File scanning | `pathlib` and `os.walk` | Fast local metadata traversal. |
| Secret heuristics | `re` | Local pattern matching with redacted findings. |
| Git integration | `subprocess` calling local `git` | No GitHub API or network access. |
| Terminal UI | ANSI sequences with ASCII fallback | Colored output in capable terminals, reliable output in legacy Windows consoles. |
| Packaging | `pyproject.toml`, setuptools, wheel | Modern installable Python package and console script. |
| Tests | `unittest` | Standard-library test suite; no test runner installation required. |

RepoXray has **zero runtime dependencies**. `setuptools` and `wheel` are build-time requirements used only when installing or building the package.

## Requirements

### Required

- Python **3.9 or newer**.
- A local directory that you are allowed to read.

### Optional

- Git on your `PATH` for branch, commit, remote, and working-tree information.
- `pip` to install the `repoxray` console command.
- A UTF-8-capable terminal for Unicode box drawing and block characters. RepoXray automatically falls back to ASCII when the terminal cannot encode them.

### Not required

- Internet access while running scans.
- GitHub credentials or a GitHub API token.
- A database, Docker, Node.js, or any cloud service.

## Installation

### Run from a source checkout

From the directory containing `repoxray/` and `pyproject.toml`:

```bash
python -m repoxray .
```

On Windows, `py` is also commonly available:

```powershell
py -m repoxray .
```

### Install the CLI command

Use a virtual environment for development or a user-level installation for personal tooling:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install .
repoxray .
```

The package installs one console entry point:

```text
repoxray = repoxray.cli:main
```

## Quick start

```bash
# General overview of the current directory
python -m repoxray .

# Scan a different local repository
repoxray ../another-project

# Learn every option
repoxray --help
```

## CLI reference

```text
repoxray [OPTIONS] [PATH]
```

`PATH` is optional and defaults to the current directory (`.`).

| Command or option | Description |
| --- | --- |
| `repoxray .` | Full human-readable repository report. |
| `repoxray ./my-project` | Scan a specific local directory. |
| `repoxray --json .` | Emit the complete report as JSON and nothing else. |
| `repoxray --tree .` | Show the overview and compact project tree. |
| `repoxray --secrets .` | Show the overview and sensitive-content findings. |
| `repoxray --health .` | Show the overview, health score, and every scoring rule. |
| `repoxray --include-ignored .` | Include normally skipped generated directories. Use carefully on large projects. |
| `repoxray --max-depth 3 --tree .` | Limit tree recursion depth; default is `4`. |
| `repoxray --max-tree-entries 40 --tree .` | Limit visible tree entries; default is `80`. |
| `repoxray --large-file-threshold-mb 20 .` | Treat files of 20 MiB or larger as large files. Default is `5`. |
| `repoxray --no-color .` | Disable ANSI colors. Unicode still falls back automatically if unsupported. |
| `repoxray --version` | Print the installed RepoXray version. |
| `repoxray --help` | Display the built-in help text. |

Options may appear before or after the path. For example, both `repoxray --json .` and `repoxray . --json` are valid.

### Command behavior and exit codes

RepoXray is read-only with respect to the directory it scans. A successful scan returns exit code `0`. An invalid or non-directory path returns `2` and writes a short error message to standard error. `argparse` also uses exit code `2` for invalid command-line arguments.

The human-readable report goes to standard output. In `--json` mode, standard output contains exactly one JSON document, so it can be safely redirected or piped into another local command:

```bash
repoxray --json . > repoxray-report.json
```

Use `--no-color` whenever output is captured by a log collector or a terminal that does not handle ANSI color codes. RepoXray detects legacy encodings on its own and uses ASCII substitutes for tree and status glyphs when necessary.

## What the scan includes and skips

The filesystem scanner inventories regular, non-symlink files. It does not follow symlinks, which avoids scanning outside the requested repository or becoming trapped in a link loop.

By default, RepoXray skips these conventional generated or dependency directories wherever they occur:

```text
.git          .next          __pycache__    node_modules
.venv         venv           dist           build
.mypy_cache   .pytest_cache  .tox           .nox           .coverage
```

Skipped paths are counted and included in JSON as `ignored_paths`. Use `--include-ignored` only when you explicitly want generated output and dependencies to affect the report.

RepoXray does not currently parse every `.gitignore` rule. This is intentional: the built-in ignore set keeps scanning predictable and dependency-free. `.gitignore` pattern support is on the roadmap.

### Performance boundaries

The scanner records file metadata in memory, so it is designed for ordinary source repositories rather than filesystem-wide inventory jobs. It avoids following symlinks, skips known generated directories by default, and only reads file contents for the sensitive-content scan. That scan reads at most 1 MB per eligible file, skipping binary-looking files after decoding. The tree is separately constrained to four levels and 80 entries by default.

For an intentionally large monorepo, begin with the defaults and increase tree limits only when you need more structure. Avoid `--include-ignored` unless dependency directories and build output are relevant to the question you are investigating.

## Language detection

Language detection is extension-based and runs without a parser or external service. The map includes Python, JavaScript, TypeScript, HTML, CSS, Sass/SCSS/Less, Java, Kotlin, Go, Rust, C/C++, C#, Ruby, PHP, Swift, Scala, Shell, PowerShell, SQL, R, Dart, Lua, Elixir, Erlang, F#, Vue, Svelte, Markdown, JSON, YAML, TOML, XML, and more.

Percentages are calculated from the **total bytes of recognized files**, not line counts. This is fast and encoding-agnostic, but it means generated source files can influence results when `--include-ignored` is used.

Unknown extensions are included in the extension breakdown and total size, but not assigned to a language.

## Large-file detection

The default large-file threshold is **5 MiB** (`5 × 1024 × 1024` bytes). The main report always lists the eight biggest scanned files; the large-file section changes its heading and adds a warning when one or more files meet the threshold.

Adjust it for projects that intentionally contain media, models, fixtures, or databases:

```bash
repoxray --large-file-threshold-mb 50 .
```

Large files are not automatically bad. The report is a prompt to inspect them, not a claim that they should be deleted.

## Sensitive-content scan

RepoXray’s secret scanner is a **local heuristic**, not a security audit. It reads text-like files up to 1 MB and looks for patterns such as:

- Private-key headers.
- AWS-style access key IDs.
- GitHub token prefixes.
- API key, secret key, access token, and auth token assignments.
- Password-like assignments.
- Sensitive filenames including `.env`, `credentials.json`, `service-account.json`, `id_rsa`, and common key/certificate suffixes.

For every finding, RepoXray reports only:

```text
[HIGH] possible API key assignment in config.py:42
```

It **never prints, serializes, or sends the matched value**. Binary-looking files are skipped, obvious placeholder values are ignored, and files larger than 1 MB receive filename checks only. A clean result does not prove that a repository contains no secrets; a finding does not prove that a real secret is present.

Everything runs on the machine that invokes the command. RepoXray never opens a network connection to scan repository contents.

## Git awareness

When `git` is installed and the target is inside a working tree, RepoXray reads local-only metadata with Git commands equivalent to:

```text
git -C PATH rev-parse --is-inside-work-tree
git -C PATH branch --show-current
git -C PATH status --porcelain
git -C PATH rev-list --count HEAD
git -C PATH config --get remote.origin.url
```

It does not invoke `git add`, `git commit`, `git push`, or any other mutating Git operation. If Git is unavailable or the path is not a repository, scanning still works and the report states that Git metadata is unavailable.

## Health score

The health score is a visible, deliberately non-scientific heuristic. It starts at 35, is clamped to the range 0–100, and uses the following rules from `repoxray/health.py`:

| Rule | Points | Condition |
| --- | ---: | --- |
| Base score | +35 | Every scan starts here. |
| README | +12 | `README` or `README.md` exists at the repository root. |
| `.gitignore` | +10 | `.gitignore` exists at the repository root. |
| Tests | +10 | A `tests`, `test`, `spec`, or `specs` directory is present. |
| Package metadata | +8 | Recognized metadata such as `pyproject.toml` or `package.json` is present. |
| Source structure | +5 | A conventional source directory such as `src`, `app`, `lib`, or `packages` is present. |
| Git repository | +5 | Local Git metadata is available. |
| No heuristic findings | +5 | The sensitive-content scan found nothing. |
| Large files | −8 each, maximum −16 | One or two or more files exceed the configured threshold. |
| High secret finding | −20 each | A high-severity heuristic finding is present. |
| Medium secret finding | −8 each | A medium-severity heuristic finding is present. |
| Low secret finding | −3 each | A low-severity heuristic finding is present. |
| Generated clutter | −5 | Three or more top-level generated directories were ignored. |

Run `repoxray --health .` to see both the outcome and this rule list in the terminal. Use the score as a quick conversation starter, not as a release gate or a measurement of engineering quality.

## JSON output

Use JSON mode when another program needs the results:

```bash
repoxray --json .
repoxray --json --tree .
```

The command writes one JSON document to standard output. Its top-level shape is:

```json
{
  "repository": "/absolute/path/to/project",
  "files": 124,
  "directories": 18,
  "size_bytes": 1234567,
  "hidden_files": 4,
  "ignored_paths": ["node_modules"],
  "extensions": {".py": 12},
  "languages": {
    "Python": {"bytes": 42000, "files": 12, "percentage": 82.3}
  },
  "largest_files": [{"path": "data/example.db", "size_bytes": 500000}],
  "large_files": [],
  "secrets": [],
  "git": {
    "is_repository": true,
    "branch": "main",
    "is_clean": true,
    "commit_count": 42,
    "remote_url": "https://github.com/example/project.git",
    "error": null
  },
  "health": {
    "score": 87,
    "positives": [],
    "warnings": [],
    "rules": []
  }
}
```

`secrets` contains redacted finding metadata only: severity, category, path, message, and (when available) line number. Add `--tree` to include the compact tree string as a `tree` field.

## Architecture

```text
repoxray/
├── __init__.py    # package metadata and version
├── __main__.py    # enables: python -m repoxray
├── cli.py         # argparse options, orchestration, JSON mode
├── models.py      # typed report data structures and serialization
├── scanner.py     # filesystem inventory, extensions, file sizes
├── analyzer.py    # extension-to-language analysis
├── secrets.py     # redacted local heuristic checks
├── gitinfo.py     # read-only local Git inspection
├── health.py      # public health scoring rules and calculation
├── tree.py        # compact, bounded directory tree
└── output.py      # formatted terminal report and encoding fallback

tests/
├── test_scanner.py   # scan counts, bytes, ignored directories
├── test_analyzer.py  # language detection percentages
├── test_secrets.py   # fake-secret detection and redaction behavior
└── test_health.py    # transparent score calculation
```

### Data flow

1. `cli.py` parses the command and resolves the target path.
2. `scanner.py` creates a `ScanResult` with metadata for eligible files.
3. `analyzer.py`, `secrets.py`, `gitinfo.py`, and `scanner.py` derive languages, findings, Git state, and file rankings.
4. `health.py` converts those facts into an explainable `HealthReport`.
5. `output.py` renders the terminal report, or `cli.py` serializes all report objects to JSON.

This separation keeps filesystem traversal, detection logic, scoring, presentation, and serialization independently testable.

## Development

### Run the test suite

```bash
python -m unittest discover -s tests -v
```

The suite uses temporary directories and a deliberately fake token value. It never creates a real credential or contacts the network.

### Run the tool against itself

```bash
python -m repoxray .
python -m repoxray --json .
python -m repoxray --health .
```

### Build an installable package

```bash
python -m pip install .
repoxray --version
```

For a distributable wheel, use your preferred Python build workflow. The project follows PEP 517 through `pyproject.toml` and declares setuptools and wheel as build requirements.

### Using JSON in local automation

JSON mode is intended for scripts, CI checks, and editor tasks that want repository facts without scraping terminal formatting. For example, this standard-library Python command prints the health score from a generated report:

```bash
repoxray --json . > repoxray-report.json
python -c "import json; print(json.load(open('repoxray-report.json', encoding='utf-8'))['health']['score'])"
```

The tool itself does not currently turn findings into failing exit codes. If a CI workflow needs that behavior, consume the `health`, `large_files`, or `secrets` fields and apply the policy that fits that repository.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `No module named repoxray` | The command was run outside the source checkout and RepoXray is not installed. | Run it from the directory containing `repoxray/`, or install it with `python -m pip install .`. |
| `repoxray` is not recognized | The package was installed in a different virtual environment or its scripts directory is not active. | Activate the environment used for installation, then run `repoxray --version`. Alternatively use `python -m repoxray .` from the source checkout. |
| Git section says it is not a repository | The target is not inside a Git worktree, or `git` is unavailable on `PATH`. | Scan the repository root or install/configure Git. The remaining analysis still works. |
| Output uses ASCII boxes or `#` bars | The terminal encoding cannot print the Unicode UI characters. | This is an automatic compatibility fallback; switch the terminal to UTF-8 for the Unicode display. |
| Scan is slower or noisier than expected | Generated output was explicitly included or the repository contains many non-standard generated files. | Remove `--include-ignored`, scan a narrower path, or wait for configurable ignore rules from the roadmap. |

## Limitations and deliberate non-goals

- RepoXray is not a replacement for a full secret-scanning, dependency-auditing, SAST, or license-compliance tool.
- It detects languages by filename extension, not by parsing source code or counting lines.
- It does not apply arbitrary `.gitignore` patterns yet.
- It does not inspect remote GitHub data or make network calls.
- It does not modify the scanned directory, except for normal Python bytecode caches if the tool itself is run from a source checkout.
- The health score is a heuristic and should not be treated as an objective project-quality metric.

## Roadmap

- Optional `.gitignore` pattern support.
- Configurable custom ignore rules and secret patterns.
- File-type and license summaries.
- Baseline comparisons between two local scans.
- Optional CI-friendly threshold exit codes.

## License

MIT
