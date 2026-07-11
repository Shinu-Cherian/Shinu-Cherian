from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import get_dots, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    lines_data = [[("- Contact & Links ", theme.color_title), ("-" * 67, theme.color_dots)]]
    
    for k, v in profile.contacts.items():
        label = f". {k.replace('_', '.').title()}: "
        href = f"mailto:{v}" if "@" in v else None
        lines_data.append([
            (label, theme.color_label, None),
            (get_dots(label, v), theme.color_dots, None),
            (v, theme.color_value, href)
        ])
        
    for link in profile.social_links:
        label = f". {link.platform}: "
        val = link.username or link.url
        lines_data.append([
            (label, theme.color_label, None),
            (get_dots(label, val), theme.color_dots, None),
            (val, theme.color_value, link.url)
        ])
        
    elements = []
    current_y = 0
    max_width = 0
    char_width = theme.get_char_width()
    
    for line_tuples in lines_data:
        segments = []
        for item in line_tuples:
            if len(item) == 3:
                segments.append(TextSegment(item[0], item[1], item[2]))
            else:
                segments.append(TextSegment(item[0], item[1]))
        
        line_width = measure_line(segments, char_width)
        max_width = max(max_width, line_width)
        
        elements.append(Element(x=0, y=current_y, segments=segments))
        current_y += theme.line_height
        
    return SectionResult(width=max_width, height=current_y, elements=elements)
