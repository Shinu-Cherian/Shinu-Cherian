import os
import sys

# Ensure we can import from scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.profile_builder import ProfileBuilder
from scripts.render.theme import DarkTheme, LightTheme
from scripts.render.engine import LayoutEngine

# Import render modules
from scripts.render.sections import ascii_art, system_info, skills, projects, contact, opensource

def generate():
    # 1. Build the unified data object
    builder = ProfileBuilder()
    profile = builder.build(validate=False)
    
    themes = [
        ("dark", DarkTheme()),
        ("light", LightTheme())
    ]
    
    for theme_name, theme in themes:
        # 2. Initialize the architecture for this theme
        layout = LayoutEngine(theme)
        
        # 3. Render left column
        layout.add_left(ascii_art.render(profile, theme))
        
        # 4. Render right column components
        layout.add_right(system_info.render(profile, theme))
        
        skills_sec = skills.render(profile, theme)
        if skills_sec.elements:
            layout.add_right(skills_sec)
            
        projects_sec = projects.render(profile, theme)
        if projects_sec.elements:
            layout.add_right(projects_sec)
            
        layout.add_right(contact.render(profile, theme))
        layout.add_right(opensource.render(profile, theme))
        
        # 5. Generate final SVG using the canvas engine
        svg_content = layout.build()
        
        output_path = os.path.join("assets", "generated", f"{theme_name}.svg")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate()
