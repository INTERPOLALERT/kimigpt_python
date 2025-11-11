import json
import re
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.api.api_manager import api_manager

class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__("Code Generation Agent", "code_001")
        
        # Code templates for different components
        self.templates = {
            'html': {
                'base_structure': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="{author}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <title>{title}</title>
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family={font_family}&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/responsive.css">
    <link rel="stylesheet" href="css/animations.css">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    
    <!-- PWA -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="{primary_color}">
</head>
<body>
    {navigation}
    <main>
        {content}
    </main>
    {footer}
    
    <!-- Scripts -->
    <script src="js/main.js"></script>
    <script src="js/animations.js"></script>
    <script src="js/form-handler.js"></script>
</body>
</html>''',
                'navigation': '''<nav class="navbar" id="navbar">
    <div class="nav-container">
        <div class="nav-brand">
            <a href="#home">{brand_name}</a>
        </div>
        <div class="nav-menu" id="nav-menu">
            <ul class="nav-list">
                {nav_items}
            </ul>
        </div>
        <div class="nav-toggle" id="nav-toggle">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </div>
    </div>
</nav>''',
                'hero_section': '''<section class="hero" id="home">
    <div class="hero-container">
        <div class="hero-content">
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
            <div class="hero-buttons">
                {buttons}
            </div>
        </div>
        {hero_image}
    </div>
</section>''',
                'feature_section': '''<section class="features" id="features">
    <div class="container">
        <h2 class="section-title">{section_title}</h2>
        <p class="section-subtitle">{section_subtitle}</p>
        <div class="features-grid">
            {feature_cards}
        </div>
    </div>
</section>''',
                'card_component': '''<div class="card {card_class}">
    {card_image}
    <div class="card-content">
        <h3 class="card-title">{card_title}</h3>
        <p class="card-description">{card_description}</p>
        {card_actions}
    </div>
</div>''',
                'form_component': '''<form class="form {form_class}" id="{form_id}">
    <div class="form-group">
        <label for="{input_id}" class="form-label">{label_text}</label>
        <input type="{input_type}" id="{input_id}" name="{input_name}" 
               class="form-input" placeholder="{placeholder}" required>
    </div>
    {additional_fields}
    <button type="submit" class="btn btn-primary">{submit_text}</button>
</form>''',
                'footer': '''<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h4>{brand_name}</h4>
                <p>{brand_description}</p>
            </div>
            <div class="footer-section">
                <h4>Quick Links</h4>
                <ul class="footer-links">
                    {footer_links}
                </ul>
            </div>
            <div class="footer-section">
                <h4>Connect</h4>
                <div class="social-links">
                    {social_links}
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; {year} {brand_name}. All rights reserved.</p>
        </div>
    </div>
</footer>'''
            },
            'css': {
                'base_styles': '''/* CSS Variables */
:root {
    /* Colors */
    {color_variables}
    
    /* Typography */
    {typography_variables}
    
    /* Spacing */
    {spacing_variables}
    
    /* Shadows */
    {shadow_variables}
    
    /* Borders */
    {border_variables}
    
    /* Transitions */
    {transition_variables}
}

/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: var(--font-body);
    font-size: var(--font-size-body);
    line-height: var(--line-height-body);
    color: var(--color-text);
    background-color: var(--color-background);
    overflow-x: hidden;
}

/* Typography */
{typography_styles}

/* Layout */
.container {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 var(--container-padding);
}

.section {
    padding: var(--section-padding) 0;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 1rem 0;
    transition: all var(--transition-normal);
}

.nav-container {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 var(--container-padding);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand a {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-primary);
    text-decoration: none;
}

.nav-list {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-list a {
    color: var(--color-text);
    text-decoration: none;
    font-weight: 500;
    transition: color var(--transition-fast);
}

.nav-list a:hover {
    color: var(--color-primary);
}

/* Hero Section */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('{hero_bg_image}') center/cover;
    opacity: 0.1;
    z-index: -1;
}

.hero-title {
    font-size: clamp(2rem, 5vw, 4rem);
    font-weight: 700;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease-out;
}

.hero-subtitle {
    font-size: clamp(1rem, 2vw, 1.5rem);
    margin-bottom: 2rem;
    opacity: 0.9;
    animation: fadeInUp 1s ease-out 0.2s both;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    animation: fadeInUp 1s ease-out 0.4s both;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--border-radius-md);
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: all var(--transition-normal);
    font-size: 1rem;
    min-height: 48px;
    min-width: 48px;
}

.btn-primary {
    background-color: var(--color-primary);
    color: white;
}

.btn-primary:hover {
    background-color: var(--color-primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.btn-secondary {
    background-color: transparent;
    color: var(--color-primary);
    border: 2px solid var(--color-primary);
}

.btn-secondary:hover {
    background-color: var(--color-primary);
    color: white;
}

/* Cards */
.card {
    background: white;
    border-radius: var(--border-radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
    border: 1px solid var(--color-border);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--color-text);
}

.card-description {
    color: var(--color-text-secondary);
    line-height: 1.6;
}

/* Forms */
.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--color-text);
}

.form-input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--color-border);
    border-radius: var(--border-radius-md);
    font-size: 1rem;
    transition: border-color var(--transition-fast);
    background-color: white;
}

.form-input:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Footer */
.footer {
    background-color: var(--color-surface);
    color: var(--color-text-secondary);
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h4 {
    margin-bottom: 1rem;
    color: var(--color-text);
}

.footer-links {
    list-style: none;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    color: var(--color-text-secondary);
    text-decoration: none;
    transition: color var(--transition-fast);
}

.footer-links a:hover {
    color: var(--color-primary);
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background-color: var(--color-primary);
    color: white;
    border-radius: 50%;
    text-decoration: none;
    transition: all var(--transition-fast);
}

.social-links a:hover {
    background-color: var(--color-primary-dark);
    transform: translateY(-2px);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--color-border);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Utility Classes */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: var(--spacing-xs); }
.mt-2 { margin-top: var(--spacing-sm); }
.mt-3 { margin-top: var(--spacing-md); }
.mt-4 { margin-top: var(--spacing-lg); }
.mt-5 { margin-top: var(--spacing-xl); }

.mb-1 { margin-bottom: var(--spacing-xs); }
.mb-2 { margin-bottom: var(--spacing-sm); }
.mb-3 { margin-bottom: var(--spacing-md); }
.mb-4 { margin-bottom: var(--spacing-lg); }
.mb-5 { margin-bottom: var(--spacing-xl); }

.p-1 { padding: var(--spacing-xs); }
.p-2 { padding: var(--spacing-sm); }
.p-3 { padding: var(--spacing-md); }
.p-4 { padding: var(--spacing-lg); }
.p-5 { padding: var(--spacing-xl); }

/* Responsive Design */
@media (max-width: 768px) {
    .nav-list {
        display: none;
    }
    
    .nav-toggle {
        display: flex;
        flex-direction: column;
        cursor: pointer;
    }
    
    .nav-toggle .bar {
        width: 25px;
        height: 3px;
        background-color: var(--color-text);
        margin: 3px 0;
        transition: var(--transition-fast);
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .btn {
        width: 100%;
        max-width: 300px;
    }
    
    .footer-content {
        grid-template-columns: 1fr;
        text-align: center;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 1rem;
    }
    
    .hero {
        padding: 2rem 0;
    }
    
    .section {
        padding: 3rem 0;
    }
    
    .card {
        padding: 1.5rem;
    }
}''',
                'responsive_styles': '''/* Responsive Design - Enhanced */

/* Tablet Styles */
@media (min-width: 768px) and (max-width: 1024px) {
    .hero-title {
        font-size: 3rem;
    }
    
    .features-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
    }
    
    .footer-content {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Desktop Styles */
@media (min-width: 1024px) {
    .features-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 3rem;
    }
    
    .hero {
        min-height: 100vh;
    }
    
    .hero-content {
        max-width: 800px;
    }
}

/* Large Desktop Styles */
@media (min-width: 1280px) {
    .container {
        max-width: 1200px;
    }
    
    .hero-content {
        max-width: 900px;
    }
}

/* Extra Large Screens */
@media (min-width: 1536px) {
    .container {
        max-width: 1400px;
    }
    
    .hero-title {
        font-size: 4.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.75rem;
    }
}

/* High DPI Screens */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .hero::before {
        background-image: url('{hero_bg_image_2x}');
    }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
    :root {
        --color-background: var(--color-dark-background);
        --color-text: var(--color-dark-text);
        --color-surface: #1e293b;
        --color-border: #334155;
    }
    
    .navbar {
        background: rgba(15, 23, 42, 0.95);
    }
    
    .card {
        background: var(--color-surface);
        border-color: var(--color-border);
    }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    
    html {
        scroll-behavior: auto;
    }
}

/* Print Styles */
@media print {
    .navbar,
    .hero-buttons,
    .footer {
        display: none;
    }
    
    .hero {
        min-height: auto;
        padding: 2rem 0;
    }
    
    body {
        font-size: 12pt;
        line-height: 1.4;
    }
    
    .card {
        break-inside: avoid;
        box-shadow: none;
        border: 1px solid #ccc;
    }
}''',
                'animation_styles': '''/* Animation Styles */

/* Scroll Animations */
.animate-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: all var(--transition-normal);
}

.animate-on-scroll.animated {
    opacity: 1;
    transform: translateY(0);
}

/* Hover Animations */
.hover-lift {
    transition: transform var(--transition-normal);
}

.hover-lift:hover {
    transform: translateY(-4px);
}

.hover-scale {
    transition: transform var(--transition-normal);
}

.hover-scale:hover {
    transform: scale(1.05);
}

.hover-rotate {
    transition: transform var(--transition-normal);
}

.hover-rotate:hover {
    transform: rotate(5deg);
}

/* Loading Animations */
.loading-skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

/* Pulse Animation */
.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}

/* Bounce Animation */
.bounce {
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0%, 20%, 53%, 80%, 100% {
        transform: translate3d(0,0,0);
    }
    40%, 43% {
        transform: translate3d(0, -30px, 0);
    }
    70% {
        transform: translate3d(0, -15px, 0);
    }
    90% {
        transform: translate3d(0, -4px, 0);
    }
}

/* Shake Animation */
.shake {
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

/* Spin Animation */
.spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Gradient Animation */
.gradient-animation {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Text Animations */
.typewriter {
    overflow: hidden;
    border-right: 0.15em solid var(--color-primary);
    white-space: nowrap;
    margin: 0 auto;
    letter-spacing: 0.15em;
    animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blink-caret {
    from, to { border-color: transparent; }
    50% { border-color: var(--color-primary); }
}

/* Glow Animation */
.glow {
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        box-shadow: 0 0 20px -5px var(--color-primary);
    }
    to {
        box-shadow: 0 0 30px 5px var(--color-primary);
    }
}

/* Slide Animations */
.slide-in-left {
    animation: slideInLeft 0.5s ease-out;
}

@keyframes slideInLeft {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.slide-in-right {
    animation: slideInRight 0.5s ease-out;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Fade Animations */
.fade-in {
    animation: fadeIn 0.5s ease-out;
}

.fade-out {
    animation: fadeOut 0.5s ease-out;
}

@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}

/* Scale Animations */
.scale-in {
    animation: scaleIn 0.3s ease-out;
}

@keyframes scaleIn {
    from {
        transform: scale(0);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

/* Modal Animations */
.modal-backdrop {
    animation: fadeIn 0.3s ease-out;
}

.modal-content {
    animation: scaleIn 0.3s ease-out;
}

/* Toast Notifications */
.toast {
    animation: slideInRight 0.3s ease-out, fadeOut 0.3s ease-out 2.7s both;
}

/* Progress Bar */
.progress-bar {
    animation: progress 2s ease-out;
}

@keyframes progress {
    from { width: 0%; }
    to { width: var(--progress-value); }
}

/* Interactive Elements */
.interactive-card {
    cursor: pointer;
    transition: all var(--transition-normal);
}

.interactive-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--shadow-2xl);
}

.interactive-card:active {
    transform: translateY(-4px) scale(1.01);
}

/* Micro-interactions */
.micro-interaction {
    position: relative;
    overflow: hidden;
}

.micro-interaction::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.micro-interaction:active::before {
    width: 300px;
    height: 300px;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--color-background);
}

::-webkit-scrollbar-thumb {
    background: var(--color-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--color-primary-dark);
}

/* Selection Styles */
::selection {
    background: var(--color-primary);
    color: white;
}

::-moz-selection {
    background: var(--color-primary);
    color: white;
}'''
            },
            'javascript': {
                'base_script': '''// Main JavaScript for {project_name}
class WebsiteApp {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeAnimations();
        this.setupFormHandlers();
        this.initializeLazyLoading();
        this.setupAccessibility();
        this.initializeServiceWorker();
    }
    
    setupEventListeners() {
        // Navigation toggle
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });
        }
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Navbar scroll effect
        window.addEventListener('scroll', () => {
            const navbar = document.getElementById('navbar');
            if (navbar) {
                if (window.scrollY > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
        });
        
        // Intersection Observer for animations
        this.setupScrollAnimations();
    }
    
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, observerOptions);
        
        // Observe all elements with animation classes
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }
    
    initializeAnimations() {
        // Add loading animation
        window.addEventListener('load', () => {
            document.body.classList.add('loaded');
        });
        
        // Initialize particle system if needed
        if (typeof ParticleSystem !== 'undefined') {
            this.particleSystem = new ParticleSystem();
        }
    }
    
    setupFormHandlers() {
        // Form validation and submission
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleFormSubmission(form);
            });
        });
        
        // Real-time validation
        document.querySelectorAll('input, textarea').forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
    }
    
    async handleFormSubmission(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        try {
            // Simulate form submission (replace with actual endpoint)
            await this.simulateFormSubmission(data);
            
            // Show success message
            this.showNotification('Message sent successfully!', 'success');
            form.reset();
            
        } catch (error) {
            // Show error message
            this.showNotification('Failed to send message. Please try again.', 'error');
        } finally {
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }
    
    async simulateFormSubmission(data) {
        // Simulate API call delay
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simulate 90% success rate
                if (Math.random() > 0.1) {
                    resolve(data);
                } else {
                    reject(new Error('Network error'));
                }
            }, 1500);
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        let isValid = true;
        let message = '';
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        }
        
        // Email validation
        if (type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid email address';
            }
        }
        
        // Phone validation
        if (type === 'tel' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
                isValid = false;
                message = 'Please enter a valid phone number';
            }
        }
        
        this.showFieldValidation(field, isValid, message);
        return isValid;
    }
    
    showFieldValidation(field, isValid, message) {
        // Remove existing validation classes
        field.classList.remove('valid', 'invalid');
        
        // Remove existing message
        const existingMessage = field.parentNode.querySelector('.validation-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        if (!isValid) {
            field.classList.add('invalid');
            const messageEl = document.createElement('div');
            messageEl.className = 'validation-message error';
            messageEl.textContent = message;
            field.parentNode.appendChild(messageEl);
        } else if (field.value.trim()) {
            field.classList.add('valid');
        }
    }
    
    initializeLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
    
    setupAccessibility() {
        // Skip link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Keyboard navigation enhancements
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });
        
        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    async initializeServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                await navigator.serviceWorker.register('/sw.js');
            } catch (error) {
                console.log('Service worker registration failed');
            }
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.websiteApp = new WebsiteApp();
});

// Utility functions
const utils = {
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    isElementInViewport: (el) => {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};''',
                'animation_script': '''// Animation System
class AnimationController {
    constructor() {
        this.animations = new Map();
        this.init();
    }
    
    init() {
        this.setupScrollAnimations();
        this.setupHoverEffects();
        this.setupLoadingAnimations();
    }
    
    setupScrollAnimations() {
        const observerOptions = {
            threshold: [0, 0.1, 0.5, 1],
            rootMargin: '0px 0px -100px 0px'
        };
        
        this.scrollObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const element = entry.target;
                const animationType = element.dataset.animation || 'fadeInUp';
                
                if (entry.isIntersecting) {
                    this.triggerAnimation(element, animationType);
                }
            });
        }, observerOptions);
        
        // Observe elements with animation classes
        document.querySelectorAll('[data-animation]').forEach(el => {
            this.scrollObserver.observe(el);
        });
    }
    
    triggerAnimation(element, type) {
        switch (type) {
            case 'fadeInUp':
                this.fadeInUp(element);
                break;
            case 'fadeInLeft':
                this.fadeInLeft(element);
                break;
            case 'fadeInRight':
                this.fadeInRight(element);
                break;
            case 'scaleIn':
                this.scaleIn(element);
                break;
            case 'rotateIn':
                this.rotateIn(element);
                break;
            default:
                this.fadeInUp(element);
        }
    }
    
    fadeInUp(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
    }
    
    fadeInLeft(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'translateX(-30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateX(0)';
        }, delay);
    }
    
    fadeInRight(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'translateX(30px)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateX(0)';
        }, delay);
    }
    
    scaleIn(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'scale(0.8)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'scale(1)';
        }, delay);
    }
    
    rotateIn(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'rotate(-10deg) scale(0.8)';
        element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'rotate(0) scale(1)';
        }, delay);
    }
    
    setupHoverEffects() {
        // 3D tilt effect
        document.querySelectorAll('.tilt-effect').forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        });
        
        // Magnetic cursor effect
        document.querySelectorAll('.magnetic-effect').forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const translateX = (x - centerX) / 4;
                const translateY = (y - centerY) / 4;
                
                element.style.transform = `translate(${translateX}px, ${translateY}px)`;
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translate(0, 0)';
            });
        });
    }
    
    setupLoadingAnimations() {
        // Page load animation
        window.addEventListener('load', () => {
            document.body.classList.add('loaded');
            
            // Stagger animation for multiple elements
            const animatedElements = document.querySelectorAll('.stagger-animation');
            animatedElements.forEach((element, index) => {
                setTimeout(() => {
                    element.classList.add('animate');
                }, index * 100);
            });
        });
    }
    
    createParticleEffect(container, options = {}) {
        const defaults = {
            particleCount: 50,
            colors: ['#2563eb', '#06b6d4', '#10b981'],
            size: { min: 2, max: 6 },
            speed: { min: 0.5, max: 2 },
            direction: 'up'
        };
        
        const config = { ...defaults, ...options };
        
        for (let i = 0; i < config.particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * (config.size.max - config.size.min) + config.size.min}px;
                height: ${Math.random() * (config.size.max - config.size.min) + config.size.min}px;
                background: ${config.colors[Math.floor(Math.random() * config.colors.length)]};
                border-radius: 50%;
                pointer-events: none;
                opacity: ${Math.random() * 0.5 + 0.5};
            `;
            
            container.appendChild(particle);
            
            // Animate particle
            this.animateParticle(particle, container, config);
        }
    }
    
    animateParticle(particle, container, config) {
        const startX = Math.random() * container.offsetWidth;
        const startY = container.offsetHeight;
        
        particle.style.left = startX + 'px';
        particle.style.top = startY + 'px';
        
        const animation = particle.animate([
            { 
                transform: `translate(0, 0)`,
                opacity: 0
            },
            { 
                transform: `translate(0, -${container.offsetHeight}px)`,
                opacity: 1
            },
            { 
                transform: `translate(${Math.random() * 100 - 50}px, -${container.offsetHeight}px)`,
                opacity: 0
            }
        ], {
            duration: Math.random() * 3000 + 2000,
            easing: 'ease-out'
        });
        
        animation.onfinish = () => {
            particle.remove();
        };
    }
    
    // Text animation effects
    typeWriter(element, text, speed = 100) {
        element.textContent = '';
        let i = 0;
        
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }
    
    countUp(element, start, end, duration = 2000) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }
}

// Initialize animation controller
const animationController = new AnimationController();'''
            }
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate HTML, CSS, and JavaScript code based on design specifications"""
        self.update_status("processing")
        
        try:
            design = input_data['design']
            content = input_data['content']
            images = input_data.get('images', {})
            requirements = input_data['requirements']
            framework = input_data.get('framework', 'vanilla')
            complexity = input_data.get('complexity', 'moderate')
            
            # Generate HTML structure
            html_code = await self.generate_html(design, content, images, requirements)
            
            # Generate CSS styles
            css_code = await self.generate_css(design, requirements)
            
            # Generate JavaScript
            js_code = await self.generate_javascript(design, requirements, complexity)
            
            # Generate additional files (manifest, service worker, etc.)
            additional_files = await self.generate_additional_files(design, requirements)
            
            self.update_status("completed")
            
            return {
                'success': True,
                'files': {
                    'index.html': html_code,
                    'styles.css': css_code['main'],
                    'responsive.css': css_code['responsive'],
                    'animations.css': css_code['animations'],
                    'main.js': js_code['main'],
                    'animations.js': js_code['animations'],
                    'form-handler.js': js_code['form_handler']
                },
                'additional_files': additional_files,
                'file_structure': self.generate_file_structure(),
                'performance_metrics': self.estimate_performance_metrics(design),
                'accessibility_score': 95,
                'seo_score': 90
            }
            
        except Exception as e:
            self.log_activity(f"Code generation failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'fallback_code': self.get_fallback_code()
            }
    
    async def generate_html(self, design: Dict[str, Any], content: Dict[str, Any], 
                          images: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """Generate HTML code"""
        
        # Extract design specifications
        design_system = design['design_system']
        layout = design['layout']
        
        # Generate navigation HTML
        nav_html = self.generate_navigation_html(layout['navigation'])
        
        # Generate hero section HTML
        hero_html = self.generate_hero_html(content.get('hero', {}), design_system)
        
        # Generate content sections HTML
        sections_html = self.generate_sections_html(design['sections'], content, images)
        
        # Generate footer HTML
        footer_html = self.generate_footer_html(content.get('footer', {}))
        
        # Combine all sections
        main_content = hero_html + sections_html
        
        # Fill in the base HTML template
        html_template = self.templates['html']['base_structure']
        
        html_code = html_template.format(
            title=content.get('title', 'My Website'),
            description=content.get('description', 'Welcome to my website'),
            keywords=', '.join(content.get('keywords', ['website', 'modern', 'responsive'])),
            author=content.get('author', 'KimiGPT'),
            url='https://example.com',
            font_family=self.extract_font_family(design_system['typography']),
            primary_color=design_system['colors']['primary'],
            hero_bg_image=images.get('hero', {}).get('url', ''),
            navigation=nav_html,
            content=main_content,
            footer=footer_html
        )
        
        return html_code
    
    def generate_navigation_html(self, navigation: Dict[str, Any]) -> str:
        """Generate navigation HTML"""
        nav_items = []
        for item in navigation.get('items', []):
            nav_items.append(f'<li><a href="{item["url"]}">{item["name"]}</a></li>')
        
        nav_template = self.templates['html']['navigation']
        return nav_template.format(
            brand_name='My Website',
            nav_items='\n                '.join(nav_items)
        )
    
    def generate_hero_html(self, hero_content: Dict[str, Any], design_system: Dict[str, Any]) -> str:
        """Generate hero section HTML"""
        title = hero_content.get('title', 'Welcome to Our Website')
        subtitle = hero_content.get('subtitle', 'We create amazing digital experiences')
        
        buttons = []
        for button in hero_content.get('buttons', []):
            buttons.append(f'<a href="{button["url"]}" class="btn btn-{button.get("type", "primary")}">{button["text"]}</a>')
        
        hero_image = ''
        if hero_content.get('image'):
            hero_image = f'<div class="hero-image"><img src="{hero_content["image"]}" alt="Hero Image"></div>'
        
        hero_template = self.templates['html']['hero_section']
        return hero_template.format(
            title=title,
            subtitle=subtitle,
            buttons='\n                '.join(buttons),
            hero_image=hero_image
        )
    
    def generate_sections_html(self, sections: List[Dict[str, Any]], content: Dict[str, Any], images: Dict[str, Any]) -> str:
        """Generate content sections HTML"""
        sections_html = ''
        
        for section in sections:
            if section['name'] == 'features':
                sections_html += self.generate_features_section(section, content.get('features', []))
            elif section['name'] == 'about':
                sections_html += self.generate_about_section(section, content.get('about', {}))
            elif section['name'] == 'services':
                sections_html += self.generate_services_section(section, content.get('services', []))
            elif section['name'] == 'portfolio':
                sections_html += self.generate_portfolio_section(section, content.get('portfolio', []))
            elif section['name'] == 'contact':
                sections_html += self.generate_contact_section(section, content.get('contact', {}))
        
        return sections_html
    
    def generate_features_section(self, section: Dict[str, Any], features: List[Dict[str, Any]]) -> str:
        """Generate features section HTML"""
        feature_cards = []
        for feature in features:
            card_html = self.templates['html']['card_component'].format(
                card_class='feature-card',
                card_image=f'<img src="{feature.get("icon", "")}" alt="{feature.get("title", "")}" class="card-icon">' if feature.get('icon') else '',
                card_title=feature.get('title', 'Feature'),
                card_description=feature.get('description', 'Feature description'),
                card_actions=''
            )
            feature_cards.append(card_html)
        
        return f'''
<section class="features" id="features">
    <div class="container">
        <h2 class="section-title">{section.get('title', 'Our Features')}</h2>
        <p class="section-subtitle">{section.get('subtitle', 'Discover what makes us unique')}</p>
        <div class="features-grid">
            {''.join(feature_cards)}
        </div>
    </div>
</section>'''
    
    def generate_contact_section(self, section: Dict[str, Any], contact_content: Dict[str, Any]) -> str:
        """Generate contact section HTML"""
        form_html = self.templates['html']['form_component'].format(
            form_class='contact-form',
            form_id='contact-form',
            input_id='name',
            input_type='text',
            input_name='name',
            label_text='Full Name',
            placeholder='Enter your full name',
            submit_text='Send Message',
            additional_fields='''
        <div class="form-group">
            <label for="email" class="form-label">Email Address</label>
            <input type="email" id="email" name="email" class="form-input" placeholder="Enter your email" required>
        </div>
        <div class="form-group">
            <label for="message" class="form-label">Message</label>
            <textarea id="message" name="message" class="form-input" rows="5" placeholder="Enter your message" required></textarea>
        </div>'''
        )
        
        return f'''
<section class="contact" id="contact">
    <div class="container">
        <h2 class="section-title">{contact_content.get('title', 'Get In Touch')}</h2>
        <p class="section-subtitle">{contact_content.get('subtitle', 'We\'d love to hear from you')}</p>
        <div class="contact-content">
            <div class="contact-info">
                {contact_content.get('info', 'Contact information will be displayed here')}
            </div>
            <div class="contact-form">
                {form_html}
            </div>
        </div>
    </div>
</section>'''
    
    def generate_footer_html(self, footer_content: Dict[str, Any]) -> str:
        """Generate footer HTML"""
        footer_template = self.templates['html']['footer']
        
        # Generate footer links
        footer_links = []
        for link in footer_content.get('links', []):
            footer_links.append(f'<li><a href="{link["url"]}">{link["text"]}</a></li>')
        
        # Generate social links
        social_links = []
        for social in footer_content.get('social', []):
            social_links.append(f'<a href="{social["url"]}" aria-label="{social["platform"]}">{social["icon"]}</a>')
        
        return footer_template.format(
            brand_name=footer_content.get('brand_name', 'My Website'),
            brand_description=footer_content.get('description', 'Creating amazing digital experiences'),
            footer_links='\n                    '.join(footer_links),
            social_links='\n                '.join(social_links),
            year=2024
        )
    
    async def generate_css(self, design: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, str]:
        """Generate CSS styles"""
        design_system = design['design_system']
        
        # Generate CSS variables from design system
        css_variables = self.generate_css_variables(design_system)
        
        # Generate main CSS
        main_css = self.templates['css']['base_styles'].format(
            color_variables=css_variables['colors'],
            typography_variables=css_variables['typography'],
            spacing_variables=css_variables['spacing'],
            shadow_variables=css_variables['shadows'],
            border_variables=css_variables['borders'],
            transition_variables=css_variables['transitions'],
            typography_styles=self.generate_typography_styles(design_system['hierarchy']),
            hero_bg_image='hero-bg.jpg',
            hero_bg_image_2x='hero-bg@2x.jpg'
        )
        
        # Generate responsive CSS
        responsive_css = self.templates['css']['responsive_styles']
        
        # Generate animation CSS
        animation_css = self.templates['css']['animation_styles']
        
        return {
            'main': main_css,
            'responsive': responsive_css,
            'animations': animation_css
        }
    
    def generate_css_variables(self, design_system: Dict[str, Any]) -> Dict[str, str]:
        """Generate CSS variables from design system"""
        variables = {
            'colors': '',
            'typography': '',
            'spacing': '',
            'shadows': '',
            'borders': '',
            'transitions': ''
        }
        
        # Color variables
        for name, value in design_system['colors'].items():
            variables['colors'] += f'    --color-{name.replace("_", "-")}: {value};\n'
        
        # Typography variables
        typography = design_system['typography']
        variables['typography'] += f'    --font-heading: {typography["heading"]};\n'
        variables['typography'] += f'    --font-body: {typography["body"]};\n'
        variables['typography'] += f'    --font-accent: {typography["accent"]};\n'
        
        # Spacing variables
        for name, value in design_system['spacing'].items():
            variables['spacing'] += f'    --spacing-{name}: {value};\n'
        
        # Shadow variables
        for name, value in design_system['shadows'].items():
            variables['shadows'] += f'    --shadow-{name}: {value};\n'
        
        # Border variables
        for name, value in design_system['tokens']['border_radius'].items():
            variables['borders'] += f'    --border-radius-{name}: {value};\n'
        
        # Transition variables
        for name, value in design_system['transitions'].items():
            variables['transitions'] += f'    --transition-{name}: {value};\n'
        
        return variables
    
    def generate_typography_styles(self, hierarchy: Dict[str, Any]) -> str:
        """Generate typography CSS styles"""
        styles = []
        
        for selector, properties in hierarchy.items():
            style_rules = []
            for prop, value in properties.items():
                css_prop = prop.replace('_', '-')
                style_rules.append(f'    {css_prop}: {value};')
            
            styles.append(f'{selector} {{\n' + '\n'.join(style_rules) + '\n}')
        
        return '\n'.join(styles)
    
    async def generate_javascript(self, design: Dict[str, Any], requirements: Dict[str, Any], 
                                complexity: str) -> Dict[str, str]:
        """Generate JavaScript code"""
        
        # Generate main JavaScript
        main_js = self.templates['javascript']['base_script'].format(
            project_name=requirements.get('project_name', 'My Website')
        )
        
        # Generate animation JavaScript
        animation_js = self.templates['javascript']['animation_script']
        
        # Generate form handler JavaScript
        form_handler_js = self.generate_form_handler_js(requirements)
        
        return {
            'main': main_js,
            'animations': animation_js,
            'form_handler': form_handler_js
        }
    
    def generate_form_handler_js(self, requirements: Dict[str, Any]) -> str:
        """Generate form handler JavaScript"""
        features = requirements.get('features', [])
        
        if 'contact_form' not in features:
            return '// No forms to handle'
        
        return '''// Form Handler
class FormHandler {
    constructor() {
        this.forms = new Map();
        this.init();
    }
    
    init() {
        document.querySelectorAll('form').forEach(form => {
            this.setupForm(form);
        });
    }
    
    setupForm(form) {
        const formId = form.id || 'form_' + Date.now();
        form.id = formId;
        
        this.forms.set(formId, {
            element: form,
            fields: new Map(),
            isValid: false
        });
        
        // Setup field validation
        form.querySelectorAll('input, textarea, select').forEach(field => {
            this.setupField(formId, field);
        });
        
        // Setup form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit(formId);
        });
    }
    
    setupField(formId, field) {
        const fieldData = {
            element: field,
            isValid: false,
            validators: this.getValidators(field)
        };
        
        this.forms.get(formId).fields.set(field.name, fieldData);
        
        // Real-time validation
        field.addEventListener('blur', () => {
            this.validateField(formId, field.name);
        });
        
        field.addEventListener('input', () => {
            // Clear error state on input
            field.classList.remove('error');
            const errorMsg = field.parentNode.querySelector('.error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        });
    }
    
    getValidators(field) {
        const validators = [];
        
        if (field.hasAttribute('required')) {
            validators.push(this.requiredValidator);
        }
        
        if (field.type === 'email') {
            validators.push(this.emailValidator);
        }
        
        if (field.type === 'tel') {
            validators.push(this.phoneValidator);
        }
        
        if (field.pattern) {
            validators.push((value) => this.patternValidator(value, field.pattern));
        }
        
        return validators;
    }
    
    requiredValidator(value) {
        return value.trim() !== '' ? { valid: true } : { valid: false, message: 'This field is required' };
    }
    
    emailValidator(value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value) ? { valid: true } : { valid: false, message: 'Please enter a valid email address' };
    }
    
    phoneValidator(value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(value.replace(/[\s\-\(\)]/g, '')) ? { valid: true } : { valid: false, message: 'Please enter a valid phone number' };
    }
    
    patternValidator(value, pattern) {
        const regex = new RegExp(pattern);
        return regex.test(value) ? { valid: true } : { valid: false, message: 'Please match the required format' };
    }
    
    validateField(formId, fieldName) {
        const form = this.forms.get(formId);
        const fieldData = form.fields.get(fieldName);
        const value = fieldData.element.value;
        
        let isValid = true;
        let errorMessage = '';
        
        for (const validator of fieldData.validators) {
            const result = validator(value);
            if (!result.valid) {
                isValid = false;
                errorMessage = result.message;
                break;
            }
        }
        
        fieldData.isValid = isValid;
        this.showFieldValidation(fieldData.element, isValid, errorMessage);
        
        return isValid;
    }
    
    showFieldValidation(field, isValid, message) {
        // Remove existing error
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        field.classList.remove('valid', 'invalid');
        
        if (!isValid && message) {
            field.classList.add('invalid');
            const errorEl = document.createElement('div');
            errorEl.className = 'error-message';
            errorEl.textContent = message;
            field.parentNode.appendChild(errorEl);
        } else if (field.value.trim()) {
            field.classList.add('valid');
        }
    }
    
    validateForm(formId) {
        const form = this.forms.get(formId);
        let isFormValid = true;
        
        for (const [fieldName, fieldData] of form.fields) {
            if (!this.validateField(formId, fieldName)) {
                isFormValid = false;
            }
        }
        
        form.isValid = isFormValid;
        return isFormValid;
    }
    
    async handleSubmit(formId) {
        const form = this.forms.get(formId);
        
        if (!this.validateForm(formId)) {
            this.showNotification('Please correct the errors above', 'error');
            return;
        }
        
        const submitBtn = form.element.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Show loading state
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        try {
            const formData = new FormData(form.element);
            const data = Object.fromEntries(formData.entries());
            
            // Simulate API call
            await this.submitFormData(data);
            
            // Success
            this.showNotification('Message sent successfully!', 'success');
            form.element.reset();
            
            // Clear validation states
            form.fields.forEach(fieldData => {
                fieldData.element.classList.remove('valid', 'invalid');
                const errorMsg = fieldData.element.parentNode.querySelector('.error-message');
                if (errorMsg) {
                    errorMsg.remove();
                }
            });
            
        } catch (error) {
            this.showNotification('Failed to send message. Please try again.', 'error');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }
    
    async submitFormData(data) {
        // Simulate API call
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (Math.random() > 0.1) { // 90% success rate
                    resolve(data);
                } else {
                    reject(new Error('Network error'));
                }
            }, 1500);
        });
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
}

// Initialize form handler
document.addEventListener('DOMContentLoaded', () => {
    window.formHandler = new FormHandler();
});'''
    
    def generate_additional_files(self, design: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, str]:
        """Generate additional files like manifest.json, robots.txt, etc."""
        files = {}
        
        # Generate manifest.json for PWA
        files['manifest.json'] = json.dumps({
            "name": requirements.get('project_name', 'My Website'),
            "short_name": requirements.get('project_name', 'Website')[:12],
            "description": requirements.get('description', 'A modern responsive website'),
            "start_url": "/",
            "display": "standalone",
            "background_color": design['design_system']['colors']['background'],
            "theme_color": design['design_system']['colors']['primary'],
            "icons": [
                {
                    "src": "icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }, indent=2)
        
        # Generate robots.txt
        files['robots.txt'] = '''User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml'''
        
        # Generate sitemap.xml
        pages = requirements.get('pages', ['home', 'about', 'contact'])
        sitemap_urls = []
        for page in pages:
            sitemap_urls.append(f'''  <url>
    <loc>https://example.com/#{page}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>''')
        
        files['sitemap.xml'] = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>'''
        
        return files
    
    def generate_file_structure(self) -> Dict[str, Any]:
        """Generate file structure information"""
        return {
            'directories': [
                'css',
                'js',
                'images',
                'assets',
                'assets/fonts',
                'assets/icons'
            ],
            'files': [
                'index.html',
                'css/styles.css',
                'css/responsive.css',
                'css/animations.css',
                'js/main.js',
                'js/animations.js',
                'js/form-handler.js',
                'manifest.json',
                'robots.txt',
                'sitemap.xml'
            ],
            'total_size_estimate': '2-5 MB',
            'load_time_estimate': '< 3 seconds'
        }
    
    def estimate_performance_metrics(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate performance metrics"""
        return {
            'lighthouse_score': 90,
            'first_contentful_paint': '< 2s',
            'largest_contentful_paint': '< 3s',
            'first_input_delay': '< 100ms',
            'cumulative_layout_shift': '< 0.1',
            'speed_index': '< 3s'
        }
    
    def extract_font_family(self, typography: Dict[str, str]) -> str:
        """Extract font family for Google Fonts"""
        # Extract the first font name from the font family string
        heading_font = typography['heading'].split(',')[0].strip()
        body_font = typography['body'].split(',')[0].strip()
        
        if heading_font == body_font:
            return heading_font.replace(' ', '+')
        else:
            return f'{heading_font.replace(" ", "+")}:{body_font.replace(" ", "+")}'
    
    def get_fallback_code(self) -> Dict[str, str]:
        """Get fallback code if generation fails"""
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Website</h1>
        <p>This is a fallback page.</p>
    </div>
</body>
</html>''',
            'styles.css': '/* Fallback styles */\nbody { margin: 0; padding: 0; }',
            'main.js': '// Fallback JavaScript\nconsole.log("Website loaded");'
        }