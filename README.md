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

## Continuous Play
Two GitHub Actions in `.github/workflows/` mirror other players:
- `register.yml` registers the player on each push
- `penalty-shootout-manual.yml` triggers a manual penalty session

Add the required secrets (`GAME_TOKEN`, `SERVER_URL`, `GITHUB_TOKEN`) once you create a GitHub token for this repo.

