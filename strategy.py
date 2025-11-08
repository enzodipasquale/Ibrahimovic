#!/usr/bin/env python3
import os
import random
from typing import Any, Dict

import requests


PLAYER_NAME = os.getenv("PLAYER_NAME", "ibrahimovic")
SERVER_URL = os.getenv("SERVER_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not SERVER_URL:
    raise SystemExit("SERVER_URL env var required")


def strategy(state: Dict[str, Any]) -> str:
    return random.choice(["0", "1", "2"])


def main() -> None:
    print(f"[strategy] Fetching status from {SERVER_URL}/status")
    response = requests.get(f"{SERVER_URL}/status", timeout=10)
    print(f"[strategy] Status HTTP {response.status_code}")
    response.raise_for_status()
    state = response.json()
    print(
        "[strategy] Current turn:",
        state.get("turn_id"),
        "| players:",
        list((state.get("state") or {}).keys()),
    )

    action = strategy(state)
    print(f"[strategy] Chosen action: {action}")

    headers = {"Content-Type": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    payload = {"action": action}
    if PLAYER_NAME:
        payload["player_name"] = PLAYER_NAME

    print("[strategy] Submitting payload:", payload)

    submission = requests.post(
        f"{SERVER_URL}/action",
        headers=headers,
        json=payload,
        timeout=10,
    )
    print(f"[strategy] Action HTTP {submission.status_code}")
    try:
        submission.raise_for_status()
    except requests.HTTPError:
        detail = submission.text or submission.reason
        print(f"[strategy] Submission failed: {submission.status_code} {detail}")
        return

    try:
        print("[strategy] Submission result:", submission.json())
    except ValueError:
        print("[strategy] Submission succeeded; response had no JSON body.")


if __name__ == "__main__":
    main()


