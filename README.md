# 🚀 WebsiteNow Desktop - AI Website Builder

**Transform your ideas into professional websites using AI - No browser required!**

WebsiteNow Desktop is a standalone Python application that uses multiple AI agents to generate beautiful, production-ready websites from simple text descriptions.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## ✨ Features

### 🤖 **Multi-Agent AI System**
- **8 Specialized AI Agents** working together:
  - 🧠 Understanding Agent - Analyzes your requirements
  - 🎨 Design Agent - Creates design specifications
  - 💻 Code Agent - Generates HTML/CSS/JavaScript
  - 📝 Content Agent - Writes engaging copy
  - ✅ QA Agent - Validates code quality
  - 🚀 Deployment Agent - Packages for deployment

### 🔄 **Smart API Rotation**
- Automatic failover across 8+ AI providers
- Uses **only free-tier APIs** (no paid subscriptions required!)
- Intelligent load balancing and caching

### 🎨 **Beautiful Desktop Interface**
- Native Windows application (no browser needed!)
- Purple gradient theme matching the original web design
- Real-time generation progress monitoring
- In-app API configuration

### 📦 **Complete Features**
- Multi-modal input (text, images, videos, audio)
- Real-time preview of generated websites
- One-click ZIP download
- Deployment guides for Netlify, Vercel, GitHub Pages
- SEO-optimized output
- Responsive design guaranteed
- Accessibility compliant (WCAG AA)

---

## 🔧 Installation

### Prerequisites
- **Windows Home** (or any Windows version)
- **Python 3.9 or higher** installed
- Internet connection

### Quick Start

1. **Download/Clone** this repository to `Z:\websitenow`

2. **Run Installation**:
   ```cmd
   Double-click installgpt.bat
   ```
   This will:
   - Check Python installation
   - Install all required packages
   - Set up directories
   - Prepare the environment

3. **Get FREE API Keys** (see [API Configuration](#-api-configuration))

4. **Launch WebsiteNow**:
   ```cmd
   Double-click startgpt.bat
   ```

That's it! 🎉

---

## 🔑 API Configuration

### Required APIs (All FREE!)

WebsiteNow works with **completely free AI APIs**. You need at least ONE API key to start.

#### 🌟 Recommended (Get these first):

1. **Groq** ⚡ - Most generous free tier!
   - 14,400 requests/day (completely free)
   - Ultra-fast generation
   - Get it: https://console.groq.com/

2. **Google Gemini** 🔮
   - 60 requests/minute (free forever)
   - Great for general use
   - Get it: https://makersuite.google.com/app/apikey

3. **Anthropic Claude** 🤖
   - $5 free credit for new accounts
   - Best quality output
   - Get it: https://console.anthropic.com/

#### 📋 All Supported APIs:

| API | Free Tier | Best For | Get Key |
|-----|-----------|----------|---------|
| Groq | 14,400 req/day | Speed | [console.groq.com](https://console.groq.com/) |
| Google Gemini | 60 req/min | General use | [makersuite.google.com](https://makersuite.google.com/app/apikey) |
| Anthropic Claude | $5 credit | Quality | [console.anthropic.com](https://console.anthropic.com/) |
| DeepSeek | Free credits | Code | [platform.deepseek.com](https://platform.deepseek.com/) |
| OpenRouter | Free models | Variety | [openrouter.ai/keys](https://openrouter.ai/keys) |
| Cohere | Free tier | Text | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) |
| Hugging Face | Free | Images | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| Cloudinary | 25GB free | Image hosting | [cloudinary.com/users/register/free](https://cloudinary.com/users/register/free) |

### Adding API Keys:

1. Launch WebsiteNow (`startgpt.bat`)
2. Click **"⚙️ API Settings"** tab
3. For each API:
   - Click **"🔗 Get API Key"** to visit provider
   - Copy your API key
   - Paste into the input field
   - Click **"👁️ Show"** to verify (optional)
4. Click **"💾 Save API Keys"**
5. Click **"🧪 Test Connections"** to verify

**📖 Detailed instructions in `api.txt`**

---

## 🎯 Usage

### Basic Workflow

1. **Launch** WebsiteNow using `startgpt.bat`

2. **Configure APIs** (first time only):
   - Go to "⚙️ API Settings" tab
   - Add at least one API key
   - Save and test

3. **Generate Website**:
   - Go to "🚀 Generator" tab
   - Enter project name
   - Describe your website in the text box
   - (Optional) Upload reference files
   - (Optional) Adjust advanced settings
   - Click **"✨ Generate My Website"**

4. **Monitor Progress**:
   - Watch the AI agents work in real-time
   - See progress bar and agent status
   - Generation takes 30-60 seconds

5. **Get Your Website**:
   - Click **"👁️ Preview Website"** to see it
   - Click **"📦 Download ZIP"** to save
   - Click **"📁 Open Folder"** to browse files

### Example Prompts

**Business Website:**
```
Create a modern consulting firm website with a clean, professional design.
Include a hero section, services showcase, team profiles, and contact form.
Use a blue and white color scheme with subtle animations.
Make it fully responsive and SEO-optimized.
```

**Portfolio:**
```
Design a creative portfolio for a photographer with image galleries,
about section, and client testimonials. Use a minimalist style with
earth tones and elegant typography.
```

**E-commerce:**
```
Build an online store for handmade jewelry with product showcase,
shopping cart interface, and secure checkout flow. Use an elegant
design with gold accents and professional product displays.
```

---

## 📁 File Structure

```
Z:\websitenow\
├── main.py                 # Main application entry point
├── installgpt.bat         # Installation script
├── startgpt.bat           # Launch script
├── requirements.txt       # Python dependencies
├── api.txt               # API setup guide
├── README.md             # This file
│
├── src/
│   ├── ui/               # User interface components
│   │   ├── main_window.py
│   │   ├── dashboard_widget.py
│   │   ├── generator_widget.py
│   │   └── api_config_widget.py
│   │
│   ├── agents/           # AI agents
│   │   ├── orchestrator.py
│   │   ├── understanding_agent.py
│   │   ├── design_agent.py
│   │   ├── code_agent.py
│   │   ├── content_agent.py
│   │   ├── qa_agent.py
│   │   └── deployment_agent.py
│   │
│   ├── api/              # API management
│   │   └── api_manager.py
│   │
│   └── core/             # Core functionality
│       └── config_manager.py
│
├── config/               # Configuration files
│   └── config.json      # (Created after first use)
│
├── output/               # Generated websites
│   └── project_*/       # (Each project gets its own folder)
│
└── uploads/              # Uploaded reference files
```

---

## 🎨 Advanced Options

### Design Styles
- **Modern & Clean** - Professional business sites
- **Classic & Professional** - Traditional corporate look
- **Creative & Artistic** - Unique, expressive designs
- **Minimalist & Simple** - Clean, focused layouts
- **Playful & Fun** - Colorful, engaging designs

### Color Schemes
- Blue (professional, trustworthy)
- Green (natural, growth)
- Purple (creative, innovative)
- Red (bold, energetic)
- Orange (friendly, warm)

### Complexity Levels
- **Simple** - Fast generation, basic features
- **Moderate** - Balanced features and quality (recommended)
- **Advanced** - Feature-rich, detailed implementation

### Technologies
- **Pure HTML/CSS/JS** - Vanilla web technologies
- **Tailwind CSS** - Utility-first CSS framework
- **Bootstrap** - Popular component framework

---

## 🚀 Deployment

Your generated website includes:
- ✅ Complete, production-ready code
- ✅ Deployment guide (`DEPLOYMENT_GUIDE.md`)
- ✅ README with project info
- ✅ ZIP file for easy upload

### Quick Deployment Options:

**1. Netlify (Recommended)**
- Go to https://www.netlify.com/
- Drag and drop your ZIP file
- Site is live instantly!

**2. Vercel**
- Go to https://vercel.com/
- Import your project
- Deploy with one click

**3. GitHub Pages**
- Create a GitHub repository
- Upload files
- Enable GitHub Pages in settings

**4. Traditional Hosting**
- Upload files via FTP
- Place in `public_html` directory

---

## 🐛 Troubleshooting

### Common Issues

**"No suitable API available"**
- Solution: Configure at least one API key in Settings

**"Python not found"**
- Solution: Install Python 3.9+ from python.org
- Make sure to check "Add Python to PATH" during installation

**"Required packages not installed"**
- Solution: Run `installgpt.bat` to install dependencies

**"Generation fails"**
- Check internet connection
- Verify API keys are correct
- Try a different API (app auto-rotates)
- Some APIs have rate limits - wait a few minutes

**"Slow generation"**
- Add Groq API (fastest)
- Complex websites take 30-60 seconds (normal)
- Check internet speed

---

## 💡 Tips & Best Practices

### Getting the Best Results:

1. **Be Specific** - Describe colors, sections, style in detail
2. **Use Examples** - Mention similar websites you like
3. **Start Simple** - Test with basic sites first
4. **Multiple APIs** - Configure 2-3 APIs for reliability
5. **Save Settings** - Backup `config\config.json` file

### API Usage:

- **Groq** - Use for most generations (fastest, generous)
- **Gemini** - Great for general websites
- **Claude** - Use for complex, high-quality sites
- **OpenRouter** - Good backup/variety

---

## 📊 Statistics

- **AI Agents**: 8 specialized agents
- **API Providers**: 8+ supported (all free-tier)
- **Supported Formats**: 10+ file types
- **Generation Speed**: 30-60 seconds average
- **Code Quality**: Professional, production-ready

---

## 🔒 Privacy & Security

- ✅ All API keys stored **locally only** (`Z:\websitenow\config\config.json`)
- ✅ No data sent to any server except AI providers
- ✅ You maintain full control of your keys
- ✅ Can delete keys anytime
- ✅ Open source - inspect the code yourself

---

## 📝 System Requirements

**Minimum:**
- Windows 7 or higher
- Python 3.9+
- 4GB RAM
- 500MB free disk space
- Internet connection

**Recommended:**
- Windows 10/11
- Python 3.11+
- 8GB RAM
- 1GB free disk space
- Stable broadband connection

---

## 🆘 Support

Need help?

1. **Check** `api.txt` for API setup
2. **Check** this README for general help
3. **Check** error messages in the console window
4. **Review** AI provider documentation

---

## 🎉 Credits

Built with:
- **PyQt6** - GUI framework
- **Multiple AI APIs** - Anthropic, Google, Groq, DeepSeek, OpenRouter, Cohere, Hugging Face
- **Python** - Core language

Special thanks to all the AI providers for their generous free tiers!

---

## 📜 License

MIT License - Feel free to use and modify!

---

## 🚀 Quick Reference

```cmd
# Installation
Double-click: installgpt.bat

# Launch Application
Double-click: startgpt.bat

# Manual Launch
python main.py

# Output Location
Z:\websitenow\output\

# Config Location
Z:\websitenow\config\config.json
```

---

**🎨 Happy Website Building!**

*Generated with ❤️ by WebsiteNow Team*
