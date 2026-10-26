# Changelog

## Unreleased

- Releases of `jarl-pre-commit` no longer match releases of Jarl. This made it impossible to
  add fixes related to `jarl-pre-commit` only (e.g. #5) while using older versions of Jarl.
  Each release installs by default the latest version of Jarl at the time of the release. Use
  `additional_dependencies` to choose the version of Jarl. This new feature means that Jarl is
  now installed from PyPI (`jarl-linter`) instead of GitHub releases.

- Fix installation on Windows (#5, @BjarkeHautop).
