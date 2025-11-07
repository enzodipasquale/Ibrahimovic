#!/usr/bin/env python3
"""Register the Ibrahimovic penalty shooter with the platform."""

from __future__ import annotations

import os
import sys
from typing import Final

import requests


PLAYER_NAME: Final[str] = "ibrahimovic"
DEFAULT_SERVER_URL: Final[str] = "https://SERVER_URL_PLACEHOLDER"

SERVER_URL = os.getenv("SERVER_URL", "").strip() or DEFAULT_SERVER_URL
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()


def _normalise_server(url: str) -> str:
    if not url:
        raise SystemExit("SERVER_URL could not be determined")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url.lstrip("/")
    return url.rstrip("/")


def main() -> None:
    server = _normalise_server(SERVER_URL)

    if not GITHUB_TOKEN:
        raise SystemExit("GITHUB_TOKEN environment variable not set")

    response = requests.post(
        f"{server}/register",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
        },
        json={"player_name": PLAYER_NAME},
        timeout=10,
    )

    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - CLI helper
        print(f"❌ Registration error: {exc}")
        sys.exit(1)

