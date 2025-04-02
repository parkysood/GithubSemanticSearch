# Transform and clean extracted repos from GitHub API
from datetime import datetime
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def clean_repos(repos):
    cleaned = []  # Store cleaned repository data

    for repo in repos:
        # Ignore forks, archived repos, poorly structured repositories (no license, )
        if repo["isFork"] or repo["isArchived"] or not repo["licenseInfo"]:
            continue

        cleaned.append(
            {
                "name": repo["name"],
                "description": repo["description"] or "",
                "owner": repo["owner"]["login"],
                "language": repo["primaryLanguage"]["name"]
                if repo["primaryLanguage"]
                else None,
                "stars": repo["stargazerCount"],
                "updated_at": repo["pushedAt"],
                "license": repo["licenseInfo"]["name"],
                "url": repo["url"],
            }
        )

    return cleaned


# Generate embeddings for each cleaned repo
def generate_embeddings(cleaned):
    descriptions = [repo["description"] for repo in cleaned]
    vectors = model.encode(descriptions)

    for i, repo in enumerate(cleaned):
        repo["embedding"] = vectors[i].toList()

    return cleaned


def __init__():
    pass
