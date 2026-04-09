from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Colors
GREEN = RGBColor(76, 175, 80)
DARK_GREEN = RGBColor(46, 125, 50)
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(33, 33, 33)
GRAY = RGBColor(100, 100, 100)
LIGHT_BG = RGBColor(245, 245, 245)
ACCENT_BLUE = RGBColor(21, 101, 192)
ACCENT_ORANGE = RGBColor(230, 115, 0)
ACCENT_RED = RGBColor(211, 47, 47)
LIGHT_GREEN_BG = RGBColor(232, 245, 233)

ONION_IMG = "C:/Users/12345/Desktop/Projects/OnionGuard/onion-guard-mobile/frontend/assets/onion-image.jpg"
SCREENSHOT_DIR = "C:/Users/12345/Desktop/Projects/OnionGuard/onion-guard-mobile/frontend/screenshots/"


def add_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape_bg(slide, left, top, width, height, color, alpha=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=18, bold=False, color=DARK, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=DARK, spacing=Pt(6)):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = 'Calibri'
        p.space_after = spacing
        p.level = 0
    return txBox


def slide_header(slide, title, subtitle=None):
    # Green bar at top
    add_shape_bg(slide, Inches(0), Inches(0), prs.slide_width, Inches(1.2), GREEN)
    add_text_box(slide, Inches(0.8), Inches(0.25), Inches(10), Inches(0.7), title,
                 font_size=32, bold=True, color=WHITE)
    if subtitle:
        add_text_box(slide, Inches(0.8), Inches(0.75), Inches(10), Inches(0.4), subtitle,
                     font_size=16, color=RGBColor(200, 255, 200))


# ============================================================
# SLIDE 1: TITLE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_bg(slide, DARK_GREEN)

# Gradient overlay effect with shapes
add_shape_bg(slide, Inches(0), Inches(0), prs.slide_width, prs.slide_height, RGBColor(38, 120, 45))

# Onion image
if os.path.exists(ONION_IMG):
    slide.shapes.add_picture(ONION_IMG, Inches(5.2), Inches(0.8), Inches(3), Inches(2))

add_text_box(slide, Inches(1), Inches(1.5), Inches(8), Inches(1.2), 'OnionGuard',
             font_size=54, bold=True, color=WHITE)
add_text_box(slide, Inches(1), Inches(2.8), Inches(8), Inches(0.8),
             'AI-Powered Onion Disease Detection for Farmers',
             font_size=24, color=RGBColor(200, 255, 200))

# Divider line
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(3.8), Inches(3), Pt(3))
shape.fill.solid()
shape.fill.fore_color.rgb = WHITE
shape.line.fill.background()

add_text_box(slide, Inches(1), Inches(4.2), Inches(8), Inches(0.5),
             'Management Presentation', font_size=20, color=WHITE)
add_text_box(slide, Inches(1), Inches(4.8), Inches(8), Inches(0.5),
             'Nkabom Honours Team  |  University of Ghana  |  2026',
             font_size=16, color=RGBColor(180, 230, 180))

add_text_box(slide, Inches(1), Inches(5.8), Inches(10), Inches(0.5),
             'Currently in Closed Testing on Google Play Store',
             font_size=14, color=RGBColor(255, 235, 59), bold=True)


# ============================================================
# SLIDE 2: PROBLEM STATEMENT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'The Problem', 'Why OnionGuard is needed')

# Left column - stats
add_shape_bg(slide, Inches(0.5), Inches(1.6), Inches(3.5), Inches(2.2), RGBColor(255, 235, 238))
add_text_box(slide, Inches(0.8), Inches(1.8), Inches(3), Inches(0.6), '50%',
             font_size=48, bold=True, color=ACCENT_RED)
add_text_box(slide, Inches(0.8), Inches(2.5), Inches(3), Inches(1),
             'Crop losses in West Africa\ndue to pests & diseases',
             font_size=16, color=DARK)

add_shape_bg(slide, Inches(0.5), Inches(4.1), Inches(3.5), Inches(2.2), RGBColor(227, 242, 253))
add_text_box(slide, Inches(0.8), Inches(4.3), Inches(3), Inches(0.6), 'ZERO',
             font_size=48, bold=True, color=ACCENT_BLUE)
add_text_box(slide, Inches(0.8), Inches(5.0), Inches(3), Inches(1),
             'Pre-existing ML models for\nonion disease classification',
             font_size=16, color=DARK)

# Right column - challenges
add_text_box(slide, Inches(4.8), Inches(1.6), Inches(7), Inches(0.5), 'Key Challenges',
             font_size=22, bold=True, color=DARK_GREEN)
challenges = [
    'No ML models exist for the TOM2024 onion disease dataset',
    'Limited access to agricultural extension officers in rural areas',
    'Language barriers prevent farmers from accessing disease info',
    'No affordable diagnostic tools for smallholder farmers',
    'No centralized system for tracking regional disease outbreaks',
]
add_bullet_list(slide, Inches(4.8), Inches(2.2), Inches(7.5), Inches(4), challenges,
                font_size=17, spacing=Pt(12))

add_text_box(slide, Inches(4.8), Inches(5.5), Inches(7.5), Inches(1),
             'Source: Appiah et al., 2025 (Data in Brief, Elsevier)',
             font_size=12, color=GRAY)


# ============================================================
# SLIDE 3: SOLUTION OVERVIEW
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Our Solution', 'OnionGuard mobile application')

features = [
    ('Disease Detection', 'On-device AI classifies 6 onion\nconditions from camera photos.\nWorks offline.', RGBColor(232, 245, 233)),
    ('Freshness Check', 'Gemini Vision AI evaluates\nonion freshness with storage\nrecommendations.', RGBColor(227, 242, 253)),
    ('Treatment Guides', 'Detailed treatment in 5 languages\nwith voice playback for\nlow-literacy farmers.', RGBColor(255, 243, 224)),
    ('Analytics', 'Personal & regional disease\ntracking dashboards for\nfarmers and officers.', RGBColor(243, 229, 245)),
]

x_start = Inches(0.5)
for i, (title, desc, bg_color) in enumerate(features):
    x = x_start + Inches(i * 3.15)
    card = add_shape_bg(slide, x, Inches(1.8), Inches(2.9), Inches(3.5), bg_color)
    card.shadow.inherit = False
    add_text_box(slide, x + Inches(0.3), Inches(2.1), Inches(2.3), Inches(0.5), title,
                 font_size=20, bold=True, color=DARK_GREEN)
    # Divider
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.3), Inches(2.7), Inches(1.5), Pt(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = GREEN
    shape.line.fill.background()
    add_text_box(slide, x + Inches(0.3), Inches(2.9), Inches(2.3), Inches(2), desc,
                 font_size=14, color=GRAY)

# Bottom bar
add_shape_bg(slide, Inches(0.5), Inches(5.8), Inches(12.3), Inches(1), LIGHT_GREEN_BG)
add_text_box(slide, Inches(1), Inches(5.9), Inches(11), Inches(0.8),
             'Security:  JWT Auth  +  Bcrypt  +  Biometric Login  +  HTTPS (TLS 1.2/1.3)  +  Let\'s Encrypt SSL',
             font_size=16, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)


# ============================================================
# SLIDE 4: ML MODEL
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Machine Learning Model', 'MobileNetV3-Large trained on TOM2024 dataset')

# Left - Model info
add_text_box(slide, Inches(0.8), Inches(1.6), Inches(5), Inches(0.4), 'Model Architecture',
             font_size=20, bold=True, color=DARK_GREEN)

model_info = [
    'Base: MobileNetV3-Large (ImageNet pretrained)',
    'Input: 224 x 224 x 3 RGB images',
    'Output: 6 disease classes with confidence scores',
    'Training: 3-stage progressive fine-tuning',
    'Quantization: Float16 for mobile deployment',
    'Size: 5.72 MB (TFLite)',
]
add_bullet_list(slide, Inches(0.8), Inches(2.1), Inches(5), Inches(3), model_info,
                font_size=15, spacing=Pt(8))

# Right - Dataset
add_text_box(slide, Inches(7), Inches(1.6), Inches(5), Inches(0.4), 'TOM2024 Dataset (Onion Subset)',
             font_size=20, bold=True, color=DARK_GREEN)

# Dataset table
table_data = [
    ('Class', 'Type', 'Images'),
    ('Caterpillar', 'Pest', '879'),
    ('Fusarium', 'Disease', '738'),
    ('Healthy', 'Healthy', '679'),
    ('Alternaria', 'Disease', '515'),
    ('Virosis', 'Disease', '203'),
    ('Bulb Blight', 'Disease', '30'),
]
table_shape = slide.shapes.add_table(len(table_data), 3, Inches(7), Inches(2.1), Inches(5), Inches(2.8))
table = table_shape.table
for row_idx, row_data in enumerate(table_data):
    for col_idx, cell_text in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = cell_text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(13)
            paragraph.font.name = 'Calibri'
            if row_idx == 0:
                paragraph.font.bold = True
                paragraph.font.color.rgb = WHITE
        if row_idx == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = GREEN

# Training phases at bottom
add_shape_bg(slide, Inches(0.5), Inches(5.3), Inches(12.3), Inches(1.5), LIGHT_GREEN_BG)
add_text_box(slide, Inches(0.8), Inches(5.4), Inches(12), Inches(0.4), '3-Stage Progressive Fine-Tuning',
             font_size=18, bold=True, color=DARK_GREEN)

phases = ['Phase 1: Classifier head only (20 epochs, lr=1e-3)',
          'Phase 2: Unfreeze 30% backbone (25 epochs, lr=1e-4)',
          'Phase 3: Full fine-tuning (15 epochs, lr=1e-5)']
for i, phase in enumerate(phases):
    add_text_box(slide, Inches(0.8) + Inches(i * 4.1), Inches(5.9), Inches(3.8), Inches(0.5),
                 phase, font_size=13, color=DARK)


# ============================================================
# SLIDE 5: MODEL RESULTS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Model Performance', 'Evaluation on held-out test set (304 images)')

# Big accuracy number
add_shape_bg(slide, Inches(0.5), Inches(1.6), Inches(3.5), Inches(2.5), LIGHT_GREEN_BG)
add_text_box(slide, Inches(0.7), Inches(1.8), Inches(3), Inches(1), '93.75%',
             font_size=56, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.7), Inches(2.9), Inches(3), Inches(0.5), 'Overall Test Accuracy',
             font_size=18, color=DARK, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.7), Inches(3.4), Inches(3), Inches(0.4), 'TFLite: 93.75%  |  Size: 5.72 MB',
             font_size=13, color=GRAY, alignment=PP_ALIGN.CENTER)

# Classification report table
add_text_box(slide, Inches(4.5), Inches(1.5), Inches(5), Inches(0.4), 'Classification Report',
             font_size=18, bold=True, color=DARK_GREEN)

cr_data = [
    ('Class', 'Precision', 'Recall', 'F1-Score', 'Accuracy'),
    ('Alternaria', '0.766', '0.878', '0.818', '87.80%'),
    ('Bulb Blight', '1.000', '1.000', '1.000', '100.00%'),
    ('Caterpillar', '1.000', '0.987', '0.994', '98.73%'),
    ('Fusarium', '0.958', '0.840', '0.895', '83.95%'),
    ('Healthy', '0.945', '1.000', '0.972', '100.00%'),
    ('Virosis', '0.970', '1.000', '0.985', '100.00%'),
    ('Macro Avg', '0.940', '0.951', '0.944', ''),
]
table_shape = slide.shapes.add_table(len(cr_data), 5, Inches(4.5), Inches(2.0), Inches(8), Inches(3.2))
table = table_shape.table
for row_idx, row_data in enumerate(cr_data):
    for col_idx, cell_text in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = cell_text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(12)
            paragraph.font.name = 'Calibri'
            if row_idx == 0:
                paragraph.font.bold = True
                paragraph.font.color.rgb = WHITE
            if row_idx == len(cr_data) - 1:
                paragraph.font.bold = True
        if row_idx == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = GREEN

# Key insights
add_text_box(slide, Inches(0.5), Inches(4.5), Inches(12), Inches(0.4), 'Key Insights',
             font_size=18, bold=True, color=DARK_GREEN)
insights = [
    'Caterpillar, Healthy, Virosis & Bulb Blight achieve 98-100% accuracy',
    'Fusarium (83.95%) shows lowest accuracy due to visual similarity with Alternaria',
    'Class weights handle imbalance effectively (879 Caterpillar vs 30 Bulb Blight)',
    'TFLite quantization maintains full accuracy with 5.72 MB model size',
]
add_bullet_list(slide, Inches(0.5), Inches(5.0), Inches(12), Inches(2), insights,
                font_size=14, spacing=Pt(6))


# ============================================================
# SLIDE 6: APP SCREENSHOTS (1 of 2)
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Mobile Application (1/2)', 'Home  |  Freshness  |  AI Analysis  |  Disease Detection')

screenshots_1 = [
    ('onionguard_1.png', 'Home Screen'),
    ('onionguard_2.png', 'Freshness Check'),
    ('onionguard_3.png', 'AI Analysis'),
    ('onionguard_4.png', 'Disease Detection'),
]
x_pos = Inches(0.3)
for fname, label in screenshots_1:
    path = os.path.join(SCREENSHOT_DIR, fname)
    if os.path.exists(path):
        slide.shapes.add_picture(path, x_pos, Inches(1.5), Inches(2.8), Inches(5.3))
        add_text_box(slide, x_pos, Inches(6.85), Inches(2.8), Inches(0.4), label,
                     font_size=13, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)
        x_pos += Inches(3.2)

# ============================================================
# SLIDE 7: APP SCREENSHOTS (2 of 2)
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Mobile Application (2/2)', 'Analytics  |  Settings  |  Login')

screenshots_2 = [
    ('onionguard_5.png', 'Farm Analytics'),
    ('onionguard_6.png', 'Settings'),
    ('onionguard_7.png', 'Secure Login'),
]
x_pos = Inches(1.7)
for fname, label in screenshots_2:
    path = os.path.join(SCREENSHOT_DIR, fname)
    if os.path.exists(path):
        slide.shapes.add_picture(path, x_pos, Inches(1.5), Inches(2.8), Inches(5.3))
        add_text_box(slide, x_pos, Inches(6.85), Inches(2.8), Inches(0.4), label,
                     font_size=13, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)
        x_pos += Inches(3.2)


# ============================================================
# SLIDE 7: ARCHITECTURE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'System Architecture', 'Microservices deployed on AWS EC2')

# Architecture boxes
components = [
    ('Flutter App', Inches(5.2), Inches(1.6), Inches(3), Inches(0.7), RGBColor(227, 242, 253), ACCENT_BLUE),
    ('Nginx + SSL', Inches(5.2), Inches(2.6), Inches(3), Inches(0.7), RGBColor(255, 243, 224), ACCENT_ORANGE),
    ('API Gateway :8000', Inches(5.2), Inches(3.6), Inches(3), Inches(0.7), LIGHT_GREEN_BG, DARK_GREEN),
]
for text, x, y, w, h, bg, fg in components:
    add_shape_bg(slide, x, y, w, h, bg)
    add_text_box(slide, x, y + Inches(0.1), w, h, text, font_size=16, bold=True, color=fg, alignment=PP_ALIGN.CENTER)

# Arrow connectors (simple shapes)
for y_pos in [Inches(2.35), Inches(3.35)]:
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.4), y_pos, Inches(0.5), Inches(0.25))
    shape.fill.solid()
    shape.fill.fore_color.rgb = GREEN
    shape.line.fill.background()

# Services row
services = [
    ('Auth\n:8001', Inches(1.5)),
    ('Diagnosis\n:8002', Inches(4)),
    ('Treatment\n:8003', Inches(6.5)),
    ('Analytics\n:8004', Inches(9)),
]
for text, x in services:
    add_shape_bg(slide, x, Inches(4.8), Inches(2.2), Inches(0.9), LIGHT_GREEN_BG)
    add_text_box(slide, x, Inches(4.8), Inches(2.2), Inches(0.9), text,
                 font_size=14, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)

# Arrow down to DB
shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.4), Inches(5.75), Inches(0.5), Inches(0.25))
shape.fill.solid()
shape.fill.fore_color.rgb = GREEN
shape.line.fill.background()

# MongoDB
add_shape_bg(slide, Inches(3.5), Inches(6.1), Inches(6.3), Inches(0.8), RGBColor(232, 245, 233))
add_text_box(slide, Inches(3.5), Inches(6.2), Inches(6.3), Inches(0.6), 'MongoDB Atlas (Cloud Database)',
             font_size=16, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)


# ============================================================
# SLIDE 8: DEPLOYMENT & SECURITY
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Deployment & Security', 'AWS EC2 + Docker + HTTPS')

# Left - Deployment
add_shape_bg(slide, Inches(0.5), Inches(1.6), Inches(5.8), Inches(5.2), RGBColor(227, 242, 253))
add_text_box(slide, Inches(0.8), Inches(1.8), Inches(5), Inches(0.4), 'Infrastructure',
             font_size=22, bold=True, color=ACCENT_BLUE)
deploy_items = [
    'AWS EC2 instance hosting all services',
    'Docker + Docker Compose orchestration',
    '7 containers: Nginx, Certbot, Gateway, Auth, Diagnosis, Treatment, Analytics',
    'Backend ports internal only (not exposed)',
    'Nginx handles ports 80 & 443',
    'Auto-restart policies for reliability',
]
add_bullet_list(slide, Inches(0.8), Inches(2.4), Inches(5.2), Inches(4), deploy_items,
                font_size=15, spacing=Pt(10))

# Right - Security
add_shape_bg(slide, Inches(7), Inches(1.6), Inches(5.8), Inches(5.2), RGBColor(232, 245, 233))
add_text_box(slide, Inches(7.3), Inches(1.8), Inches(5), Inches(0.4), 'HTTPS & Security',
             font_size=22, bold=True, color=DARK_GREEN)
security_items = [
    'DuckDNS: onion-guard.duckdns.org domain',
    'Let\'s Encrypt SSL (auto-renewed every 12h)',
    'TLS 1.2/1.3 with strong cipher suites',
    'HTTP auto-redirects to HTTPS',
    'JWT + Bcrypt authentication',
    'Biometric login (fingerprint/face)',
    'Cleartext traffic blocked in Android manifest',
]
add_bullet_list(slide, Inches(7.3), Inches(2.4), Inches(5.2), Inches(4), security_items,
                font_size=15, spacing=Pt(8), color=DARK)


# ============================================================
# SLIDE 9: USER ROLES
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'User Roles', 'Three distinct roles with tailored dashboards')

roles = [
    ('Farmer', 'The primary user', [
        'Scan crops for diseases (camera/gallery)',
        'Check onion freshness with AI',
        'View personal scan history',
        'Track farm analytics & trends',
    ], RGBColor(232, 245, 233), DARK_GREEN),
    ('Extension Officer', 'Monitors communities', [
        'Same scanning capabilities',
        'View ALL farmer scans platform-wide',
        'Regional disease statistics',
        'Identify outbreak patterns',
    ], RGBColor(227, 242, 253), ACCENT_BLUE),
    ('Admin', 'Platform management', [
        'User management (activate/deactivate)',
        'Filter users by type',
        'Platform-wide analytics',
        'System health monitoring',
    ], RGBColor(243, 229, 245), RGBColor(106, 27, 154)),
]

for i, (title, subtitle, features, bg, fg) in enumerate(roles):
    x = Inches(0.5) + Inches(i * 4.2)
    add_shape_bg(slide, x, Inches(1.6), Inches(3.9), Inches(5.2), bg)
    add_text_box(slide, x + Inches(0.3), Inches(1.8), Inches(3.3), Inches(0.5), title,
                 font_size=24, bold=True, color=fg)
    add_text_box(slide, x + Inches(0.3), Inches(2.4), Inches(3.3), Inches(0.3), subtitle,
                 font_size=14, color=GRAY)
    # Divider
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.3), Inches(2.9), Inches(2), Pt(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fg
    shape.line.fill.background()
    add_bullet_list(slide, x + Inches(0.3), Inches(3.2), Inches(3.3), Inches(3.5), features,
                    font_size=14, spacing=Pt(10))


# ============================================================
# SLIDE 10: MULTI-LANGUAGE & VOICE
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Multi-Language & Voice Support', 'Accessible to low-literacy farmers')

languages = [
    ('English', 'Default'),
    ('Twi', 'Ashanti Region'),
    ('Dagbani', 'Northern Ghana'),
    ('Ewe', 'Volta Region'),
    ('Hausa', 'West Africa'),
]

add_text_box(slide, Inches(0.8), Inches(1.6), Inches(5), Inches(0.4), '5 Supported Languages',
             font_size=22, bold=True, color=DARK_GREEN)

table_shape = slide.shapes.add_table(6, 2, Inches(0.8), Inches(2.2), Inches(5), Inches(2.5))
table = table_shape.table
table.cell(0, 0).text = 'Language'
table.cell(0, 1).text = 'Region'
for p in table.cell(0, 0).text_frame.paragraphs:
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.size = Pt(14)
for p in table.cell(0, 1).text_frame.paragraphs:
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.size = Pt(14)
table.cell(0, 0).fill.solid()
table.cell(0, 0).fill.fore_color.rgb = GREEN
table.cell(0, 1).fill.solid()
table.cell(0, 1).fill.fore_color.rgb = GREEN
for i, (lang, region) in enumerate(languages):
    table.cell(i+1, 0).text = lang
    table.cell(i+1, 1).text = region
    for col in range(2):
        for p in table.cell(i+1, col).text_frame.paragraphs:
            p.font.size = Pt(13)

# Right side - voice features
add_text_box(slide, Inches(7), Inches(1.6), Inches(5), Inches(0.4), 'Voice & Accessibility',
             font_size=22, bold=True, color=DARK_GREEN)
voice_features = [
    '240+ translated UI strings across all languages',
    'Google TTS voice playback for treatment guides',
    'Audio treatment instructions in all 5 languages',
    'Language preference persists per user',
    'Designed for farmers with limited literacy',
    'OpenRouter LLM for dynamic content translation',
]
add_bullet_list(slide, Inches(7), Inches(2.2), Inches(5.5), Inches(3.5), voice_features,
                font_size=16, spacing=Pt(12))


# ============================================================
# SLIDE 11: TECH STACK
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Technology Stack', 'Full-stack modern architecture')

stack_left = [
    ('Frontend', 'Flutter / Dart'),
    ('Backend', 'FastAPI / Python 3.11'),
    ('Database', 'MongoDB Atlas'),
    ('ML Model', 'TensorFlow Lite'),
    ('Vision AI', 'Google Gemini 2.5 Flash'),
    ('Voice', 'Google TTS (gTTS)'),
    ('State Mgmt', 'Provider'),
]
stack_right = [
    ('Charts', 'fl_chart'),
    ('Auth', 'JWT + Bcrypt'),
    ('Biometrics', 'local_auth'),
    ('Containers', 'Docker + Compose'),
    ('Proxy', 'Nginx'),
    ('SSL', 'Let\'s Encrypt + Certbot'),
    ('DNS', 'DuckDNS'),
]

for col_idx, stack in enumerate([stack_left, stack_right]):
    x_base = Inches(0.5) + Inches(col_idx * 6.5)
    for i, (layer, tech) in enumerate(stack):
        y = Inches(1.6) + Inches(i * 0.75)
        bg = LIGHT_GREEN_BG if i % 2 == 0 else RGBColor(227, 242, 253)
        add_shape_bg(slide, x_base, y, Inches(5.8), Inches(0.65), bg)
        add_text_box(slide, x_base + Inches(0.2), y + Inches(0.1), Inches(2.2), Inches(0.5),
                     layer, font_size=15, bold=True, color=DARK_GREEN)
        add_text_box(slide, x_base + Inches(2.5), y + Inches(0.1), Inches(3), Inches(0.5),
                     tech, font_size=15, color=DARK)


# ============================================================
# SLIDE 12: FEATURES DISCUSSED
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Features Discussed', 'Future development and improvements')

features_left = [
    ('Fingerprint Auth', 'Biometric login using fingerprint\nand face recognition'),
    ('LLM Disease Analysis', 'AI-generated contextual advice\nwhen a disease is detected'),
    ('Farmers to Customers', 'Marketplace connecting farmers\ndirectly to buyers'),
    ('Freshness to Customer', 'Share freshness results as\nproof of quality for buyers'),
]
features_right = [
    ('Simplify Admin UI', 'Remove/restructure admin role\nfrom the main app flow'),
    ('Enhanced Analytics', 'Richer charts, trends over time,\ncomparative & actionable data'),
    ('Voice for All Text', 'Read all app content in local\nlanguages for accessibility'),
]

for i, (title, desc) in enumerate(features_left):
    y = Inches(1.6) + Inches(i * 1.35)
    add_shape_bg(slide, Inches(0.5), y, Inches(5.8), Inches(1.2), LIGHT_GREEN_BG if i % 2 == 0 else RGBColor(227, 242, 253))
    add_text_box(slide, Inches(0.8), y + Inches(0.1), Inches(5), Inches(0.4), title,
                 font_size=17, bold=True, color=DARK_GREEN)
    add_text_box(slide, Inches(0.8), y + Inches(0.55), Inches(5), Inches(0.6), desc,
                 font_size=13, color=GRAY)

for i, (title, desc) in enumerate(features_right):
    y = Inches(1.6) + Inches(i * 1.35)
    add_shape_bg(slide, Inches(7), y, Inches(5.8), Inches(1.2), RGBColor(255, 243, 224) if i % 2 == 0 else RGBColor(243, 229, 245))
    add_text_box(slide, Inches(7.3), y + Inches(0.1), Inches(5), Inches(0.4), title,
                 font_size=17, bold=True, color=ACCENT_ORANGE if i % 2 == 0 else RGBColor(106, 27, 154))
    add_text_box(slide, Inches(7.3), y + Inches(0.55), Inches(5), Inches(0.6), desc,
                 font_size=13, color=GRAY)

# Needed section
add_shape_bg(slide, Inches(7), Inches(5.65), Inches(5.8), Inches(1.2), RGBColor(255, 235, 238))
add_text_box(slide, Inches(7.3), Inches(5.75), Inches(5), Inches(0.4), 'Needed',
             font_size=17, bold=True, color=ACCENT_RED)
add_text_box(slide, Inches(7.3), Inches(6.2), Inches(5), Inches(0.5),
             'API keys for additional services\nApple Developer account for iOS deployment',
             font_size=13, color=DARK)


# ============================================================
# SLIDE 13: GOOGLE PLAY STATUS
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
slide_header(slide, 'Google Play Store Status', 'Currently in closed testing')

# Status card
add_shape_bg(slide, Inches(2), Inches(2), Inches(9.3), Inches(4), LIGHT_GREEN_BG)

add_text_box(slide, Inches(2.5), Inches(2.3), Inches(8), Inches(0.6), 'Closed Testing',
             font_size=36, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)

# Divider
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5), Inches(3.1), Inches(3.3), Pt(2))
shape.fill.solid()
shape.fill.fore_color.rgb = GREEN
shape.line.fill.background()

status_items = [
    'App bundle uploaded and under review',
    'Minimum 12 testers required to opt-in',
    '14-day closed testing period before production access',
    'Production release pending successful testing phase',
]
add_bullet_list(slide, Inches(3.5), Inches(3.5), Inches(6.3), Inches(2.5), status_items,
                font_size=18, spacing=Pt(14), color=DARK)


# ============================================================
# SLIDE 14: THANK YOU
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_GREEN)
add_shape_bg(slide, Inches(0), Inches(0), prs.slide_width, prs.slide_height, RGBColor(38, 120, 45))

if os.path.exists(ONION_IMG):
    slide.shapes.add_picture(ONION_IMG, Inches(5.2), Inches(0.5), Inches(3), Inches(2))

add_text_box(slide, Inches(1), Inches(2), Inches(11), Inches(1), 'Thank You',
             font_size=54, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5), Inches(3.2), Inches(3.3), Pt(3))
shape.fill.solid()
shape.fill.fore_color.rgb = WHITE
shape.line.fill.background()

add_text_box(slide, Inches(1), Inches(3.6), Inches(11), Inches(0.5), 'Nkabom Honours Team',
             font_size=24, color=RGBColor(200, 255, 200), alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(4.2), Inches(11), Inches(0.5), 'University of Ghana  |  2026',
             font_size=18, color=RGBColor(180, 230, 180), alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1), Inches(5.2), Inches(11), Inches(0.8),
             'OnionGuard  |  AI-Powered Onion Disease Detection\nhttps://onion-guard.duckdns.org',
             font_size=16, color=RGBColor(160, 220, 160), alignment=PP_ALIGN.CENTER)


# SAVE
output_path = 'C:/Users/12345/Desktop/Projects/OnionGuard/OnionGuard-Presentation.pptx'
prs.save(output_path)
print(f'Done! Saved to {output_path}')
