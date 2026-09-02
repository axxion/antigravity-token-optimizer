"""
Tests for AST Skeleton Extractor.
"""

from antigravity_optimizer.parsers.ast_skeleton import ASTSkeletonExtractor


def test_python_ast_skeleton():
    code = '''
import os
import sys
from pathlib import Path

class UserService:
    """Handles user registration and auth."""
    def __init__(self, db_url: str):
        self.db = db_url
        self.cache = {}
        # 20 lines of setup logic...
        x = 1 + 2
        y = 3 + 4

    async def get_user_by_id(self, user_id: int) -> dict:
        """Retrieves user from database or cache."""
        if user_id in self.cache:
            return self.cache[user_id]
        # Query DB...
        return {"id": user_id, "name": "Test"}

def helper_func(a: int, b: int) -> int:
    """Calculates sum."""
    return a + b
'''
    res = ASTSkeletonExtractor.extract_skeleton(code, file_path="service.py")
    assert res.language == "python"
    assert "class UserService:" in res.skeleton
    assert "def __init__(self, db_url: str):" in res.skeleton
    assert "async def get_user_by_id(self, user_id: int) -> dict:" in res.skeleton
    assert "def helper_func(a: int, b: int) -> int:" in res.skeleton
    assert res.compression_ratio_pct > 30
    assert "self.db = db_url" not in res.skeleton  # Method bodies stripped!


def test_typescript_skeleton():
    ts_code = '''
import { Request, Response } from "express";

export interface UserDTO {
    id: number;
    name: string;
}

export class AuthController {
    public async login(req: Request, res: Response): Promise<void> {
        const { username, password } = req.body;
        // Heavy implementation...
        res.json({ token: "xyz" });
    }
}
'''
    res = ASTSkeletonExtractor.extract_skeleton(ts_code, file_path="auth.controller.ts")
    assert res.language == "typescript"
    assert "export interface UserDTO" in res.skeleton
    assert "export class AuthController" in res.skeleton


def test_typescript_multiline_imports_are_not_truncated():
    """Regression: a multi-line `import { ... } from 'x'` used to collapse to a bare
    `import`, losing every imported symbol name from the skeleton."""
    ts_code = '''
import {
    subscribeToBudgets,
    subscribeToGuests,
    updateWeddingPlan,
} from '@/lib/firestore';

import { toast } from 'sonner';

export default function Dashboard() {
    const x = 1;
    return null;
}
'''
    res = ASTSkeletonExtractor.extract_skeleton(ts_code, file_path="Dashboard.tsx")

    # The collapsed single line must carry the symbols AND the module path.
    assert "subscribeToBudgets" in res.skeleton
    assert "updateWeddingPlan" in res.skeleton
    assert "@/lib/firestore" in res.skeleton
    # A single-line import must still survive untouched.
    assert "import { toast } from 'sonner';" in res.skeleton
    # No line may be left as a bare, information-free `import`.
    assert not any(
        line.strip() == "import" for line in res.skeleton.splitlines()
    ), f"bare `import` line found in skeleton:\n{res.skeleton}"


def test_ast_skeleton_syntax_errors_and_edge_cases():
    # 1. Code with Syntax Errors should fallback without exception
    broken_py = "def broken_syntax(x, y:\n  print('missing paren'"
    res = ASTSkeletonExtractor.extract_skeleton(broken_py, file_path="broken.py")
    assert res.skeleton is not None
    assert len(res.skeleton) > 0

    # 2. Empty code
    empty_res = ASTSkeletonExtractor.extract_skeleton("", file_path="empty.py")
    assert empty_res.original_lines >= 1

    # 3. Complex Python async, type annotations, and docstrings
    complex_py = """
from typing import Optional, List, Dict, Any

class DataProcessor:
    \"\"\"Core processor docstring.\"\"\"
    version: str = "1.0"

    def __init__(self, items: List[int]) -> None:
        self.items = items
        for i in range(100):
            print(i)

    @classmethod
    async def process_async(cls, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        \"\"\"Async process description.\"\"\"
        if not payload:
            return None
        return {"status": "ok"}
"""
    comp_res = ASTSkeletonExtractor.extract_skeleton(complex_py, file_path="proc.py")
    assert "class DataProcessor:" in comp_res.skeleton
    assert "Core processor docstring." in comp_res.skeleton
    assert "def __init__(self, items: List[int]) -> None:" in comp_res.skeleton
    assert "async def process_async(cls, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:" in comp_res.skeleton
    assert "for i in range(100):" not in comp_res.skeleton
