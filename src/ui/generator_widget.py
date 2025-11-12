"""
Generator Widget for KimiGPT
Main website generation interface
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QGroupBox, QFileDialog, QListWidget, QProgressBar,
    QComboBox, QRadioButton, QButtonGroup, QFrame, QListWidgetItem,
    QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
import os
from datetime import datetime


class GenerationThread(QThread):
    """Thread for website generation"""

    progress_updated = pyqtSignal(int, str)
    agent_status_updated = pyqtSignal(str, str)
    generation_complete = pyqtSignal(dict)
    generation_error = pyqtSignal(str)

    def __init__(self, input_data):
        super().__init__()
        self.input_data = input_data

    def run(self):
        """Run the generation process"""
        try:
            from src.agents.orchestrator import OrchestratorAgent
            import asyncio
            import sys

            # Initialize orchestrator
            self.progress_updated.emit(10, "Initializing AI agents...")
            orchestrator = OrchestratorAgent()

            # Start generation
            self.progress_updated.emit(20, "Processing your request...")

            # Windows-specific asyncio setup for threads
            # This prevents the set_wakeup_fd error
            if sys.platform == 'win32':
                # Set the event loop policy to avoid set_wakeup_fd issues
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Run the async process
                result = loop.run_until_complete(
                    orchestrator.process(
                        self.input_data,
                        self.emit_progress,
                        self.emit_agent_status
                    )
                )

                if result.get('success', False):
                    self.generation_complete.emit(result)
                else:
                    self.generation_error.emit(result.get('error', 'Unknown error occurred'))
            finally:
                loop.close()

        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n\nDetails: {traceback.format_exc()}"
            self.generation_error.emit(error_msg)

    def emit_progress(self, value, message):
        """Safe progress emission"""
        try:
            self.progress_updated.emit(value, message)
        except:
            pass

    def emit_agent_status(self, agent, status):
        """Safe agent status emission"""
        try:
            self.agent_status_updated.emit(agent, status)
        except:
            pass


class GeneratorWidget(QWidget):
    """Generator tab widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        from src.core.config_manager import ConfigManager
        self.config_manager = ConfigManager()
        self.uploaded_files = []
        self.generation_thread = None
        self.current_project_id = None
        self.init_ui()

    def init_ui(self):
        """Initialize the generator UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(35)

        # Left column - Input form
        left_column = self.create_input_form()
        main_layout.addWidget(left_column, stretch=2)

        # Right column - Status and preview
        right_column = self.create_status_panel()
        main_layout.addWidget(right_column, stretch=1)

    def create_input_form(self):
        """Create the input form"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(30)

        # Title
        title = QLabel("🚀 AI Website Generator")
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        subtitle = QLabel(
            "Describe your dream website, upload reference materials, "
            "and watch our AI agents create it for you"
        )
        subtitle.setObjectName("sectionSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Project name
        project_group = QGroupBox("📁 Project Name")
        project_layout = QVBoxLayout(project_group)
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("My Awesome Website")
        self.project_name_input.setText(f"Website_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.project_name_input.setMinimumHeight(45)
        project_layout.addWidget(self.project_name_input)
        layout.addWidget(project_group)

        # Main prompt
        prompt_group = QGroupBox("💬 Describe Your Website")
        prompt_layout = QVBoxLayout(prompt_group)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Example:\n\n"
            "Create a modern business website for a tech consulting firm. "
            "I want a clean, professional design with a hero section, services showcase, "
            "team profiles, and contact form. Use a blue and white color scheme with subtle "
            "animations. The website should be fully responsive and SEO-optimized.\n\n"
            "Be specific about style, colors, sections, and functionality you want!"
        )
        self.prompt_input.setMinimumHeight(180)
        self.prompt_input.setFont(QFont("Segoe UI", 12))
        prompt_layout.addWidget(self.prompt_input)

        # Example prompts
        examples_label = QLabel("💡 Quick Examples:")
        examples_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        examples_label.setStyleSheet("color: #6366f1; margin-top: 12px;")
        prompt_layout.addWidget(examples_label)

        examples = [
            "Modern consulting firm with blue theme, hero, services, team, contact",
            "Creative portfolio for photographer with galleries and testimonials",
            "E-commerce store for handmade jewelry with product showcase"
        ]

        for example in examples:
            example_btn = QPushButton(f"📋 {example}")
            example_btn.setObjectName("secondaryButton")
            example_btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px 14px;
                    font-size: 12px;
                    min-height: 38px;
                }
            """)
            example_btn.clicked.connect(lambda checked, text=example: self.prompt_input.setText(text))
            prompt_layout.addWidget(example_btn)

        layout.addWidget(prompt_group)

        # File upload
        file_group = QGroupBox("📎 Upload Reference Materials (Optional)")
        file_layout = QVBoxLayout(file_group)

        file_btn_layout = QHBoxLayout()
        upload_btn = QPushButton("📁 Add Files")
        upload_btn.setObjectName("secondaryButton")
        upload_btn.setMinimumHeight(45)
        upload_btn.clicked.connect(self.upload_files)

        clear_files_btn = QPushButton("🗑️ Clear")
        clear_files_btn.setObjectName("secondaryButton")
        clear_files_btn.setMinimumHeight(45)
        clear_files_btn.clicked.connect(self.clear_files)

        file_btn_layout.addWidget(upload_btn)
        file_btn_layout.addWidget(clear_files_btn)
        file_layout.addLayout(file_btn_layout)

        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(120)
        file_layout.addWidget(self.file_list)

        file_info = QLabel("Supports: Images, Documents, Videos, Audio")
        file_info.setFont(QFont("Segoe UI", 9))
        file_info.setStyleSheet("color: #9ca3af;")
        file_layout.addWidget(file_info)

        layout.addWidget(file_group)

        # Advanced options
        advanced_group = QGroupBox("⚙️ Advanced Options")
        advanced_group.setCheckable(True)
        advanced_group.setChecked(False)

        # Create scroll area for advanced options
        advanced_scroll = QScrollArea()
        advanced_scroll.setWidgetResizable(True)
        advanced_scroll.setFrameShape(QFrame.Shape.NoFrame)
        advanced_scroll.setMaximumHeight(400)

        advanced_container = QWidget()
        advanced_layout = QVBoxLayout(advanced_container)

        # === DESIGN & STYLE ===
        design_section = QLabel("🎨 DESIGN & STYLE")
        design_section.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        design_section.setStyleSheet("color: #6366f1; margin-top: 12px; margin-bottom: 8px;")
        advanced_layout.addWidget(design_section)

        # Style selection
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Design Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            "Modern & Clean",
            "Classic & Professional",
            "Creative & Artistic",
            "Minimalist & Simple",
            "Playful & Fun",
            "Bold & Vibrant",
            "Elegant & Luxury"
        ])
        self.style_combo.setMinimumHeight(35)
        style_layout.addWidget(self.style_combo)
        advanced_layout.addLayout(style_layout)

        # Color scheme
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color Scheme:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Blue", "Green", "Purple", "Red", "Orange", "Pink", "Teal", "Gray", "Custom"])
        self.color_combo.setMinimumHeight(35)
        color_layout.addWidget(self.color_combo)
        advanced_layout.addLayout(color_layout)

        # Layout style
        layout_style_layout = QHBoxLayout()
        layout_style_layout.addWidget(QLabel("Layout Style:"))
        self.layout_style_combo = QComboBox()
        self.layout_style_combo.addItems([
            "Grid-based",
            "Flexbox Flow",
            "Card Layout",
            "Magazine Style",
            "Split Screen"
        ])
        self.layout_style_combo.setMinimumHeight(35)
        layout_style_layout.addWidget(self.layout_style_combo)
        advanced_layout.addLayout(layout_style_layout)

        # Font preference
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Style:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Sans-Serif (Modern)",
            "Serif (Classic)",
            "Monospace (Tech)",
            "Mixed (Dynamic)"
        ])
        self.font_combo.setMinimumHeight(35)
        font_layout.addWidget(self.font_combo)
        advanced_layout.addLayout(font_layout)

        # === FEATURES & FUNCTIONALITY ===
        features_section = QLabel("⚙️ FEATURES & FUNCTIONALITY")
        features_section.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        features_section.setStyleSheet("color: #6366f1; margin-top: 18px; margin-bottom: 8px;")
        advanced_layout.addWidget(features_section)

        # Complexity
        complexity_layout = QHBoxLayout()
        complexity_layout.addWidget(QLabel("Complexity:"))
        self.complexity_combo = QComboBox()
        self.complexity_combo.addItems([
            "Simple (1-3 sections)",
            "Moderate (4-6 sections)",
            "Advanced (7+ sections)"
        ])
        self.complexity_combo.setCurrentIndex(1)
        self.complexity_combo.setMinimumHeight(35)
        complexity_layout.addWidget(self.complexity_combo)
        advanced_layout.addLayout(complexity_layout)

        # Animations
        animation_layout = QHBoxLayout()
        animation_layout.addWidget(QLabel("Animations:"))
        self.animation_combo = QComboBox()
        self.animation_combo.addItems([
            "None (Static)",
            "Subtle (Minimal)",
            "Moderate (Balanced)",
            "Heavy (Interactive)"
        ])
        self.animation_combo.setCurrentIndex(2)
        self.animation_combo.setMinimumHeight(35)
        animation_layout.addWidget(self.animation_combo)
        advanced_layout.addLayout(animation_layout)

        # Interactivity level
        interactivity_layout = QHBoxLayout()
        interactivity_layout.addWidget(QLabel("Interactivity:"))
        self.interactivity_combo = QComboBox()
        self.interactivity_combo.addItems([
            "Basic (Links only)",
            "Standard (Forms, modals)",
            "Advanced (Full interactions)"
        ])
        self.interactivity_combo.setCurrentIndex(2)
        self.interactivity_combo.setMinimumHeight(35)
        interactivity_layout.addWidget(self.interactivity_combo)
        advanced_layout.addLayout(interactivity_layout)

        # Form types
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Include Forms:"))
        self.form_combo = QComboBox()
        self.form_combo.addItems([
            "Contact only",
            "Contact + Newsletter",
            "Contact + Signup",
            "All forms",
            "No forms"
        ])
        self.form_combo.setMinimumHeight(35)
        form_layout.addWidget(self.form_combo)
        advanced_layout.addLayout(form_layout)

        # Mobile menu style
        mobile_menu_layout = QHBoxLayout()
        mobile_menu_layout.addWidget(QLabel("Mobile Menu:"))
        self.mobile_menu_combo = QComboBox()
        self.mobile_menu_combo.addItems([
            "Hamburger (Side)",
            "Bottom Nav Bar",
            "Full Screen Overlay",
            "Slide-in Drawer"
        ])
        self.mobile_menu_combo.setMinimumHeight(35)
        mobile_menu_layout.addWidget(self.mobile_menu_combo)
        advanced_layout.addLayout(mobile_menu_layout)

        # === OPTIMIZATION ===
        optimization_section = QLabel("🚀 OPTIMIZATION")
        optimization_section.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        optimization_section.setStyleSheet("color: #6366f1; margin-top: 18px; margin-bottom: 8px;")
        advanced_layout.addWidget(optimization_section)

        # SEO level
        seo_layout = QHBoxLayout()
        seo_layout.addWidget(QLabel("SEO Level:"))
        self.seo_combo = QComboBox()
        self.seo_combo.addItems([
            "Basic (Meta tags)",
            "Standard (Meta + Schema)",
            "Advanced (Full optimization)"
        ])
        self.seo_combo.setCurrentIndex(1)
        self.seo_combo.setMinimumHeight(35)
        seo_layout.addWidget(self.seo_combo)
        advanced_layout.addLayout(seo_layout)

        # Performance optimization
        performance_layout = QHBoxLayout()
        performance_layout.addWidget(QLabel("Performance:"))
        self.performance_combo = QComboBox()
        self.performance_combo.addItems([
            "Standard",
            "Optimized (Lazy loading)",
            "Maximum (All optimizations)"
        ])
        self.performance_combo.setCurrentIndex(1)
        self.performance_combo.setMinimumHeight(35)
        performance_layout.addWidget(self.performance_combo)
        advanced_layout.addLayout(performance_layout)

        # Accessibility
        accessibility_layout = QHBoxLayout()
        accessibility_layout.addWidget(QLabel("Accessibility:"))
        self.accessibility_combo = QComboBox()
        self.accessibility_combo.addItems([
            "Basic (ARIA labels)",
            "Standard (WCAG A)",
            "Advanced (WCAG AA)"
        ])
        self.accessibility_combo.setCurrentIndex(1)
        self.accessibility_combo.setMinimumHeight(35)
        accessibility_layout.addWidget(self.accessibility_combo)
        advanced_layout.addLayout(accessibility_layout)

        # Browser compatibility
        browser_layout = QHBoxLayout()
        browser_layout.addWidget(QLabel("Browser Support:"))
        self.browser_combo = QComboBox()
        self.browser_combo.addItems([
            "Modern browsers only",
            "Last 2 versions",
            "Maximum compatibility"
        ])
        self.browser_combo.setCurrentIndex(1)
        self.browser_combo.setMinimumHeight(35)
        browser_layout.addWidget(self.browser_combo)
        advanced_layout.addLayout(browser_layout)

        # === TECHNOLOGY ===
        tech_section = QLabel("💻 TECHNOLOGY")
        tech_section.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        tech_section.setStyleSheet("color: #6366f1; margin-top: 18px; margin-bottom: 8px;")
        advanced_layout.addWidget(tech_section)

        # Framework
        framework_layout = QHBoxLayout()
        framework_layout.addWidget(QLabel("CSS Framework:"))
        self.framework_combo = QComboBox()
        self.framework_combo.addItems([
            "Pure HTML/CSS/JS",
            "Tailwind CSS",
            "Bootstrap 5"
        ])
        self.framework_combo.setMinimumHeight(35)
        framework_layout.addWidget(self.framework_combo)
        advanced_layout.addLayout(framework_layout)

        # Page type
        page_type_layout = QHBoxLayout()
        page_type_layout.addWidget(QLabel("Page Type:"))
        self.page_type_combo = QComboBox()
        self.page_type_combo.addItems([
            "Single Page (SPA)",
            "Multi-Page (Traditional)"
        ])
        self.page_type_combo.setMinimumHeight(35)
        page_type_layout.addWidget(self.page_type_combo)
        advanced_layout.addLayout(page_type_layout)

        # === ANALYTICS & TRACKING ===
        analytics_section = QLabel("📊 ANALYTICS & TRACKING")
        analytics_section.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        analytics_section.setStyleSheet("color: #6366f1; margin-top: 18px; margin-bottom: 8px;")
        advanced_layout.addWidget(analytics_section)

        # Analytics integration
        analytics_layout = QHBoxLayout()
        analytics_layout.addWidget(QLabel("Analytics:"))
        self.analytics_combo = QComboBox()
        self.analytics_combo.addItems([
            "None",
            "Google Analytics placeholder",
            "Google Analytics + Meta Pixel",
            "Full tracking suite"
        ])
        self.analytics_combo.setMinimumHeight(35)
        analytics_layout.addWidget(self.analytics_combo)
        advanced_layout.addLayout(analytics_layout)

        advanced_scroll.setWidget(advanced_container)

        # Add scroll area to group
        advanced_group_layout = QVBoxLayout(advanced_group)
        advanced_group_layout.addWidget(advanced_scroll)

        layout.addWidget(advanced_group)

        # Generate button
        self.generate_btn = QPushButton("✨ Generate My Website")
        self.generate_btn.setObjectName("primaryButton")
        self.generate_btn.setMinimumHeight(60)
        self.generate_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.generate_btn.clicked.connect(self.start_generation)
        layout.addWidget(self.generate_btn)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def create_status_panel(self):
        """Create the status panel"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(25)

        # Generation progress
        self.progress_group = QGroupBox("⚙️ Generation Progress")
        self.progress_group.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_group)
        progress_layout.setSpacing(15)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(12)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)

        # Status text
        self.status_label = QLabel("Initializing...")
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: #667eea;")
        progress_layout.addWidget(self.status_label)

        # Agent status
        self.agent_status_list = QListWidget()
        self.agent_status_list.setMaximumHeight(300)
        agents = [
            "🎯 Master Orchestrator",
            "🧠 Understanding Agent",
            "🎨 Design Agent",
            "💻 Code Agent",
            "📝 Content Agent",
            "✅ QA Agent",
            "🚀 Deployment Agent"
        ]

        for agent in agents:
            item = QListWidgetItem(f"{agent} - Waiting")
            item.setData(Qt.ItemDataRole.UserRole, agent)
            self.agent_status_list.addItem(item)

        progress_layout.addWidget(self.agent_status_list)

        # Time estimate
        time_frame = QFrame()
        time_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0e7ff, stop:1 #ddd6fe
                );
                border: 2px solid #c7d2fe;
                border-radius: 10px;
                padding: 14px;
            }
        """)
        time_layout = QVBoxLayout(time_frame)
        time_label = QLabel("⏱️ Estimated time: 30-60 seconds")
        time_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        time_label.setStyleSheet("color: #4338ca;")
        time_layout.addWidget(time_label)
        progress_layout.addWidget(time_frame)

        layout.addWidget(self.progress_group)

        # Result panel
        self.result_group = QGroupBox("✅ Generation Complete!")
        self.result_group.setVisible(False)
        result_layout = QVBoxLayout(self.result_group)

        success_label = QLabel("🎉 Your website has been generated successfully!")
        success_label.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        success_label.setStyleSheet("color: #059669;")
        success_label.setWordWrap(True)
        result_layout.addWidget(success_label)

        # Result stats
        self.result_stats = QLabel("")
        self.result_stats.setFont(QFont("Segoe UI", 10))
        self.result_stats.setStyleSheet("color: #6b7280;")
        result_layout.addWidget(self.result_stats)

        # Action buttons
        self.preview_btn = QPushButton("👁️ Preview Website")
        self.preview_btn.setObjectName("primaryButton")
        self.preview_btn.setMinimumHeight(50)
        self.preview_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.preview_btn.clicked.connect(self.preview_website)
        result_layout.addWidget(self.preview_btn)

        self.download_btn = QPushButton("📦 Download ZIP")
        self.download_btn.setObjectName("secondaryButton")
        self.download_btn.setMinimumHeight(50)
        self.download_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.download_btn.clicked.connect(self.download_website)
        result_layout.addWidget(self.download_btn)

        self.open_folder_btn = QPushButton("📁 Open Folder")
        self.open_folder_btn.setObjectName("secondaryButton")
        self.open_folder_btn.setMinimumHeight(50)
        self.open_folder_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        result_layout.addWidget(self.open_folder_btn)

        layout.addWidget(self.result_group)

        # System status
        system_group = QGroupBox("📊 System Status")
        system_layout = QVBoxLayout(system_group)

        status_items = [
            ("🤖 AI Providers", "Online"),
            ("⚡ Processing Queue", "Normal"),
            ("🔄 API Rotation", "Active")
        ]

        for label, status in status_items:
            item_layout = QHBoxLayout()
            item_layout.addWidget(QLabel(label))
            status_label = QLabel(status)
            status_label.setStyleSheet("color: #059669; font-weight: 600;")
            item_layout.addWidget(status_label)
            item_layout.addStretch()
            system_layout.addLayout(item_layout)

        layout.addWidget(system_group)

        layout.addStretch()
        return container

    def upload_files(self):
        """Handle file upload"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Reference Files",
            "",
            "All Files (*);;Images (*.png *.jpg *.jpeg *.gif *.webp);;Documents (*.pdf *.docx *.txt);;Videos (*.mp4 *.webm *.mov);;Audio (*.mp3 *.wav *.ogg)"
        )

        for file in files:
            if file and file not in self.uploaded_files:
                self.uploaded_files.append(file)
                item = QListWidgetItem(f"📄 {os.path.basename(file)}")
                self.file_list.addItem(item)

    def clear_files(self):
        """Clear uploaded files"""
        self.uploaded_files.clear()
        self.file_list.clear()

    def start_generation(self):
        """Start website generation"""
        # Validate input
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(
                self,
                "Missing Input",
                "Please describe the website you want to create."
            )
            return

        # Check if APIs are configured
        from src.core.config_manager import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.load_config()

        if not config.get('api_keys'):
            reply = QMessageBox.question(
                self,
                "No API Keys",
                "No API keys configured. Would you like to configure them now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.parent.tabs.setCurrentIndex(2)
            return

        # Prepare input data with comprehensive preferences
        input_data = {
            'project_id': f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'project_name': self.project_name_input.text().strip(),
            'prompt': prompt,
            'files': self.uploaded_files,
            'preferences': {
                # Design & Style
                'style': self.style_combo.currentText(),
                'color_scheme': self.color_combo.currentText().lower(),
                'layout_style': self.layout_style_combo.currentText(),
                'font_style': self.font_combo.currentText().split()[0],

                # Features & Functionality
                'complexity': self.complexity_combo.currentText().split()[0].lower(),
                'animations': self.animation_combo.currentText().split()[0].lower(),
                'interactivity': self.interactivity_combo.currentText().split()[0].lower(),
                'forms': self.form_combo.currentText(),
                'mobile_menu': self.mobile_menu_combo.currentText().split()[0],

                # Optimization
                'seo_level': self.seo_combo.currentText().split()[0].lower(),
                'performance': self.performance_combo.currentText().split()[0].lower(),
                'accessibility': self.accessibility_combo.currentText().split()[0].lower(),
                'browser_support': self.browser_combo.currentText(),

                # Technology
                'framework': self.framework_combo.currentText().split()[0].lower(),
                'page_type': self.page_type_combo.currentText().split()[0].lower(),

                # Analytics
                'analytics': self.analytics_combo.currentText()
            }
        }

        self.current_project_id = input_data['project_id']

        # Show progress panel
        self.progress_group.setVisible(True)
        self.result_group.setVisible(False)
        self.progress_bar.setValue(0)
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("⏳ Generating...")

        # Reset agent status
        for i in range(self.agent_status_list.count()):
            item = self.agent_status_list.item(i)
            agent_name = item.data(Qt.ItemDataRole.UserRole)
            item.setText(f"{agent_name} - Waiting")

        # Start generation thread
        self.generation_thread = GenerationThread(input_data)
        self.generation_thread.progress_updated.connect(self.update_progress)
        self.generation_thread.agent_status_updated.connect(self.update_agent_status)
        self.generation_thread.generation_complete.connect(self.generation_finished)
        self.generation_thread.generation_error.connect(self.generation_failed)
        self.generation_thread.start()

    def update_progress(self, value, message):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def update_agent_status(self, agent_name, status):
        """Update agent status"""
        for i in range(self.agent_status_list.count()):
            item = self.agent_status_list.item(i)
            agent_display = item.data(Qt.ItemDataRole.UserRole)
            if agent_name.lower() in agent_display.lower():
                item.setText(f"{agent_display} - {status}")
                break

    def generation_finished(self, result):
        """Handle generation completion"""
        # CRITICAL: Update project_id from result to show the NEW website
        self.current_project_id = result.get('project_id', self.current_project_id)

        self.progress_group.setVisible(False)
        self.result_group.setVisible(True)
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("✨ Generate My Website")

        # Update result stats
        file_count = len(result.get('code', {}))
        self.result_stats.setText(
            f"📁 Generated {file_count} files\n"
            f"⏱️ Project ID: {self.current_project_id}"
        )

        self.parent.statusBar().showMessage("Website generated successfully!", 5000)

    def generation_failed(self, error):
        """Handle generation failure"""
        self.progress_group.setVisible(False)
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("✨ Generate My Website")

        QMessageBox.critical(
            self,
            "Generation Failed",
            f"An error occurred during generation:\n\n{error}\n\n"
            f"Please check your API keys and try again."
        )

        self.parent.statusBar().showMessage("Generation failed", 5000)

    def preview_website(self):
        """Preview generated website"""
        if self.current_project_id:
            base_output_dir = self.config_manager.get_output_dir()
            output_path = os.path.join(base_output_dir, self.current_project_id)
            index_file = os.path.join(output_path, "index.html")

            if os.path.exists(index_file):
                import webbrowser
                webbrowser.open(f"file:///{index_file}")
            else:
                QMessageBox.warning(self, "Not Found", "Preview file not found.")

    def download_website(self):
        """Download website as ZIP"""
        if self.current_project_id:
            base_output_dir = self.config_manager.get_output_dir()
            output_path = os.path.join(base_output_dir, self.current_project_id)

            if os.path.exists(output_path):
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Website",
                    f"{self.current_project_id}.zip",
                    "ZIP Files (*.zip)"
                )

                if save_path:
                    import shutil
                    shutil.make_archive(save_path.replace('.zip', ''), 'zip', output_path)
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Website saved to:\n{save_path}"
                    )

    def open_output_folder(self):
        """Open output folder"""
        if self.current_project_id:
            base_output_dir = self.config_manager.get_output_dir()
            output_path = os.path.join(base_output_dir, self.current_project_id)

            if os.path.exists(output_path):
                import subprocess
                subprocess.Popen(f'explorer "{output_path}"')
            else:
                QMessageBox.warning(self, "Not Found", "Output folder not found.")
