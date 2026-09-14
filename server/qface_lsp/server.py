"""pygls-based language server for the QFace IDL.

Implements Phase 2 of the implementation plan: parses .qface documents
on open/change/save and publishes syntax diagnostics to the client.
"""
import logging

from lsprotocol.types import (
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
)
from pygls.server import LanguageServer

from .diagnostics import semantic_diagnostics, to_diagnostics
from .parser_bridge import build_system, parse_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qface_lsp")

server = LanguageServer("qface-lsp", "v0.0.1")


def _validate(uri: str, text: str) -> None:
    try:
        result = parse_document(uri, text)
        diagnostics = to_diagnostics(result)
        system, locations = build_system(text)
        diagnostics.extend(semantic_diagnostics(system, locations))
        server.publish_diagnostics(uri, diagnostics)
    except Exception:  # noqa: BLE001 - the server must never crash on bad input
        logger.exception("Failed to validate %s", uri)


@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams) -> None:
    doc = ls.workspace.get_text_document(params.text_document.uri)
    _validate(doc.uri, doc.source)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams) -> None:
    doc = ls.workspace.get_text_document(params.text_document.uri)
    _validate(doc.uri, doc.source)


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams) -> None:
    doc = ls.workspace.get_text_document(params.text_document.uri)
    _validate(doc.uri, doc.source)


def main() -> None:
    server.start_io()


if __name__ == "__main__":
    main()
