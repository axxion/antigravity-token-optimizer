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
