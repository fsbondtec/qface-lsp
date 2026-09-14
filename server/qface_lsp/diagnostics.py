"""Converts qface parse results into LSP diagnostics."""
from typing import Any, List

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from .parser_bridge import ParseResult, SymbolLocations


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


def _iter_complex_types(type_: Any):
    """Yields the complex (non-primitive) leaf types of a, possibly nested, type."""
    if type_.is_list or type_.is_map or type_.is_model:
        if type_.nested is not None:
            yield from _iter_complex_types(type_.nested)
    elif type_.is_complex:
        yield type_


def _check_unresolved_types(
    symbol: Any, locations: SymbolLocations, diagnostics: List[Diagnostic]
) -> None:
    line, column = locations.get(id(symbol), (1, 0))
    for type_ in _iter_complex_types(symbol.type):
        try:
            resolved = type_.reference
        except Exception:  # noqa: BLE001 - qface raises a plain Exception on lookup failure
            resolved = None
        if resolved is None:
            diagnostics.append(
                Diagnostic(
                    range=Range(
                        start=Position(line=max(line - 1, 0), character=column),
                        end=Position(line=max(line - 1, 0), character=column + 1),
                    ),
                    message=f"Unknown type '{type_.name}'",
                    severity=DiagnosticSeverity.Error,
                    source="qface",
                )
            )


def semantic_diagnostics(system: Any, locations: SymbolLocations) -> List[Diagnostic]:
    """Checks the domain model for unresolved type references."""
    diagnostics: List[Diagnostic] = []
    if system is None:
        return diagnostics
    for module in system.modules:
        for interface in module.interfaces:
            for prop in interface.properties:
                _check_unresolved_types(prop, locations, diagnostics)
            for operation in interface.operations:
                _check_unresolved_types(operation, locations, diagnostics)
                for parameter in operation.parameters:
                    _check_unresolved_types(parameter, locations, diagnostics)
            for signal in interface.signals:
                for parameter in signal.parameters:
                    _check_unresolved_types(parameter, locations, diagnostics)
        for struct in module.structs:
            for struct_field in struct.fields:
                _check_unresolved_types(struct_field, locations, diagnostics)
    return diagnostics
