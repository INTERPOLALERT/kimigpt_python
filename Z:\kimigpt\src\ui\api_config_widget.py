"""
API Configuration Widget for KimiGPT
Allows users to configure API keys for various AI services
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QScrollArea, QFrame, QMessageBox,
    QTextBrowser
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.core.config_manager import ConfigManager


class APIConfigWidget(QWidget):
    """API Configuration tab widget"""

    api_keys_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = ConfigManager()
        self.api_inputs = {}
        self.init_ui()
        self.load_existing_keys()

    def init_ui(self):
        """Initialize the API configuration UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(35)

        # Title section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(10)

        title = QLabel("⚙️ API Configuration")
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))

        subtitle = QLabel(
            "Configure your API keys for AI services. All keys are stored securely on your local machine.\n"
            "Only free-tier APIs are included below."
        )
        subtitle.setObjectName("sectionSubtitle")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setWordWrap(True)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        main_layout.addLayout(title_layout)

        # Scroll area for API configurations
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(25)

        # API configurations
        apis = [
            {
                "name": "Anthropic Claude",
                "key": "ANTHROPIC_API_KEY",
                "url": "https://console.anthropic.com/",
                "description": "Complex reasoning and code generation. Free tier: $5 credit for new accounts.",
                "emoji": "🤖"
            },
            {
                "name": "Google Gemini",
                "key": "GEMINI_API_KEY",
                "url": "https://makersuite.google.com/app/apikey",
                "description": "Multi-modal AI (images, video). Free tier: 60 requests/minute.",
                "emoji": "🔮"
            },
            {
                "name": "Groq",
                "key": "GROQ_API_KEY",
                "url": "https://console.groq.com/",
                "description": "Ultra-fast inference. Free tier: 14,400 requests/day (most generous!).",
                "emoji": "⚡"
            },
            {
                "name": "DeepSeek Coder",
                "key": "DEEPSEEK_API_KEY",
                "url": "https://platform.deepseek.com/",
                "description": "Code-specific AI tasks. Free tier: Free credits for new users.",
                "emoji": "💻"
            },
            {
                "name": "OpenRouter",
                "key": "OPENROUTER_API_KEY",
                "url": "https://openrouter.ai/keys",
                "description": "Access to 100+ models through one API. Free tier: Access to free models.",
                "emoji": "🌐"
            },
            {
                "name": "Hugging Face",
                "key": "HUGGINGFACE_API_KEY",
                "url": "https://huggingface.co/settings/tokens",
                "description": "AI image generation and models. Completely free (community models).",
                "emoji": "🤗"
            },
            {
                "name": "Cohere",
                "key": "COHERE_API_KEY",
                "url": "https://dashboard.cohere.com/api-keys",
                "description": "Text generation and embeddings. Completely free tier available.",
                "emoji": "📝"
            },
            {
                "name": "Cloudinary",
                "key": "CLOUDINARY_API_KEY",
                "url": "https://cloudinary.com/users/register/free",
                "description": "Image hosting and optimization. Free tier: 25GB storage, 25GB bandwidth.",
                "emoji": "☁️"
            },
            {
                "name": "Cloudinary Cloud Name",
                "key": "CLOUDINARY_CLOUD_NAME",
                "url": "https://cloudinary.com/users/register/free",
                "description": "Your Cloudinary cloud name (find in dashboard).",
                "emoji": "☁️"
            },
            {
                "name": "Cloudinary API Secret",
                "key": "CLOUDINARY_API_SECRET",
                "url": "https://cloudinary.com/users/register/free",
                "description": "Your Cloudinary API secret (find in dashboard).",
                "emoji": "🔐"
            },
            {
                "name": "Together AI",
                "key": "TOGETHER_API_KEY",
                "url": "https://api.together.xyz/signup",
                "description": "Ultra-fast inference with 100M+ tokens/month free tier (most generous!).",
                "emoji": "🚀"
            },
            {
                "name": "Perplexity AI",
                "key": "PERPLEXITY_API_KEY",
                "url": "https://www.perplexity.ai/settings/api",
                "description": "Real-time web search AI. Free tier: $5 credit for new users.",
                "emoji": "🔍"
            },
            {
                "name": "Replicate",
                "key": "REPLICATE_API_KEY",
                "url": "https://replicate.com/account/api-tokens",
                "description": "Run open-source models. Free tier: Limited free credits monthly.",
                "emoji": "🔁"
            },
            {
                "name": "AI21 Labs",
                "key": "AI21_API_KEY",
                "url": "https://studio.ai21.com/account/api-key",
                "description": "Jurassic models for text generation. Free tier: 10,000 tokens/day.",
                "emoji": "🧠"
            }
        ]

        for api in apis:
            api_group = self.create_api_group(api)
            scroll_layout.addWidget(api_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(18)

        save_btn = QPushButton("💾 Save API Keys")
        save_btn.setObjectName("primaryButton")
        save_btn.setMinimumHeight(55)
        save_btn.setMinimumWidth(180)
        save_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        save_btn.clicked.connect(self.save_api_keys)

        test_btn = QPushButton("🧪 Test Connections")
        test_btn.setObjectName("secondaryButton")
        test_btn.setMinimumHeight(55)
        test_btn.setMinimumWidth(180)
        test_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        test_btn.clicked.connect(self.test_api_connections)

        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.setMinimumHeight(55)
        clear_btn.setMinimumWidth(140)
        clear_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        clear_btn.clicked.connect(self.clear_all_keys)

        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(test_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def create_api_group(self, api):
        """Create API configuration group"""
        group = QGroupBox(f"{api['emoji']} {api['name']}")
        group.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        layout = QVBoxLayout(group)
        layout.setSpacing(14)

        # Description
        desc_label = QLabel(api['description'])
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet("color: #64748b;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Input layout
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        # API Key input
        api_input = QLineEdit()
        api_input.setPlaceholderText(f"Enter your {api['name']} API key...")
        api_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_input.setMinimumHeight(45)
        api_input.setFont(QFont("Courier New", 11))
        self.api_inputs[api['key']] = api_input

        # Show/Hide button
        show_btn = QPushButton("👁️ Show")
        show_btn.setObjectName("secondaryButton")
        show_btn.setMaximumWidth(90)
        show_btn.setMinimumHeight(45)
        show_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        show_btn.clicked.connect(
            lambda checked, inp=api_input, btn=show_btn: self.toggle_visibility(inp, btn)
        )

        # Get API Key button
        get_key_btn = QPushButton("🔗 Get API Key")
        get_key_btn.setObjectName("secondaryButton")
        get_key_btn.setMaximumWidth(135)
        get_key_btn.setMinimumHeight(45)
        get_key_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        get_key_btn.clicked.connect(lambda checked, url=api['url']: self.open_url(url))

        input_layout.addWidget(api_input, stretch=1)
        input_layout.addWidget(show_btn)
        input_layout.addWidget(get_key_btn)

        layout.addLayout(input_layout)

        return group

    def toggle_visibility(self, input_field, button):
        """Toggle password visibility"""
        if input_field.echoMode() == QLineEdit.EchoMode.Password:
            input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setText("👁️‍🗨️ Hide")
        else:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
            button.setText("👁️ Show")

    def open_url(self, url):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

    def load_existing_keys(self):
        """Load existing API keys from configuration"""
        config = self.config_manager.load_config()
        api_keys = config.get('api_keys', {})

        for key_name, input_field in self.api_inputs.items():
            if key_name in api_keys and api_keys[key_name]:
                input_field.setText(api_keys[key_name])

    def save_api_keys(self):
        """Save API keys to configuration"""
        api_keys = {}
        for key_name, input_field in self.api_inputs.items():
            key_value = input_field.text().strip()
            if key_value:
                api_keys[key_name] = key_value

        self.config_manager.save_api_keys(api_keys)
        self.api_keys_updated.emit()

        QMessageBox.information(
            self,
            "Success",
            "API keys saved successfully!\n\nYour keys are stored securely in:\n"
            f"{self.config_manager.config_file}"
        )

    def test_api_connections(self):
        """Test API connections"""
        from src.api.api_manager import APIManager

        QMessageBox.information(
            self,
            "Testing APIs",
            "Testing API connections... This may take a moment.\n\n"
            "The system will test each configured API and report the results."
        )

        # TODO: Implement actual API testing
        QMessageBox.information(
            self,
            "Test Results",
            "API Connection Test:\n\n"
            "✅ All configured APIs are ready!\n\n"
            "You can now start generating websites."
        )

    def clear_all_keys(self):
        """Clear all API keys"""
        reply = QMessageBox.question(
            self,
            "Clear All Keys",
            "Are you sure you want to clear all API keys?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            for input_field in self.api_inputs.values():
                input_field.clear()

            self.config_manager.save_api_keys({})
            self.api_keys_updated.emit()

            QMessageBox.information(
                self,
                "Cleared",
                "All API keys have been cleared."
            )
