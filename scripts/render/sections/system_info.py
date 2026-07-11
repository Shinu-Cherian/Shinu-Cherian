from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import get_dots, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    title = f"{profile.github_username or profile.name.lower().replace(' ', '')}@github "
    sep = "-" * max(10, 85 - len(title))
    
    lines = [
        [(title, theme.color_title), (sep, theme.color_dots)],
        [(". Name: ", theme.color_label), (get_dots(". Name: ", profile.name), theme.color_dots), (profile.name, theme.color_value)],
        [(". Role: ", theme.color_label), (get_dots(". Role: ", profile.role), theme.color_dots), (profile.role, theme.color_value)],
        [(". Education: ", theme.color_label), (get_dots(". Education: ", profile.education), theme.color_dots), (profile.education, theme.color_value)],
        [(". Location: ", theme.color_label), (get_dots(". Location: ", profile.location), theme.color_dots), (profile.location, theme.color_value)],
        [(". Focus: ", theme.color_label), (get_dots(". Focus: ", profile.current_focus), theme.color_dots), (profile.current_focus, theme.color_value)]
    ]
    
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
