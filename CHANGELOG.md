# Changelog

## 0.1.0 - 2026-09-22

Initial release.

- Syntax highlighting for `.qface` files: declarations, members, primitive and
  container types, literals, comments, and QFace annotations
- Editor support: comment toggling, bracket matching and auto-closing,
  indentation rules, and region folding
- Optional Python language server, disabled by default, reporting syntax errors
  and unresolved type references. It reuses QFace's own parser and domain model,
  so the editor and the code generator agree on what is valid. Enable it with
  `qface.server.enable`
- `QFace: Restart Language Server` command
