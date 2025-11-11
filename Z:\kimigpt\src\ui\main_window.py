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


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
