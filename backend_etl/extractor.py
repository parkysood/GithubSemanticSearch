# Extract repositories using GitHub GraphQL API

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

API_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}

GRAPHQL_QUERY = """
query ($cursor: String) {
    search(query: "stars:>10 pushed:>2024-09-01", type: REPOSITORY, first: 50, after: $cursor) {
        pageInfo {
            endCursor
            hasNextPage
        }
        edges {
            node {
                ... on Repository {
                    name
                    description
                    stargazerCount
                    pushedAt
                    isFork
                    isArchived
                    url
                    licenseInfo { name }
                    owner { login }
                    primaryLanguage { name }
                }
            }
        }
    }
}
"""


def fetch_github_repos():
    all_repos = []
    cursor = None
    has_next = True

    while has_next:
        response = requests.post(
            API_URL,
            json={"query": GRAPHQL_QUERY, "variables": {"cursor": cursor}},
            headers=HEADERS,
        )

        data = response.json()
        search_data = data["data"]["search"]
        for edge in search_data["edges"]:
            repo = edge["node"]
            all_repos.append(repo)

        has_next = search_data["pageInfo"]["hasNextPage"]
        cursor = search_data["pageInfo"]["endCursor"]

    return all_repos
