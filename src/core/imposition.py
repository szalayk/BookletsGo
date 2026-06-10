"""
imposition.py - Core imposition (page layout) engine for BookletsGo.
Handles auto-padding to a multiple of 4, optional dynamic page numbering,
and pairs A5 pages onto landscape A4 sheets for professional booklet binding.
"""

import os
import tempfile
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

class BookletImposer:
    def __init__(self):
        # A5 standard dimensions
        self.a5_width, self.a5_height = A5
        # A4 Landscape dimensions (841.89 x 595.27 points)
        self.a4_width = self.a5_width * 2
        self.a4_height = self.a5_height

    def impose_to_a5_booklet(self, raw_pdf_path, final_pdf_path, enable_numbering=False):
        """
        Takes a sequential A5 PDF, applies padding, and rearranges pages
        onto landscape A4 sheets for professional booklet binding.
        Uses merge_transformed_page to prevent content clipping and layout anomalies.
        """
        reader = PdfReader(raw_pdf_path)
        original_count = len(reader.pages)
        
        if original_count == 0:
            return

        # Calculate padded total pages (must be a multiple of 4)
        remainder = original_count % 4
        padding_needed = (4 - remainder) if remainder != 0 else 0
        total_pages = original_count + padding_needed

        writer = PdfWriter()
        num_sheets = total_pages // 4
        
        # Track temporary files generated for A4 numbering layers
        temp_numbering_files = []

        for i in range(num_sheets):
            # ==========================================
            # --- FRONT SIDE OF SHEET ---
            # Left: Countdown from back | Right: Count forward from start
            lf_idx = total_pages - 1 - (2 * i)
            rf_idx = 2 * i

            # Create an independent, clean A4 canvas
            front_sheet = PageObject.create_blank_page(width=self.a4_width, height=self.a4_height)

            # Merge Left Front Page (Even page in booklet logic)
            if lf_idx < original_count:
                left_page = reader.pages[lf_idx]
                # Normalize lower-left corner to (0,0) of the left A5 block
                shift_left = Transformation().translate(
                    tx=-float(left_page.mediabox.left), 
                    ty=-float(left_page.mediabox.bottom)
                )
                front_sheet.merge_transformed_page(left_page, shift_left)

            # Merge Right Front Page (Odd page in booklet logic)
            if rf_idx < original_count:
                right_page = reader.pages[rf_idx]
                # Normalize lower-left corner and shift to the right half of the A4 sheet
                shift_right = Transformation().translate(
                    tx=self.a5_width - float(right_page.mediabox.left), 
                    ty=-float(right_page.mediabox.bottom)
                )
                front_sheet.merge_transformed_page(right_page, shift_right)

            # Apply Page Numbering Overlay to Front Sheet if requested
            if enable_numbering:
                stamp_path = self._create_a4_numbering_overlay(lf_idx, rf_idx, original_count)
                temp_numbering_files.append(stamp_path)
                stamp_reader = PdfReader(stamp_path)
                front_sheet.merge_page(stamp_reader.pages[0])

            writer.add_page(front_sheet)

            # ==========================================
            # --- BACK SIDE OF SHEET ---
            # Left: Next forward page | Right: Next backward page
            lb_idx = (2 * i) + 1
            rb_idx = total_pages - 2 - (2 * i)

            # Create an independent, clean A4 canvas
            back_sheet = PageObject.create_blank_page(width=self.a4_width, height=self.a4_height)

            # Merge Left Back Page
            if lb_idx < original_count:
                left_page = reader.pages[lb_idx]
                # Normalize lower-left corner to (0,0) of the left A5 block
                shift_left = Transformation().translate(
                    tx=-float(left_page.mediabox.left), 
                    ty=-float(left_page.mediabox.bottom)
                )
                back_sheet.merge_transformed_page(left_page, shift_left)

            # Merge Right Back Page
            if rb_idx < original_count:
                right_page = reader.pages[rb_idx]
                # Normalize lower-left corner and shift to the right half of the A4 sheet
                shift_right = Transformation().translate(
                    tx=self.a5_width - float(right_page.mediabox.left), 
                    ty=-float(right_page.mediabox.bottom)
                )
                back_sheet.merge_transformed_page(right_page, shift_right)

            # Apply Page Numbering Overlay to Back Sheet if requested
            if enable_numbering:
                stamp_path = self._create_a4_numbering_overlay(lb_idx, rb_idx, original_count)
                temp_numbering_files.append(stamp_path)
                stamp_reader = PdfReader(stamp_path)
                back_sheet.merge_page(stamp_reader.pages[0])

            writer.add_page(back_sheet)

        # 4. Save the structurally flawless PDF file
        with open(final_pdf_path, "wb") as f_out:
            writer.write(f_out)

        # 5. Safe cleanup of temporary numbering overlay files
        for path in temp_numbering_files:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

    def _create_a4_numbering_overlay(self, left_idx, right_idx, original_count):
        """Generates a transient landscape A4 PDF layer containing the required page numbers."""
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp_path = tmp.name
        tmp.close()

        c = canvas.Canvas(tmp_path, pagesize=(self.a4_width, self.a4_height))
        c.setFont("Helvetica", 9)
        c.setFillColor("#64748B")  # Elegant slate gray

        # Stamp Left Zone Center (X: center of the left A5 block)
        if left_idx < original_count:
            c.drawCentredString(self.a5_width / 2, 20, str(left_idx + 1))

        # Stamp Right Zone Center (X: A5 width + center of the right A5 block)
        if right_idx < original_count:
            c.drawCentredString(self.a5_width + (self.a5_width / 2), 20, str(right_idx + 1))

        c.showPage()
        c.save()
        return tmp_path