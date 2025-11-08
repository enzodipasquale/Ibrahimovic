#!/usr/bin/env python3
import os
import random

import requests


PLAYER_NAME = os.getenv("PLAYER_NAME", "ibrahimovic")
SERVER_URL = os.getenv("SERVER_URL", "https://SERVER_URL_PLACEHOLDER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def strategy(state):
    rounds = ((state.get("gameState") or {}).get("state") or [])
    latest = rounds[-1] if rounds else {}
    players = list(latest.keys()) if isinstance(latest, dict) else []
    length = len(players) or 1
    return "".join(random.choice("012") for _ in range(length))


def main():
    status = requests.get(f"{SERVER_URL}/status", timeout=10)
    status.raise_for_status()
    action = strategy(status.json())

    headers = {"Content-Type": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    payload = {"action": action}
    if PLAYER_NAME:
        payload["player_name"] = PLAYER_NAME

    response = requests.post(
        f"{SERVER_URL}/action",
        headers=headers,
        json=payload,
        timeout=10,
    )

    if not response.ok:
        detail = response.text or response.reason
        raise SystemExit(f"Submission failed: {response.status_code} {detail}")


if __name__ == "__main__":
    main()


