# qface-lsp — Implementierungsplan

VS-Code-Extension mit Language Server für die QFace IDL.
Referenz: https://qface.readthedocs.io/en/latest/

---

## 1. Zielsetzung

- Syntax-Highlighting für `.qface`-Dateien
- Diagnostics (Syntaxfehler, später auch semantische Fehler wie unbekannte Typen)
- Editor-Komfort: Hover, Autocomplete, Go to Definition, Document Symbols
- Wiederverwendung des bestehenden Python-Parsers aus dem `qface`-Paket (Pelagicore), statt eigene Grammatik zu schreiben

---

## 2. Architektur

```
┌─────────────────────────────┐        JSON-RPC über stdio        ┌──────────────────────────────┐
│  VS Code Extension (Client) │ ─────────────────────────────────▶│  Language Server (Python)     │
│  TypeScript                 │◀───────────────────────────────── │  pygls + qface-Lib             │
│  vscode-languageclient       │                                  │                               │
└─────────────────────────────┘                                    └──────────────────────────────┘
        │
        │ liest package.json Contributions
        ▼
┌─────────────────────────────┐
│  Syntax Highlighting          │
│  TextMate Grammar (.tmLanguage.json)
│  language-configuration.json │
└─────────────────────────────┘
```

**Warum diese Aufteilung?**
- Syntax-Highlighting läuft rein clientseitig (kein Server nötig, sofort verfügbar, kein Overhead).
- Der Language Server läuft als separater Python-Prozess, kommuniziert über das Language Server Protocol (LSP). Das erlaubt später Wiederverwendung durch andere Editoren (Neovim, Emacs) ohne VS-Code-spezifischen Code anzufassen.
- `qface`-Python-Paket liefert Parser + Domain-Model bereits fertig — wir schreiben nur die LSP-Schicht darum.

---

## 3. Tech-Stack

| Komponente | Technologie | Begründung |
|---|---|---|
| Extension Client | TypeScript | Standard für VS-Code-Extensions |
| Client-Server-Kommunikation | `vscode-languageclient` (npm) | offizielle Microsoft-Bibliothek |
| Language Server | Python 3.9+ | `qface`-Paket ist Python, keine Neuimplementierung des Parsers nötig |
| LSP-Server-Framework | `pygls` | ausgereifte Python-LSP-Implementierung, aktiv gepflegt |
| Parser/Domain-Model | `qface` (PyPI) | ANTLR4-basierter Parser, liefert Module/Interfaces/Structs/Enums als Objekte |
| Syntax-Highlighting | TextMate Grammar (JSON) | Standard-Mechanismus in VS Code, kein Server nötig |
| Packaging | `vsce` | offizielles Tool zum Bauen von `.vsix` |

---

## 4. Repo-Struktur (Zielzustand)

```
qface-lsp/
├── .vscode/
│   ├── launch.json
│   └── tasks.json
├── client/                          # VS Code Extension
│   ├── src/
│   │   └── extension.ts             # startet den Server-Prozess, registriert Client
│   ├── package.json
│   └── tsconfig.json
├── server/                          # Python Language Server
│   ├── qface_lsp/
│   │   ├── __init__.py
│   │   ├── server.py                # pygls Server-Instanz, LSP-Handler
│   │   ├── parser_bridge.py         # Wrapper um qface-Lib
│   │   ├── diagnostics.py
│   │   ├── hover.py
│   │   ├── completion.py
│   │   └── definitions.py
│   ├── pyproject.toml
│   └── requirements.txt
├── syntaxes/
│   └── qface.tmLanguage.json
├── language-configuration.json
├── images/
│   └── icon.png
├── examples/
│   └── sample.qface                 # Testdatei zum manuellen Ausprobieren
├── package.json                     # Root-Manifest der Extension (Contributions)
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## 5. Umsetzung in Phasen

### Phase 0 — Setup

- [ ] Repo `qface-lsp` auf GitHub anlegen, MIT-Lizenz auswählen
- [ ] `yo code` ausführen → TypeScript-Extension-Grundgerüst generieren
- [ ] Python-Virtualenv für den Server anlegen, `qface`-Paket installieren:
  ```bash
  python3 -m venv server/.venv
  source server/.venv/bin/activate
  pip install qface pygls
  ```
- [ ] `.gitignore` ergänzen (`node_modules/`, `.venv/`, `out/`, `*.vsix`)

**Ergebnis:** Repo ist lauffähig, aber ohne Funktionalität.

---

### Phase 1 — Syntax-Highlighting (kein Server nötig)

- [ ] `language-configuration.json` anlegen (Kommentare, Klammern, Einrückung — siehe vorheriger Chat-Verlauf)
- [ ] `syntaxes/qface.tmLanguage.json` schreiben mit Regeln für:
  - Keywords: `module`, `import`, `interface`, `struct`, `enum`, `flag`, `signal`, `readonly`, `extends`
  - Primitive Typen: `int`, `real`, `string`, `bool`, `var`
  - Container-Typen: `list<>`, `map<>`, `model<>`
  - Kommentare: `//`, `/* */`, Javadoc-artige `/** */`
  - Annotationen: `@key: value` (YAML-Inline-Syntax)
  - String- und Zahlenliterale
- [ ] `package.json`-Contributions ergänzen (`languages`, `grammars`)
- [ ] Testen: `examples/sample.qface` im Extension Development Host öffnen (F5), Highlighting prüfen

**Ergebnis:** `.qface`-Dateien werden farbig dargestellt, Klammern schließen automatisch.

---

### Phase 2 — Minimaler Language Server (Diagnostics)

- [ ] `server/qface_lsp/parser_bridge.py`: Funktion, die eine `.qface`-Datei via `qface.generator.FileSystem` einliest und bei Parse-Fehlern eine strukturierte Fehlermeldung (Zeile, Spalte, Text) zurückgibt
- [ ] `server/qface_lsp/server.py`: `pygls`-Server-Instanz mit Handler für:
  - `textDocument/didOpen`
  - `textDocument/didChange` (mit Debounce, z. B. 300 ms, um nicht bei jedem Tastendruck neu zu parsen)
  - `textDocument/didSave`
  - Jeweils: Datei parsen → Fehler als `publishDiagnostics` an den Client senden
- [ ] `client/src/extension.ts`: Server-Prozess starten (`LanguageClient` aus `vscode-languageclient`), Pfad zum Python-Interpreter/Server konfigurierbar machen (Setting `qface.pythonPath` o. Ä.)
- [ ] End-to-End-Test: absichtlich fehlerhafte `.qface`-Datei öffnen → rote Wellenlinie muss erscheinen

**Ergebnis:** Syntaxfehler werden live im Editor angezeigt.

---

### Phase 3 — Semantische Diagnostics

- [ ] Nach erfolgreichem Parse: Domain-Model durchlaufen und prüfen:
  - Referenzierte Typen (`module.Symbol`) existieren tatsächlich (in importierten Modulen oder lokal)
  - Keine doppelten Interface-/Struct-/Enum-Namen im selben Modul
  - `extends`-Referenzen lösen sich auf
- [ ] Workspace-weites Modul-Register aufbauen: alle `.qface`-Dateien im Workspace einlesen und nach Modulname indexieren (Grundlage für Cross-File-Referenzen in Phase 4)

**Ergebnis:** Auch inhaltliche Fehler (unbekannter Typ, kaputter Import) werden gemeldet.

---

### Phase 4 — Editor-Komfort

- [ ] **Hover** (`textDocument/hover`): bei Cursor auf einem Symbol → Typ, Dokumentationskommentar (Javadoc-Tags: `@brief`, `@description`, `@see`, `@deprecated`) anzeigen
- [ ] **Autocomplete** (`textDocument/completion`):
  - Keywords kontextabhängig (z. B. `signal`, `readonly` nur innerhalb `interface { }`)
  - Typnamen aus lokalem Modul + importierten Modulen
- [ ] **Document Symbols** (`textDocument/documentSymbol`): Outline-Ansicht mit Interfaces/Structs/Enums/Properties
- [ ] **Go to Definition** (`textDocument/definition`): von einer Typreferenz zur Deklaration springen (ggf. in anderer Datei)
- [ ] **Find References** (`textDocument/references`): alle Verwendungsstellen eines Typs finden

**Ergebnis:** Editor fühlt sich wie eine "echte" IDE-Unterstützung an.

---

### Phase 5 — Qualität & Robustheit

- [ ] Fehlerbehandlung: Server darf bei kaputten Dateien nicht abstürzen (try/except um jeden Parse-Aufruf)
- [ ] Performance: Parsing nur für geänderte Datei, nicht kompletten Workspace bei jedem Tastendruck
- [ ] Logging: Server-Log-Ausgabe in VS-Code-Output-Channel sichtbar machen (hilft beim Debuggen für Nutzer)
- [ ] Unit-Tests für `parser_bridge.py` (z. B. mit `pytest`)
- [ ] Manuelles Testprotokoll: Liste von `.qface`-Testdateien mit bekannten Fehlerarten, die vor jedem Release durchgeklickt werden

---

### Phase 6 — Packaging & Distribution

- [ ] Icon (`images/icon.png`, 256×256, quadratisch) erstellen
- [ ] README.md fertigstellen (Screenshots/GIFs der Features einfügen)
- [ ] CHANGELOG.md anlegen (Keep-a-Changelog-Format)
- [ ] Entscheidung: Python-Server-Distribution
  - Option A: Nutzer installiert Python + `pip install qface-lsp-server` selbst (einfacher für dich, mehr Aufwand für Nutzer)
  - Option B: Server via PyInstaller zu einer Standalone-Binary bündeln und mit der Extension ausliefern (mehr Aufwand für dich, nahtlose Installation für Nutzer)
- [ ] `vsce package` → `.vsix` erzeugen, lokal testen (`code --install-extension`)
- [ ] Marketplace-Publisher-Account anlegen, `vsce publish`

---

## 6. Offene Entscheidungen (vor Implementierungsstart klären)

| Frage | Optionen |
|---|---|
| Server-Sprache | Python (schnellerer Start dank `qface`-Lib) vs. TypeScript (eigene Grammatik-Portierung via ANTLR4, aber keine Python-Runtime-Abhängigkeit für Nutzer) |
| Distribution des Python-Servers | pip-Installation durch Nutzer vs. gebündelte Binary |
| Umfang v1.0 | Nur Highlighting + Syntax-Diagnostics vs. direkt mit Hover/Completion starten |
| Monorepo vs. getrennte Repos | `qface-lsp` als ein Repo (Client + Server zusammen) vs. Server als eigenes editor-unabhängiges Paket |

---

## 7. Nächster konkreter Schritt

Empfehlung: mit **Phase 0 + Phase 1** starten (Setup + Syntax-Highlighting), da das ohne Server sofort sichtbare Ergebnisse liefert und die Grundlage für alles Weitere legt.
