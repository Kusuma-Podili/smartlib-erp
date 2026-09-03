"""
GitHub Pull Request Automation Helper for SmartLibrary ERP.
Uses the GitHub REST API v3 to automate creating, querying, merging, and closing PRs.
Reads credentials dynamically from GITHUB_TOKEN environment variable or git credential manager.
"""
import json
import os
import sys
import subprocess
import urllib.request
import urllib.error

DEFAULT_REPO = "Kusuma-Podili/smartlib-erp"

def get_git_credential_token() -> str:
    """Dynamically query git credential helper without storing tokens in source code."""
    try:
        proc = subprocess.Popen(
            ["git", "credential", "fill"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, _ = proc.communicate(input="protocol=https\nhost=github.com\n\n")
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""

class GitHubHelper:
    def __init__(self, repo=DEFAULT_REPO, token=None):
        self.repo = repo
        self.token = token or os.environ.get("GITHUB_TOKEN") or get_git_credential_token()
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SmartLibraryERP-Automation"
        }

    def _request(self, endpoint, method="GET", data=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_data = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=req_data, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read().decode("utf-8")
                return json.loads(resp_body) if resp_body else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"HTTP Error {e.code} on {method} {url}: {err_body}", file=sys.stderr)
            raise

    def create_pr(self, title: str, body: str, head_branch: str, base_branch: str = "main") -> dict:
        """Open a Pull Request on GitHub."""
        payload = {
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base_branch
        }
        result = self._request("pulls", method="POST", data=payload)
        pr_number = result.get("number")
        pr_url = result.get("html_url")
        print(f"Successfully opened PR #{pr_number}: {title}")
        print(f"PR URL: {pr_url}")
        return result

    def get_pr(self, pr_number: int) -> dict:
        return self._request(f"pulls/{pr_number}", method="GET")

    def merge_pr(self, pr_number: int, commit_title: str = None, merge_method: str = "merge") -> dict:
        payload = {
            "commit_title": commit_title or f"Merge pull request #{pr_number}",
            "merge_method": merge_method
        }
        result = self._request(f"pulls/{pr_number}/merge", method="PUT", data=payload)
        print(f"Successfully merged PR #{pr_number}. Merged: {result.get('merged')}")
        return result

    def close_pr(self, pr_number: int) -> dict:
        payload = {"state": "closed"}
        result = self._request(f"pulls/{pr_number}", method="PATCH", data=payload)
        print(f"PR #{pr_number} state updated to: {result.get('state')}")
        return result

if __name__ == "__main__":
    helper = GitHubHelper()
    print("GitHub PR helper initialized for repo:", helper.repo)
    if helper.token:
        print("Credential helper retrieved active authorization.")
    else:
        print("Warning: No token found.")
