# Ibrahimovic Penalty Player

## Strategy
Zlatan keeps opponents guessing by firing the ball in a **random direction**:
- Picks from `0` (left), `1` (centre), `2` (right)
- Ignores history – pure unpredictability

## Getting Started
```bash
python strategy.py
```

Before running, set:
- `SERVER_URL` – base URL of the game platform
- `GITHUB_TOKEN` – optional locally, required for authenticated calls

## Registering the Player
```bash
export SERVER_URL="https://SERVER_URL_PLACEHOLDER"
export GITHUB_TOKEN="ghp_example123"
PLAYER_NAME="ibrahimovic"
curl -sS -X POST "$SERVER_URL/register" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d "{\"player_name\":\"${PLAYER_NAME}\"}"
```

The JSON response echoes the player name and includes the `player_id` assigned by the server.

## Continuous Play
`.github/workflows/schedule_strategy.yml` submits a turn every 5 minutes (and can be dispatched manually). Populate `GAME_TOKEN` and `SERVER_URL` secrets before enabling it.

