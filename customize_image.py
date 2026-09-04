from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

img_path = r'C:\Users\HP\Downloads\téléchargement.jpg'
orig = Image.open(img_path).convert('RGB')
w, h = orig.size

# Font paths
font_path_bold = r'C:/Windows/Fonts/arialbd.ttf'
font_path_regular = r'C:/Windows/Fonts/arial.ttf'

# ==========================================
# VARIATION 1: Sleek Professional Vertical Card
# ==========================================
# Canvas size: width x (height + 120)
v1_w = w + 80
v1_h = h + 160
v1 = Image.new('RGB', (v1_w, v1_h), (15, 15, 18)) # Dark charcoal background

# Paste original fingerprint centered horizontally, offset vertically
paste_x = (v1_w - w) // 2
paste_y = 40
v1.paste(orig, (paste_x, paste_y))

draw1 = ImageDraw.Draw(v1)

# Add glowing accent line or border
draw1.rectangle([20, 20, v1_w - 20, v1_h - 20], outline=(50, 180, 255), width=2)

# Text: ELVO LEADERSHIP
try:
    font_title = ImageFont.truetype(font_path_bold, 28)
    font_sub = ImageFont.truetype(font_path_regular, 16)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

text_title = "ELVO LEADERSHIP"
text_sub = "BIOMETRIC VERIFIED IDENTITY"

# Center text title
bbox = draw1.textbbox((0, 0), text_title, font=font_title)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = (v1_w - tw) // 2
ty = paste_y + h + 20

# Draw text with subtle cyan glow / shadow
draw1.text((tx+1, ty+1), text_title, font=font_title, fill=(0, 100, 150))
draw1.text((tx, ty), text_title, font=font_title, fill=(255, 255, 255))

# Center subtitle
bbox_sub = draw1.textbbox((0, 0), text_sub, font=font_sub)
sw = bbox_sub[2] - bbox_sub[0]
sx = (v1_w - sw) // 2
sy = ty + th + 10

draw1.text((sx, sy), text_sub, font=font_sub, fill=(160, 175, 190))

out1_path = r'C:\Users\HP\Downloads\Elvo_Leadership_Badge_1.jpg'
v1.save(out1_path, quality=95)
print(f"Saved: {out1_path}")

# ==========================================
# VARIATION 2: Circular Tech Emblem Style (Square 600x600)
# ==========================================
size2 = 600
v2 = Image.new('RGB', (size2, size2), (10, 10, 12))
draw2 = ImageDraw.Draw(v2)

# Resize orig fingerprint to fit nicely in center
fp_size = 380
orig_resized = orig.resize((fp_size, fp_size), Image.Resampling.LANCZOS)
fx = (size2 - fp_size) // 2
fy = (size2 - fp_size) // 2 - 30
v2.paste(orig_resized, (fx, fy))

# Outer circular ring design
draw2.ellipse([fx - 15, fy - 15, fx + fp_size + 15, fy + fp_size + 15], outline=(0, 220, 255), width=3)

# Top text: ELVO
try:
    font_top = ImageFont.truetype(font_path_bold, 32)
    font_bottom = ImageFont.truetype(font_path_bold, 24)
except:
    font_top = ImageFont.load_default()
    font_bottom = ImageFont.load_default()

top_text = "ELVO"
t_bbox = draw2.textbbox((0, 0), top_text, font=font_top)
t_w = t_bbox[2] - t_bbox[0]
draw2.text(((size2 - t_w) // 2, 35), top_text, font=font_top, fill=(255, 255, 255))

# Bottom text: LEADERSHIP
bottom_text = "LEADERSHIP"
b_bbox = draw2.textbbox((0, 0), bottom_text, font=font_bottom)
b_w = b_bbox[2] - b_bbox[0]
draw2.text(((size2 - b_w) // 2, size2 - 65), bottom_text, font=font_bottom, fill=(0, 220, 255))

out2_path = r'C:\Users\HP\Downloads\Elvo_Leadership_Emblem_2.jpg'
v2.save(out2_path, quality=95)
print(f"Saved: {out2_path}")
