# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-21

First release prepared for the Visual Studio Code Marketplace.

### Added

- Syntax highlighting for `.qface` files via a TextMate grammar, covering
  declarations, members, primitive and container types, literals, comments,
  and QFace annotations
- Language configuration: comment toggling, bracket matching and auto-closing,
  indentation rules, and region folding
- Python language server based on `pygls`, reusing QFace's own ANTLR parser and
  domain model, publishing diagnostics on open, change, and save
- Syntax error diagnostics surfaced from the QFace parser
- Semantic diagnostics for unresolved complex type references in properties,
  operation return types, operation and signal parameters, and struct fields,
  including the leaf types of nested `list<>`, `map<>`, and `model<>` types
- `qface.server.enable` setting to run the extension with syntax highlighting
  only, without requiring a Python installation
- `QFace: Restart Language Server` command; the server also restarts
  automatically when `qface.pythonPath` or `qface.server.enable` changes
- Actionable warning with links to settings and the server log when the server
  cannot be started, instead of a bare activation failure
- `THIRD-PARTY-NOTICES.md` listing all bundled and required components with
  their licenses
- Example file [`examples/sample.qface`](examples/sample.qface) for manual
  testing

### Fixed

- The extension failed to activate with `Cannot find module
  'client/out/extension.js'`, because a stale `tsconfig.tsbuildinfo` was
  committed to the repository and made `tsc -b` skip emitting output. The
  TypeScript project-reference setup was replaced by a single type-check pass
  plus an esbuild bundle, which removes that failure mode
- `qface.trace.server` had no effect: the language client derived its trace
  setting from its client id `qfaceLanguageServer`, so it looked for
  `qfaceLanguageServer.trace.server`. The client id is now `qface`, matching
  the contributed settings

[Unreleased]: https://github.com/fsbondtec/qface-lsp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fsbondtec/qface-lsp/releases/tag/v0.1.0
