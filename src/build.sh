#!/bin/bash

clear

echo "===================================================="
echo "             BookletsGo Build Automation            "
echo "===================================================="
echo ""

# 1. CHECK: Are we already in an active venv?
# ------------------------------------------------------
if [ -n "$VIRTUAL_ENV" ]; then
    echo "[INFO] An active virtual environment was detected."
    echo "       Path: $VIRTUAL_ENV"
    echo ""
    SHOULD_DEACTIVATE=0
else
    echo "[INFO] No active virtual environment detected. Attempting activation..."
    
    # Check if the venv folder and the activation file exist
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        SHOULD_DEACTIVATE=1
        echo "[SUCCESS] Virtual environment activated successfully."
        echo ""
    else
        echo "[ERROR] The file '.venv/bin/activate' was not found!"
        echo "        Make sure to run this script from the project root directory."
        echo ""
        echo "Press enter to exit..."
        read
        exit 1
    fi
fi


# 2. EXECUTION: Run PyInstaller
# ------------------------------------------------------
echo "[BUILD] Launching PyInstaller compilation for Linux..."
echo ""

# Note: On Linux, PyInstaller does not support the --icon option for embedding in the binary, so we will specify it with the system-wide .desktop file.
pyinstaller --noconsole --onedir --collect-all customtkinter --add-data "assets/Inter-Regular.ttf:assets" --name BookletsGo run.py

# Check if PyInstaller ran successfully (returned with error code 0)
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] PyInstaller encountered an error during compilation!"
    echo "Press enter to exit..."
    read
    exit 1
fi

echo ""
echo "[SUCCESS] Compilation completed successfully. Target: dist/BookletsGo/"
echo ""


# 3. EXIT: Venv deactivate (only if we entered)
# ------------------------------------------------------
if [ "$SHOULD_DEACTIVATE" -eq 1 ]; then
    echo "[INFO] Deactivating the temporary virtual environment session..."
    deactivate
fi

echo ""
echo "===================================================="
echo "   Done! You can close this window."
echo "===================================================="
echo "Press enter to exit..."
read
 Ester