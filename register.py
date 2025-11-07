#!/usr/bin/env python3
import os
import sys

import requests


def main() -> None:
    server_url = os.getenv("SERVER_URL", "").strip()
    github_token = os.getenv("GITHUB_TOKEN", "").strip()
    player_name = "ibrahimovic"

    if not server_url:
        raise SystemExit("SERVER_URL environment variable not set")
    if not github_token:
        raise SystemExit("GITHUB_TOKEN environment variable not set")

    response = requests.post(
        f"{server_url.rstrip('/')}/register",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {github_token}",
        },
        json={"player_name": player_name},
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

