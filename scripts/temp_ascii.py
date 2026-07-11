from PIL import Image
import sys

def image_to_ascii(image_path, new_width=40, new_height=25):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Convert to grayscale
    image = image.convert('L')
    
    # Resize image
    # Note: Terminal fonts are usually ~0.5 aspect ratio, so height gets stretched.
    # We force the height to 25 lines to fit our layout.
    image = image.resize((new_width, new_height))
    
    # ASCII characters from darkest to lightest
    # Since we are on a dark terminal background (black), white pixels should map to dense characters,
    # and black pixels to spaces.
    ASCII_CHARS = [' ', '.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
    
    pixels = image.getdata()
    ascii_str = ''
    for pixel in pixels:
        # Background is white (>200), hair is black (<40)
        if pixel > 200:
            idx = 0
        elif pixel < 40:
            idx = 0
        else:
            # Scale skin tones (40-200) to the ASCII range
            val = (pixel - 40) / 160
            idx = int(val * (len(ASCII_CHARS) - 1))
            
        ascii_str += ASCII_CHARS[idx]
        
    # Split into lines
    ascii_img = ""
    for i in range(0, len(ascii_str), new_width):
        line = ascii_str[i:i+new_width]
        ascii_img += f'            r"{line}",\n'
        
    print(ascii_img)

if __name__ == '__main__':
    image_to_ascii("assets/shinu profile pic.png", 40, 25)
