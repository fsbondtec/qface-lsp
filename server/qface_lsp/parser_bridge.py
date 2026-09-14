"""Bridges the qface parser to structured, LSP-friendly parse results.

NOTE: the exact internal module layout of the ``qface`` ANTLR parser
(``qface.idl.QFaceLexer`` / ``qface.idl.QFaceParser``) depends on the
installed version of the ``qface`` PyPI package. Verify these import
paths against the installed version and adjust if the generator moved
the generated ANTLR sources to a different package.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class ParseError:
    line: int
    column: int
    message: str


@dataclass
class ParseResult:
    errors: List[ParseError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_document(uri: str, source: str) -> ParseResult:
    """Parses a single .qface document and collects syntax errors.

    qface's ANTLR-based parser reports errors via an error listener
    rather than exceptions, so a collecting listener is installed to
    capture them instead of letting them go to stderr.
    """
    errors: List[ParseError] = []
    try:
        from antlr4 import CommonTokenStream, InputStream
        from antlr4.error.ErrorListener import ErrorListener
        from qface.idl.QFaceLexer import QFaceLexer
        from qface.idl.QFaceParser import QFaceParser

        class _CollectingErrorListener(ErrorListener):
            def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
                errors.append(ParseError(line=line, column=column, message=msg))

        input_stream = InputStream(source)
        lexer = QFaceLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(_CollectingErrorListener())

        tokens = CommonTokenStream(lexer)
        parser = QFaceParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(_CollectingErrorListener())
        parser.document()
    except ImportError as exc:
        errors.append(
            ParseError(line=1, column=0, message=f"qface parser not available: {exc}")
        )
    except Exception as exc:  # noqa: BLE001 - server must never crash on bad input
        errors.append(ParseError(line=1, column=0, message=str(exc)))

    return ParseResult(errors=errors)
