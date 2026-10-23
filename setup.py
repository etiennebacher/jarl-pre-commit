# The Jarl version is pinned in `.pre-commit-hooks.yaml` (via
# `additional_dependencies`) so that users can override it.
from setuptools import setup

setup(
    name="jarl-pre-commit",
    version="0.0.0",
    description="pre-commit hook for jarl R linter",
    install_requires=["jarl-linter"],
    py_modules=[],
)
