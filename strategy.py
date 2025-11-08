#!/usr/bin/env python3
import os
import random
from typing import Dict, List

import requests


PLAYER_NAME = os.getenv("PLAYER_NAME", "ibrahimovic")
SERVER_URL = os.getenv("SERVER_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not SERVER_URL:
    raise SystemExit("SERVER_URL env var required")


def random_sequence(length: int) -> str:
    return "".join(random.choice("012") for _ in range(length))


def extract_players(state: Dict) -> List[str]:
    game_state = state.get("gameState") or state.get("state") or {}
    if isinstance(game_state, dict):
        return list(game_state.keys())
    if isinstance(game_state, list):
        return [player.get("player_id") or player.get("player_name") for player in game_state]
    return []


def main() -> None:
    status_response = requests.get(f"{SERVER_URL}/status", timeout=10)
    status_response.raise_for_status()
    status = status_response.json()

    players = extract_players(status)
    sequence = random_sequence(len(players) or 1)

    headers = {"Content-Type": "application/json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    payload = {"action": sequence}
    if PLAYER_NAME:
        payload["player_name"] = PLAYER_NAME

    submission = requests.post(
        f"{SERVER_URL}/action",
        headers=headers,
        json=payload,
        timeout=10,
    )
    submission.raise_for_status()


if __name__ == "__main__":
    main()


