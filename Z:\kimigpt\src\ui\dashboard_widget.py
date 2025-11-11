"""
Dashboard Widget for KimiGPT
Shows overview, statistics, and quick actions
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DashboardWidget(QWidget):
    """Dashboard tab widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the dashboard UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Hero Section
        hero_section = self.create_hero_section()
        main_layout.addWidget(hero_section)

        # Statistics Section
        stats_section = self.create_stats_section()
        main_layout.addWidget(stats_section)

        # Features Section
        features_section = self.create_features_section()
        main_layout.addWidget(features_section)

        main_layout.addStretch()

    def create_hero_section(self):
        """Create hero section"""
        frame = QFrame()
        frame.setObjectName("card")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("Build Websites with AI Intelligence")
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel(
            "Revolutionary multi-agent AI system that creates professional, production-ready websites\n"
            "from any input - text, images, audio, or video. Smart API rotation, real-time preview,\n"
            "and one-click deployment."
        )
        subtitle.setObjectName("sectionSubtitle")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch()

        start_btn = QPushButton("🚀 Start Building")
        start_btn.setObjectName("primaryButton")
        start_btn.setMinimumHeight(50)
        start_btn.setMinimumWidth(180)
        start_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        start_btn.clicked.connect(lambda: self.parent.tabs.setCurrentIndex(1))

        api_btn = QPushButton("⚙️ Configure APIs")
        api_btn.setObjectName("secondaryButton")
        api_btn.setMinimumHeight(50)
        api_btn.setMinimumWidth(180)
        api_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        api_btn.clicked.connect(lambda: self.parent.tabs.setCurrentIndex(2))

        button_layout.addWidget(start_btn)
        button_layout.addWidget(api_btn)
        button_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(button_layout)

        return frame

    def create_stats_section(self):
        """Create statistics section"""
        frame = QFrame()
        frame.setObjectName("card")

        layout = QGridLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        stats = [
            ("🤖 AI Agents", "8", "Specialized Agents"),
            ("🔗 API Providers", "8+", "AI Services"),
            ("📁 Supported Formats", "10+", "File Types"),
            ("⚡ Generation Speed", "< 60s", "Average Time")
        ]

        for i, (emoji_title, value, description) in enumerate(stats):
            stat_widget = self.create_stat_card(emoji_title, value, description)
            layout.addWidget(stat_widget, 0, i)

        return frame

    def create_stat_card(self, title, value, description):
        """Create a statistic card"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #6b7280;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("color: #667eea;")

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #9ca3af;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(desc_label)

        return widget

    def create_features_section(self):
        """Create features section"""
        frame = QFrame()
        frame.setObjectName("card")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Title
        title = QLabel("Why Choose KimiGPT?")
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        # Features grid
        features_grid = QGridLayout()
        features_grid.setSpacing(20)

        features = [
            ("🤖 Multi-Agent AI", "8 specialized AI agents work together for perfect results"),
            ("🔄 Smart API Rotation", "Automatic failover across 8+ AI providers"),
            ("🎨 Multi-Modal Input", "Text, images, videos, audio - any input works"),
            ("👀 Real-Time Preview", "Watch your website being built live"),
            ("⚡ Advanced Features", "PWA, accessibility, SEO optimization included"),
            ("📦 One-Click Export", "Download as ready-to-deploy ZIP package")
        ]

        for i, (emoji_title, description) in enumerate(features):
            row = i // 2
            col = i % 2
            feature_card = self.create_feature_card(emoji_title, description)
            features_grid.addWidget(feature_card, row, col)

        layout.addLayout(features_grid)

        return frame

    def create_feature_card(self, title, description):
        """Create a feature card"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
                padding: 25px;
            }
            QFrame:hover {
                background-color: #ede9fe;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #111827;")

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 13))
        desc_label.setStyleSheet("color: #6b7280;")
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        return widget
