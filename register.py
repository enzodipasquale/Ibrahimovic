#!/usr/bin/env python3
import os
import sys

import requests


SERVER_URL = "https://SERVER_URL_PLACEHOLDER"


def main() -> None:
    github_token = os.getenv("GITHUB_TOKEN", "").strip()

    if not github_token:
        raise SystemExit("GITHUB_TOKEN environment variable not set")

    try:
        response = requests.post(
            f"{SERVER_URL}/register",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {github_token}",
            },
            json={"player_name": "ibrahimovic"},
            timeout=10,
        )
    except Exception as exc:
        raise SystemExit(f"Registration error: {exc}") from exc

    if not response.ok:
        raise SystemExit(f"Registration failed: {response.status_code} {response.text}")
    
    try:
        payload = response.json()
    except ValueError:
        print("Registration succeeded but response was not JSON.")
        return

    status = (payload.get("status") or "").lower()
    if status == "registered":
        print(f"Player '{payload.get('player_name')}' registered with id {payload.get('player_id')}.")
    elif status == "already_registered":
        print(f"Player '{payload.get('player_name')}' already registered. Using id {payload.get('player_id')}.")
    else:
        print(f"Registration response: {payload}")


if __name__ == "__main__":
    main()

