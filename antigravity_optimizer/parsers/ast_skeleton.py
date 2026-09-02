"""
AST and structural code skeleton extractor.
Generates lightweight signatures and type definitions for large source files.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class SkeletonResult:
    skeleton: str
    original_lines: int
    skeleton_lines: int
    compression_ratio_pct: int
    language: str


class ASTSkeletonExtractor:
    @staticmethod
    def extract_python_skeleton(code: str) -> str:
        """Extracts class, method, function signatures and docstrings using Python AST."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            # Fallback to regex parser if AST fails
            return ASTSkeletonExtractor.extract_generic_skeleton(code, lang="python")

        skeleton_lines = []

        class SkeletonTransformer(ast.NodeVisitor):
            def __init__(self):
                self.indent_level = 0

            def _indent(self) -> str:
                return "    " * self.indent_level

            def visit_Import(self, node: ast.Import):
                names = ", ".join(n.name for n in node.names)
                skeleton_lines.append(f"{self._indent()}import {names}")

            def visit_ImportFrom(self, node: ast.ImportFrom):
                names = ", ".join(n.name for n in node.names)
                mod = node.module or ""
                skeleton_lines.append(f"{self._indent()}from {mod} import {names}")

            def visit_ClassDef(self, node: ast.ClassDef):
                bases = ", ".join(ast.unparse(b) for b in node.bases)
                base_str = f"({bases})" if bases else ""
                skeleton_lines.append(f"\n{self._indent()}class {node.name}{base_str}:")
                
                # Check for docstring
                doc = ast.get_docstring(node)
                if doc:
                    first_line = doc.strip().splitlines()[0]
                    skeleton_lines.append(f"{self._indent()}    \"\"\"{first_line}\"\"\"")

                self.indent_level += 1
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.AnnAssign)):
                        self.visit(item)
                self.indent_level -= 1

            def visit_FunctionDef(self, node: ast.FunctionDef):
                self._handle_func(node, is_async=False)

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
                self._handle_func(node, is_async=True)

            def _handle_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool):
                # Extract decorators
                for dec in node.decorator_list:
                    try:
                        dec_str = ast.unparse(dec)
                        skeleton_lines.append(f"{self._indent()}@{dec_str}")
                    except Exception:
                        pass

                prefix = "async def" if is_async else "def"
                args_str = ast.unparse(node.args)
                ret_ann = f" -> {ast.unparse(node.returns)}" if node.returns else ""
                skeleton_lines.append(f"{self._indent()}{prefix} {node.name}({args_str}){ret_ann}:")
                
                doc = ast.get_docstring(node)
                if doc:
                    first_line = doc.strip().splitlines()[0]
                    skeleton_lines.append(f"{self._indent()}    \"\"\"{first_line}\"\"\"")
                skeleton_lines.append(f"{self._indent()}    ...")

            def visit_AnnAssign(self, node: ast.AnnAssign):
                target = ast.unparse(node.target)
                ann = ast.unparse(node.annotation)
                skeleton_lines.append(f"{self._indent()}{target}: {ann}")

        transformer = SkeletonTransformer()
        for stmt in tree.body:
            transformer.visit(stmt)

        result = "\n".join(skeleton_lines).strip()
        return result or code[:1000]

    @staticmethod
    def extract_generic_skeleton(code: str, lang: str = "generic") -> str:
        """Extracts function/class signatures using pattern matching."""
        lines = code.splitlines()
        skeleton_lines = []

        signature_patterns = [
            r"^\s*(export\s+)?(default\s+)?(async\s+)?function\b",
            r"^\s*(export\s+)?(abstract\s+)?class\b",
            r"^\s*(export\s+)?interface\b",
            r"^\s*(export\s+)?type\s+\w+\s*=",
            r"^\s*(public|private|protected|static|async)?\s*(\w+)\s*\(.*\)\s*:\s*.*\{?",
            r"^\s*func\s+(\(.*\)\s*)?\w+\s*\(",
            r"^\s*(pub\s+)?(async\s+)?fn\s+\w+",
            r"^\s*def\s+\w+\s*\(",
            r"^\s*class\s+\w+",
            r"^\s*import\b",
            r"^\s*from\b",
        ]
        combined = re.compile("|".join(signature_patterns))

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("#"):
                continue
            if combined.search(line):
                skeleton_lines.append(line.rstrip("{ \t"))
                if "class " in line or "interface " in line:
                    continue
                if line.endswith(":"):
                    skeleton_lines.append("    ...")

        return "\n".join(skeleton_lines)

    @classmethod
    def extract_skeleton(cls, code: str, file_path: Optional[str] = None) -> SkeletonResult:
        orig_lines = len(code.splitlines()) or 1
        lang = "python"
        if file_path:
            ext = file_path.lower().split(".")[-1]
            if ext in ("py", "pyw"):
                lang = "python"
            elif ext in ("ts", "tsx", "js", "jsx"):
                lang = "typescript"
            elif ext in ("go", "rs", "java", "c", "cpp"):
                lang = ext
            else:
                lang = "generic"

        if lang == "python":
            skeleton = cls.extract_python_skeleton(code)
        else:
            skeleton = cls.extract_generic_skeleton(code, lang=lang)

        skel_lines = len(skeleton.splitlines()) or 1
        ratio = max(0, int((1.0 - (skel_lines / orig_lines)) * 100))

        return SkeletonResult(
            skeleton=skeleton,
            original_lines=orig_lines,
            skeleton_lines=skel_lines,
            compression_ratio_pct=ratio,
            language=lang,
        )
