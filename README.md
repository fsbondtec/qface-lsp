# QFace IDL for Visual Studio Code

Language support for the [QFace interface definition language](https://qface.readthedocs.io/en/latest/) —
the IDL used by [Qt Interface Framework](https://doc.qt.io/QtInterfaceFramework/) and the
`qface` code generator — in Visual Studio Code.

Syntax highlighting works out of the box, with no dependencies. Diagnostics are
opt-in: they come from a Python language server that reuses QFace's own ANTLR
parser and domain model, so what the editor flags is what the real generator
sees.

## Features

### Syntax highlighting

Full TextMate grammar for `.qface` files, covering declarations
(`module`, `import`, `interface`, `struct`, `enum`, `flag`), members
(`property`, `readonly`, `signal`, `extends`), primitive types
(`int`, `real`, `string`, `bool`, `var`, `void`), container types
(`list<>`, `map<>`, `model<>`), string and numeric literals, comments, and
QFace annotations (`@brief`, `@description`, `@see`, and custom `@key: value`
tags).

### Editor behaviour

Comment toggling, bracket matching and auto-closing, indentation rules for
block bodies, and `// #region` / `// #endregion` folding, via
[`language-configuration.json`](language-configuration.json).

### Diagnostics (opt-in)

Once enabled via `qface.server.enable`, the language server validates open
documents as you type and reports:

- **Syntax errors** — surfaced directly from QFace's ANTLR parser, at the
  reported line and column.
- **Unresolved type references** — a property, operation return type,
  operation parameter, signal parameter, or struct field that names a complex
  type which cannot be resolved in the module or its imports. Nested container
  types such as `list<Foo>` and `map<Bar>` are unwrapped and checked on their
  leaf type.

Diagnostics are reported under the `qface` source, so they can be filtered in
the Problems panel. See [Enabling diagnostics](#enabling-diagnostics) for setup.

## Requirements

Syntax highlighting and the editor behaviour described above have no
dependencies and work as soon as the extension is installed.

**Diagnostics are opt-in.** They run in a Python language server that the
extension does not start unless you enable it, so installing this extension
never requires Python.

## Enabling diagnostics

Install the server's dependencies into a Python 3.9 or newer interpreter:

```bash
pip install pygls qface
```

Then set `qface.server.enable` to `true`. Unless `python` on your `PATH` is the
interpreter you just installed into, also point `qface.pythonPath` at the right
one. The server starts as soon as either setting changes — no window reload
needed.

If it cannot be started, the extension shows a warning with links to the
relevant setting and to its log, and syntax highlighting keeps working.

## Extension settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `qface.pythonPath` | string | `python` | Path to the Python interpreter used to run the language server. Use an absolute path to select a virtual environment, e.g. `${workspaceFolder}/.venv/Scripts/python.exe` on Windows or `${workspaceFolder}/.venv/bin/python` elsewhere. |
| `qface.server.enable` | boolean | `false` | Set to `true` to start the Python language server and get diagnostics. Requires a working `qface.pythonPath`. |
| `qface.trace.server` | enum | `off` | Log LSP traffic between VS Code and the server to the *QFace Language Server* output channel. Useful values: `messages`, `verbose`. |

## Commands

| Command | Description |
| --- | --- |
| `QFace: Restart Language Server` | Stops and restarts the server process. |

The server also restarts automatically when `qface.pythonPath` or
`qface.server.enable` changes.

## Troubleshooting

**No diagnostics appear.** First check that `qface.server.enable` is `true` — it
is `false` by default. If it is enabled, open the *QFace Language Server* output
channel (View → Output, then pick the channel) and check for a startup error.
The most common cause is an interpreter without `pygls` or `qface` installed.
Verify it independently:

```bash
python -c "import pygls, qface; print('ok')"
```

**Diagnostics look wrong or incomplete.** Set `qface.trace.server` to
`verbose`, reproduce the problem, and attach the output channel contents to a
[bug report](https://github.com/fsbondtec/qface-lsp/issues).

## Status

Under active development. Syntax highlighting and diagnostics are usable;
hover, completion, go-to-definition, and find-references are not implemented
yet. Issues and pull requests are welcome.

## License

[MIT](LICENSE). Third-party components and their licenses are listed in
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
