from datetime import datetime
from grindsync.config import OBSIDIAN_VAULT_PATH


NOTE_PATH = f"{OBSIDIAN_VAULT_PATH}/LeetCode/solutions.md"


def append_to_sheet(problem_id: str, title: str, difficulty: str, lang: str, github_url: str):
    date = datetime.now().strftime("%Y-%m-%d")
    row = f"| {problem_id} | {title} | {difficulty} | {lang} | {date} | [link]({github_url}) |\n"

    with open(NOTE_PATH, "a") as f:
        f.write(row)