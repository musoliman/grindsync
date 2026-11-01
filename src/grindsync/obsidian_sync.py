import os
from datetime import datetime

from grindsync.config import OBSIDIAN_VAULT_PATH

HEADER = "| # | Title | Difficulty | Language | Date | Solution |\n|---|---|---|---|---|---|\n"


def append_to_sheet(problem_id: str, title: str, difficulty: str, lang: str, github_url: str):
    if not OBSIDIAN_VAULT_PATH:
        raise SystemExit("Missing OBSIDIAN_VAULT_PATH in .env")

    note_path = os.path.join(os.path.expanduser(OBSIDIAN_VAULT_PATH), "LeetCode", "solutions.md")
    os.makedirs(os.path.dirname(note_path), exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")
    row = f"| {problem_id} | {title} | {difficulty} | {lang} | {date} | [link]({github_url}) |\n"

    is_new = not os.path.exists(note_path) or os.path.getsize(note_path) == 0
    with open(note_path, "a") as f:
        if is_new:
            f.write(HEADER)
        f.write(row)
