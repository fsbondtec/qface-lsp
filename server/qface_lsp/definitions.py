"""Go to Definition support (Phase 4, not yet implemented).

Will resolve a type reference to its declaration, potentially in
another file, using a workspace-wide module index.
"""
from __future__ import annotations

from typing import List

from lsprotocol.types import Location, Position


def definitions_at(uri: str, source: str, position: Position) -> List[Location]:
    return []
