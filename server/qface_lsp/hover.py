"""Hover support (Phase 4, not yet implemented).

Will resolve the symbol under the cursor against the parsed qface
domain model and return its type plus Javadoc-style documentation
(@brief, @description, @see, @deprecated).
"""
from __future__ import annotations

from lsprotocol.types import Hover, Position


def hover_for(uri: str, source: str, position: Position) -> Hover | None:
    return None
