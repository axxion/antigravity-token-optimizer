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

It identifies and eliminates conversational fluff, compresses verbose test and compiler streams, extracts AST-based code skeletons, compacts structured data payloads, and externalizes session memory into deterministic artifacts.

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
| **3. `code_skeleton`** | Extracts AST signatures (Python, TS, JS, Go, Rust, Java, C++) preserving types and docstrings. | Explores architecture without loading implementation bodies. | **60% - 85%** |
| **4. `command_compression`** | Applies output filters to `pytest`, `npm test`, `cargo test`, `go test`, and `git log`. | Discards passing test noise while retaining failure traces. | **50% - 80%** |
| **5. `data_compactor`** | Transforms object collections into column-oriented tables and strips null/empty keys. | Massive token reduction on JSON tool outputs and API responses. | **50% - 70%** |
| **6. `context_buffer`** | Lossless local caching storing raw uncompressed outputs indexed by unique reference tokens (`ref_...`). | Fully reversible; restore original output on demand via CLI or tools. | **Lossless** |
| **7. `search_dedup`** | Enforces match limits, truncates long lines (120 chars), and deduplicates search results. | Prevents regex searches from overwhelming the context window. | **30% - 60%** |
| **8. `context_memory`** | Checkpoints state, active tasks, and architecture decisions directly to disk (`BOARD.md`, `LEDGER.md`). | Survives context compaction without degrading model memory. | **50% - 90%** |

---

## Optimization Profiles

Antigravity Token Optimizer provides four pre-configured operating modes:

*   **`aggressive` (Maximum Savings ~60-75%):** All 8 engines active. Strict command output trimming, AST skeletons for all files above 80 lines, and tight search boundaries.
*   **`balanced` (Recommended ~45-60%):** Balanced developer profile. Lean prompts, surgical edits, code skeletons, data compaction, search deduplication, and test filtering.
*   **`developer` (Detailed Debugging ~30-45%):** Preserves full stack traces and verbose diffs while removing conversational filler and full-file rewrites.
*   **`custom`:** Interactively toggle individual engines and specify custom thresholds.

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
