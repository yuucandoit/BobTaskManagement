import httpx
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class GitHubClient:
    def __init__(self):
        self.token = settings.GITHUB_ACCESS_TOKEN
        self.base_url = "https://api.github.com"

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "IBM-Bob-Kanban-Evidence-Tracker"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_pull_request(self, repo_full_name: str, pr_number: int) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/repos/{repo_full_name}/pulls/{pr_number}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self._headers())
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.warning(f"Error fetching PR from GitHub API: {e}")
        return None

    async def get_commit(self, repo_full_name: str, commit_sha: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/repos/{repo_full_name}/commits/{commit_sha}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=self._headers())
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.warning(f"Error fetching commit from GitHub API: {e}")
        return None

github_client = GitHubClient()
