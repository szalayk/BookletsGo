"""
file_list.py - File management list component for BookletsGo.
Handles file queuing, visual reordering (Up/Down), and item deletion 
using a modern, scrollable CustomTkinter interface.
"""

import os
import customtkinter as ctk
from tkinter import filedialog
from ..styles import Styles

class FileListPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_PANEL, corner_radius=Styles.CORNER_RADIUS)
        
        # Internal state: list of absolute file paths
        self.files = []

        # Configure Grid Layout
        self.grid_rowconfigure(0, weight=0) # Header & Add Button
        self.grid_rowconfigure(1, weight=1) # Scrollable List Area
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_scroll_area()

    def _build_header(self):
        """Creates the section title and the 'Add Files' action button."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=Styles.PADDING_MD, pady=Styles.PADDING_MD)
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame, 
            text="Source Documents", 
            font=Styles.FONT_HEADER, 
            text_color=Styles.TEXT_MAIN
        )
        title.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(
            header_frame,
            text="+ Add Files",
            font=Styles.FONT_BODY,
            fg_color=Styles.ACCENT,
            hover_color=Styles.ACCENT_HOVER,
            corner_radius=Styles.CORNER_RADIUS,
            command=self._on_add_files_click
        )
        add_btn.grid(row=0, column=1, sticky="e")

    def _build_scroll_area(self):
        """Initializes the modern scrollable container for file items."""
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            label_text=""
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=Styles.PADDING_MD, pady=(0, Styles.PADDING_MD))

    def _on_add_files_click(self):
        """Opens a native file dialog to select supported file formats."""
        file_types = [
            ("All Supported Formats", "*.pdf *.docx *.txt *.jpg *.jpeg *.tiff"),
            ("PDF Documents", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Text Files", "*.txt"),
            ("Images", "*.jpg *.jpeg *.tiff")
        ]
        
        selected_paths = filedialog.askopenfilenames(
            title="Select Files to Include in Booklet",
            filetypes=file_types
        )

        if selected_paths:
            for path in selected_paths:
                if path not in self.files:
                    self.files.append(path)
            self._refresh_list()

    def _refresh_list(self):
        """Clears the visual list and re-renders all items based on the current state."""
        # Destroy all existing child widgets in the scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Render each file row
        for index, filepath in enumerate(self.files):
            self._render_file_row(index, filepath)

    def _render_file_row(self, index, filepath):
        """Renders a single file entry with its action buttons."""
        filename = os.path.basename(filepath)
        
        # Alternating background colors for a subtle spreadsheet/list effect
        row_bg = Styles.BG_MAIN if index % 2 == 0 else "transparent"

        row_frame = ctk.CTkFrame(
            self.scroll_frame, 
            fg_color=row_bg, 
            corner_radius=Styles.CORNER_RADIUS
        )
        row_frame.pack(fill="x", pady=2, ipady=4)
        row_frame.grid_columnconfigure(0, weight=1)

        # File Name Label
        file_lbl = ctk.CTkLabel(
            row_frame, 
            text=f"  {index + 1}.  {filename}", 
            font=Styles.FONT_BODY,
            text_color=Styles.TEXT_MAIN,
            anchor="w"
        )
        file_lbl.grid(row=0, column=0, sticky="w", padx=Styles.PADDING_SM)

        # Button Group Container
        btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e", padx=Styles.PADDING_SM)

        # Reorder Up Button (▲)
        up_btn = ctk.CTkButton(
            btn_frame, text="▲", width=28, height=28, font=Styles.FONT_BODY,
            fg_color="transparent", text_color=Styles.TEXT_MUTED, hover_color=Styles.BG_PANEL,
            command=lambda i=index: self._move_item(i, -1)
        )
        up_btn.grid(row=0, column=0, padx=2)
        # Disable if it's already the top item
        if index == 0:
            up_btn.configure(state="disabled", text_color="#475569")

        # Reorder Down Button (▼)
        down_btn = ctk.CTkButton(
            btn_frame, text="▼", width=28, height=28, font=Styles.FONT_BODY,
            fg_color="transparent", text_color=Styles.TEXT_MUTED, hover_color=Styles.BG_PANEL,
            command=lambda i=index: self._move_item(i, 1)
        )
        down_btn.grid(row=0, column=1, padx=2)
        # Disable if it's already the bottom item
        if index == len(self.files) - 1:
            down_btn.configure(state="disabled", text_color="#475569")

        # Delete Button (✕)
        del_btn = ctk.CTkButton(
            btn_frame, text="✕", width=28, height=28, font=Styles.FONT_BODY,
            fg_color="transparent", text_color=Styles.COLOR_DANGER, hover_color=Styles.COLOR_DANGER_HOVER,
            command=lambda i=index: self._delete_item(i)
        )
        del_btn.grid(row=0, column=2, padx=(6, 2))

    def _move_item(self, index, direction):
        """Swaps the item at the given index with its neighbor based on direction (-1 or 1)."""
        target_index = index + direction
        if 0 <= target_index < len(self.files):
            self.files[index], self.files[target_index] = self.files[target_index], self.files[index]
            self._refresh_list()

    def _delete_item(self, index):
        """Removes a file from the internal tracking array and updates the view."""
        if 0 <= index < len(self.files):
            self.files.pop(index)
            self._refresh_list()

    def get_ordered_files(self):
        """Public API method to fetch the final sorted list of absolute file paths."""
        return self.files