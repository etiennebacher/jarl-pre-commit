Use Jarl with [pre-commit](https://pre-commit.com/) or [prek](https://prek.j178.dev/).

## Quick start

### `pre-commit`

Use this in `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: 1.0.0
    hooks:
      - id: jarl-check
```

You can pass additional arguments with `args`, for instance:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: 1.0.0
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
rev = "1.0.0"
hooks = [
  { id = "jarl-check" },
]
```

You can pass additional arguments with `args`, for instance:

```toml
[[repos]]
repo = "https://github.com/etiennebacher/jarl-pre-commit"
rev = "1.0.0"
hooks = [
  { id = "jarl-check", args = ["--fix"] },
]
```

### Choosing the version of Jarl to use

Each release of `jarl-pre-commit` installs by default the latest version of Jarl at the time of the release, as listed in the [changelog](CHANGELOG.md). A new release of `jarl-pre-commit` is made for each new version of Jarl, so `pre-commit autoupdate` or `prek autoupdate` also updates Jarl.

> [!NOTE]
> Before `jarl-pre-commit` 1.0.0, the version tags of `jarl-pre-commit` were matching the release 
> version of Jarl, which made it impossible to have integrate fixes for `jarl-pre-commit` while using
> older versions of Jarl. 

To choose the version of Jarl to use, pass it in `additional_dependencies`:

```yaml
repos:
-   repo: https://github.com/etiennebacher/jarl-pre-commit
    rev: 1.0.0
    hooks:
      - id: jarl-check
        additional_dependencies: ["jarl-linter==0.6.0"]
```

In `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/etiennebacher/jarl-pre-commit"
rev = "1.0.0"
hooks = [
  { id = "jarl-check", additional_dependencies = ["jarl-linter==0.6.0"] },
]
```


This is the most explicit way to know which version of Jarl is used. Note that:

- `autoupdate` doesn't update `additional_dependencies`, so you have to update the version of Jarl manually.
- if you already used `additional_dependencies` then it must always contain `jarl-linter`, otherwise 
  Jarl will not be installed.
- any version of Jarl published on [PyPI](https://pypi.org/project/jarl-linter/) can be used this way (0.5.0 and later).

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
- **Version pinning is respected:** the `rev:` value in your config determines which tag of this repo is checked out, and that tag's `.pre-commit-hooks.yaml` pins the jarl version, unless you override it with `additional_dependencies`.
The pre-commit environment cache means the download only happens once per `rev:`. You may have projects using different versions of jarl simultaneously without them interfering with each other or with any system-wide jarl installation.
