import os
import platform
import shutil
import stat
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

VERSION = "0.7.1"

PACKAGE_DIR = Path(__file__).parent / "jarl_pre_commit"


def _get_platform_info():
    system = platform.system()
    machine = platform.machine()

    if system == "Linux" and machine == "x86_64":
        return "x86_64-unknown-linux-gnu", "tar.gz", "jarl"
    elif system == "Linux" and machine == "aarch64":
        return "aarch64-unknown-linux-gnu", "tar.gz", "jarl"
    elif system == "Darwin" and machine == "x86_64":
        return "x86_64-apple-darwin", "tar.gz", "jarl"
    elif system == "Darwin" and machine == "arm64":
        return "aarch64-apple-darwin", "tar.gz", "jarl"
    elif system == "Windows":
        return "x86_64-pc-windows-msvc", "zip", "jarl.exe"
    else:
        raise RuntimeError(
            f"Unsupported platform: {system}-{machine}. "
            "Please install jarl manually and ensure it is on PATH."
        )


def _download_jarl():
    target, ext, binary_name = _get_platform_info()
    dst = PACKAGE_DIR / binary_name

    if dst.exists():
        return

    url = (
        f"https://github.com/etiennebacher/jarl/releases/download/"
        f"{VERSION}/jarl-{target}.{ext}"
    )

    print(f"Downloading jarl {VERSION} for {target}...")
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        archive = os.path.join(tmpdir, "jarl-archive")
        urllib.request.urlretrieve(url, archive)

        if ext == "zip":
            with zipfile.ZipFile(archive) as z:
                z.extractall(tmpdir)
        else:
            with tarfile.open(archive) as t:
                t.extractall(tmpdir, filter="data")

        # The tar.gz archives put the binary in a `jarl-{target}/` folder,
        # while the Windows zip has it at the top level.
        candidates = [
            os.path.join(tmpdir, f"jarl-{target}", binary_name),
            os.path.join(tmpdir, binary_name),
        ]
        src = next((p for p in candidates if os.path.isfile(p)), None)
        if src is None:
            raise RuntimeError(f"Could not find {binary_name} in {url}")
        shutil.copy2(src, dst)
        if platform.system() != "Windows":
            dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"jarl {VERSION} installed to {dst}")


class BuildPy(build_py):
    """Custom build step: download jarl binary before packaging."""

    def run(self):
        _download_jarl()
        super().run()


setup(
    name="jarl-pre-commit",
    version=VERSION,
    description="pre-commit hook for jarl R linter",
    packages=["jarl_pre_commit"],
    package_data={"jarl_pre_commit": ["jarl", "jarl.exe"]},
    entry_points={
        "console_scripts": [
            "jarl-check=jarl_pre_commit:main",
        ],
    },
    cmdclass={"build_py": BuildPy},
    python_requires=">=3.7",
)
