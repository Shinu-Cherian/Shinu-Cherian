import os
import json
import hashlib
import time
from typing import TypeVar, Generic, Optional, Dict, Any, List
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

from scripts.constants import GRAPHQL_ENDPOINT, DEFAULT_HEADERS, REQUEST_TIMEOUT

# --- Core Types ---
T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

# --- Data Models ---
@dataclass
class ProfileData:
    username: str
    name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    company: Optional[str]
    website: Optional[str]
    twitter: Optional[str]

@dataclass
class RepositoryData:
    name: str
    description: Optional[str]
    stars: int
    forks: int
    language: Optional[str]
    language_color: Optional[str]
    is_private: bool
    url: str

@dataclass
class LanguageStats:
    name: str
    color: str
    size: int

@dataclass
class ContributionData:
    total_commits: int
    total_issues: int
    total_prs: int
    total_contributions: int

# --- GraphQL Fragments ---
USER_INFO_FRAGMENT = """
fragment UserInfo on User {
  login
  name
  bio
  location
  company
  websiteUrl
  twitterUsername
}
"""

REPO_FRAGMENT = """
fragment RepoInfo on Repository {
  name
  description
  stargazerCount
  forkCount
  primaryLanguage {
    name
    color
  }
  isPrivate
  url
}
"""

class GitHubClient:
    def __init__(self):
        load_dotenv()
        self.token = os.environ.get("GITHUB_TOKEN")
        self.username = os.environ.get("GITHUB_USERNAME") or os.environ.get("GITHUB_REPOSITORY_OWNER")
        self.cache_dir = os.path.join("data", "cache")
        self.cache_ttl = 15 * 60  # 15 minutes in seconds

    # --- Caching Engine ---
    def _get_cache_key(self, query: str, variables: dict) -> str:
        key_string = query + json.dumps(variables, sort_keys=True)
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()

    def _read_cache(self, key: str) -> Optional[dict]:
        path = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(path):
            return None
            
        # Check TTL
        if time.time() - os.path.getmtime(path) > self.cache_ttl:
            return None
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _write_cache(self, key: str, data: dict):
        os.makedirs(self.cache_dir, exist_ok=True)
        path = os.path.join(self.cache_dir, f"{key}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    # --- API Engine ---
    def _run_query(self, query: str, variables: dict = None) -> Result[dict]:
        if not self.token:
            return Result(success=False, error="Missing GITHUB_TOKEN in environment")
            
        variables = variables or {}
        if 'login' not in variables:
            if not self.username:
                return Result(success=False, error="Missing GITHUB_USERNAME or GITHUB_REPOSITORY_OWNER in environment")
            variables['login'] = self.username
            
        cache_key = self._get_cache_key(query, variables)
        cached = self._read_cache(cache_key)
        if cached:
            return Result(success=True, data=cached)
            
        headers = DEFAULT_HEADERS.copy()
        headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = requests.post(
                GRAPHQL_ENDPOINT,
                json={'query': query, 'variables': variables},
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 401:
                return Result(success=False, error="Invalid GITHUB_TOKEN (401 Unauthorized)")
            if response.status_code == 403 or response.status_code == 429:
                return Result(success=False, error="Rate limit exceeded")
                
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                err_msg = data['errors'][0].get('message', 'GraphQL Error')
                return Result(success=False, error=err_msg)
                
            self._write_cache(cache_key, data)
            return Result(success=True, data=data)
            
        except requests.exceptions.Timeout:
            return Result(success=False, error="Network request timed out")
        except requests.exceptions.ConnectionError:
            return Result(success=False, error="Network connection failed")
        except requests.exceptions.RequestException as e:
            return Result(success=False, error=f"HTTP request failed: {str(e)}")
        except Exception as e:
            return Result(success=False, error=f"Unexpected error: {str(e)}")

    # --- Public Methods ---
    def get_profile(self) -> Result[ProfileData]:
        query = USER_INFO_FRAGMENT + """
        query($login: String!) {
            user(login: $login) {
                ...UserInfo
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
            
        user = res.data.get('data', {}).get('user')
        if not user:
            return Result(success=False, error="User not found")
            
        profile = ProfileData(
            username=user.get('login'),
            name=user.get('name'),
            bio=user.get('bio'),
            location=user.get('location'),
            company=user.get('company'),
            website=user.get('websiteUrl'),
            twitter=user.get('twitterUsername')
        )
        return Result(success=True, data=profile)

    def get_repositories(self, limit: int = 6) -> Result[List[RepositoryData]]:
        query = REPO_FRAGMENT + """
        query($login: String!, $limit: Int!) {
            user(login: $login) {
                pinnedItems(first: $limit, types: REPOSITORY) {
                    nodes {
                        ... on Repository {
                            ...RepoInfo
                        }
                    }
                }
            }
        }
        """
        res = self._run_query(query, {'limit': limit})
        if not res.success:
            return Result(success=False, error=res.error)
            
        nodes = res.data.get('data', {}).get('user', {}).get('pinnedItems', {}).get('nodes', [])
        repos = []
        for node in nodes:
            lang = node.get('primaryLanguage') or {}
            repos.append(RepositoryData(
                name=node.get('name'),
                description=node.get('description'),
                stars=node.get('stargazerCount', 0),
                forks=node.get('forkCount', 0),
                language=lang.get('name'),
                language_color=lang.get('color'),
                is_private=node.get('isPrivate', False),
                url=node.get('url')
            ))
        return Result(success=True, data=repos)

    def get_followers(self) -> Result[int]:
        query = """
        query($login: String!) {
            user(login: $login) {
                followers {
                    totalCount
                }
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
        count = res.data.get('data', {}).get('user', {}).get('followers', {}).get('totalCount', 0)
        return Result(success=True, data=count)

    def get_following(self) -> Result[int]:
        query = """
        query($login: String!) {
            user(login: $login) {
                following {
                    totalCount
                }
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
        count = res.data.get('data', {}).get('user', {}).get('following', {}).get('totalCount', 0)
        return Result(success=True, data=count)

    def get_stars(self) -> Result[int]:
        # Gets total stars across all owned repositories
        query = """
        query($login: String!) {
            user(login: $login) {
                repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
                    nodes {
                        stargazerCount
                    }
                }
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
        nodes = res.data.get('data', {}).get('user', {}).get('repositories', {}).get('nodes', [])
        total = sum(node.get('stargazerCount', 0) for node in nodes)
        return Result(success=True, data=total)

    def get_languages(self) -> Result[List[LanguageStats]]:
        query = """
        query($login: String!) {
            user(login: $login) {
                repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
                    nodes {
                        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                            edges {
                                size
                                node {
                                    name
                                    color
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
            
        nodes = res.data.get('data', {}).get('user', {}).get('repositories', {}).get('nodes', [])
        lang_map = {}
        for repo in nodes:
            edges = repo.get('languages', {}).get('edges', [])
            for edge in edges:
                size = edge.get('size', 0)
                node = edge.get('node', {})
                name = node.get('name')
                color = node.get('color')
                if name:
                    if name not in lang_map:
                        lang_map[name] = LanguageStats(name=name, color=color, size=0)
                    lang_map[name].size += size
                    
        sorted_langs = sorted(lang_map.values(), key=lambda x: x.size, reverse=True)
        return Result(success=True, data=sorted_langs)

    def get_repo_stats(self, repo_name: str) -> Dict[str, int]:
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/stats/contributors"
        headers = DEFAULT_HEADERS.copy()
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            cache_key = self._get_cache_key(f"repo_stats_{repo_name}", {})
            cached = self._read_cache(cache_key)
            if cached:
                data = cached
            else:
                res = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                if res.status_code == 200:
                    data = res.json()
                    self._write_cache(cache_key, data)
                elif res.status_code == 202:
                    time.sleep(1.0)
                    res = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                    if res.status_code == 200:
                        data = res.json()
                        self._write_cache(cache_key, data)
                    else:
                        data = []
                else:
                    data = []
            
            additions = 0
            deletions = 0
            for contributor in data:
                if contributor.get("author", {}).get("login", "").lower() == self.username.lower():
                    for week in contributor.get("weeks", []):
                        additions += week.get("a", 0)
                        deletions += week.get("d", 0)
            return {"additions": additions, "deletions": deletions}
        except Exception:
            return {"additions": 0, "deletions": 0}

    def get_all_profile_data(self) -> Result[dict]:
        query = USER_INFO_FRAGMENT + REPO_FRAGMENT + """
        query($login: String!) {
            user(login: $login) {
                ...UserInfo
                
                followers { totalCount }
                following { totalCount }
                
                pinnedItems(first: 6, types: REPOSITORY) {
                    nodes {
                        ... on Repository {
                            ...RepoInfo
                        }
                    }
                }
                
                repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
                    nodes {
                        name
                        stargazerCount
                        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                            edges {
                                size
                                node { name color }
                            }
                        }
                    }
                }
                
                contributionsCollection {
                    totalCommitContributions
                    totalIssueContributions
                    totalPullRequestContributions
                    contributionCalendar {
                        totalContributions
                    }
                }
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
            
        user_data = res.data.get('data', {}).get('user', {})
        repos = user_data.get('repositories', {}).get('nodes', [])
        total_additions = 0
        total_deletions = 0
        for r in repos:
            name = r.get('name')
            if name:
                stats = self.get_repo_stats(name)
                total_additions += stats["additions"]
                total_deletions += stats["deletions"]
                
        res.data['loc_stats'] = {
            'additions': total_additions,
            'deletions': total_deletions,
            'total': total_additions - total_deletions
        }
        return Result(success=True, data=res.data)

    def get_contributions(self) -> Result[ContributionData]:
        query = """
        query($login: String!) {
            user(login: $login) {
                contributionsCollection {
                    totalCommitContributions
                    totalIssueContributions
                    totalPullRequestContributions
                    contributionCalendar {
                        totalContributions
                    }
                }
            }
        }
        """
        res = self._run_query(query)
        if not res.success:
            return Result(success=False, error=res.error)
            
        coll = res.data.get('data', {}).get('user', {}).get('contributionsCollection', {})
        total_contribs = coll.get('contributionCalendar', {}).get('totalContributions', 0)
        
        data = ContributionData(
            total_commits=coll.get('totalCommitContributions', 0),
            total_issues=coll.get('totalIssueContributions', 0),
            total_prs=coll.get('totalPullRequestContributions', 0),
            total_contributions=total_contribs
        )
        return Result(success=True, data=data)
