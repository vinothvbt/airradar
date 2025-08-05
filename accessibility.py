#!/usr/bin/env python3
"""
Accessibility Module for WiFi Security Radar Suite
Provides enhanced accessibility features including keyboard navigation, 
screen reader support, and high contrast modes
"""

from PyQt5.QtWidgets import (
    QWidget, QApplication, QShortcut, QMessageBox, QDialog, 
    QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QCheckBox, QSlider, QGroupBox, QColorDialog
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QEvent, QTimer
from PyQt5.QtGui import (
    QKeySequence, QPalette, QColor, QFont, QFontMetrics, 
    QPixmap, QPainter, QBrush
)
import json
import os


class AccessibilityManager(QObject):
    """Central manager for accessibility features"""
    
    theme_changed = pyqtSignal(str)  # theme_name
    font_size_changed = pyqtSignal(int)  # new_size
    contrast_changed = pyqtSignal(bool)  # high_contrast_enabled
    
    def __init__(self):
        super().__init__()
        self.high_contrast_enabled = False
        self.current_theme = "default"
        self.font_scale = 1.0
        self.keyboard_navigation_enabled = True
        self.screen_reader_enabled = False
        self.focus_indicators_enhanced = True
        
        # Load accessibility settings
        self._load_settings()
        
        # Setup global shortcuts
        self._setup_shortcuts()
        
    def _load_settings(self):
        """Load accessibility settings from file"""
        settings_file = "accessibility_settings.json"
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.high_contrast_enabled = settings.get('high_contrast', False)
                    self.current_theme = settings.get('theme', 'default')
                    self.font_scale = settings.get('font_scale', 1.0)
                    self.keyboard_navigation_enabled = settings.get('keyboard_navigation', True)
                    self.screen_reader_enabled = settings.get('screen_reader', False)
                    self.focus_indicators_enhanced = settings.get('enhanced_focus', True)
        except Exception as e:
            print(f"Failed to load accessibility settings: {e}")
            
    def save_settings(self):
        """Save accessibility settings to file"""
        settings = {
            'high_contrast': self.high_contrast_enabled,
            'theme': self.current_theme,
            'font_scale': self.font_scale,
            'keyboard_navigation': self.keyboard_navigation_enabled,
            'screen_reader': self.screen_reader_enabled,
            'enhanced_focus': self.focus_indicators_enhanced
        }
        
        try:
            with open("accessibility_settings.json", 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save accessibility settings: {e}")
            
    def _setup_shortcuts(self):
        """Setup global accessibility shortcuts"""
        # These would be registered globally if the app supports it
        pass
    
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        self.high_contrast_enabled = not self.high_contrast_enabled
        self.contrast_changed.emit(self.high_contrast_enabled)
        self.save_settings()
        
    def set_font_scale(self, scale):
        """Set font scaling factor"""
        self.font_scale = max(0.5, min(3.0, scale))
        self.font_size_changed.emit(int(12 * self.font_scale))
        self.save_settings()
        
    def set_theme(self, theme_name):
        """Set accessibility theme"""
        self.current_theme = theme_name
        self.theme_changed.emit(theme_name)
        self.save_settings()
        
    def get_high_contrast_style(self):
        """Get high contrast stylesheet"""
        if not self.high_contrast_enabled:
            return ""
            
        return """
            * {
                background-color: #000000 !important;
                color: #ffffff !important;
                selection-background-color: #ffff00 !important;
                selection-color: #000000 !important;
            }
            QWidget:focus {
                border: 3px solid #ffff00 !important;
                background-color: #333333 !important;
            }
            QPushButton {
                background-color: #333333 !important;
                color: #ffffff !important;
                border: 2px solid #ffffff !important;
                font-weight: bold !important;
            }
            QPushButton:hover {
                background-color: #ffff00 !important;
                color: #000000 !important;
                border: 2px solid #000000 !important;
            }
            QPushButton:pressed {
                background-color: #ff0000 !important;
                color: #ffffff !important;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #333333 !important;
                color: #ffffff !important;
                border: 2px solid #ffffff !important;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 3px solid #ffff00 !important;
            }
            QLabel {
                color: #ffffff !important;
                font-weight: bold !important;
            }
            QTabWidget::pane {
                border: 2px solid #ffffff !important;
                background-color: #000000 !important;
            }
            QTabBar::tab {
                background-color: #333333 !important;
                color: #ffffff !important;
                border: 1px solid #ffffff !important;
                font-weight: bold !important;
            }
            QTabBar::tab:selected {
                background-color: #ffff00 !important;
                color: #000000 !important;
            }
        """
        
    def get_enhanced_focus_style(self):
        """Get enhanced focus indicators stylesheet"""
        if not self.focus_indicators_enhanced:
            return ""
            
        return """
            *:focus {
                border: 2px solid #ff0066 !important;
                outline: 2px solid #ffff00 !important;
                outline-offset: 2px !important;
            }
            QPushButton:focus {
                background-color: #ff0066 !important;
                color: #ffffff !important;
                font-weight: bold !important;
            }
        """


class KeyboardNavigationHandler(QObject):
    """Handles enhanced keyboard navigation"""
    
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.navigation_enabled = True
        self.current_focus_index = 0
        self.focusable_widgets = []
        self._setup_navigation()
        
    def _setup_navigation(self):
        """Setup keyboard navigation shortcuts"""
        # Tab navigation enhancement
        self.tab_shortcut = QShortcut(QKeySequence("Tab"), self.parent_widget)
        self.tab_shortcut.activated.connect(self._navigate_forward)
        
        self.shift_tab_shortcut = QShortcut(QKeySequence("Shift+Tab"), self.parent_widget)
        self.shift_tab_shortcut.activated.connect(self._navigate_backward)
        
        # Arrow key navigation
        self.up_shortcut = QShortcut(QKeySequence("Up"), self.parent_widget)
        self.up_shortcut.activated.connect(self._navigate_up)
        
        self.down_shortcut = QShortcut(QKeySequence("Down"), self.parent_widget)
        self.down_shortcut.activated.connect(self._navigate_down)
        
        self.left_shortcut = QShortcut(QKeySequence("Left"), self.parent_widget)
        self.left_shortcut.activated.connect(self._navigate_left)
        
        self.right_shortcut = QShortcut(QKeySequence("Right"), self.parent_widget)
        self.right_shortcut.activated.connect(self._navigate_right)
        
        # Accessibility shortcuts
        self.help_shortcut = QShortcut(QKeySequence("F1"), self.parent_widget)
        self.help_shortcut.activated.connect(self._show_help)
        
        self.screen_reader_shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self.parent_widget)
        self.screen_reader_shortcut.activated.connect(self._toggle_screen_reader_mode)
        
    def update_focusable_widgets(self):
        """Update list of focusable widgets"""
        self.focusable_widgets = []
        self._find_focusable_widgets(self.parent_widget)
        
    def _find_focusable_widgets(self, widget):
        """Recursively find focusable widgets"""
        if widget.focusPolicy() != Qt.NoFocus and widget.isVisible() and widget.isEnabled():
            self.focusable_widgets.append(widget)
            
        for child in widget.findChildren(QWidget):
            if child.focusPolicy() != Qt.NoFocus and child.isVisible() and child.isEnabled():
                self.focusable_widgets.append(child)
                
    def _navigate_forward(self):
        """Navigate to next focusable widget"""
        if not self.navigation_enabled or not self.focusable_widgets:
            return
            
        self.current_focus_index = (self.current_focus_index + 1) % len(self.focusable_widgets)
        self.focusable_widgets[self.current_focus_index].setFocus()
        self._announce_focus_change()
        
    def _navigate_backward(self):
        """Navigate to previous focusable widget"""
        if not self.navigation_enabled or not self.focusable_widgets:
            return
            
        self.current_focus_index = (self.current_focus_index - 1) % len(self.focusable_widgets)
        self.focusable_widgets[self.current_focus_index].setFocus()
        self._announce_focus_change()
        
    def _navigate_up(self):
        """Navigate up in spatial layout"""
        self._navigate_spatial("up")
        
    def _navigate_down(self):
        """Navigate down in spatial layout"""
        self._navigate_spatial("down")
        
    def _navigate_left(self):
        """Navigate left in spatial layout"""
        self._navigate_spatial("left")
        
    def _navigate_right(self):
        """Navigate right in spatial layout"""
        self._navigate_spatial("right")
        
    def _navigate_spatial(self, direction):
        """Navigate based on spatial arrangement"""
        if not self.focusable_widgets:
            return
            
        current_widget = QApplication.focusWidget()
        if not current_widget:
            self.focusable_widgets[0].setFocus()
            return
            
        current_pos = current_widget.mapToGlobal(current_widget.rect().center())
        best_widget = None
        best_distance = float('inf')
        
        for widget in self.focusable_widgets:
            if widget == current_widget:
                continue
                
            widget_pos = widget.mapToGlobal(widget.rect().center())
            
            # Check if widget is in the right direction
            if direction == "up" and widget_pos.y() >= current_pos.y():
                continue
            elif direction == "down" and widget_pos.y() <= current_pos.y():
                continue
            elif direction == "left" and widget_pos.x() >= current_pos.x():
                continue
            elif direction == "right" and widget_pos.x() <= current_pos.x():
                continue
                
            # Calculate distance
            dx = widget_pos.x() - current_pos.x()
            dy = widget_pos.y() - current_pos.y()
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < best_distance:
                best_distance = distance
                best_widget = widget
                
        if best_widget:
            best_widget.setFocus()
            self._announce_focus_change()
            
    def _announce_focus_change(self):
        """Announce focus change for screen readers"""
        focused_widget = QApplication.focusWidget()
        if focused_widget and hasattr(focused_widget, 'accessibleName'):
            name = focused_widget.accessibleName()
            if name:
                self._speak_text(f"Focused: {name}")
                
    def _show_help(self):
        """Show accessibility help dialog"""
        help_text = """
Keyboard Navigation Help:

Tab / Shift+Tab: Navigate between controls
Arrow Keys: Spatial navigation
Enter / Space: Activate buttons and controls
F1: Show this help
Ctrl+Shift+S: Toggle screen reader mode
Ctrl+Shift+H: Toggle high contrast mode
Ctrl++ / Ctrl+-: Increase/decrease font size

Screen Reader Support:
- All controls have accessible names
- State changes are announced
- Focus changes are announced
        """
        
        msg = QMessageBox(self.parent_widget)
        msg.setWindowTitle("Accessibility Help")
        msg.setText(help_text)
        msg.exec_()
        
    def _toggle_screen_reader_mode(self):
        """Toggle screen reader announcements"""
        # This would integrate with actual screen reader APIs
        self._speak_text("Screen reader mode toggled")
        
    def _speak_text(self, text):
        """Speak text for screen readers (placeholder)"""
        # In a real implementation, this would use platform-specific screen reader APIs
        print(f"[Screen Reader]: {text}")


class AccessibilityDialog(QDialog):
    """Dialog for configuring accessibility settings"""
    
    def __init__(self, accessibility_manager, parent=None):
        super().__init__(parent)
        self.accessibility_manager = accessibility_manager
        self.setWindowTitle("Accessibility Settings")
        self.setFixedSize(500, 400)
        self._setup_ui()
        self._apply_theme()
        self._load_current_settings()
        
    def _setup_ui(self):
        """Setup accessibility settings UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Accessibility Settings")
        title.setFont(QFont("JetBrains Mono", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Visual settings
        visual_group = QGroupBox("Visual Accessibility")
        visual_layout = QVBoxLayout(visual_group)
        
        self.high_contrast_cb = QCheckBox("Enable High Contrast Mode")
        self.high_contrast_cb.setAccessibleName("High contrast mode checkbox")
        visual_layout.addWidget(self.high_contrast_cb)
        
        self.enhanced_focus_cb = QCheckBox("Enhanced Focus Indicators")
        self.enhanced_focus_cb.setAccessibleName("Enhanced focus indicators checkbox")
        visual_layout.addWidget(self.enhanced_focus_cb)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setRange(50, 300)
        self.font_slider.setValue(100)
        self.font_slider.setAccessibleName("Font size slider")
        font_layout.addWidget(self.font_slider)
        
        self.font_size_label = QLabel("100%")
        font_layout.addWidget(self.font_size_label)
        visual_layout.addLayout(font_layout)
        
        layout.addWidget(visual_group)
        
        # Navigation settings
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout(nav_group)
        
        self.keyboard_nav_cb = QCheckBox("Enhanced Keyboard Navigation")
        self.keyboard_nav_cb.setAccessibleName("Enhanced keyboard navigation checkbox")
        nav_layout.addWidget(self.keyboard_nav_cb)
        
        self.screen_reader_cb = QCheckBox("Screen Reader Support")
        self.screen_reader_cb.setAccessibleName("Screen reader support checkbox")
        nav_layout.addWidget(self.screen_reader_cb)
        
        layout.addWidget(nav_group)
        
        # Theme selection
        theme_group = QGroupBox("Accessibility Themes")
        theme_layout = QVBoxLayout(theme_group)
        
        theme_selection_layout = QHBoxLayout()
        theme_selection_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Default",
            "High Contrast Black",
            "High Contrast White", 
            "Large Text",
            "Color Blind Friendly"
        ])
        self.theme_combo.setAccessibleName("Accessibility theme selection")
        theme_selection_layout.addWidget(self.theme_combo)
        theme_layout.addLayout(theme_selection_layout)
        
        layout.addWidget(theme_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        apply_btn = QPushButton("Apply Settings")
        apply_btn.setAccessibleName("Apply accessibility settings button")
        apply_btn.clicked.connect(self._apply_settings)
        buttons_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setAccessibleName("Reset to default settings button")
        reset_btn.clicked.connect(self._reset_settings)
        buttons_layout.addWidget(reset_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setAccessibleName("Close dialog button")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        # Connect signals
        self.font_slider.valueChanged.connect(self._font_size_changed)
        
    def _apply_theme(self):
        """Apply accessibility-aware theme"""
        base_style = """
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
            QCheckBox {
                color: #00ff00;
                spacing: 8px;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555;
                background-color: #1a1a1a;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #00ff00;
                background-color: #00ff00;
            }
            QCheckBox::indicator:focus {
                border: 3px solid #ff0066;
                outline: 2px solid #ffff00;
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
                outline: 2px solid #ff0066;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 8px;
                background: #1a1a1a;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00ff00;
                border: 1px solid #00aa00;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:focus {
                border: 2px solid #ff0066;
                outline: 2px solid #ffff00;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: #00ff00;
                border: 2px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 120px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
                border: 2px solid #00aa00;
            }
            QPushButton:focus {
                border: 2px solid #ff0066;
                outline: 2px solid #ffff00;
            }
            QPushButton:pressed {
                background-color: #00aa00;
                color: #000000;
            }
        """
        
        # Add high contrast if enabled
        if self.accessibility_manager.high_contrast_enabled:
            base_style += self.accessibility_manager.get_high_contrast_style()
            
        if self.accessibility_manager.focus_indicators_enhanced:
            base_style += self.accessibility_manager.get_enhanced_focus_style()
            
        self.setStyleSheet(base_style)
        
    def _load_current_settings(self):
        """Load current accessibility settings into UI"""
        self.high_contrast_cb.setChecked(self.accessibility_manager.high_contrast_enabled)
        self.enhanced_focus_cb.setChecked(self.accessibility_manager.focus_indicators_enhanced)
        self.keyboard_nav_cb.setChecked(self.accessibility_manager.keyboard_navigation_enabled)
        self.screen_reader_cb.setChecked(self.accessibility_manager.screen_reader_enabled)
        
        font_scale_percent = int(self.accessibility_manager.font_scale * 100)
        self.font_slider.setValue(font_scale_percent)
        
        # Set theme combo
        theme_map = {
            'default': 0,
            'high_contrast_black': 1,
            'high_contrast_white': 2,
            'large_text': 3,
            'color_blind': 4
        }
        self.theme_combo.setCurrentIndex(theme_map.get(self.accessibility_manager.current_theme, 0))
        
    def _font_size_changed(self, value):
        """Handle font size slider change"""
        self.font_size_label.setText(f"{value}%")
        
    def _apply_settings(self):
        """Apply the accessibility settings"""
        # Update accessibility manager
        self.accessibility_manager.high_contrast_enabled = self.high_contrast_cb.isChecked()
        self.accessibility_manager.focus_indicators_enhanced = self.enhanced_focus_cb.isChecked()
        self.accessibility_manager.keyboard_navigation_enabled = self.keyboard_nav_cb.isChecked()
        self.accessibility_manager.screen_reader_enabled = self.screen_reader_cb.isChecked()
        
        font_scale = self.font_slider.value() / 100.0
        self.accessibility_manager.set_font_scale(font_scale)
        
        # Set theme
        theme_names = ['default', 'high_contrast_black', 'high_contrast_white', 'large_text', 'color_blind']
        selected_theme = theme_names[self.theme_combo.currentIndex()]
        self.accessibility_manager.set_theme(selected_theme)
        
        # Save settings
        self.accessibility_manager.save_settings()
        
        # Update this dialog's theme
        self._apply_theme()
        
        QMessageBox.information(self, "Settings Applied", "Accessibility settings have been applied and saved.")
        
    def _reset_settings(self):
        """Reset to default accessibility settings"""
        self.high_contrast_cb.setChecked(False)
        self.enhanced_focus_cb.setChecked(True)
        self.keyboard_nav_cb.setChecked(True)
        self.screen_reader_cb.setChecked(False)
        self.font_slider.setValue(100)
        self.theme_combo.setCurrentIndex(0)


# Global accessibility manager instance
accessibility_manager = AccessibilityManager()


def apply_accessibility_to_widget(widget):
    """Apply accessibility features to a widget"""
    # Add keyboard navigation
    nav_handler = KeyboardNavigationHandler(widget)
    nav_handler.update_focusable_widgets()
    
    # Apply current accessibility styles
    style = widget.styleSheet()
    
    if accessibility_manager.high_contrast_enabled:
        style += accessibility_manager.get_high_contrast_style()
        
    if accessibility_manager.focus_indicators_enhanced:
        style += accessibility_manager.get_enhanced_focus_style()
        
    widget.setStyleSheet(style)
    
    # Set up font scaling
    def update_fonts():
        font = widget.font()
        base_size = 12
        new_size = int(base_size * accessibility_manager.font_scale)
        font.setPointSize(new_size)
        widget.setFont(font)
        
    accessibility_manager.font_size_changed.connect(update_fonts)
    update_fonts()
    
    return nav_handler


# Export accessibility functionality
__all__ = [
    'AccessibilityManager',
    'KeyboardNavigationHandler', 
    'AccessibilityDialog',
    'accessibility_manager',
    'apply_accessibility_to_widget'
]


if __name__ == "__main__":
    # Test accessibility dialog
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = AccessibilityDialog(accessibility_manager)
    dialog.show()
    
    sys.exit(app.exec_())