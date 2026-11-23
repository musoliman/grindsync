# GrindSync

Automatically sync your accepted LeetCode solutions to a GitHub repo and an Obsidian tracking sheet.

Solve a problem on LeetCode, run GrindSync, and your code is committed to GitHub and logged as a new row in your Obsidian vault. There's no copy-pasting.

## How it works

Each run does the following:

1. Fetches your 20 most recent accepted submissions from LeetCode's GraphQL API.
2. Skips any submission already recorded in `state.json`.
3. For each new submission:
   - fetches the full source code, difficulty and problem number,
   - commits the code to your GitHub repo (or updates the file if it already exists),
   - appends a row to `LeetCode/solutions.md` in your Obsidian vault, linking to the commit,
   - records the submission ID in `state.json`, so a crash mid-run never causes duplicates.

GrindSync is a one-shot script, not a daemon. Run it manually or on a schedule (cron, launchd, etc.).

### Output

**GitHub**: solutions are organised by difficulty:

```
easy/0001-two-sum/solution.py
medium/0002-add-two-numbers/solution.cpp
hard/0004-median-of-two-sorted-arrays/solution.java
```

**Obsidian**: `<vault>/LeetCode/solutions.md` is created automatically:

| # | Title | Difficulty | Language | Date | Solution |
|---|---|---|---|---|---|
| 1 | Two Sum | Easy | python3 | 2026-11-23 | [link](https://github.com/you/leetcode-solutions/blob/main/easy/0001-two-sum/solution.py) |

## Configuration

Copy `.env.example` to `.env` and fill it in:

| Variable | Description |
|---|---|
| `LC_USERNAME` | Your LeetCode username |
| `LC_SESSION_COOKIE` | Value of the `LEETCODE_SESSION` cookie (browser dev tools → Application → Cookies on leetcode.com) |
| `GITHUB_TOKEN` | GitHub personal access token with write access to the target repo |
| `GITHUB_REPO` | Target repo, as `owner/name` |
| `OBSIDIAN_VAULT_PATH` | Path to your Obsidian vault |

Optionally, `STATE_FILE` sets where the sync state is stored. It defaults to `state.json`.

> The session cookie expires periodically. If you see "Failed to fetch submissions", grab a fresh one. Never commit `.env`; it's already git-ignored.

## Running locally

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python main.py
```

## Running with Docker

```bash
docker compose run --rm grindsync
```

Compose reads secrets from `.env`, mounts your vault at `/vault`, and persists sync state in `./data/state.json`. To avoid re-syncing old submissions, copy an existing `state.json` into `./data/` first.

## Project layout

```
main.py                      # entry point: orchestrates the sync, manages state
src/grindsync/
  config.py                  # loads settings from .env
  lc.py                      # LeetCode GraphQL client
  github_sync.py             # commits solutions to GitHub
  obsidian_sync.py           # appends rows to the Obsidian sheet
```

## Limitations

- Only the 20 most recent accepted submissions are checked per run. Run it at least that often to avoid gaps.
- Each problem/language pair maps to one file, so a newer accepted solution overwrites the previous one.
