"""
converter.py - File normalization pipeline for BookletsGo.
Converts various incoming file formats (.docx, .txt, images, .pdf)
into a unified, sequential raw PDF where every page is strictly resized to A5.
"""

import os
import tempfile

from docx import Document
from PIL import Image as PILImage
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from gui.utils import resource_path


class FileConverter:
    def __init__(self):
        # A5 standard dimensions in points (419.53 x 595.27)
        self.target_width, self.target_height = A5
        self.styles = getSampleStyleSheet()

        font_path = resource_path("assets", "Inter-Regular.ttf")
        pdfmetrics.registerFont(TTFont("ProjectFont", font_path))

        # Define a clean typography style for converted text files
        self.custom_body_style = ParagraphStyle(
            "ConvertBody",
            parent=self.styles["Normal"],
            fontName="ProjectFont",
            fontSize=10,
            leading=14,
            spaceAfter=6,
        )

    def convert_to_raw_pdf(self, file_paths, output_path):
        """
        Processes a list of mixed file paths, normalizes them to A5 pages,
        and merges them into a single sequential PDF file.

        :param file_paths: List of absolute paths to source files.
        :param output_path: Destination path for the combined raw A5 PDF.
        :return: Total number of pages generated.
        """
        writer = PdfWriter()

        for path in file_paths:
            if not os.path.exists(path):
                continue

            ext = os.path.splitext(path)[1].lower()

            # Route file to its specialized structural converter
            if ext == ".pdf":
                self._process_pdf(path, writer)
            elif ext == ".docx":
                self._process_docx(path, writer)
            elif ext == ".txt":
                self._process_txt(path, writer)
            elif ext in [".jpg", ".jpeg", ".tiff"]:
                self._process_image(path, writer)

        # Write out the consolidated raw sequence
        with open(output_path, "wb") as f_out:
            writer.write(f_out)

        return len(writer.pages)

    def _process_pdf(self, path, master_writer):
        """Extracts pages from an existing PDF and scales/fits them onto an A5 canvas."""
        reader = PdfReader(path)
        for page in reader.pages:
            # Get current page dimensions
            current_width = float(page.mediabox.width)
            current_height = float(page.mediabox.height)

            # Calculate dynamic scaling factors to fit inside A5 boundaries safely
            scale_x = self.target_width / current_width
            scale_y = self.target_height / current_height
            scale_factor = min(scale_x, scale_y)

            # Apply uniform transformation matrix
            transform = Transformation().scale(scale_factor, scale_factor)

            # Center the scaled page onto the new A5 dimensions
            new_w = current_width * scale_factor
            new_h = current_height * scale_factor
            dx = (self.target_width - new_w) / 2
            dy = (self.target_height - new_h) / 2
            transform = transform.translate(dx, dy)

            # Create standard A5 blank template page
            blank_writer = PdfWriter()
            blank_writer.add_blank_page(
                width=self.target_width, height=self.target_height
            )
            target_page = blank_writer.pages[0]

            # FIX: Apply the transformation to the source page first,
            # then merge it into the clean A5 destination canvas.
            page.add_transformation(transform)
            target_page.merge_page(page)

            master_writer.add_page(target_page)

    def _process_docx(self, path, master_writer):
        """Reads a Word document paragraphs via python-docx and renders to a temporary A5 PDF."""
        doc = Document(path)
        story = []

        for p in doc.paragraphs:
            text = p.text.strip()
            if text:
                story.append(Paragraph(text, self.custom_body_style))
            else:
                story.append(Spacer(1, 10))  # Preserve empty paragraphs as small gaps

        self._render_story_to_writer(story, master_writer)

    def _process_txt(self, path, master_writer):
        """Reads a plain text file, handles basic lines, and builds an A5 PDF layout."""
        story = []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                text = line.strip()
                if text:
                    story.append(Paragraph(text, self.custom_body_style))
                else:
                    story.append(Spacer(1, 10))

        self._render_story_to_writer(story, master_writer)

    def _process_image(self, path, master_writer):
        """Scales images using Pillow and embeds them centered on a clean A5 page canvas."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Set tight standard margins (0.5 inch / 36 points)
            margin = 36
            max_w = self.target_width - (margin * 2)
            max_h = self.target_height - (margin * 2)

            img = PILImage.open(path)
            img_w, img_h = img.size

            # Calculate aspect ratio preserving downscaling bounds
            ratio = min(max_w / img_w, max_h / img_h)
            draw_w = img_w * ratio
            draw_h = img_h * ratio

            # Center coordinates on the canvas
            x = (self.target_width - draw_w) / 2
            y = (self.target_height - draw_h) / 2

            # Render via ReportLab Canvas API
            c = canvas.Canvas(tmp_path, pagesize=A5)
            c.drawImage(
                path, x, y, width=draw_w, height=draw_h, preserveAspectRatio=True
            )
            c.showPage()
            c.save()

            # Load back into the master timeline
            self._merge_temporary_pdf(tmp_path, master_writer)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _render_story_to_writer(self, story, master_writer):
        """Helper method to compile a ReportLab Flowable story onto A5 template and link to master."""
        if not story:
            # Fallback if the document was completely empty
            story.append(Paragraph(" ", self.custom_body_style))

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Safe 0.5-inch padding layout for text flows
            doc = SimpleDocTemplate(
                tmp_path,
                pagesize=A5,
                leftMargin=36,
                rightMargin=36,
                topMargin=36,
                bottomMargin=36,
            )
            doc.build(story)
            self._merge_temporary_pdf(tmp_path, master_writer)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _merge_temporary_pdf(self, temp_pdf_path, master_writer):
        """Appends all sequential pages from a sub-task PDF directly into the main document stack."""
        reader = PdfReader(temp_pdf_path)
        for page in reader.pages:
            master_writer.add_page(page)