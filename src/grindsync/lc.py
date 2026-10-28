import requests

GRAPHQL_URL = "https://leetcode.com/graphql"

RECENT_SUBMISSIONS_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
    recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
        lang
    }
}
"""

SUBMISSION_DETAILS_QUERY = """
query submissionDetails($submissionId: Int!) {
    submissionDetails(submissionId: $submissionId) {
        code
        lang { name }
        question { questionFrontendId difficulty title }
    }
}
"""

def get_recent_submissions(username: str, session_cookie: str):
    response = requests.post(
        url=GRAPHQL_URL,
        json={
            "query": RECENT_SUBMISSIONS_QUERY,
            "variables": {"username": username, "limit": 20}
        },
        headers={
            "Cookie": f"LEETCODE_SESSION={session_cookie}",
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com"
        }
    )
    return response.json()

def get_submission_code(submission_id: str, session_cookie: str):
    response = requests.post(
        url=GRAPHQL_URL,
        json={
            "query": SUBMISSION_DETAILS_QUERY,
            "variables": {"submissionId": int(submission_id)}
        },
        headers={
            "Cookie": f"LEETCODE_SESSION={session_cookie}",
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com"
        }
    )
    return response.json()