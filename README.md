# BookletsGo
Simple Booklet Maker and Imposition Utility

**BookletsGo** is an intuitive, modular, and open-source desktop application designed to simplify and streamline the print preparation process. It automates the complex task of transforming independent source documents and assets into perfectly ordered, print-ready signatures (booklets). 

This utility is purpose-built for individuals and organizations who need to compile various multi-format files into a cohesive, professional printout without navigating steep learning curves or dealing with expensive, overly complicated desktop publishing software. By providing a clean graphical user interface (GUI), BookletsGo ensures that anyone can achieve precise print layouts in just a few clicks, while maintaining a robust, highly documented architecture under the hood.

---

## Key Features

- **Multi-Format Input Pipeline:** Ingests mixed source assets including `.pdf`, `.docx`, `.doc`, `.txt`, `.jpg`, and `.tiff`.
- **Visual Sequence Ordering:** Rearrange files sequentially within a modern graphical queue to define the definitive booklet flow.
- **Automated Page-Budget Tracking:** Dynamically evaluates and displays individual asset page counts upon loading.
- **Mathematical Page Padding:** Automatically computes signature shortfalls. If total source pages aren't a multiple of 4, the imposition engine inserts clean, structural blank pages at the trailing edge.
- **A5 Booklet:** Automatically maps pairs of A5 pages onto physical A4 landscape sheets with pristine structural ordering.
- **Dynamic Prepress Numbering:** Includes an optional, elegant slate-gray numbering overlay system that applies localized canvas pagination to the combined layout sheet without defacing core document structures.
- **Lossless Coordinate Normalization:** Uses external coordinate transformations to eliminate the infamous PDF `Content Clipping` anomalies caused by non-standard origin boxes (`/MediaBox` offsets).

---

## The 4-Page Signature Matrix

For every physical A4 sheet (which holds 4 booklet pages), pages are distributed between the Front Side and Back Side:

* **Sheet Front (Left half):** Last unmapped even slot counting down from the end.
* **Sheet Front (Right half):** First unmapped odd slot counting up from the start.
* **Sheet Back (Left half):** Next sequential odd slot counting up.
* **Sheet Back (Right half):** Next sequential even slot counting down.

---
