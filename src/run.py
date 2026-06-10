#!/usr/bin/env python3
"""
run.py - Main entry point to launch the BookletsGo application.
"""

import sys
import os

# Append 'src' directory to python path to handle local imports smoothly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gui.app import BookletsGoApp

if __name__ == "__main__":
    # Initialize and run the application main loop
    app = BookletsGoApp()
    app.mainloop()