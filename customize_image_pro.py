from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

img_path = r'C:\Users\HP\Downloads\téléchargement.jpg'
orig = Image.open(img_path).convert('RGB')
w, h = orig.size

font_path_bold = r'C:/Windows/Fonts/arialbd.ttf'
font_path_regular = r'C:/Windows/Fonts/arial.ttf'

# ==========================================
# VARIATION 3: Executive VIP Platinum / Gold Badge (Card Style)
# ==========================================
# High-res horizontal or vertical executive card: 800 x 900
card_w = 800
card_h = 900
card = Image.new('RGB', (card_w, card_h), (12, 14, 18))
draw = ImageDraw.Draw(card)

# Draw subtle gradient/background lines for tech executive feel
for i in range(0, card_h, 4):
    draw.line([(0, i), (card_w, i)], fill=(16, 19, 24))

# Outer executive border (Platinum/Silver gradient look)
draw.rectangle([30, 30, card_w - 30, card_h - 30], outline=(190, 205, 220), width=2)
draw.rectangle([36, 36, card_w - 36, card_h - 36], outline=(70, 85, 100), width=1)

# Resize original fingerprint nicely
fp_size = 360
orig_resized = orig.resize((fp_size, fp_size), Image.Resampling.LANCZOS)
fx = (card_w - fp_size) // 2
fy = 100
card.paste(orig_resized, (fx, fy))

# Frame around fingerprint
draw.ellipse([fx - 12, fy - 12, fx + fp_size + 12, fy + fp_size + 12], outline=(218, 165, 32), width=3) # Gold accent ring

try:
    font_name = ImageFont.truetype(font_path_bold, 36)
    font_sub = ImageFont.truetype(font_path_regular, 18)
    font_meta = ImageFont.truetype(font_path_regular, 14)
except:
    font_name = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_meta = ImageFont.load_default()

# Name: ELVO LEADERSHIP
name_text = "ELVO LEADERSHIP"
nb = draw.textbbox((0, 0), name_text, font=font_name)
nw = nb[2] - nb[0]
nx = (card_w - nw) // 2
ny = fy + fp_size + 40

# Draw name with drop shadow
draw.text((nx+2, ny+2), name_text, font=font_name, fill=(0, 0, 0))
draw.text((nx, ny), name_text, font=font_name, fill=(255, 215, 0)) # Gold title

# Subtitle / Role
sub_text = "CHIEF EXECUTIVE & VISIONARY"
sb = draw.textbbox((0, 0), sub_text, font=font_sub)
sw = sb[2] - sb[0]
sx = (card_w - sw) // 2
sy = ny + 50
draw.text((sx, sy), sub_text, font=font_sub, fill=(220, 225, 235))

# Divider line
draw.line([(150, sy + 35), (card_w - 150, sy + 35)], fill=(70, 85, 100), width=1)

# Metadata footer
meta_text = "SECURE ACCESS • VERIFIED CREDENTIAL • GLOBAL STRATEGY"
mb = draw.textbbox((0, 0), meta_text, font=font_meta)
mw = mb[2] - mb[0]
mx = (card_w - mw) // 2
my = sy + 55
draw.text((mx, my), meta_text, font=font_meta, fill=(120, 140, 160))

out3_path = r'C:\Users\HP\Downloads\Elvo_Leadership_Executive_VIP.jpg'
card.save(out3_path, quality=95)
print(f"Saved: {out3_path}")

# ==========================================
# VARIATION 4: Modern Cyber-Glassmorphism Dark Banner
# ==========================================
w4, h4 = 900, 500
banner = Image.new('RGB', (w4, h4), (8, 10, 15))
draw4 = ImageDraw.Draw(banner)

# Left side: fingerprint inside a rounded glowing box
box_size = 380
box_x = 60
box_y = (h4 - box_size) // 2
draw4.rounded_rectangle([box_x - 10, box_y - 10, box_x + box_size + 10, box_y + box_size + 10], radius=16, outline=(0, 200, 255), width=2, fill=(15, 22, 35))

orig_b = orig.resize((box_size, box_size), Image.Resampling.LANCZOS)
banner.paste(orig_b, (box_x, box_y))

# Right side: Text branding
try:
    font_b_title = ImageFont.truetype(font_path_bold, 42)
    font_b_desc = ImageFont.truetype(font_path_regular, 20)
    font_b_small = ImageFont.truetype(font_path_regular, 14)
except:
    font_b_title = ImageFont.load_default()
    font_b_desc = ImageFont.load_default()
    font_b_small = ImageFont.load_default()

tx_start = box_x + box_size + 60

# Tag
draw4.text((tx_start, box_y + 30), "AUTHENTICATED PROFILE", font=font_b_small, fill=(0, 180, 255))

# Main Name
draw4.text((tx_start, box_y + 60), "ELVO", font=font_b_title, fill=(255, 255, 255))
draw4.text((tx_start, box_y + 110), "LEADERSHIP", font=font_b_title, fill=(0, 200, 255))

# Description / Quote
quote = "“Vision, Strategy & Excellence”"
draw4.text((tx_start, box_y + 180), quote, font=font_b_desc, fill=(180, 190, 205))

# Security status badge
draw4.rounded_rectangle([tx_start, box_y + 260, tx_start + 220, box_y + 295], radius=6, fill=(0, 80, 120))
draw4.text((tx_start + 15, box_y + 268), "STATUS: SECURED", font=font_b_small, fill=(255, 255, 255))

out4_path = r'C:\Users\HP\Downloads\Elvo_Leadership_Cyber_Banner.jpg'
banner.save(out4_path, quality=95)
print(f"Saved: {out4_path}")
