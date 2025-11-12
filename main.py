#!/usr/bin/env python3
"""
WebsiteNow - Multi-Agent AI Website Builder (Desktop Version)
A standalone desktop application for generating professional websites using AI
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from src.ui.main_window import MainWindow

def main():
    """Main entry point for the application"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("WebsiteNow")
    app.setOrganizationName("WebsiteNow")
    app.setStyle("Fusion")

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
