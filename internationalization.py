#!/usr/bin/env python3
"""
Internationalization (i18n) Module for WiFi Security Radar Suite
Provides multi-language support and localization features
"""

import json
import os
from typing import Dict, Any, Optional
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QMessageBox, QGroupBox, QTextEdit
)
from PyQt5.QtCore import QObject, pyqtSignal, QLocale, QTranslator
from PyQt5.QtGui import QFont


class TranslationManager(QObject):
    """Manages translations and language switching"""
    
    language_changed = pyqtSignal(str)  # language_code
    
    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.translations = {}
        self.available_languages = {}
        self._load_translations()
        
    def _load_translations(self):
        """Load all available translations"""
        translations_dir = "translations"
        
        # Create translations directory if it doesn't exist
        if not os.path.exists(translations_dir):
            os.makedirs(translations_dir)
            
        # Define available languages
        self.available_languages = {
            "en": "English",
            "es": "Español", 
            "fr": "Français",
            "de": "Deutsch",
            "it": "Italiano",
            "pt": "Português",
            "ru": "Русский",
            "zh": "中文",
            "ja": "日本語",
            "ko": "한국어",
            "ar": "العربية"
        }
        
        # Load translation files
        for lang_code in self.available_languages.keys():
            translation_file = os.path.join(translations_dir, f"{lang_code}.json")
            
            if os.path.exists(translation_file):
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Failed to load translation for {lang_code}: {e}")
                    self.translations[lang_code] = {}
            else:
                # Create default translation file
                self.translations[lang_code] = {}
                self._create_default_translation(lang_code, translation_file)
                
        # Set system default language
        system_locale = QLocale.system().name()[:2]
        if system_locale in self.available_languages:
            self.current_language = system_locale
            
    def _create_default_translation(self, lang_code, file_path):
        """Create default translation file with English strings"""
        default_translations = self._get_default_translations()
        
        # If not English, create empty template for translation
        if lang_code != "en":
            translated = {}
            for section, strings in default_translations.items():
                translated[section] = {}
                for key, value in strings.items():
                    translated[section][key] = f"[{lang_code.upper()}] {value}"
        else:
            translated = default_translations
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translated, f, indent=2, ensure_ascii=False)
            self.translations[lang_code] = translated
        except Exception as e:
            print(f"Failed to create default translation for {lang_code}: {e}")
            
    def _get_default_translations(self):
        """Get default English translations"""
        return {
            "main_window": {
                "title": "WiFi Security Radar Suite",
                "scan_button": "Start Scan",
                "stop_button": "Stop Scan", 
                "refresh_button": "Refresh",
                "export_button": "Export Data",
                "settings_button": "Settings",
                "help_button": "Help",
                "about_button": "About",
                "exit_button": "Exit"
            },
            "menu": {
                "file": "File",
                "edit": "Edit", 
                "view": "View",
                "tools": "Tools",
                "help": "Help",
                "new_scan": "New Scan",
                "save_results": "Save Results",
                "export_data": "Export Data",
                "preferences": "Preferences",
                "accessibility": "Accessibility",
                "language": "Language"
            },
            "toolbar": {
                "scan": "Scan Networks",
                "stop": "Stop Scanning",
                "refresh": "Refresh Display",
                "export": "Export Results",
                "graphs": "Show Graphs",
                "zoom_in": "Zoom In",
                "zoom_out": "Zoom Out",
                "fullscreen": "Fullscreen"
            },
            "network_info": {
                "ssid": "Network Name (SSID)",
                "bssid": "MAC Address (BSSID)",
                "security": "Security Type",
                "signal": "Signal Strength",
                "channel": "Channel",
                "frequency": "Frequency",
                "vendor": "Vendor",
                "last_seen": "Last Seen",
                "distance": "Estimated Distance",
                "threat_level": "Threat Level"
            },
            "security_types": {
                "open": "Open Network",
                "wep": "WEP Encryption",
                "wpa": "WPA Encryption", 
                "wpa2": "WPA2 Encryption",
                "wpa3": "WPA3 Encryption",
                "unknown": "Unknown Security"
            },
            "threat_levels": {
                "critical": "Critical Risk",
                "high": "High Risk",
                "medium": "Medium Risk",
                "low": "Low Risk",
                "minimal": "Minimal Risk"
            },
            "graphs": {
                "signal_strength": "Signal Strength",
                "network_activity": "Network Activity", 
                "security_trends": "Security Trends",
                "real_time_monitoring": "Real-time Monitoring Dashboard",
                "auto_update": "Auto Update",
                "update_interval": "Update Interval (seconds)",
                "clear_data": "Clear Data"
            },
            "export": {
                "title": "Export WiFi Data",
                "format": "Export Format",
                "csv_format": "CSV (Comma Separated Values)",
                "json_format": "JSON (JavaScript Object Notation)",
                "html_format": "HTML Report (Web Page)",
                "include_metadata": "Include scan metadata",
                "pretty_format": "Pretty formatting",
                "output_file": "Output File",
                "browse": "Browse...",
                "export_button": "Export Data",
                "cancel": "Cancel",
                "success": "Data successfully exported",
                "failed": "Export failed"
            },
            "accessibility": {
                "title": "Accessibility Settings",
                "visual_accessibility": "Visual Accessibility",
                "high_contrast": "Enable High Contrast Mode",
                "enhanced_focus": "Enhanced Focus Indicators", 
                "font_size": "Font Size",
                "navigation": "Navigation",
                "keyboard_navigation": "Enhanced Keyboard Navigation",
                "screen_reader": "Screen Reader Support",
                "themes": "Accessibility Themes",
                "theme": "Theme",
                "apply": "Apply Settings",
                "reset": "Reset to Defaults",
                "close": "Close"
            },
            "scanner": {
                "status_scanning": "Scanning for networks...",
                "status_stopped": "Scan stopped",
                "status_complete": "Scan complete",
                "networks_found": "networks found",
                "no_networks": "No networks detected",
                "scan_error": "Scan error occurred",
                "interface_error": "No wireless interface detected",
                "permission_error": "Permission denied - run as root"
            },
            "dialogs": {
                "error": "Error",
                "warning": "Warning", 
                "information": "Information",
                "confirmation": "Confirm",
                "yes": "Yes",
                "no": "No",
                "ok": "OK",
                "cancel": "Cancel",
                "apply": "Apply",
                "close": "Close"
            },
            "status": {
                "ready": "Ready",
                "scanning": "Scanning...",
                "processing": "Processing...",
                "exporting": "Exporting...",
                "error": "Error",
                "connected": "Connected",
                "disconnected": "Disconnected"
            },
            "help": {
                "keyboard_shortcuts": "Keyboard Shortcuts",
                "about_title": "About WiFi Security Radar",
                "about_text": "Professional WiFi Security Analysis Tool v5.0",
                "copyright": "© 2025 WiFi Security Tools",
                "license": "For authorized security testing only"
            }
        }
        
    def get_text(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """Get translated text for a specific key"""
        try:
            return self.translations[self.current_language][section][key]
        except KeyError:
            # Fallback to English
            try:
                return self.translations["en"][section][key]
            except KeyError:
                return fallback or f"[Missing: {section}.{key}]"
                
    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.available_languages:
            self.current_language = language_code
            self.language_changed.emit(language_code)
            self._save_language_preference()
            
    def _save_language_preference(self):
        """Save language preference to file"""
        try:
            with open("language_settings.json", 'w') as f:
                json.dump({"language": self.current_language}, f)
        except Exception as e:
            print(f"Failed to save language preference: {e}")
            
    def _load_language_preference(self):
        """Load language preference from file"""
        try:
            if os.path.exists("language_settings.json"):
                with open("language_settings.json", 'r') as f:
                    settings = json.load(f)
                    saved_lang = settings.get("language", "en")
                    if saved_lang in self.available_languages:
                        self.current_language = saved_lang
        except Exception as e:
            print(f"Failed to load language preference: {e}")
            
    def get_available_languages(self) -> Dict[str, str]:
        """Get dictionary of available languages"""
        return self.available_languages.copy()


class LanguageDialog(QDialog):
    """Dialog for selecting application language"""
    
    def __init__(self, translation_manager, parent=None):
        super().__init__(parent)
        self.translation_manager = translation_manager
        self.setWindowTitle("Language Selection")
        self.setFixedSize(400, 300)
        self._setup_ui()
        self._apply_theme()
        self._load_current_language()
        
    def _setup_ui(self):
        """Setup language selection UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(self.translation_manager.get_text("accessibility", "title", "Language Settings"))
        title.setFont(QFont("JetBrains Mono", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Language selection
        lang_group = QGroupBox(self.translation_manager.get_text("menu", "language", "Language"))
        lang_layout = QVBoxLayout(lang_group)
        
        self.language_combo = QComboBox()
        available_langs = self.translation_manager.get_available_languages()
        
        for code, name in available_langs.items():
            self.language_combo.addItem(f"{name} ({code})", code)
            
        lang_layout.addWidget(self.language_combo)
        layout.addWidget(lang_group)
        
        # Preview area
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setMaximumHeight(100)
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        apply_btn = QPushButton(self.translation_manager.get_text("dialogs", "apply", "Apply"))
        apply_btn.clicked.connect(self._apply_language)
        buttons_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton(self.translation_manager.get_text("dialogs", "cancel", "Cancel"))
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        # Connect signals
        self.language_combo.currentTextChanged.connect(self._language_selection_changed)
        
    def _apply_theme(self):
        """Apply consistent theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel {
                color: #00ff00;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                color: #00ff00;
                border: 2px solid #333;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QComboBox {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #555;
                padding: 6px;
                border-radius: 4px;
                font-size: 12px;
            }
            QComboBox:focus {
                border: 2px solid #00ff00;
            }
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #555;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: #00ff00;
                border: 2px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
                border: 2px solid #00aa00;
            }
            QPushButton:pressed {
                background-color: #00aa00;
                color: #000000;
            }
        """)
        
    def _load_current_language(self):
        """Load current language selection"""
        current_lang = self.translation_manager.current_language
        
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
                
        self._update_preview()
        
    def _language_selection_changed(self):
        """Handle language selection change"""
        self._update_preview()
        
    def _update_preview(self):
        """Update preview text with selected language"""
        selected_lang = self.language_combo.currentData()
        if not selected_lang:
            return
            
        # Temporarily switch language for preview
        old_lang = self.translation_manager.current_language
        self.translation_manager.current_language = selected_lang
        
        preview_texts = [
            self.translation_manager.get_text("main_window", "title"),
            self.translation_manager.get_text("main_window", "scan_button"),
            self.translation_manager.get_text("network_info", "ssid"),
            self.translation_manager.get_text("network_info", "security"),
            self.translation_manager.get_text("scanner", "networks_found")
        ]
        
        self.preview_text.setText("\n".join(preview_texts))
        
        # Restore original language
        self.translation_manager.current_language = old_lang
        
    def _apply_language(self):
        """Apply selected language"""
        selected_lang = self.language_combo.currentData()
        if selected_lang:
            self.translation_manager.set_language(selected_lang)
            
            lang_name = self.translation_manager.available_languages[selected_lang]
            QMessageBox.information(
                self, 
                "Language Changed",
                f"Language changed to {lang_name}.\nSome changes may require application restart."
            )
            
        self.accept()


class TranslatedWidget:
    """Mixin class for widgets that need translation support"""
    
    def __init__(self, translation_manager):
        self.translation_manager = translation_manager
        self.translation_manager.language_changed.connect(self._retranslate_ui)
        
    def _retranslate_ui(self):
        """Override this method to update UI text when language changes"""
        pass
        
    def tr(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """Convenience method for getting translated text"""
        return self.translation_manager.get_text(section, key, fallback)


# Global translation manager instance
translation_manager = TranslationManager()


def create_translation_file_template():
    """Create translation file templates for translators"""
    translations_dir = "translations"
    template_dir = os.path.join(translations_dir, "templates")
    
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        
    # Create template with English strings and empty translations
    default_translations = translation_manager._get_default_translations()
    
    template = {}
    for section, strings in default_translations.items():
        template[section] = {}
        for key, english_text in strings.items():
            template[section][key] = {
                "english": english_text,
                "translation": "",
                "notes": ""
            }
            
    template_file = os.path.join(template_dir, "translation_template.json")
    try:
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print(f"Translation template created: {template_file}")
    except Exception as e:
        print(f"Failed to create translation template: {e}")


# Export internationalization functionality
__all__ = [
    'TranslationManager',
    'LanguageDialog',
    'TranslatedWidget',
    'translation_manager',
    'create_translation_file_template'
]


if __name__ == "__main__":
    # Test language dialog and create templates
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create translation templates
    create_translation_file_template()
    
    # Show language dialog
    dialog = LanguageDialog(translation_manager)
    dialog.show()
    
    sys.exit(app.exec_())