"""
control_panel.py - Configuration options and action panel for BookletsGo.
Provides the UI controls for page numbering toggles and triggers the 
final booklet generation workflow.
"""

import customtkinter as ctk
from ..styles import Styles

class ControlPanel(ctk.CTkFrame):
    def __init__(self, parent, on_generate_callback):
        """
        Initializes the control panel.
        :param parent: The parent tkinter/customtkinter container.
        :param on_generate_callback: Callable function triggered when 'Generate' is clicked.
        """
        super().__init__(parent, fg_color=Styles.BG_PANEL, corner_radius=Styles.CORNER_RADIUS)
        
        self.on_generate = on_generate_callback

        # Layout configuration
        self.grid_rowconfigure(0, weight=0)  # Section Header
        self.grid_rowconfigure(1, weight=1)  # Options Box (stretches to push button down)
        self.grid_rowconfigure(2, weight=0)  # Action Button
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_options()
        self._build_action_button()

    def _build_header(self):
        """Renders the panel title block."""
        title_lbl = ctk.CTkLabel(
            self, 
            text="Configuration", 
            font=Styles.FONT_HEADER, 
            text_color=Styles.TEXT_MAIN,
            anchor="w"
        )
        title_lbl.grid(row=0, column=0, sticky="ew", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)

    def _build_options(self):
        """Renders the available layout adjustments and toggles."""
        options_container = ctk.CTkFrame(self, fg_color="transparent")
        options_container.grid(row=1, column=0, sticky="nsew", padx=Styles.PADDING_MD, pady=(0, Styles.PADDING_MD))
        options_container.grid_columnconfigure(0, weight=1)

        # CustomTkinter Boolean variable to track checkbox state
        self.numbering_var = ctk.BooleanVar(value=False)

        # Elegant, modern checkbox for page numbering
        self.numbering_chk = ctk.CTkCheckBox(
            options_container,
            text="Enable Page Numbering",
            font=Styles.FONT_BODY,
            variable=self.numbering_var,
            border_color=Styles.TEXT_MUTED,
            fg_color=Styles.ACCENT,
            hover_color=Styles.ACCENT_HOVER,
            corner_radius=4  # Slightly sharper corners for the checkbox matrix
        )
        self.numbering_chk.grid(row=0, column=0, sticky="w", pady=Styles.PADDING_SM)

        # Helpful micro-copy under the checkbox to guide the user
        hint_lbl = ctk.CTkLabel(
            options_container,
            text="Adds dynamic page numbers to the bottom center of each booklet page.",
            font=Styles.FONT_CAPTION,
            text_color=Styles.TEXT_MUTED,
            wraplength=180,  # Ensure it wraps cleanly inside the narrow panel
            justify="left"
        )
        hint_lbl.grid(row=1, column=0, sticky="w", padx=(24, 0))

    def _build_action_button(self):
        """Creates the primary call-to-action button anchored to the bottom."""
        self.generate_btn = ctk.CTkButton(
            self,
            text="Generate Booklet",
            font=Styles.FONT_HEADER,
            fg_color=Styles.ACCENT,
            hover_color=Styles.ACCENT_HOVER,
            height=45,  # Taller, more touch/click-friendly professional button
            corner_radius=Styles.CORNER_RADIUS,
            command=self._on_generate_click
        )
        self.generate_btn.grid(row=2, column=0, sticky="ew", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)

    def _on_generate_click(self):
        """Internal event handler that collects options and fires the callback."""
        options = {
            "numbering": self.numbering_var.get()
        }
        if self.on_generate:
            self.on_generate(options)