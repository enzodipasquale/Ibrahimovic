#!/usr/bin/env python3
import os
import random
from typing import Any, Dict

import requests


PLAYER_NAME = "ibrahimovic"
SERVER_URL = os.getenv("SERVER_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not SERVER_URL:
    raise SystemExit("SERVER_URL env var required")


def strategy(state: Dict[str, Any]) -> str:
    return random.choice(["0", "1", "2"])


def main() -> None:
    response = requests.get(f"{SERVER_URL}/status", timeout=10)
    response.raise_for_status()
    state = response.json()

    action = strategy(state)

    headers = {"Content-Type": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    submission = requests.post(
        f"{SERVER_URL}/action",
        headers=headers,
        json={"action": action},
        timeout=10,
    )
    try:
        submission.raise_for_status()
    except requests.HTTPError:
        detail = submission.text or submission.reason
        print(f"Submission failed: {submission.status_code} {detail}")
        return


if __name__ == "__main__":
    main()


