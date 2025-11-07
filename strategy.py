#!/usr/bin/env python3
"""Penalty shootout template – pick a random direction each turn."""

import os
import random
import sys
from typing import Any, Dict

import requests


PLAYER_NAME = "ibrahimovic"
SERVER_URL = os.getenv("SERVER_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not SERVER_URL:
    print("❌ SERVER_URL missing")
    sys.exit(1)


def strategy(state: Dict[str, Any]) -> str:
    """Return a random direction as '0', '1', or '2'."""
    return random.choice(["0", "1", "2"])


def submit_action(action: str) -> None:
    headers = {"Content-Type": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.post(
        f"{SERVER_URL}/action",
        headers=headers,
        json={"action": action},
        timeout=10,
    )

    if response.ok:
        print(f"✅ Submitted: {response.json()}")
    else:
        print(f"❌ Submission failed: {response.status_code} - {response.text}")


def main() -> None:
    print(f"🎮 {PLAYER_NAME} taking a shot")

    try:
        state: Dict[str, Any] = requests.get(
            f"{SERVER_URL}/status", timeout=10
        ).json()
    except Exception as exc:  # pragma: no cover - network failure path
        print(f"❌ Unable to fetch state: {exc}")
        return

    print(f"📊 Turn {state.get('turn_id')}: {state.get('state', {})}")

    action = strategy(state)
    print(f"🎯 {PLAYER_NAME.capitalize()} shoots {action}")
    submit_action(action)


if __name__ == "__main__":
    main()


