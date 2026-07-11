from PIL import Image, ImageEnhance, ImageFilter

def generate():
    img = Image.open("assets/shinu profile pic.png")
    
    width, height = img.size
    
    # Crop tightly to face
    left = width * 0.15
    right = width * 0.85
    top = height * 0.1
    bottom = height * 0.8
    img = img.crop((left, top, right, bottom))
    
    rows = 25
    img_width, img_height = img.size
    img_ratio = img_width / img_height
    char_aspect_ratio = (14 * 0.62) / 20.0
    cols = int(rows * img_ratio / char_aspect_ratio)
    
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    img = img.resize((cols, rows), Image.Resampling.LANCZOS)
    img = img.convert('L')
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    enhancer2 = ImageEnhance.Brightness(img)
    img = enhancer2.enhance(1.1)
    
    chars = " .,:;=~+*?%S#MW&8B$"
    
    pixels = img.getdata()
    ascii_str = ""
    
    for pixel in pixels:
        if pixel < 40:
            idx = 0
        else:
            val = (pixel - 40) / 215.0
            idx = int(val * (len(chars) - 1))
        
        idx = max(0, min(len(chars)-1, idx))
        ascii_str += chars[idx]
        
    res = ""
    for i in range(0, len(ascii_str), cols):
        line = ascii_str[i:i+cols]
        res += f'            r"{line}",\n'
    return res

if __name__ == "__main__":
    print(generate())
