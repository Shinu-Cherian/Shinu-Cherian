from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TextSegment:
    text: str
    color: str
    href: Optional[str] = None

@dataclass
class Element:
    x: float
    y: float
    segments: List[TextSegment] = field(default_factory=list)
    raw_text: Optional[str] = None
    css_class: str = "text"

@dataclass
class SectionResult:
    width: float
    height: float
    elements: List[Element]
