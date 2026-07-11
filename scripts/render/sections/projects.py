from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import get_dots, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    if not profile.featured_projects:
        return SectionResult(width=0, height=0, elements=[])
        
    lines = [[("- Featured Projects ", theme.color_title), ("-" * 65, theme.color_dots)]]
    
    for p in profile.featured_projects[:3]:
        label = f". {p.name}: "
        desc = p.description or ""
        if len(desc) > 40:
            desc = desc[:37] + "..."
        stats = f" {p.language}" if p.language else ""
        val = f"{desc}{stats}"
        
        lines.append([
            (label, theme.color_label),
            (get_dots(label, val), theme.color_dots),
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
