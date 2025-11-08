#!/usr/bin/env python3
import os
import random
from typing import Any, Dict, List

import requests


PLAYER_NAME = os.getenv("PLAYER_NAME", "ibrahimovic")
SERVER_URL = os.getenv("SERVER_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def random_direction() -> str:
    return random.choice(["0", "1", "2"])


def strategy(state: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    players = state.get("players") or []
    self_name = (PLAYER_NAME or "").lower()

    opponent_ids: List[str] = []
    for player in players:
        pid = player.get("player_id") or player.get("playerId")
        name = (player.get("player_name") or player.get("playerName") or "").lower()
        if not pid or (self_name and name == self_name):
            continue
        opponent_ids.append(str(pid))

    shoot = {pid: random_direction() for pid in opponent_ids}
    keep = {pid: random_direction() for pid in opponent_ids}
    if not shoot:
        direction = random_direction()
        shoot["*"] = direction
        keep["*"] = direction
    return {"shoot": shoot, "keep": keep}


def main() -> None:
    if not SERVER_URL:
        raise SystemExit("SERVER_URL env var required")

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
