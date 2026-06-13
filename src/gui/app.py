"""
app.py - Main GUI Window Class for BookletsGo.
Manages application state, window initialization, layout structure,
and coordinates the end-to-end PDF processing pipeline.
"""

import os
import tempfile
from tkinter import filedialog, messagebox  # Native desktop dialogs for optimal UX

import customtkinter as ctk

from .components.control_panel import ControlPanel
from .components.file_list import FileListPanel
from .styles import Styles
from .utils import resource_path


class BookletsGoApp(ctk.CTk):
    def _center_window(self, width: int, height: int):
        """Centers the window on the screen at startup."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def __init__(self):
        super().__init__()

        # Window Metadata & Constraints
        self.title("BookletsGo")
        self.geometry("900x650")
        self._center_window(900, 650)
        self.minsize(850, 550)
        # self.iconbitmap(resource_path("assets", "bookletsgo.ico")) # Only Windows

        # Enforce modern appearance defaults
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=Styles.BG_MAIN)

        # Layout Architecture (Top Header, Center Workspace, Optional Footer)
        self.grid_rowconfigure(0, weight=0, pad=Styles.PADDING_LG)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Build UI Sections
        self._build_header()
        self._build_workspace()

    def _build_header(self):
        """Creates the top typography block with title and project description."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=Styles.PADDING_LG,
            pady=(Styles.PADDING_SM, 0),
        )
        header_frame.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="BookletsGo",
            font=Styles.FONT_TITLE,
            text_color=Styles.TEXT_MAIN,
            justify="left",
            anchor="w",
        )
        title_lbl.grid(row=0, column=0, sticky="w")

        subtitle_lbl = ctk.CTkLabel(
            header_frame,
            text="Simple Booklet Maker and Imposition Utility\nCreated by Krisztián Szalay",
            font=Styles.FONT_CAPTION,
            text_color=Styles.TEXT_MUTED,
            justify="left",
            anchor="w",
        )
        subtitle_lbl.grid(row=1, column=0, sticky="w", pady=(2, 0))

    def _build_workspace(self):
        """Creates a modern two-column layout split between File List and Control options."""
        workspace_frame = ctk.CTkFrame(self, fg_color="transparent")
        workspace_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=Styles.PADDING_LG,
            pady=(Styles.PADDING_SM, Styles.PADDING_LG),
        )

        # 3:1 column ratio between the file queue and the sidebar controls
        workspace_frame.grid_columnconfigure(0, weight=3)
        workspace_frame.grid_columnconfigure(1, weight=1)
        workspace_frame.grid_rowconfigure(0, weight=1)

        # Left Column: File List Panel (Handles the queue visual sequencing)
        self.file_list_panel = FileListPanel(workspace_frame)
        self.file_list_panel.grid(
            row=0, column=0, sticky="nsew", padx=(0, Styles.PADDING_MD)
        )

        # Right Column: Operational Control Panel (Bridges triggers back via callback)
        self.control_panel = ControlPanel(
            workspace_frame, on_generate_callback=self._on_generate_booklet
        )
        self.control_panel.grid(row=0, column=1, sticky="nsew")

    def _on_generate_booklet(self, options):
        """
        Bridge execution method triggered by the control panel.
        Collects queued source paths, requests target output destination,
        and orchestrates the multi-stage conversion and imposition pipeline.
        """
        ordered_files = self.file_list_panel.get_ordered_files()

        # Guard Clause: Prevent execution if the file list workspace is empty
        if not ordered_files:
            messagebox.showwarning(
                "No Source Files",
                "Please add at least one document to the queue before generating a booklet.",
            )
            return

        # 1. Capture save target from the user.
        # Defaults to the first source file's directory to provide a smart UX assumption.
        default_directory = os.path.dirname(ordered_files[0])
        final_output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Booklet As...",
            initialdir=default_directory,
            initialfile="printable_booklet.pdf",
        )

        # Guard Clause: Abort gracefully if the user cancels or closes the dialog window
        if not final_output_path:
            return

        print("\n--- [Triggering Imposition Workflow] ---")

        # Deferred core engine imports to maintain decoupled startup memory weights
        from core.converter import FileConverter
        from core.imposition import BookletImposer

        converter = FileConverter()
        imposer = BookletImposer()

        # Initialize a named temporary file to receive normalized asset streams.
        # This keeps intermediate raw calculations off the user's permanent workspace.
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_raw:
            raw_sequence_path = tmp_raw.name

        try:
            # Pipeline Step 1: Normalize independent heterogeneous documents into standard A5 sheets
            print(
                "Step 1: Normalizing individual documents into a clean uniform template..."
            )
            converter.convert_to_raw_pdf(ordered_files, raw_sequence_path)

            # Pipeline Step 2: Handle layout signature distribution, cell matrix padding, and pagination overlays
            print("Step 2: Processing layout imposition matrix & pagination rules...")
            imposer.impose_to_a5_booklet(
                raw_pdf_path=raw_sequence_path,
                final_pdf_path=final_output_path,
                enable_numbering=options.get("numbering", False),
            )

            # Console Logging Diagnostics
            print("\nSuccess! Output booklet is ready for printing.")
            print(f"Destination Path: {final_output_path}")
            print("----------------------------------------\n")

            # User-Facing UI Notification
            messagebox.showinfo(
                "Success!",
                f"Your printable booklet has been successfully generated and saved to:\n\n{final_output_path}",
            )

        except Exception as e:
            # Consolidated exception handler to catch underlying file I/O or PDF stream syntax issues
            error_msg = (
                f"An error occurred during the booklet imposition pipeline:\n{str(e)}"
            )
            print(f"[Core Engine Error] {error_msg}")
            messagebox.showerror("Imposition Failure", error_msg)

        finally:
            # Enforce clean disk footprint policies by removing the temporary raw stream file
            if os.path.exists(raw_sequence_path):
                try:
                    os.remove(raw_sequence_path)
                except Exception as cleanup_error:
                    print(
                        f"[Cleanup Warning] Failed to delete temporary file: {str(cleanup_error)}"
                    )