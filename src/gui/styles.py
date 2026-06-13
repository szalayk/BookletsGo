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

    BG_MAIN = ("#d6d3d1", "#171717")
    BG_PANEL = ("#e7e5e4", "#262626")

    # Brand & Interactive colors
    ACCENT = ("#57534e", "#b91c1c")
    ACCENT_HOVER = ("#78716c", "#dc2626")

    # Functional colors
    COLOR_DANGER = ("#dc2626", "#fca5a5")
    COLOR_DANGER_HOVER = ("#ef4444", "#b91c1c")

    # Typography colors
    TEXT_MAIN = ("#262626", "#f5f5f5")
    TEXT_MUTED = ("#525252", "#a3a3a3")

    # ---------------------------------------------------------
    # Typography (System-native clean sans-serif fonts)
    # ---------------------------------------------------------
    FONT_FAMILY = "Segoe UI"  # CustomTkinter automatically falls back to system fonts (Inter/Ubuntu)

    FONT_TITLE = (FONT_FAMILY, 32, "bold")
    FONT_HEADER = (FONT_FAMILY, 16, "bold")
    FONT_BODY = (FONT_FAMILY, 14, "normal")
    FONT_CAPTION = (FONT_FAMILY, 12, "normal")

    # ---------------------------------------------------------
    # Geometry & Layout padding
    # ---------------------------------------------------------
    PADDING_SM = 6
    PADDING_MD = 12
    PADDING_LG = 20

    CORNER_RADIUS = 5  # Smooth modern rounded corners for frames and buttons