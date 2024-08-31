import os
import sys

from github import Github

# Singleton pattern for GitHub instance
_github_instance = None


def github() -> Github:
    global _github_instance
    if _github_instance is None:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("Error: No GitHub token provided and $GITHUB_TOKEN is not set.", file=sys.stderr)
            sys.exit(-1)
        _github_instance = Github(token)
    return _github_instance
