import os
import yaml
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

from scripts.github_api import GitHubClient, Result

@dataclass
class FeaturedProject:
    name: str
    description: Optional[str]
    stars: int = 0
    forks: int = 0
    language: Optional[str] = None
    language_color: Optional[str] = None
    url: Optional[str] = None
    is_private: bool = False

@dataclass
class SocialLink:
    platform: str
    url: str
    username: Optional[str]

@dataclass
class SkillCategory:
    category: str
    items: List[str]

@dataclass
class Profile:
    # Static Data from YAML
    name: str = ""
    subtitle: str = ""
    location: str = ""
    role: str = ""
    current_focus: str = ""
    education: str = ""
    
    contacts: Dict[str, str] = field(default_factory=dict)
    social_links: List[SocialLink] = field(default_factory=list)
    skills: List[SkillCategory] = field(default_factory=list)
    
    # Combined/Featured Projects (API + YAML)
    featured_projects: List[FeaturedProject] = field(default_factory=list)
    
    # Dynamic GitHub Statistics
    github_username: str = ""
    followers: int = 0
    following: int = 0
    total_stars: int = 0
    total_commits: int = 0
    total_prs: int = 0
    total_issues: int = 0
    total_contributions: int = 0
    total_repos: int = 0
    loc_additions: int = 0
    loc_deletions: int = 0
    loc_total: int = 0
    top_languages: List[Dict[str, Any]] = field(default_factory=list)
    
    # Meta State
    github_available: bool = False
    last_updated: Optional[datetime] = None


class ProfileBuilder:
    def __init__(self, yaml_path: str = "data/profile.yaml"):
        self.yaml_path = yaml_path
        self.yaml_data = {}
        
    def _load_yaml(self):
        if not os.path.exists(self.yaml_path):
            raise FileNotFoundError(f"Configuration file not found: {self.yaml_path}")
        with open(self.yaml_path, "r", encoding="utf-8") as f:
            self.yaml_data = yaml.safe_load(f) or {}

    def _validate_env(self):
        load_dotenv()
        username = os.environ.get("GITHUB_USERNAME") or os.environ.get("GITHUB_REPOSITORY_OWNER")
        if not username:
            raise ValueError("GITHUB_USERNAME or GITHUB_REPOSITORY_OWNER is missing from environment variables.")
        return username

    def build(self, validate: bool = True) -> Profile:
        if validate:
            self._load_yaml()
            username = self._validate_env()
        else:
            try:
                self._load_yaml()
                load_dotenv()
                username = os.environ.get("GITHUB_USERNAME") or os.environ.get("GITHUB_REPOSITORY_OWNER", "")
            except Exception:
                username = ""
                
        profile = Profile()
        profile.name = self.yaml_data.get("name", "")
        profile.subtitle = self.yaml_data.get("subtitle", "")
        profile.location = self.yaml_data.get("location", "")
        profile.role = self.yaml_data.get("role", "")
        profile.current_focus = self.yaml_data.get("current_focus", "")
        profile.education = self.yaml_data.get("education", "")
        profile.contacts = self.yaml_data.get("contacts", {})
        profile.github_username = username
        
        for link in self.yaml_data.get("social_links", []):
            profile.social_links.append(SocialLink(
                platform=link.get("platform", ""),
                url=link.get("url", ""),
                username=link.get("username")
            ))
            
        for skill in self.yaml_data.get("skills", []):
            profile.skills.append(SkillCategory(
                category=skill.get("category", ""),
                items=skill.get("items", [])
            ))
            
        # Parse fallback projects from YAML
        for proj in self.yaml_data.get("featured_projects", []):
            profile.featured_projects.append(FeaturedProject(
                name=proj.get("name", ""),
                description=proj.get("description", "")
            ))
            
        # Fetch GitHub Data
        client = GitHubClient()
        api_res = client.get_all_profile_data()
        
        if validate and not api_res.success:
            raise RuntimeError(f"GitHub API validation failed: {api_res.error}")
            
        if api_res.success:
            profile.github_available = True
            user_data = api_res.data.get("data", {}).get("user")
            
            if user_data:
                profile.followers = user_data.get("followers", {}).get("totalCount", 0)
                profile.following = user_data.get("following", {}).get("totalCount", 0)
                
                # Contributions
                coll = user_data.get("contributionsCollection", {})
                profile.total_commits = coll.get("totalCommitContributions", 0)
                profile.total_issues = coll.get("totalIssueContributions", 0)
                profile.total_prs = coll.get("totalPullRequestContributions", 0)
                profile.total_contributions = coll.get("contributionCalendar", {}).get("totalContributions", 0)
                
                # Repositories & Languages
                repos = user_data.get("repositories", {}).get("nodes", [])
                total_stars = 0
                lang_map = {}
                
                for r in repos:
                    total_stars += r.get("stargazerCount", 0)
                    for edge in r.get("languages", {}).get("edges", []):
                        size = edge.get("size", 0)
                        node = edge.get("node", {})
                        lname = node.get("name")
                        lcolor = node.get("color")
                        if lname:
                            if lname not in lang_map:
                                lang_map[lname] = {"name": lname, "color": lcolor, "size": 0}
                            lang_map[lname]["size"] += size
                            
                profile.total_stars = total_stars
                profile.total_repos = len(repos)
                loc_stats = api_res.data.get('loc_stats', {})
                profile.loc_additions = loc_stats.get('additions', 0)
                profile.loc_deletions = loc_stats.get('deletions', 0)
                profile.loc_total = loc_stats.get('total', 0)
                
                sorted_langs = sorted(lang_map.values(), key=lambda x: x["size"], reverse=True)
                profile.top_languages = sorted_langs
                
                # Pinned Repositories override yaml projects if available
                pinned = user_data.get("pinnedItems", {}).get("nodes", [])
                if pinned:
                    profile.featured_projects = [] # Clear yaml fallback
                    for p in pinned:
                        if p.get("name", "").lower() == "clinexa":
                            continue
                        lang = p.get("primaryLanguage") or {}
                        profile.featured_projects.append(FeaturedProject(
                            name=p.get("name", ""),
                            description=p.get("description", ""),
                            stars=p.get("stargazerCount", 0),
                            forks=p.get("forkCount", 0),
                            language=lang.get("name"),
                            language_color=lang.get("color"),
                            is_private=p.get("isPrivate", False),
                            url=p.get("url")
                        ))
        else:
            profile.github_available = False
            
        profile.last_updated = datetime.now(timezone.utc)
        return profile
