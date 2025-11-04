# =======================================================================#
# Github Banner Image Code-----------------------------------------------
# =======================================================================#
# Library Import
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)  # For initializing a canvas, drawing on it, and fonts
import imageio  # For animating
import random
import math

# Image Specs
img_height = 900
img_width = 1600
num_frames = 100
banner_text = "Hi! I'm Meghan!"
custom_font = ImageFont.truetype("ShadowsIntoLight-Regular.ttf", size=200)


# empty dict for gif frames
frames = []

# Generate star positions (consistent across frames)
num_stars = 150
stars = [
    (
        random.randint(0, img_width),
        random.randint(0, img_height // 2),
        random.random() * 20,  # Phase offset for each star
    )
    for _ in range(num_stars)
]


# Make some buildings (left to right)
def make_buildings(min_height, max_height):
    """Make building positions"""
    buildings = []
    building_n = 0

    while building_n < img_width:
        building_width = random.randint(40, 130)
        building_height = random.randint(min_height, max_height)
        buildings.append(
            (
                building_n,
                img_height - building_height,
                building_width,
                building_height,
            )
        )
        building_n += random.randint(70, 90)

    return buildings


def make_windows(buildings):
    """Make window positions for buildings"""
    windows = []

    for bx, by, bw, bh in buildings:
        for wy in range(by + 10, img_height - 10, 15):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if random.random() > 0.95:
                    windows.append((wx, wy))

    return windows


def make_building_details(utensil, buildings, windows, color, frame):
    """make_buildings with windows"""
    for bx, by, bw, bh in buildings:
        utensil.rectangle([bx, by, bx + bw, img_height], fill=color)
        # add an outline
        utensil.rectangle([bx, by, bx + bw, img_height], outline=(20, 20, 40), width=1)

    for wx, wy in windows:
        window_color = (225, 220, 100)  # a yellow
        utensil.rectangle([wx, wy, wx + 4, wy + 8], fill=window_color)
        utensil.rectangle([wx, wy, wx + 4, wy + 8], outline=(20, 20, 40), width=1)


# Background, middle, foreground with different height ranges
height_ranges = ((120, 250), (200, 300), (285, 400))  # (min, max) for each layer
color = ((0, 0, 0), (15, 15, 15), (30, 30, 30))  # RGB only, no alpha channel

# Generate building positions
all_buildings = [
    make_buildings(height_ranges[n][0], height_ranges[n][1]) for n in range(3)
]

# Create window positions
all_windows = [make_windows(all_buildings[n]) for n in range(3)]

# Create animation frames
for frame in range(num_frames):
    # Initialize the canvas
    canvas = Image.new("RGB", (img_width, img_height))
    paint_brush = ImageDraw.Draw(canvas)

    # Twilight gradient (top to bottom)
    for y in range(img_height):
        # Interpolate from deep blue to purple/orange
        ratio = y / img_height
        r = int(20 + ratio * 60)  # Dark blue to orange-ish
        g = int(10 + ratio * 40)  # Keep relatively low
        b = int(40 + ratio * 80)  # Blue to purple
        paint_brush.line([(0, y), (img_width, y)], fill=(r, g, b))

    # Add stars with twinkling (sine calc should make it glow??)
    for sx, sy, phase in stars:
        brightness = 0.5 + 0.5 * math.sin((frame + phase * 10) / 10)

        # Star color (white to yellow)
        star_color = (
            int(200 + 55 * brightness),
            int(200 + 55 * brightness),
            int(150 + 105 * brightness),  # Less blue = more yellow when bright
        )

        # Add stars
        star_radius = int(brightness * 2)
        paint_brush.ellipse(
            [sx - star_radius, sy - star_radius, sx + star_radius, sy + star_radius],
            fill=star_color,
        )

    # Create buildings w/ details from background to foreground
    for n in range(2, -1, -1):
        make_building_details(
            utensil=paint_brush,
            buildings=all_buildings[n],
            windows=all_windows[n],
            color=color[n],
            frame=frame,
        )
    # Create textbox for better text positioning
    bbox = paint_brush.textbbox((0, 0), banner_text, font=custom_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # position text in the sky
    text_x = (img_width - text_width) / 2 + 30
    text_y = (img_height * 0.3) - (text_height / 2)

    # Add banner text
    paint_brush.text(
        (text_x, text_y),
        banner_text,
        fill=(255, 255, 255),
        font=custom_font,
        embedded_color=True,
    )

    # Add the frame to the canvas
    frames.append(canvas)

# Save it out
imageio.mimsave("github_header_w_text.gif", frames, duration=0.05, loop=1)
