# QFace IDL for VS Code

Syntax highlighting and language support for the [QFace IDL](https://qface.readthedocs.io/en/latest/),
backed by a Python language server that reuses the `qface` parser and domain model.

## Status

Early-stage implementation, following the phased plan in
[qface-lsp-implementierungsplan.md](../qface-lsp-implementierungsplan.md):

- [x] Phase 0 — Project setup
- [x] Phase 1 — Syntax highlighting (TextMate grammar)
- [x] Phase 2 — Minimal language server (syntax diagnostics)
- [x] Phase 3 — Semantic diagnostics
- [ ] Phase 4 — Hover / completion / go-to-definition / find references
- [ ] Phase 5 — Robustness & tests
- [ ] Phase 6 — Packaging & distribution

## Development

### Prerequisites

- Node.js + npm
- Python 3.9+

### Setup

```bash
npm install
cd client && npm install && cd ..

python -m venv server/.venv
server/.venv/Scripts/activate   # on Windows
pip install -r server/requirements.txt
```

### Build & run

```bash
npm run compile
```

Then press `F5` in VS Code to launch the Extension Development Host and open
[examples/sample.qface](examples/sample.qface) to try it out.

### Configuration

| Setting | Description | Default |
|---|---|---|
| `qface.pythonPath` | Path to the Python interpreter used to run the language server | `python` |
| `qface.trace.server` | Traces LSP communication between client and server | `off` |

## License

MIT, see [LICENSE](LICENSE).
