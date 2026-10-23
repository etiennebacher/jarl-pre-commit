Use Jarl with [pre-commit](https://pre-commit.com/) or [prek](https://prek.j178.dev/).

## Quick start

### `pre-commit`

Use this in `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: 0.5.0
    hooks:
      - id: jarl-check
```

You can pass additional arguments with `args`, for instance:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: 0.5.0
    hooks:
      - id: jarl-check
        args: [--fix]
```

### `prek`

`prek` can read `.pre-commit-config.yaml` but also has its own format, `prek.toml`.

Use this in `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/etiennebacher/jarl-pre-commit"
rev = "0.5.0"
hooks = [
  { id = "jarl-check" },
]
```

You can pass additional arguments with `args`, for instance:

```toml
[[repos]]
repo = "https://github.com/etiennebacher/jarl-pre-commit"
rev = "0.5.0"
hooks = [
  { id = "jarl-check", args = ["--fix"] },
]
```

### Choosing the version of Jarl to use

By default, the `rev` parameter determines the version of Jarl to use. Starting from 0.5.0, all releases of Jarl have a matching release in `jarl-pre-commit`.

Fixes to the hook itself are released together with the next Jarl release. To benefit from them while using an older version of Jarl, use the latest `rev` and pick the version of Jarl with `additional_dependencies`:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: 0.7.1
    hooks:
      - id: jarl-check
        additional_dependencies: ["jarl-linter==0.6.0"]
```

In `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/etiennebacher/jarl-pre-commit"
rev = "0.7.1"
hooks = [
  { id = "jarl-check", additional_dependencies = ["jarl-linter==0.6.0"] },
]
```

Any version of Jarl published on [PyPI](https://pypi.org/project/jarl-linter/) can be used this way (0.5.0 and later).

To use a fix before it is released, set `rev` to the SHA of the latest commit on `main`, which you can get with:

```sh
git ls-remote https://github.com/etiennebacher/jarl-pre-commit main
```

For example, in `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: <commit SHA>
    hooks:
      - id: jarl-check
```

### How the jarl binary is installed

The hook uses `language: python`. When pre-commit sets up the hook environment, it installs the [`jarl-linter`](https://pypi.org/project/jarl-linter/) package from PyPI, which contains the jarl binary for your platform. This means:

- **No network access is needed at hook execution time.** The binary is downloaded once during environment setup and cached by pre-commit.
- **Works on [pre-commit.ci](https://pre-commit.ci)** and other CI services that restrict network access during hook execution but allow it during environment setup.
- **Version pinning is respected:** the `rev:` value in your config determines which tag of this repo is checked out, and that tag's `.pre-commit-hooks.yaml` pins the matching jarl version, unless you override it with `additional_dependencies`.
The pre-commit environment cache means the download only happens once per `rev:`. You may have projects using different versions of jarl simultaneously without them interfering with each other or with any system-wide jarl installation.
