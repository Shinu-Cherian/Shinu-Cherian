def get_dots(label: str, value: str, target_length: int = 85) -> str:
    """Helper to pad a label with dotted lines for precise right-alignment."""
    dots_len = target_length - len(label) - len(value)
    return "." * max(1, dots_len) + " "

def measure_line(segments: list, char_width: float) -> float:
    return sum(len(seg.text) * char_width for seg in segments)
