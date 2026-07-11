from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import get_dots, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    lines = [[("- GitHub Stats ", theme.color_title), ("-" * 70, theme.color_dots)]]
    
    if not profile.github_available:
        lines.append([(". API Status: ", theme.color_label), (get_dots(". API Status: ", "Offline (Using Cached/YAML Data)"), theme.color_dots), ("Offline (Using Cached/YAML Data)", theme.color_error)])
        
    def stat_line(l1, v1, l2, v2):
        v1_s = str(v1)
        v2_s = str(v2)
        d1 = get_dots(l1, v1_s + " ", 40)
        d2 = get_dots(l2, v2_s, 42)
        return [
            (l1, theme.color_label), (d1, theme.color_dots), (v1_s + " ", theme.color_value),
            ("| ", theme.color_dots),
            (l2, theme.color_label), (d2, theme.color_dots), (v2_s, theme.color_value)
        ]
        
    lines.append(stat_line(". Contributions: ", profile.total_contributions, "Stars: ", profile.total_stars))
    lines.append(stat_line(". Commits: ", profile.total_commits, "Followers: ", profile.followers))
    
    repos_s = str(profile.total_repos)
    lines.append([
        (". Total Repos: ", theme.color_label), (get_dots(". Total Repos: ", repos_s), theme.color_dots), (repos_s, theme.color_value)
    ])
    
    if profile.top_languages:
        langs = ", ".join(l['name'] for l in profile.top_languages[:3])
        lines.append([
            (". Top Languages: ", theme.color_label), (get_dots(". Top Languages: ", langs), theme.color_dots), (langs, theme.color_value)
        ])
        
    loc_val = f"{profile.loc_total:,} ( {profile.loc_additions:,}++, {profile.loc_deletions:,}-- )"
    lines.append([
        (". Lines of Code: ", theme.color_label), (get_dots(". Lines of Code: ", loc_val), theme.color_dots), (loc_val, theme.color_value)
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
