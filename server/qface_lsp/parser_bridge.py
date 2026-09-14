"""Bridges the qface parser to structured, LSP-friendly parse results.

qface itself ships two generations of its ANTLR-generated parser
(``qface.idl.parser.TLexer``/``TParser`` for old ANTLR 4.7.1 output, and
``T4Lexer``/``T4Parser`` for ANTLR 4.10 output) and picks the matching one
at import time based on ``antlr4.atn.ATNDeserializer.SERIALIZED_VERSION``
(see ``qface.idl.listener`` / ``qface.generator``). We mirror that same
dispatch here instead of hardcoding one generation, so this works with
whatever ``antlr4-python3-runtime`` version happens to be installed.
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
        import antlr4.atn.ATNDeserializer
        from antlr4 import CommonTokenStream, InputStream
        from antlr4.error.ErrorListener import ErrorListener

        if antlr4.atn.ATNDeserializer.SERIALIZED_VERSION == 3:
            from qface.idl.parser.TLexer import TLexer
            from qface.idl.parser.TParser import TParser
        else:
            from qface.idl.parser.T4Lexer import T4Lexer as TLexer
            from qface.idl.parser.T4Parser import T4Parser as TParser

        class _CollectingErrorListener(ErrorListener):
            def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
                errors.append(ParseError(line=line, column=column, message=msg))

        input_stream = InputStream(source)
        lexer = TLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(_CollectingErrorListener())

        tokens = CommonTokenStream(lexer)
        parser = TParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(_CollectingErrorListener())
        parser.documentSymbol()
    except ImportError as exc:
        errors.append(
            ParseError(line=1, column=0, message=f"qface parser not available: {exc}")
        )
    except Exception as exc:  # noqa: BLE001 - server must never crash on bad input
        errors.append(ParseError(line=1, column=0, message=str(exc)))

    return ParseResult(errors=errors)
