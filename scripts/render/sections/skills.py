from scripts.profile_builder import Profile
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, Element, TextSegment
from scripts.render.utils import pad, measure_line

def render(profile: Profile, theme: Theme) -> SectionResult:
    if not profile.skills:
        return SectionResult(width=0, height=0, elements=[])
        
    elements = []
    current_y = 0
    max_width = 0
    char_width = theme.get_char_width()
    
    for skill in profile.skills:
        label = f". {skill.category}: "
        val = ", ".join(skill.items)
        
        segments = [
            TextSegment(label, theme.color_label),
            TextSegment(pad(label, 30), theme.color_dots),
            TextSegment(val, theme.color_value)
        ]
        
        line_width = measure_line(segments, char_width)
        max_width = max(max_width, line_width)
        
        elements.append(Element(x=0, y=current_y, segments=segments))
        current_y += theme.line_height
        
    return SectionResult(width=max_width, height=current_y, elements=elements)
