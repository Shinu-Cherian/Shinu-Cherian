from PIL import Image, ImageEnhance
import math

def generate_detailed_ascii():
    img = Image.open("assets/shinu profile pic.png")
    
    # We want much higher resolution ASCII.
    # Typical neofetch ascii art is about 40-50 characters wide and 20-30 lines high.
    # Let's use 55 characters wide, which allows more detail.
    target_width = 55
    
    width, height = img.size
    
    # Crop tightly to the face to maximize detail within the character grid.
    # Original is 2400x3000. 
    # Left: 400, Right: 2000, Top: 300, Bottom: 2300 gives a tight crop on face & glasses.
    left = width * 0.15
    right = width * 0.85
    top = height * 0.1
    bottom = height * 0.75
    
    img = img.crop((left, top, right, bottom))
    
    # Resize to text grid, compensating for font aspect ratio (~0.5)
    img_width, img_height = img.size
    # char height is approx 2x char width
    # so we need half as many rows as a square grid would dictate
    aspect_ratio = img_height / img_width
    target_height = int(target_width * aspect_ratio * 0.5)
    
    img = img.resize((target_width, target_height))
    img = img.convert('L') # Grayscale
    
    # Enhance contrast to make facial features pop
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    
    enhancer2 = ImageEnhance.Brightness(img)
    img = enhancer2.enhance(1.2)
    
    # Detailed ASCII palette from dark to light
    # We will invert later since dark terminal background needs light characters for highlights.
    # " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    # A slightly simpler but effective palette:
    chars = " .',:;+*?%S#@"
    
    pixels = img.getdata()
    ascii_str = ""
    
    # We invert the mapping so dark hair/glasses = " " (transparent/dark),
    # and skin/highlights = bright characters like "#" or "@"
    
    for pixel in pixels:
        # Invert: pixel 0 (black) -> idx 0 (space)
        # pixel 255 (white) -> idx max (@)
        # We also want to crush blacks so the background drops out
        if pixel < 60:
            idx = 0
        else:
            # map 60-255 to 0-max
            normalized = (pixel - 60) / 195.0
            idx = int(normalized * (len(chars) - 1))
            
        idx = max(0, min(len(chars)-1, idx))
        ascii_str += chars[idx]
        
    # Format as Python list of raw strings
    res = "        ascii_lines = [\n"
    for i in range(0, len(ascii_str), target_width):
        line = ascii_str[i:i+target_width]
        res += f'            r"{line}",\n'
    res += "        ]\n"
    return res

if __name__ == "__main__":
    print(generate_detailed_ascii())
