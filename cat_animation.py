import os
import time
import itertools

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

frames2 = [
"""
   |\\_._/|     
   | o o |      
   (  T  )     
  .^`-^-'^.    
  `.  ;  .'    
  | | | | |    
 ((_((|))_))  
""",
"""
    |,\\__/|     
    |  o o|     
    (   T )    
  .^`--^'^.      
  `.  ;  .'      
  | | | | |    
 ((_((|))_))    
    """,
    """
    |\\__/,|    
    |o o  |     
    ( T   )    
  .^`^--'^.     
  `.  ;  .'      
  | | | | |    
 ((_((|))_))   
    """,
    """
   |\\_._/|
   | 0 0 |
   (  T  )
  .^`-^-'^.
  `.  ;  .'    
  | | | | |    
 ((_((|))_))   
    """,
"""
   |\\_._/|  
   |-o^o-| 
   (  T  )     
  .^`-^-'^.  
  `.  ;  .'    
  | | | | |    
 ((_((|))_))  
""",
"""
   |\\_._/|
   |-@~@-|
   (  T  )       
  .^`-^-'^.    
  `.  ;  .'    
  | | | | |   
 ((_((|))_))  
"""
    
]


def _clear():
    os.system("cls" if os.name == "nt" else "clear")


def animate(seq, interval: float = 5, cycles: int | None = None) -> None:
    """Render frames to the console.

    - interval: seconds between frames
    - cycles: number of full iterations over frames; None loops forever
    """
    try:
        it = itertools.cycle(seq) if cycles is None else (f for _ in range(cycles) for f in seq)
        for frame in it:
            _clear()
            print(frame, flush=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


def export_gif(frames_list, output_path="cat_animation.gif", interval=500, font_size=16):
    """Export animation frames to a GIF with transparent background.
    
    Args:
        frames_list: List of ASCII art strings
        output_path: Path to save the GIF file
        interval: Duration of each frame in milliseconds
        font_size: Font size for rendering (default 16)
    
    Returns:
        bool: True if successful, False if Pillow not available
    """
    if not PILLOW_AVAILABLE:
        print("Error: Pillow library not installed. Run: pip install Pillow")
        return False
    
    def pick_font(size):
        """Try to find a monospace font, fallback to default."""
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/System/Library/Fonts/Monaco.ttf",  # macOS
            "C:/Windows/Fonts/consola.ttf",      # Windows
            "DejaVuSansMono.ttf",
            "Courier New.ttf",
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size=size)
                except Exception:
                    continue
        return ImageFont.load_default()
    
    def render_frame(text, font, pad=8):
        """Render ASCII text to an image with transparent background."""
        lines = text.splitlines()
        if not lines:
            lines = [""]
        
        # Measure character dimensions
        bbox = font.getbbox("M")
        char_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1] + 2  # Add small line spacing
        
        max_cols = max(len(line) for line in lines)
        width = char_w * max_cols + pad * 2
        height = line_h * len(lines) + pad * 2
        
        # Create image with transparent background
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw each line
        y = pad
        for line in lines:
            draw.text((pad, y), line, fill=(255, 255, 255, 255), font=font)
            y += line_h
        
        return img
    
    def to_palette_with_transparency(img):
        """Convert RGBA to palette mode with transparency."""
        # Convert to palette mode
        pal_img = img.convert("P", palette=Image.ADAPTIVE, colors=255)
        
        # Set transparency for fully transparent pixels
        transparency_index = 0
        pal_img.putpixel((0, 0), transparency_index)
        
        return pal_img, transparency_index
    
    try:
        font = pick_font(font_size)
        
        # Render all frames
        rgba_images = []
        for frame_text in frames_list:
            img = render_frame(frame_text, font)
            rgba_images.append(img)
        
        # Convert to palette mode with transparency
        pal_images = []
        transparency_index = 0
        
        for i, img in enumerate(rgba_images):
            pal_img, trans_idx = to_palette_with_transparency(img)
            pal_images.append(pal_img)
            if i == 0:
                transparency_index = trans_idx
        
        # Save as animated GIF
        if pal_images:
            pal_images[0].save(
                output_path,
                save_all=True,
                append_images=pal_images[1:],
                duration=interval,
                loop=0,
                transparency=transparency_index,
                disposal=2,  # Clear frame before next
            )
            
            print(f"✅ GIF exported successfully: {output_path}")
            return True
        else:
            print("Error: No frames to export")
            return False
            
    except Exception as e:
        print(f"Error exporting GIF: {e}")
        return False


if __name__ == "__main__":
    # Export frames2 as GIF with 500ms interval
    export_gif(frames2, "cat_animation.gif", interval=500)
    
    # Run the animation
    # animate(frames2, interval=1)