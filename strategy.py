#!/usr/bin/env python3
import os
from typing import Any, Dict, List

import numpy as np
import requests


PLAYER_NAME = "ibrahimovic"
SERVER_URL = os.getenv("SERVER_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def strategy(state: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
    player_names = state.get("playerNames") or []
    normalized_self = PLAYER_NAME.lower()
    opponents = [
        str(name)
        for name in player_names
        if name and str(name).strip().lower() != normalized_self
    ]
    if not opponents:
        return {"shoot": {}, "keep": {}}

    shoot_dirs = np.random.randint(0, 3, len(opponents)).tolist()
    keep_dirs = np.random.randint(0, 3, len(opponents)).tolist()

    return {
        "shoot": {pid: int(direction) for pid, direction in zip(opponents, shoot_dirs)},
        "keep": {pid: int(direction) for pid, direction in zip(opponents, keep_dirs)},
    }


def main() -> None:
    if not SERVER_URL:
        raise SystemExit("SERVER_URL env var required")

    status = requests.get(f"{SERVER_URL}/status", timeout=10)
    status.raise_for_status()
    action = strategy(status.json())

    headers = {"Content-Type": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    payload = {"action": action, "player_name": PLAYER_NAME}

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
