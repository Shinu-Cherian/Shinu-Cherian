from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import pad, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    lines = [[("- GitHub Stats ", theme.color_title), ("--------------------------------------------------", theme.color_dots)]]
    
    if not profile.github_available:
        lines.append([(". API Status: ", theme.color_label), (pad(". API Status: "), theme.color_dots), ("Offline (Using Cached/YAML Data)", theme.color_error)])
        
    lines.append([
        (". Contributions: ", theme.color_label), (pad(". Contributions: "), theme.color_dots), (f"{profile.total_contributions:,} ", theme.color_value),
        ("| ", theme.color_dots), ("Stars: ", theme.color_label), (pad("Stars: ", 10), theme.color_dots), (f"{profile.total_stars:,}", theme.color_value)
    ])
    
    lines.append([
        (". Commits: ", theme.color_label), (pad(". Commits: "), theme.color_dots), (f"{profile.total_commits:,} ", theme.color_value),
        ("| ", theme.color_dots), ("Followers: ", theme.color_label), (pad("Followers: ", 10), theme.color_dots), (f"{profile.followers:,}", theme.color_value)
    ])
    
    lines.append([
        (". Issues: ", theme.color_label), (pad(". Issues: "), theme.color_dots), (f"{profile.total_issues:,} ", theme.color_value),
        ("| ", theme.color_dots), ("PRs: ", theme.color_label), (pad("PRs: ", 10), theme.color_dots), (f"{profile.total_prs:,}", theme.color_value)
    ])
    
    if profile.top_languages:
        langs = ", ".join(l['name'] for l in profile.top_languages[:3])
        lines.append([
            (". Top Languages: ", theme.color_label), (pad(". Top Languages: "), theme.color_dots), (langs, theme.color_value)
        ])
        
    if profile.last_updated:
        ts = profile.last_updated.strftime("%Y-%m-%d %H:%M UTC")
        lines.append([
            (". Last Updated: ", theme.color_label), (pad(". Last Updated: "), theme.color_dots), (ts, theme.color_muted)
        ])
        
    elements = []
    current_y = 0
    max_width = 0
    char_width = theme.get_char_width()
    
    for line_segments in lines:
        segments = [TextSegment(t, c) for t, c in line_segments]
        line_width = measure_line(segments, char_width)
        max_width = max(max_width, line_width)
        
        elements.append(Element(x=0, y=current_y, segments=segments))
        current_y += theme.line_height
        
    return SectionResult(width=max_width, height=current_y, elements=elements)
