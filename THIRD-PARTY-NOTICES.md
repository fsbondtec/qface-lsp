# Third-Party Notices

The QFace IDL extension is licensed under the MIT License (see [LICENSE](LICENSE)).
It incorporates and depends on the third-party components listed below. Each
component remains under its own license; nothing here modifies those terms.

Version numbers reflect the versions this extension was built and tested
against. Run `npm ls --omit=dev --all` and `pip list` to inspect the exact
versions in your own installation.

---

## Bundled in the extension (`dist/extension.js`)

The extension client is bundled with [esbuild](https://esbuild.github.io/), so
the following npm packages are compiled into the shipped JavaScript file and
are redistributed as part of the VSIX.

| Component | Version | License | Copyright / Project |
| --- | --- | --- | --- |
| [vscode-languageclient](https://github.com/microsoft/vscode-languageserver-node) | 9.0.1 | MIT | Copyright (c) Microsoft Corporation |
| [vscode-languageserver-protocol](https://github.com/microsoft/vscode-languageserver-node) | 3.17.5 | MIT | Copyright (c) Microsoft Corporation |
| [vscode-languageserver-types](https://github.com/microsoft/vscode-languageserver-node) | 3.17.5 | MIT | Copyright (c) Microsoft Corporation |
| [vscode-jsonrpc](https://github.com/microsoft/vscode-languageserver-node) | 8.2.0 | MIT | Copyright (c) Microsoft Corporation |
| [semver](https://github.com/npm/node-semver) | 7.x | ISC | Copyright (c) Isaac Z. Schlueter and Contributors |
| [minimatch](https://github.com/isaacs/minimatch) | 5.x | ISC | Copyright (c) Isaac Z. Schlueter and Contributors |
| [brace-expansion](https://github.com/juliangruber/brace-expansion) | 2.x | MIT | Copyright (c) Julian Gruber |
| [balanced-match](https://github.com/juliangruber/balanced-match) | 1.0.2 | MIT | Copyright (c) Julian Gruber |

The `vscode` module is provided by the Visual Studio Code extension host at
runtime and is not bundled or redistributed.

---

## Required at runtime, installed separately by the user

The Python language server is shipped as source, but its dependencies are
**not** redistributed with the extension. Users install them into their own
Python environment (`pip install pygls qface`), so these components are listed
for attribution and license-compatibility purposes only.

### Direct dependencies

| Component | Version | License | Copyright / Project |
| --- | --- | --- | --- |
| [pygls](https://github.com/openlawlibrary/pygls) | 1.3.1 | Apache-2.0 | Copyright Open Law Library |
| [qface](https://github.com/Pelagicore/qface) | 2.0.14 | MIT | Copyright (c) Pelagicore AB |

### Transitive dependencies

| Component | Version | License | Copyright / Project |
| --- | --- | --- | --- |
| [lsprotocol](https://github.com/microsoft/lsprotocol) | 2023.0.1 | MIT | Copyright (c) Microsoft Corporation |
| [cattrs](https://github.com/python-attrs/cattrs) | 26.2.0 | MIT | Copyright (c) Tin Tvrtković and contributors |
| [attrs](https://github.com/python-attrs/attrs) | 26.1.0 | MIT | Copyright (c) Hynek Schlawack and contributors |
| [typing-extensions](https://github.com/python/typing_extensions) | 4.16.0 | PSF-2.0 | Copyright (c) Python Software Foundation |
| [antlr4-python3-runtime](https://github.com/antlr/antlr4) | 4.13.2 | BSD-3-Clause | Copyright (c) 2012-2022 The ANTLR Project |
| [Jinja2](https://github.com/pallets/jinja) | 3.1.6 | BSD-3-Clause | Copyright (c) Pallets |
| [MarkupSafe](https://github.com/pallets/markupsafe) | 3.0.3 | BSD-3-Clause | Copyright (c) Pallets |
| [click](https://github.com/pallets/click) | 8.5.0 | BSD-3-Clause | Copyright (c) Pallets |
| [PyYAML](https://github.com/yaml/pyyaml) | 6.0.3 | MIT | Copyright (c) 2017-2021 Ingy döt Net, Copyright (c) 2006-2016 Kirill Simonov |
| [watchdog](https://github.com/gorakhargosh/watchdog) | 6.0.0 | Apache-2.0 | Copyright (c) Yesudeep Mangalapilly and contributors |
| [coloredlogs](https://github.com/xolox/python-coloredlogs) | 15.0.1 | MIT | Copyright (c) Peter Odding |
| [humanfriendly](https://github.com/xolox/python-humanfriendly) | 10.0 | MIT | Copyright (c) Peter Odding |
| [six](https://github.com/benjaminp/six) | 1.17.0 | MIT | Copyright (c) 2010-2024 Benjamin Peterson |
| [colorama](https://github.com/tartley/colorama) | 0.4.6 | BSD-3-Clause | Copyright (c) Jonathan Hartley and contributors |
| [pyreadline3](https://github.com/pyreadline3/pyreadline3) | 3.5.6 | BSD-3-Clause | Copyright (c) Jörgen Stenarson and contributors (Windows only) |

---

## Development-only dependencies

These are used to build, type-check, and package the extension. They are not
bundled and not redistributed.

| Component | License |
| --- | --- |
| [TypeScript](https://github.com/microsoft/TypeScript) | Apache-2.0 |
| [esbuild](https://github.com/evanw/esbuild) | MIT |
| [@vscode/vsce](https://github.com/microsoft/vscode-vsce) | MIT |
| [@types/node](https://github.com/DefinitelyTyped/DefinitelyTyped) | MIT |
| [@types/vscode](https://github.com/DefinitelyTyped/DefinitelyTyped) | MIT |
| [pytest](https://github.com/pytest-dev/pytest) | MIT |

---

## Language reference

The TextMate grammar and language configuration in this repository are original
work, written against the publicly documented QFace grammar
(<https://qface.readthedocs.io/en/latest/>). No grammar files were copied from
the `qface` project.
