import json
import os
from grindsync.lc import get_recent_submissions, get_submission_code
from grindsync.github_sync import commit_solution
from grindsync.obsidian_sync import append_to_sheet
from grindsync.config import LC_SESSION_COOKIE, LC_USERNAME

STATE_FILE = os.getenv("STATE_FILE", "state.json")


def load_state() -> set:
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return set()
    return set(data.get("synced_ids", []))


def save_state(synced_ids: set):
    with open(STATE_FILE, "w") as f:
        json.dump({"synced_ids": list(synced_ids)}, f)


def main():
    print("GrindSync starting...")

    if not all([LC_USERNAME, LC_SESSION_COOKIE]):
        raise SystemExit("Missing LC_USERNAME or LC_SESSION_COOKIE in .env")

    synced_ids = load_state()

    response = get_recent_submissions(LC_USERNAME, LC_SESSION_COOKIE)
    if not response.get("data") or response["data"].get("recentAcSubmissionList") is None:
        raise SystemExit(f"Failed to fetch submissions: {response}")
    submissions = response["data"]["recentAcSubmissionList"]

    new_submissions = [s for s in submissions if s["id"] not in synced_ids]

    if not new_submissions:
        print("Nothing new to sync.")
        return

    print(f"Found {len(new_submissions)} new submission(s).")

    for submission in new_submissions:
        submission_id = submission["id"]
        title = submission["title"]
        title_slug = submission["titleSlug"]
        lang = submission["lang"]

        print(f"Syncing: {title}")

        code_response = get_submission_code(submission_id, LC_SESSION_COOKIE)
        details = (code_response.get("data") or {}).get("submissionDetails")
        if not details:
            print(f"Skipping {title}: could not fetch code ({code_response})")
            continue
        code = details["code"]
        difficulty = details["question"]["difficulty"]
        problem_id = details["question"]["questionFrontendId"]

        github_url = commit_solution(problem_id, title_slug, difficulty, code, lang)
        append_to_sheet(problem_id, title, difficulty, lang, github_url)

        synced_ids.add(submission_id)
        save_state(synced_ids)

        print(f"Done: {title}")

    print("Sync complete.")


if __name__ == "__main__":
    main()


