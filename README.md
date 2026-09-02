# Antigravity Token Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity](https://img.shields.io/badge/Google%20Antigravity-IDE%20%7C%20CLI%20%7C%202.0-blueviolet.svg)]()
[![Tests: Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

> **The Next-Generation Token, Context & Output Optimization Suite for Google Antigravity IDE & CLI.**  
> Reduces context bloat by 40% to 75%, conserves daily quotas, and maximizes AI agent execution bandwidth.

---

## Overview

**Antigravity Token Optimizer** is a lightweight, zero-dependency context optimization suite engineered specifically for **Google Antigravity (IDE, CLI, and Antigravity 2.0)** and LLM-driven development environments.

It identifies and eliminates conversational fluff, compresses verbose test and compiler streams, extracts code skeletons (AST-based for Python, pattern-based for other languages), compacts structured data payloads, and externalizes session memory into deterministic artifacts.

```
+------------------------------------------------------------------------+
|                   ANTIGRAVITY TOKEN OPTIMIZER                          |
|                                                                        |
|  [Lean Prompts]      --> Strip conversational filler & preambles (15%) |
|  [Surgical Edits]    --> Prevent full-file rewrite regressions   (40%) |
|  [Code Skeletons]    --> AST class/function signature maps       (60%) |
|  [Command Compress]  --> Filter test and build output noise      (50%) |
|  [Data Compactor]    --> Columnar schema & null purge            (50%) |
|  [Context Buffer]    --> Lossless local cache & expand store     (100%)|
|  [Search Dedup]      --> Grep match limiters & line trimmers     (30%) |
|  [Context Memory]    --> Externalized state (BOARD.md)           (50%) |
+------------------------------------------------------------------------+
```

---

## Core Optimization Engines

| Engine Name | Functional Description | Impact Rationale | Estimated Savings |
|---|---|---|---|
| **1. `lean_prompt`** | Strips polite filler, restated user instructions, and lengthy preambles. | Eliminates 100-300 completion tokens per turn. | **15% - 30%** |
| **2. `surgical_edits`** | Enforces targeted block modifications (`replace_file_content`) and sliced views (`view_file`). | Prevents rewriting hundreds of lines for minor changes. | **40% - 70%** |
| **3. `code_skeleton`** | Extracts signatures preserving types and docstrings. Python uses a real AST walk; TS, JS, Go, Rust, Java and C++ use pattern matching over source lines. | Explores architecture without loading implementation bodies. | **60% - 85%** |
| **4. `command_compression`** | Applies output filters to `pytest`, `npm test`, `cargo test`, `go test`, and `git log`. | Discards passing test noise while retaining failure traces. | **50% - 80%** |
| **5. `search_dedup`** | Enforces match limits, truncates long lines (120 chars), and deduplicates search results. | Prevents regex searches from overwhelming the context window. | **30% - 60%** |
| **6. `context_memory`** | Checkpoints state, active tasks, and architecture decisions directly to disk (`BOARD.md`, `LEDGER.md`). | Survives context compaction without degrading model memory. | **50% - 90%** |

Two further capabilities are always available and are not profile-toggleable, so they
are not counted among the six engines above:

| Capability | Functional Description | Where it applies |
|---|---|---|
| `data_compactor` | Transforms object collections into column-oriented tables and strips null/empty keys. | `compress` on structured data |
| `context_buffer` | Lossless local cache holding raw uncompressed output behind a reference token (`ref_...`). | `compress` / `expand`, fully reversible |

> **Savings percentages are design targets, not measurements.** They come from fixed
> per-engine coefficients, not from profiling your repository. `antigravity-optimizer audit`
> reports the same kind of estimate. Treat them as relative guidance between engines.

---

## Optimization Profiles

Antigravity Token Optimizer provides four pre-configured operating modes:

All profiles use a code-skeleton threshold of **120 lines**; they differ in how much
command output and how many file lines they allow through.

*   **`aggressive`:** All 6 engines active. Tightest limits — 2,500 chars of command output, 100 lines per file view.
*   **`balanced` (recommended):** All 6 engines active. 4,000 chars of command output, 150 lines per file view.
*   **`developer`:** 4 of 6 engines active — `command_compression` and `search_dedup` are off, so full stack traces and complete search results survive. 8,000 chars of command output, 250 lines per file view.
*   **`custom`:** Currently a non-interactive alias that installs all 6 engines with `balanced` thresholds. Edit the generated `.agents/rules/token_optimization.md` to tune it by hand. (The `setup` wizard offers the three profiles above, not per-engine toggles.)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/axxion/antigravity-token-optimizer.git
cd antigravity-token-optimizer

# Install in editable mode
pip install -e .
```

---

## Command Line Interface (CLI)

### 1. Project Token & Context Audit
Scan any repository to detect token bloat, unindexed large files, and missing context rules:
```bash
antigravity-optimizer audit .
```

### 2. Interactive Configuration Wizard
Launch the interactive configuration wizard to select your preferred profile:
```bash
antigravity-optimizer setup
```

### 3. Direct Profile Installation
Install optimization rules, skills, and hooks directly into your project:
```bash
# Recommended Balanced Profile
antigravity-optimizer install --profile balanced /path/to/project

# Maximum Aggressive Savings
antigravity-optimizer install --profile aggressive /path/to/project

# Developer Debugging Profile
antigravity-optimizer install --profile developer /path/to/project
```

### 4. Extract AST Code Skeletons
View classes, methods, signatures, and docstrings of any source file without implementation bodies:
```bash
antigravity-optimizer skeleton src/my_service.py
```

### 5. Expand Cached Tool Outputs
Restore original uncompressed tool output by its reference token:
```bash
antigravity-optimizer expand ref_4f89a1bc
```

### 6. Inspect Active Optimization Status
```bash
antigravity-optimizer status .
```

---

## Google Antigravity Integration

When installed in a project, the optimizer generates native Antigravity workspace artifacts:

*   **`.agents/rules/token_optimization.md`** -- Active workspace rule enforcing prompt policies.
*   **`.agents/skills/token-optimizer/SKILL.md`** -- Antigravity skill for on-demand audits and AST extraction.
*   **`.agents/hooks.json`** -- Lifecycle hooks injecting lightweight optimization directives.
*   **`.agents/plugins/token-optimizer/`** -- Distributable Antigravity plugin bundle.

> **Note on hooks.** The generated `PreInvocation` hook injects a per-turn reminder and is
> confirmed working in the Antigravity **CLI** (`agy`). At the time of writing, community reports
> indicate hooks are not dispatched by the Antigravity **IDE / desktop** app (2.x) — they fail
> silently rather than erroring. This does not affect core optimization: the behavioral policies
> live in `.agents/rules/token_optimization.md`, which the IDE loads through its own workspace-rule
> mechanism. Only the repeated on-screen reminder is lost.

---

## Test Verification

Run the test suite to verify parsers, extractors, compactor, and generators:

```bash
python -m tests.run_optimizer_tests
```

---

## License

This project is licensed under the [MIT License](LICENSE).  
Author: **axxion** ([GitHub: @axxion](https://github.com/axxion))
