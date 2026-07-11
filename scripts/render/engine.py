from typing import List
from scripts.render.theme import Theme
from scripts.render.core import SectionResult, TextSegment, Element

class SVGCanvas:
    def __init__(self, theme: Theme, width: int, height: int):
        self.theme = theme
        self.width = width
        self.height = height
        self.elements_svg = []
        
    def draw_text_line(self, x: float, y: float, segments: List[TextSegment], css_class: str = "text"):
        svg = f'        <text x="{x}" y="{y}" class="{css_class}">'
        for seg in segments:
            escaped = seg.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            svg += f'<tspan fill="{seg.color}">{escaped}</tspan>'
        svg += '</text>\\n'
        self.elements_svg.append(svg)
        
    def draw_raw_text(self, x: float, y: float, text: str, css_class: str):
        escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg = f'        <text x="{x}" y="{y}" class="{css_class}">{escaped}</text>\\n'
        self.elements_svg.append(svg)

    def render(self) -> str:
        margin = 20
        total_svg_width = self.width + (margin * 2)
        total_svg_height = self.height + (margin * 2)

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_svg_width} {total_svg_height}" width="100%" height="auto">
    <defs>
        <style>
            .text {{ 
                font-family: Consolas, "Cascadia Code", "JetBrains Mono", monospace; 
                font-size: {self.theme.font_size}px; 
                white-space: pre;
            }}
            .ascii {{
                fill: {self.theme.ascii_color};
                font-weight: bold;
            }}
        </style>
        <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
    </defs>
    
    <rect width="100%" height="100%" fill="{self.theme.outer_bg}"/>
    <rect x="{margin}" y="{margin}" width="{self.width}" height="{self.height}" fill="{self.theme.bg}" rx="12" stroke="{self.theme.border}" stroke-width="1.5" filter="url(#shadow)"/>
    
    <g transform="translate({margin}, {margin})">
{"".join(self.elements_svg)}    </g>
</svg>"""

class LayoutEngine:
    def __init__(self, theme: Theme):
        self.theme = theme
        self.sections_left: List[SectionResult] = []
        self.sections_right: List[SectionResult] = []
        
    def add_left(self, section: SectionResult):
        self.sections_left.append(section)
        
    def add_right(self, section: SectionResult):
        self.sections_right.append(section)
        
    def build(self) -> str:
        # Calculate dynamic positions
        start_y = self.theme.padding + self.theme.font_size
        
        # Process left column
        left_width = 0
        left_height = 0
        positioned_elements: List[Element] = []
        
        current_y = start_y
        for sec in self.sections_left:
            for el in sec.elements:
                positioned_elements.append(Element(
                    x=el.x + self.theme.padding,
                    y=el.y + current_y,
                    segments=el.segments,
                    raw_text=el.raw_text,
                    css_class=el.css_class
                ))
            left_width = max(left_width, sec.width)
            left_height += sec.height
            current_y += sec.height + self.theme.section_gap
            
        right_start_x = self.theme.padding + left_width + self.theme.column_gap
        
        # Process right column
        right_width = 0
        right_height = 0
        current_y = start_y
        for sec in self.sections_right:
            for el in sec.elements:
                positioned_elements.append(Element(
                    x=el.x + right_start_x,
                    y=el.y + current_y,
                    segments=el.segments,
                    raw_text=el.raw_text,
                    css_class=el.css_class
                ))
            right_width = max(right_width, sec.width)
            right_height += sec.height
            current_y += sec.height + self.theme.section_gap
            
        actual_left_height = sum(s.height for s in self.sections_left) + self.theme.section_gap * max(0, len(self.sections_left) - 1)
        actual_right_height = sum(s.height for s in self.sections_right) + self.theme.section_gap * max(0, len(self.sections_right) - 1)
        
        window_width = right_start_x + right_width + self.theme.padding
        window_height = self.theme.padding + max(actual_left_height, actual_right_height) + self.theme.padding
        
        # Draw on SVGCanvas
        canvas = SVGCanvas(self.theme, int(window_width), int(window_height))
        for el in positioned_elements:
            if el.raw_text is not None:
                canvas.draw_raw_text(el.x, el.y, el.raw_text, el.css_class)
            else:
                canvas.draw_text_line(el.x, el.y, el.segments, el.css_class)
                
        return canvas.render()
