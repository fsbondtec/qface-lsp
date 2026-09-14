"""Converts qface parse results into LSP diagnostics."""
from typing import List

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from .parser_bridge import ParseResult


def to_diagnostics(result: ParseResult) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []
    for error in result.errors:
        line = max(error.line - 1, 0)
        column = max(error.column, 0)
        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=line, character=column),
                    end=Position(line=line, character=column + 1),
                ),
                message=error.message,
                severity=DiagnosticSeverity.Error,
                source="qface",
            )
        )
    return diagnostics
