"""
styles.py - Centralized design system for BookletsGo.
Defines the color palette, typography hierarchy, and UI geometry 
to maintain a modern, clean, and minimalist aesthetic.
"""

class Styles:
    # ---------------------------------------------------------
    # Color Palette (Modern Slate / Dark Minimalist theme)
    # ---------------------------------------------------------
    # CustomTkinter widgets accept a tuple: (light_theme_color, dark_theme_color)
    # We explicitly optimize for a gorgeous dark mode experience.
    
    BG_MAIN = ("#f5f5f5", "#171717")       # Soft light gray / Deep slate blue
    BG_PANEL = ("#d4d4d4", "#262626")      # Card backgrounds
    
    # Brand & Interactive colors
    ACCENT = ("#57534e", "#3f6212")        # Primary action button
    ACCENT_HOVER = ("#78716c", "#4d7c0f")  # Primary action button for hover states
    
    # Functional colors
    COLOR_DANGER = ("#dc2626", "#991b1b")  # Red for delete/destructive actions
    COLOR_DANGER_HOVER = ("#ef4444", "#b91c1c")
    
    # Typography colors
    TEXT_MAIN = ("#262626", "#d4d4d4")     # High contrast primary text
    TEXT_MUTED = ("#525252", "#737373")    # Subtitles, labels, and placeholding
    
    # ---------------------------------------------------------
    # Typography (System-native clean sans-serif fonts)
    # ---------------------------------------------------------
    FONT_FAMILY = "Segoe UI"  # CustomTkinter automatically falls back to system fonts (Inter/Ubuntu)
    
    FONT_TITLE = (FONT_FAMILY, 22, "bold")
    FONT_HEADER = (FONT_FAMILY, 14, "bold")
    FONT_BODY = (FONT_FAMILY, 12, "normal")
    FONT_CAPTION = (FONT_FAMILY, 11, "normal")

    # ---------------------------------------------------------
    # Geometry & Layout padding
    # ---------------------------------------------------------
    PADDING_SM = 6
    PADDING_MD = 12
    PADDING_LG = 20
    
    CORNER_RADIUS = 5  # Smooth modern rounded corners for frames and buttons