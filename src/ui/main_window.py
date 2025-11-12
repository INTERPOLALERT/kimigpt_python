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
        """Apply custom stylesheet - REVAMPED PREMIUM DESIGN"""
        stylesheet = """
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fafbfc, stop:1 #f0f2f5
                );
            }

            #header {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:0.5 #8b5cf6, stop:1 #d946ef
                );
                border-bottom: 3px solid rgba(255, 255, 255, 0.2);
            }

            #appTitle {
                color: white;
                font-weight: bold;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }

            #appSubtitle {
                color: rgba(255, 255, 255, 0.95);
                font-size: 12px;
            }

            QTabWidget::pane {
                border: none;
                background: transparent;
            }

            QTabBar::tab {
                background: white;
                color: #64748b;
                padding: 14px 28px;
                margin-right: 6px;
                margin-top: 4px;
                border: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
            }

            QTabBar::tab:selected {
                background: white;
                color: #6366f1;
                font-weight: 600;
                border-bottom: 3px solid #6366f1;
            }

            QTabBar::tab:hover {
                background: #f8fafc;
                color: #6366f1;
            }

            QPushButton#primaryButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6
                );
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 28px;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c3aed
                );
                padding: 13px 29px;
            }

            QPushButton#primaryButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4338ca, stop:1 #6d28d9
                );
            }

            QPushButton#secondaryButton {
                background: white;
                color: #6366f1;
                border: 2px solid #e0e7ff;
                border-radius: 10px;
                padding: 10px 22px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#secondaryButton:hover {
                background: #f5f3ff;
                border: 2px solid #6366f1;
                color: #4f46e5;
            }

            QPushButton#secondaryButton:pressed {
                background: #ede9fe;
            }

            QLineEdit, QTextEdit {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 12px 16px;
                background: white;
                color: #1e293b;
                font-size: 14px;
                selection-background-color: #c7d2fe;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #6366f1;
                background: #fafbfc;
            }

            QComboBox {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px 16px;
                background: white;
                color: #1e293b;
                font-size: 14px;
                min-height: 22px;
            }

            QComboBox:focus {
                border: 2px solid #6366f1;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #64748b;
                margin-right: 8px;
            }

            QComboBox QAbstractItemView {
                background: white;
                color: #1e293b;
                selection-background-color: #e0e7ff;
                selection-color: #4f46e5;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 4px;
            }

            QGroupBox {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                padding: 24px;
                margin-top: 12px;
                font-weight: 600;
                font-size: 15px;
                color: #1e293b;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                background: white;
            }

            QProgressBar {
                border: none;
                border-radius: 6px;
                background: #e2e8f0;
                height: 12px;
                text-align: center;
            }

            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6
                );
                border-radius: 6px;
            }

            QLabel#sectionTitle {
                font-size: 20px;
                font-weight: 700;
                color: #0f172a;
                padding: 12px 0;
            }

            QLabel#sectionSubtitle {
                font-size: 15px;
                color: #475569;
                padding: 6px 0;
                line-height: 1.6;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 6px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }

            QFrame#card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 24px;
            }

            QListWidget {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background: white;
                padding: 8px;
            }

            QListWidget::item {
                border-radius: 8px;
                padding: 12px;
                margin: 3px 0;
                color: #334155;
            }

            QListWidget::item:selected {
                background: #e0e7ff;
                color: #4f46e5;
                font-weight: 600;
            }

            QListWidget::item:hover {
                background: #f1f5f9;
            }

            QStatusBar {
                background: white;
                border-top: 2px solid #e2e8f0;
                color: #64748b;
                font-size: 13px;
                padding: 6px;
            }

            QCheckBox {
                color: #334155;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #cbd5e1;
                border-radius: 4px;
                background: white;
            }

            QCheckBox::indicator:checked {
                background: #6366f1;
                border-color: #6366f1;
            }

            QRadioButton {
                color: #334155;
                spacing: 8px;
            }

            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                background: white;
            }

            QRadioButton::indicator:checked {
                background: #6366f1;
                border-color: #6366f1;
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
        """Apply dark mode stylesheet - TRULY DARK PREMIUM DESIGN"""
        dark_stylesheet = """
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0a0a0a, stop:1 #000000
                );
            }

            #header {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:0.5 #7c3aed, stop:1 #c026d3
                );
                border-bottom: 3px solid rgba(139, 92, 246, 0.3);
            }

            #appTitle {
                color: white;
                font-weight: bold;
                text-shadow: 0 2px 8px rgba(139, 92, 246, 0.5);
            }

            #appSubtitle {
                color: rgba(255, 255, 255, 0.95);
                font-size: 12px;
            }

            QTabWidget::pane {
                border: none;
                background: transparent;
            }

            QTabBar::tab {
                background: #141414;
                color: #94a3b8;
                padding: 14px 28px;
                margin-right: 6px;
                margin-top: 4px;
                border: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
            }

            QTabBar::tab:selected {
                background: #1a1a1a;
                color: #a78bfa;
                font-weight: 600;
                border-bottom: 3px solid #8b5cf6;
            }

            QTabBar::tab:hover {
                background: #1f1f1f;
                color: #c4b5fd;
            }

            QPushButton#primaryButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #a855f7
                );
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 28px;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #c026d3
                );
                padding: 13px 29px;
            }

            QPushButton#primaryButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6d28d9, stop:1 #a21caf
                );
            }

            QPushButton#secondaryButton {
                background: #1a1a1a;
                color: #a78bfa;
                border: 2px solid #312e81;
                border-radius: 10px;
                padding: 10px 22px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#secondaryButton:hover {
                background: #27272a;
                border: 2px solid #6366f1;
                color: #c4b5fd;
            }

            QPushButton#secondaryButton:pressed {
                background: #18181b;
            }

            QLineEdit, QTextEdit {
                border: 2px solid #27272a;
                border-radius: 10px;
                padding: 12px 16px;
                background: #141414;
                color: #f1f5f9;
                font-size: 14px;
                selection-background-color: #4c1d95;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #7c3aed;
                background: #1a1a1a;
            }

            QComboBox {
                border: 2px solid #27272a;
                border-radius: 10px;
                padding: 10px 16px;
                background: #141414;
                color: #f1f5f9;
                font-size: 14px;
                min-height: 22px;
            }

            QComboBox:focus {
                border: 2px solid #7c3aed;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #94a3b8;
                margin-right: 8px;
            }

            QComboBox QAbstractItemView {
                background: #141414;
                color: #f1f5f9;
                selection-background-color: #312e81;
                selection-color: #c4b5fd;
                border: 2px solid #27272a;
                border-radius: 8px;
                padding: 4px;
            }

            QGroupBox {
                background: #141414;
                border: 2px solid #27272a;
                border-radius: 14px;
                padding: 24px;
                margin-top: 12px;
                font-weight: 600;
                font-size: 15px;
                color: #f1f5f9;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                background: #141414;
            }

            QProgressBar {
                border: none;
                border-radius: 6px;
                background: #27272a;
                height: 12px;
                text-align: center;
            }

            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #a855f7
                );
                border-radius: 6px;
            }

            QLabel {
                color: #e2e8f0;
            }

            QLabel#sectionTitle {
                font-size: 20px;
                font-weight: 700;
                color: #f8fafc;
                padding: 12px 0;
            }

            QLabel#sectionSubtitle {
                font-size: 15px;
                color: #cbd5e1;
                padding: 6px 0;
                line-height: 1.6;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: #1a1a1a;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #3f3f46;
                border-radius: 6px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #52525b;
            }

            QFrame#card {
                background: #141414;
                border: 1px solid #27272a;
                border-radius: 16px;
                padding: 24px;
            }

            QListWidget {
                border: 2px solid #27272a;
                border-radius: 10px;
                background: #141414;
                padding: 8px;
            }

            QListWidget::item {
                border-radius: 8px;
                padding: 12px;
                margin: 3px 0;
                color: #e2e8f0;
            }

            QListWidget::item:selected {
                background: #312e81;
                color: #c4b5fd;
                font-weight: 600;
            }

            QListWidget::item:hover {
                background: #1f1f23;
            }

            QStatusBar {
                background: #0f0f0f;
                border-top: 2px solid #27272a;
                color: #94a3b8;
                font-size: 13px;
                padding: 6px;
            }

            QCheckBox {
                color: #e2e8f0;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #3f3f46;
                border-radius: 4px;
                background: #1a1a1a;
            }

            QCheckBox::indicator:checked {
                background: #7c3aed;
                border-color: #7c3aed;
            }

            QRadioButton {
                color: #e2e8f0;
                spacing: 8px;
            }

            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #3f3f46;
                border-radius: 10px;
                background: #1a1a1a;
            }

            QRadioButton::indicator:checked {
                background: #7c3aed;
                border-color: #7c3aed;
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
