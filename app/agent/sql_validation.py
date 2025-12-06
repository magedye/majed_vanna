"""
Phase 1.B — SQL Safety Layer.
Lightweight pre-execution checks: single-statement enforcement, basic
destructive/unsupported verb blocking, and comment/tautology screening.
"""

import re
from typing import Set

from app.config import DB_PROVIDER


class SQLValidationError(ValueError):
    """Raised when SQL fails basic safety validation."""


ALLOWED_STATEMENTS: Set[str] = {"select", "with", "explain", "describe", "show"}
if DB_PROVIDER == "sqlite":
    ALLOWED_STATEMENTS.add("pragma")
DESTRUCTIVE_KEYWORDS = {"drop", "truncate", "alter", "delete", "update", "insert"}
COMMENT_PATTERN = re.compile(r"--|/\\*")
TAUTOLOGY_PATTERN = re.compile(r"\\b(or|and)\\s+1\\s*=\\s*1\\b", re.IGNORECASE)


def _normalize(sql: str) -> str:
    if not isinstance(sql, str):
        raise SQLValidationError("SQL must be a string")
    cleaned = re.sub(r"\\s+", " ", sql).strip()
    if not cleaned:
        raise SQLValidationError("SQL is required")
    return cleaned


def _ensure_single_statement(sql: str) -> str:
    parts = [part.strip() for part in sql.split(";") if part.strip()]
    if len(parts) != 1:
        raise SQLValidationError("Only single SQL statements are allowed")
    return parts[0]


def _ensure_supported_statement(sql: str) -> None:
    if COMMENT_PATTERN.search(sql):
        raise SQLValidationError("Inline SQL comments are not allowed")
    if TAUTOLOGY_PATTERN.search(sql):
        raise SQLValidationError("Tautology patterns are not allowed")

    keyword = sql.split()[0].lower()
    if keyword not in ALLOWED_STATEMENTS:
        allowed = ", ".join(sorted(ALLOWED_STATEMENTS))
        raise SQLValidationError(f"Unsupported SQL statement '{keyword}'. Allowed: {allowed}")

    if re.search(r"\\b(" + "|".join(DESTRUCTIVE_KEYWORDS) + r")\\b", sql, re.IGNORECASE):
        raise SQLValidationError("Destructive statements are blocked in this mode")


def validate_sql(sql: str) -> str:
    """
    Basic SQL guardrail for Phase 1.B. Returns normalized single statement or raises SQLValidationError.
    """
    normalized = _normalize(sql)
    single_statement = _ensure_single_statement(normalized)
    _ensure_supported_statement(single_statement)
    return single_statement
