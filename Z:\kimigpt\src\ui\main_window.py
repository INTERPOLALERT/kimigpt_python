"""
Main Window for KimiGPT Desktop Application
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QTextEdit, QLineEdit, QComboBox, QProgressBar,
    QScrollArea, QFrame, QFileDialog, QMessageBox, QListWidget,
    QGroupBox, QRadioButton, QCheckBox, QSpinBox, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush, QPainter, QPixmap, QIcon

from src.ui.api_config_widget import APIConfigWidget
from src.ui.generator_widget import GeneratorWidget
from src.ui.dashboard_widget import DashboardWidget
from src.core.config_manager import ConfigManager


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.dark_mode = False
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("KimiGPT - Multi-Agent AI Website Builder")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)

        # Apply stylesheet
        self.apply_stylesheet()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)

        # Create tabs
        self.dashboard_widget = DashboardWidget(self)
        self.generator_widget = GeneratorWidget(self)
        self.api_config_widget = APIConfigWidget(self)

        # Add tabs
        self.tabs.addTab(self.dashboard_widget, "🏠 Dashboard")
        self.tabs.addTab(self.generator_widget, "🚀 Generator")
        self.tabs.addTab(self.api_config_widget, "⚙️ API Settings")

        # Connect tab change handler
        self.tabs.currentChanged.connect(self.on_tab_changed)

        main_layout.addWidget(self.tabs)

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_header(self):
        """Create the header section"""
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 10, 30, 10)

        # Logo and title
        title_layout = QVBoxLayout()
        title_label = QLabel("KimiGPT")
        title_label.setObjectName("appTitle")
        title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))

        subtitle_label = QLabel("Multi-Agent AI Website Builder")
        subtitle_label.setObjectName("appSubtitle")
        subtitle_label.setFont(QFont("Segoe UI", 11))

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.setSpacing(0)

        layout.addLayout(title_layout)
        layout.addStretch()

        # Back button (only show when not on dashboard)
        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setMinimumWidth(100)
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.hide()  # Hidden by default
        layout.addWidget(self.back_btn)

        # Dark mode toggle
        self.dark_mode_btn = QPushButton("🌙 Dark Mode")
        self.dark_mode_btn.setObjectName("secondaryButton")
        self.dark_mode_btn.setMinimumHeight(40)
        self.dark_mode_btn.setMinimumWidth(140)
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_btn)

        # Quick action buttons
        quick_gen_btn = QPushButton("Generate Website")
        quick_gen_btn.setObjectName("primaryButton")
        quick_gen_btn.setMinimumHeight(45)
        quick_gen_btn.setMinimumWidth(180)
        quick_gen_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))

        layout.addWidget(quick_gen_btn)

        return header

    def apply_stylesheet(self):
        """Apply custom stylesheet matching the web design"""
        stylesheet = """
            QMainWindow {
                background-color: #f9fafb;
            }

            #header {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
            }

            #appTitle {
                color: white;
                font-weight: bold;
            }

            #appSubtitle {
                color: rgba(255, 255, 255, 0.9);
            }

            QTabWidget::pane {
                border: none;
                background-color: #f9fafb;
            }

            QTabBar::tab {
                background-color: #ffffff;
                color: #6b7280;
                padding: 12px 24px;
                margin-right: 4px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: 500;
            }

            QTabBar::tab:selected {
                background-color: #f9fafb;
                color: #667eea;
                font-weight: 600;
            }

            QTabBar::tab:hover {
                background-color: #f3f4f6;
                color: #667eea;
            }

            QPushButton#primaryButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1
                );
            }

            QPushButton#secondaryButton {
                background-color: white;
                color: #667eea;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#secondaryButton:hover {
                background-color: #f3f4f6;
            }

            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px 12px;
                background-color: white;
                font-size: 13px;
            }

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #667eea;
                outline: none;
            }

            QGroupBox {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
                margin-top: 10px;
                font-weight: 600;
                font-size: 14px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }

            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #e5e7eb;
                height: 8px;
                text-align: center;
            }

            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
                border-radius: 4px;
            }

            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: 600;
                color: #111827;
                padding: 10px 0;
            }

            QLabel#sectionSubtitle {
                font-size: 14px;
                color: #6b7280;
                padding: 5px 0;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }

            QFrame#card {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
            }

            QFrame#card:hover {
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }

            QListWidget {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                padding: 8px;
            }

            QListWidget::item {
                border-radius: 6px;
                padding: 10px;
                margin: 2px 0;
            }

            QListWidget::item:selected {
                background-color: #ede9fe;
                color: #667eea;
            }

            QListWidget::item:hover {
                background-color: #f3f4f6;
            }

            QStatusBar {
                background-color: white;
                border-top: 1px solid #e5e7eb;
                color: #6b7280;
                font-size: 12px;
            }
        """
        self.setStyleSheet(stylesheet)

    def on_tab_changed(self, index):
        """Handle tab change events"""
        # Show back button when not on dashboard
        if index == 0:
            self.back_btn.hide()
        else:
            self.back_btn.show()

    def go_back(self):
        """Navigate back to dashboard"""
        self.tabs.setCurrentIndex(0)

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.dark_mode_btn.setText("☀️ Light Mode")
            self.apply_dark_stylesheet()
        else:
            self.dark_mode_btn.setText("🌙 Dark Mode")
            self.apply_stylesheet()

    def apply_dark_stylesheet(self):
        """Apply dark mode stylesheet"""
        dark_stylesheet = """
            QMainWindow {
                background-color: #1a1a1a;
            }

            #header {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a5568, stop:1 #2d3748
                );
            }

            #appTitle {
                color: white;
                font-weight: bold;
            }

            #appSubtitle {
                color: rgba(255, 255, 255, 0.9);
            }

            QTabWidget::pane {
                border: none;
                background-color: #1a1a1a;
            }

            QTabBar::tab {
                background-color: #2d3748;
                color: #a0aec0;
                padding: 12px 24px;
                margin-right: 4px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: 500;
            }

            QTabBar::tab:selected {
                background-color: #1a1a1a;
                color: #667eea;
                font-weight: 600;
            }

            QTabBar::tab:hover {
                background-color: #4a5568;
                color: #667eea;
            }

            QPushButton#primaryButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1
                );
            }

            QPushButton#secondaryButton {
                background-color: #2d3748;
                color: #a0aec0;
                border: 2px solid #4a5568;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#secondaryButton:hover {
                background-color: #4a5568;
                color: white;
            }

            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #4a5568;
                border-radius: 8px;
                padding: 10px 12px;
                background-color: #2d3748;
                color: #e2e8f0;
                font-size: 13px;
            }

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #667eea;
                outline: none;
            }

            QGroupBox {
                background-color: #2d3748;
                border: 1px solid #4a5568;
                border-radius: 12px;
                padding: 20px;
                margin-top: 10px;
                font-weight: 600;
                font-size: 14px;
                color: #e2e8f0;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }

            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #4a5568;
                height: 8px;
                text-align: center;
            }

            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
                border-radius: 4px;
            }

            QLabel {
                color: #e2e8f0;
            }

            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: 600;
                color: #f7fafc;
                padding: 10px 0;
            }

            QLabel#sectionSubtitle {
                font-size: 14px;
                color: #a0aec0;
                padding: 5px 0;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }

            QFrame#card {
                background-color: #2d3748;
                border: 1px solid #4a5568;
                border-radius: 12px;
                padding: 20px;
            }

            QFrame#card:hover {
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            }

            QListWidget {
                border: 1px solid #4a5568;
                border-radius: 8px;
                background-color: #2d3748;
                color: #e2e8f0;
                padding: 8px;
            }

            QListWidget::item {
                border-radius: 6px;
                padding: 10px;
                margin: 2px 0;
            }

            QListWidget::item:selected {
                background-color: #4a5568;
                color: #667eea;
            }

            QListWidget::item:hover {
                background-color: #374151;
            }

            QStatusBar {
                background-color: #2d3748;
                border-top: 1px solid #4a5568;
                color: #a0aec0;
                font-size: 12px;
            }

            QCheckBox {
                color: #e2e8f0;
            }

            QRadioButton {
                color: #e2e8f0;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #2d3748;
                color: #e2e8f0;
                selection-background-color: #4a5568;
                border: 1px solid #4a5568;
            }
        """
        self.setStyleSheet(dark_stylesheet)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
