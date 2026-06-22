# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A polyglot personal learning/knowledge monorepo. There is **no top-level build system** — each subdirectory is an independent project (or a collection of notes) with its own toolchain. When working here, `cd` into the specific project directory and use that project's commands. Don't assume a change in one project affects any other.

Top-level directories split into two kinds:

- **Code projects** (have their own build/test): `interpreter/`, `database/`, `http-server/`, `c/`, `rust/`, `go/`, `python/`, `design-patterns/`, `sorting/`, `spark/`, `kafka/`, `scala/`, `java/`, `javascript/`, `shell/`.
- **Notes/reference only** (Markdown, PDFs, xmind diagrams): `english/`, `books/`, `big-data/`, `poetry/`, `docker/`, `graphql/`, `mysql/`, `linux/`, plus the `*.md` files scattered in code dirs (e.g. `c/c.md`, `python/style-guide.md`).

`requirements` at the root is an aggregate pin list for the Python projects (pyspark, pygame, pytest, invoke, numpy/pandas, etc.); individual projects may also have their own `requirements.txt`.

## Key code projects

### `interpreter/` — Pascal-style interpreter (Python)
A full lexer → parser → semantic analyzer → tree-walking interpreter pipeline. Read in this order to understand the flow: `tokens.py`/`keywords.py` → `lexer.py` → `nodes.py` (AST node types) → `parser.py` → `analyzer.py` (`symbols.py` holds the symbol table) → `interpreter.py` (uses `stack.py` + `activation_record.py` for call frames). `errors.py` defines the error hierarchy raised across stages.

Test: `env PYTHONPATH="." pytest` (run from `interpreter/`).

### `database/` — SQL-ish database engine (Python)
Layered engine: `engine.py` is the entry point; `table.py`/`row.py`/`column.py` model storage; `where.py`/`like.py` handle query predicates; `lock.py` handles transactions; `view.py`/`join` logic sits on top. Tests in `tests/` cover engine, table, join, and transaction behavior separately.

Test: `env PYTHONPATH="." pytest` or `inv test` (run from `database/`; `inv` uses `tasks.py`).

### `c/` — C systems-programming exercises
Each subdir is standalone:

- `c/arsenal/` — algorithms/data-structures library tested with the bundled **Unity** framework. `make test` (compiles and runs `test_runner`). Note: `unity/` may need to be present under `c/arsenal/` for the Makefile's `UNITY_ROOT` to resolve. Also contains `af_packet_sniffer.c/h` (raw packet capture).
- `c/database/` — a C database walkthrough tested with **Ruby RSpec**: `make` builds `db`, `make test` runs `rspec` (requires the `Gemfile` deps installed via `bundle`).
- `c/tinyhttpd/` — minimal HTTP server. `make all` builds `httpd` + `client` (links `-lpthread`).
- Loose files (`c/demo.c`, `c/echo_server.c`, `c/learn.c`) compile directly with `gcc`.

### `rust/`
`rust/scrape_url/` is a Cargo project (`reqwest` + `html2md`): `cargo run` / `cargo build` from that dir. Loose `.rs` files (`fib.rs`, `hello.rs`, `match.rs`) compile with `rustc <file>.rs`.

### `http-server/` — Python web-server learning set
Progression from raw socket server to WSGI: `http_server.py` (raw), `wsgi_server.py` (WSGI), `flaskapp.py` (Flask app served by it), `client.py` (test client). Run a server file directly with `python`.

### `go/`
`go/web_framework/main.go` and `go/examples.go` — run with `go run <file>`.

### `python/` — assorted topics
Subdirs are self-contained explorations: `games/`, `intermediate/`, `interview/`, `machine-learning/`, `redis/`, `scapy/`, `scipy/`, `protobuf/`. `python/.python-version` pins the local interpreter (pyenv).

### `design-patterns/` & `sorting/`
Standalone Python files demonstrating one pattern/algorithm each; run individually with `python <file>.py`. `design-patterns/` is grouped into `creational-`, `structural-`, `behavioral-patterns/`.

## Quick command reference

| Project | Test / Run |
| --- | --- |
| `interpreter/` | `env PYTHONPATH="." pytest` |
| `database/` | `env PYTHONPATH="." pytest` or `inv test` |
| `c/arsenal/` | `make test` |
| `c/database/` | `make` then `make test` (needs `bundle`) |
| `c/tinyhttpd/` | `make all` |
| `rust/scrape_url/` | `cargo run` |
| `go/` | `go run <file>` |
| `design-patterns/` / `sorting/` | `python <file>.py` |
| loose `.rs` files | `rustc <file>.rs` |
| loose `.c` files | `gcc <file>.c -o <out>` |

## Conventions

- Python projects that import by package path are run with `env PYTHONPATH="."` from the project root — follow this when adding tests rather than mutating `sys.path`.
- Some inline comments in C (`c/arsenal/`) are in Chinese; match the existing language of a file when editing it.
- Generated/build artifacts (`*.o`, compiled binaries like `c/demo`, `c/database/db`, `rust/.../target/`, `*.class`, `__pycache__`) are ignored or transient — don't commit them.
