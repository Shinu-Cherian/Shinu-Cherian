def pad(label: str, target: int = 25) -> str:
    """Helper to pad a label with dotted lines for precise alignment."""
    return "." * max(1, target - len(label)) + " "

def measure_line(segments: list, char_width: float) -> float:
    return sum(len(seg.text) * char_width for seg in segments)
