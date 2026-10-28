from github import Github
import os

def commit_solution(problem_id: str, title_slug: str, difficulty: str, code: str) -> str:
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("GITHUB_REPO"))

    # build the file path
    folder = difficulty.lower()
    filename = f"{problem_id.zfill(4)}-{title_slug}"
    file_path = f"{folder}/{filename}/solution.cpp"

    # push to repo
    repo.create_file(
        path=file_path,
        message=f"Add solution: {title_slug}",
        content=code
    )

    # return the github url for obsidian
    return f"https://github.com/{os.getenv('GITHUB_REPO')}/blob/main/{file_path}"