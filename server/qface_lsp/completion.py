"""Autocomplete support (Phase 4, not yet implemented).

Will offer context-aware keyword completions (e.g. `signal`, `readonly`
only inside `interface { }`) plus type names from the local module and
its imports.
"""
from __future__ import annotations

from typing import List

from lsprotocol.types import CompletionItem, Position


def completions_at(uri: str, source: str, position: Position) -> List[CompletionItem]:
    return []
