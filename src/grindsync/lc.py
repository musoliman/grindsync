import requests

recentSubmissionQuery = '''{
        "query": """
            query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
                lang
            }
            }
  """'''
GRAPHQL_URL = "https://leetcode.com/graphql"

def get_recent_submissions(username: str, session_cookie: str):
    
    response = requests.post(
    url = GRAPHQL_URL,
    json = {
        "query": recentSubmissionQuery,
        "variables": {"username": username, "limit": 20}
            },   
    headers={
        "Cookie": f"LEETCODE_SESSION={session_cookie}",
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"

    }        


    )
    return response.json

