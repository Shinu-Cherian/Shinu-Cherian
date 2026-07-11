from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import pad, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    lines = [[("- Contact & Links ", theme.color_title), ("-----------------------------------------------", theme.color_dots)]]
    
    for k, v in profile.contacts.items():
        label = f". {k.replace('_', '.').title()}: "
        lines.append([
            (label, theme.color_label),
            (pad(label, 25), theme.color_dots),
            (v, theme.color_value)
        ])
        
    for link in profile.social_links:
        label = f". {link.platform}: "
        val = link.username or link.url
        lines.append([
            (label, theme.color_label),
            (pad(label, 25), theme.color_dots),
            (val, theme.color_value)
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
