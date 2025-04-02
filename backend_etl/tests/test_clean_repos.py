# Unit tests for clean_repos function in py
from backend_etl.transformer import clean_repos


# Test case: No repositories to clean
def test_no_repos():
    repos = []
    result = clean_repos(repos)

    # Expected output: Empty list
    assert result == []


# Test case: Forked repositories
def test_forked():
    repos = [
        {
            "name": "test1",
            "description": "test1",
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": True,  # Forked test repo
            "isArchived": False,
            "url": "test1",
            "licenseInfo": {"name": "test1"},
            "owner": {"login": "test1"},
            "primaryLanguage": {"name": "Python"},
        }
    ]

    result = clean_repos(repos)

    # Expected output: Empty list (should remove forked repos)
    assert result == []


# Test case: Archived repositories
def test_archived():
    repos = [
        {
            "name": "test1",
            "description": "test1",
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": False,
            "isArchived": True,  # Archived test repo
            "url": "test1",
            "licenseInfo": {"name": "test1"},
            "owner": {"login": "test1"},
            "primaryLanguage": {"name": "Python"},
        }
    ]

    result = clean_repos(repos)

    # Expected output: Empty list (should remove archived repos)
    assert result == []


# Test case: Repositories that don't have licenses
def test_no_license():
    repos = [
        {
            "name": "test1",
            "description": "test1",
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": False,
            "isArchived": False,
            "url": "test1",
            "licenseInfo": None,  # No license info
            "owner": {"login": "test1"},
            "primaryLanguage": {"name": "Python"},
        },
        {
            "name": "test2",
            "description": "test2",
            "stargazerCount": 1234,
            "pushedAt": "test2",
            "isFork": False,
            "isArchived": False,
            "url": "test2",
            "licenseInfo": "",  # No license info
            "owner": {"login": "test2"},
            "primaryLanguage": {"name": "Python"},
        },
        {
            "name": "test2",
            "description": "test2",
            "stargazerCount": 1234,
            "pushedAt": "test2",
            "isFork": False,
            "isArchived": False,
            "url": "test2",
            "licenseInfo": [],  # No license info
            "owner": {"login": "test2"},
            "primaryLanguage": {"name": "Python"},
        },
    ]

    result = clean_repos(repos)

    # Expected output: Empty list (should remove all instances of repos with no license metadata)
    assert result == []


# Test case: Repositories missing primary languages
def test_no_primary_language():
    repos = [
        {
            "name": "test1",
            "description": "test1",
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": False,
            "isArchived": False,
            "url": "test1",
            "licenseInfo": {"name": "test1"},
            "owner": {"login": "test1"},
            "primaryLanguage": None,  # No primary language
        },
        {
            "name": "test1",
            "description": "test1",
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": False,
            "isArchived": False,
            "url": "test1",
            "licenseInfo": {"name": "test1"},
            "owner": {"login": "test1"},
            "primaryLanguage": "",  # No primary language
        },
        {
            "name": "test1",
            "description": "test1",
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": False,
            "isArchived": False,
            "url": "test1",
            "licenseInfo": {"name": "test1"},
            "owner": {"login": "test1"},
            "primaryLanguage": [],  # No primary language
        },
    ]

    result = clean_repos(repos)

    # Expected output: 4 repos, 3 with primary language metadata = None and 1 with original primary language
    assert len(result) == 3
    for cleaned_repo in result:
        assert cleaned_repo["language"] is None


# Test case: Repository description missing
def test_no_description():
    repos = [
        {
            "name": "test1",
            "description": "",  # Missing description
            "stargazerCount": 1234,
            "pushedAt": "test1",
            "isFork": False,
            "isArchived": False,
            "url": "test1",
            "licenseInfo": {"name": "test1"},
            "owner": {"login": "test1"},
            "primaryLanguage": {"name": "Python"},
        }
    ]

    result = clean_repos(repos)

    # Expected output: Description should be empty
    assert result[0]["description"] == ""


# Test case: Normal input (no edge cases)
def test_normal_input():
    repos = [
        {
            "name": "test1",  # Repo name = test1
            "description": "testing repo",  # Repo description = testing repo
            "stargazerCount": 1234,  # Repo has 1,234 stars
            "pushedAt": "2025-03-28T13:08:17Z",  # Last update to github repo
            "isFork": False,  # Not forked
            "isArchived": False,  # Not archived
            "url": "testing.com",  # Repo URL = testing.com
            "licenseInfo": {"name": "MIT"},  # Repo has MIT License
            "owner": {"login": "test_user"},  # Repo owner has username test_user
            "primaryLanguage": {"name": "Python"},  # Primary language = Python
        }
    ]

    result = clean_repos(repos)

    # Expected output: Name should be unchanged
    assert result[0]["name"] == "test1"

    # Expected output: Description should be unchanged
    assert result[0]["description"] == "testing repo"

    # Expected output: Star count should be unchanged
    assert result[0]["stars"] == 1234

    # Expected output: Pushed time should be unchanged
    assert result[0]["updated_at"] == "2025-03-28T13:08:17Z"

    # Expected output: Cleaned repo URL is same as original repo URL
    assert result[0]["url"] == "testing.com"

    # Expected output: Cleaned repo license is same as original repo license
    assert result[0]["license"] == "MIT"

    # Expected output: Owner of repo should be the same
    assert result[0]["owner"] == "test_user"

    # Expected result: Language of original repo should be present in cleaned version
    assert result[0]["language"] == "Python"
