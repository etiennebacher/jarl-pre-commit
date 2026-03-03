#!/usr/bin/env bash
set -eu

VERSION="0.4.0"
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/jarl-pre-commit"
BINARY="$CACHE_DIR/jarl-$VERSION"

if [ ! -x "$BINARY" ] && [ ! -x "$BINARY.exe" ]; then
    OS="$(uname -s)"
    ARCH="$(uname -m)"
    EXT="tar.gz"
    case "$OS-$ARCH" in
        Linux-x86_64)    TARGET="x86_64-unknown-linux-gnu" ;;
        Linux-aarch64)   TARGET="aarch64-unknown-linux-gnu" ;;
        Darwin-x86_64)   TARGET="x86_64-apple-darwin" ;;
        Darwin-arm64)    TARGET="aarch64-apple-darwin" ;;
        MINGW*-x86_64|MSYS*-x86_64|CYGWIN*-x86_64)
            TARGET="x86_64-pc-windows-msvc"
            EXT="zip"
            ;;
        *) echo "jarl: unsupported platform: $OS-$ARCH" >&2; exit 1 ;;
    esac

    URL="https://github.com/etiennebacher/jarl/releases/download/${VERSION}/jarl-${TARGET}.${EXT}"
    mkdir -p "$CACHE_DIR"
    TMPDIR="$(mktemp -d)"
    echo "Downloading jarl v${VERSION} for ${TARGET}..." >&2
    curl -fsSL "$URL" -o "$TMPDIR/jarl-archive"

    if [ "$EXT" = "zip" ]; then
        unzip -q "$TMPDIR/jarl-archive" -d "$TMPDIR"
        mv "$TMPDIR/jarl-${TARGET}/jarl.exe" "$BINARY.exe"
    else
        tar -xzf "$TMPDIR/jarl-archive" -C "$TMPDIR"
        mv "$TMPDIR/jarl-${TARGET}/jarl" "$BINARY"
        chmod +x "$BINARY"
    fi
    rm -rf "$TMPDIR"
fi

if [ -x "$BINARY.exe" ]; then
    exec "$BINARY.exe" check "$@"
else
    exec "$BINARY" check "$@"
fi
