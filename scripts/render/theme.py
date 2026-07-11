from dataclasses import dataclass

@dataclass
class Theme:
    padding: int = 50
    column_gap: int = 20
    line_height: int = 20
    section_gap: int = 20
    
    font_size: int = 14
    
    # Base colors (to be overridden by subclasses)
    outer_bg: str = ""
    bg: str = ""
    border: str = ""
    
    color_title: str = ""
    color_label: str = ""
    color_dots: str = ""
    color_value: str = ""
    
    color_success: str = ""
    color_error: str = ""
    color_muted: str = ""
    
    ascii_color: str = ""
    
    def get_char_width(self):
        return self.font_size * 0.62

@dataclass
class DarkTheme(Theme):
    outer_bg: str = "#0d1117"
    bg: str = "#010409"
    border: str = "#30363d"
    
    color_title: str = "#c9d1d9"
    color_label: str = "#e3b341"
    color_dots: str = "#484f58"
    color_value: str = "#79c0ff"
    
    color_success: str = "#7ee787"
    color_error: str = "#ff7b72"
    color_muted: str = "#8b949e"
    
    ascii_color: str = "#c9d1d9"

@dataclass
class LightTheme(Theme):
    outer_bg: str = "#ffffff"
    bg: str = "#f6f8fa"
    border: str = "#d0d7de"
    
    color_title: str = "#24292f"
    color_label: str = "#9a6700"
    color_dots: str = "#8c959f"
    color_value: str = "#0969da"
    
    color_success: str = "#1a7f37"
    color_error: str = "#d1242f"
    color_muted: str = "#57606a"
    
    ascii_color: str = "#24292f"
