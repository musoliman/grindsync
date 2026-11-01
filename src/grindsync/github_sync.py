from github import Github, GithubException

from grindsync.config import GITHUB_REPO, GITHUB_TOKEN

EXTENSIONS = {
    "cpp": "cpp", "c": "c", "csharp": "cs", "java": "java", "python": "py",
    "python3": "py", "javascript": "js", "typescript": "ts", "golang": "go",
    "rust": "rs", "kotlin": "kt", "swift": "swift", "ruby": "rb", "scala": "scala",
    "php": "php", "mysql": "sql", "mssql": "sql", "oraclesql": "sql",
    "postgresql": "sql", "bash": "sh", "dart": "dart",
}


def commit_solution(problem_id: str, title_slug: str, difficulty: str, code: str, lang: str = "cpp") -> str:
    if not GITHUB_TOKEN or not GITHUB_REPO:
        raise SystemExit("Missing GITHUB_TOKEN or GITHUB_REPO in .env")

    repo = Github(GITHUB_TOKEN).get_repo(GITHUB_REPO)

    ext = EXTENSIONS.get(lang.lower(), lang.lower())
    folder = difficulty.lower()
    filename = f"{str(problem_id).zfill(4)}-{title_slug}"
    file_path = f"{folder}/{filename}/solution.{ext}"
    message = f"Add solution: {title_slug}"

    try:
        existing = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update solution: {title_slug}", code, existing.sha)
    except GithubException as e:
        if e.status != 404:
            raise
        repo.create_file(path=file_path, message=message, content=code)

    return f"https://github.com/{GITHUB_REPO}/blob/{repo.default_branch}/{file_path}"
