#!/usr/bin/env python3
"""
Enhanced Customizable Views and Themes Module for WiFi Security Radar Suite
Provides advanced theming, layout customization, and view management
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QGroupBox, QCheckBox, QSpinBox, QSlider, QColorDialog, QTabWidget,
    QWidget, QListWidget, QListWidgetItem, QTextEdit, QLineEdit,
    QScrollArea, QGridLayout, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSize
from PyQt5.QtGui import QColor, QFont, QPalette, QPixmap, QPainter, QBrush


@dataclass
class ThemeColors:
    """Color scheme for themes"""
    background: str = "#0a0a0a"
    surface: str = "#1a1a1a"
    primary: str = "#00ff00"
    secondary: str = "#00aa00"
    accent: str = "#ff0066"
    text_primary: str = "#00ff00"
    text_secondary: str = "#ffffff"
    border: str = "#333333"
    hover: str = "#003300"
    focus: str = "#ff0066"
    error: str = "#ff1744"
    warning: str = "#ff9800"
    success: str = "#4caf50"
    info: str = "#2196f3"


@dataclass
class ThemeConfig:
    """Complete theme configuration"""
    name: str
    display_name: str
    colors: ThemeColors
    font_family: str = "JetBrains Mono"
    font_size: int = 12
    border_radius: int = 8
    spacing: int = 10
    padding: int = 10
    shadow_enabled: bool = True
    animation_enabled: bool = True
    custom_properties: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.custom_properties is None:
            self.custom_properties = {}


class ThemeManager(QObject):
    """Manages themes and styling"""
    
    theme_changed = pyqtSignal(str)  # theme_name
    
    def __init__(self):
        super().__init__()
        self.themes = {}
        self.current_theme_name = "matrix_green"
        self.custom_styles = {}
        self._load_default_themes()
        self._load_user_themes()
        
    def _load_default_themes(self):
        """Load default built-in themes"""
        
        # Matrix Green (default)
        matrix_colors = ThemeColors(
            background="#0a0a0a",
            surface="#1a1a1a", 
            primary="#00ff00",
            secondary="#00aa00",
            accent="#ff0066",
            text_primary="#00ff00",
            text_secondary="#ffffff",
            border="#333333",
            hover="#003300",
            focus="#ff0066"
        )
        
        self.themes["matrix_green"] = ThemeConfig(
            name="matrix_green",
            display_name="Matrix Green",
            colors=matrix_colors,
            font_family="JetBrains Mono"
        )
        
        # Cyberpunk Blue
        cyber_colors = ThemeColors(
            background="#0d1117",
            surface="#21262d",
            primary="#58a6ff",
            secondary="#1f6feb",
            accent="#f85149",
            text_primary="#c9d1d9",
            text_secondary="#8b949e",
            border="#30363d",
            hover="#21262d",
            focus="#f85149"
        )
        
        self.themes["cyberpunk_blue"] = ThemeConfig(
            name="cyberpunk_blue",
            display_name="Cyberpunk Blue",
            colors=cyber_colors,
            font_family="Fira Code"
        )
        
        # Dark Red
        dark_red_colors = ThemeColors(
            background="#1a0000",
            surface="#2a0505",
            primary="#ff4444",
            secondary="#cc3333",
            accent="#ffaa00",
            text_primary="#ff6666",
            text_secondary="#ffffff",
            border="#440000",
            hover="#330000",
            focus="#ffaa00"
        )
        
        self.themes["dark_red"] = ThemeConfig(
            name="dark_red",
            display_name="Dark Red",
            colors=dark_red_colors
        )
        
        # Purple Haze
        purple_colors = ThemeColors(
            background="#0f0618",
            surface="#1a0b26",
            primary="#9d4edd",
            secondary="#7b2cbf",
            accent="#e0aaff",
            text_primary="#c77dff",
            text_secondary="#ffffff",
            border="#3c096c",
            hover="#240046",
            focus="#e0aaff"
        )
        
        self.themes["purple_haze"] = ThemeConfig(
            name="purple_haze",
            display_name="Purple Haze",
            colors=purple_colors
        )
        
        # High Contrast
        high_contrast_colors = ThemeColors(
            background="#000000",
            surface="#000000",
            primary="#ffffff",
            secondary="#cccccc",
            accent="#ffff00",
            text_primary="#ffffff",
            text_secondary="#ffffff",
            border="#ffffff",
            hover="#333333",
            focus="#ffff00"
        )
        
        self.themes["high_contrast"] = ThemeConfig(
            name="high_contrast",
            display_name="High Contrast",
            colors=high_contrast_colors,
            border_radius=2,
            shadow_enabled=False
        )
        
        # Light Mode
        light_colors = ThemeColors(
            background="#ffffff",
            surface="#f5f5f5",
            primary="#1976d2",
            secondary="#1565c0",
            accent="#e91e63",
            text_primary="#212121",
            text_secondary="#757575",
            border="#e0e0e0",
            hover="#f0f0f0",
            focus="#e91e63"
        )
        
        self.themes["light_mode"] = ThemeConfig(
            name="light_mode",
            display_name="Light Mode",
            colors=light_colors
        )
        
    def _load_user_themes(self):
        """Load user-defined custom themes"""
        themes_dir = "themes"
        if not os.path.exists(themes_dir):
            os.makedirs(themes_dir)
            
        for filename in os.listdir(themes_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(themes_dir, filename), 'r') as f:
                        theme_data = json.load(f)
                        theme_config = ThemeConfig(**theme_data)
                        theme_config.colors = ThemeColors(**theme_data['colors'])
                        self.themes[theme_config.name] = theme_config
                except Exception as e:
                    print(f"Failed to load custom theme {filename}: {e}")
                    
    def get_theme(self, theme_name: str) -> Optional[ThemeConfig]:
        """Get theme configuration by name"""
        return self.themes.get(theme_name)
        
    def get_current_theme(self) -> ThemeConfig:
        """Get current theme configuration"""
        return self.themes.get(self.current_theme_name, self.themes["matrix_green"])
        
    def set_theme(self, theme_name: str):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme_name = theme_name
            self.theme_changed.emit(theme_name)
            self._save_theme_preference()
            
    def _save_theme_preference(self):
        """Save theme preference"""
        try:
            with open("theme_settings.json", 'w') as f:
                json.dump({"current_theme": self.current_theme_name}, f)
        except Exception as e:
            print(f"Failed to save theme preference: {e}")
            
    def create_stylesheet(self, theme_name: Optional[str] = None) -> str:
        """Generate complete stylesheet for theme"""
        theme = self.get_theme(theme_name or self.current_theme_name)
        if not theme:
            theme = self.get_current_theme()
            
        colors = theme.colors
        
        stylesheet = f"""
        /* Main Application Styling */
        QMainWindow, QDialog, QWidget {{
            background-color: {colors.background};
            color: {colors.text_primary};
            font-family: '{theme.font_family}', monospace;
            font-size: {theme.font_size}px;
        }}
        
        /* Labels */
        QLabel {{
            color: {colors.text_primary};
            font-weight: bold;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            padding: {theme.padding}px {theme.padding * 2}px;
            border-radius: {theme.border_radius}px;
            font-weight: bold;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {colors.primary};
            color: {colors.background};
            border: 2px solid {colors.secondary};
        }}
        
        QPushButton:pressed {{
            background-color: {colors.secondary};
            color: {colors.background};
        }}
        
        QPushButton:focus {{
            border: 2px solid {colors.focus};
            outline: 2px solid {colors.accent};
        }}
        
        QPushButton:disabled {{
            background-color: {colors.border};
            color: {colors.text_secondary};
            border: 2px solid {colors.border};
        }}
        
        /* Input Fields */
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            padding: {theme.padding // 2}px;
            border-radius: {theme.border_radius // 2}px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border: 2px solid {colors.primary};
            outline: 1px solid {colors.focus};
        }}
        
        /* ComboBox specific */
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border: none;
            width: 12px;
            height: 12px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            selection-background-color: {colors.primary};
            selection-color: {colors.background};
        }}
        
        /* CheckBoxes and RadioButtons */
        QCheckBox, QRadioButton {{
            color: {colors.text_primary};
            spacing: {theme.spacing}px;
        }}
        
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 18px;
            height: 18px;
        }}
        
        QCheckBox::indicator:unchecked {{
            border: 2px solid {colors.border};
            background-color: {colors.surface};
            border-radius: 3px;
        }}
        
        QCheckBox::indicator:checked {{
            border: 2px solid {colors.primary};
            background-color: {colors.primary};
            border-radius: 3px;
        }}
        
        QCheckBox::indicator:focus {{
            border: 2px solid {colors.focus};
            outline: 1px solid {colors.accent};
        }}
        
        /* Sliders */
        QSlider::groove:horizontal {{
            border: 1px solid {colors.border};
            height: 8px;
            background: {colors.surface};
            margin: 2px 0;
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {colors.primary};
            border: 1px solid {colors.secondary};
            width: 18px;
            margin: -2px 0;
            border-radius: 9px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {colors.secondary};
        }}
        
        QSlider::handle:horizontal:focus {{
            border: 2px solid {colors.focus};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            font-weight: bold;
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            border-radius: {theme.border_radius}px;
            margin-top: {theme.spacing}px;
            padding-top: {theme.padding}px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {theme.padding}px;
            padding: 0 {theme.spacing // 2}px 0 {theme.spacing // 2}px;
        }}
        
        /* Tab Widgets */
        QTabWidget::pane {{
            border: 2px solid {colors.border};
            background-color: {colors.surface};
            border-radius: {theme.border_radius}px;
        }}
        
        QTabBar::tab {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            padding: {theme.padding}px {theme.padding * 2}px;
            margin: 2px;
            border: 1px solid {colors.border};
            border-radius: {theme.border_radius // 2}px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors.primary};
            color: {colors.background};
            font-weight: bold;
            border: 1px solid {colors.secondary};
        }}
        
        QTabBar::tab:hover {{
            background-color: {colors.hover};
            border: 1px solid {colors.primary};
        }}
        
        QTabBar::tab:focus {{
            border: 2px solid {colors.focus};
        }}
        
        /* Lists and Tables */
        QListWidget, QTableWidget {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            gridline-color: {colors.border};
            selection-background-color: {colors.primary};
            selection-color: {colors.background};
            border-radius: {theme.border_radius}px;
        }}
        
        QListWidget::item, QTableWidget::item {{
            padding: {theme.padding // 2}px;
            border-bottom: 1px solid {colors.border};
        }}
        
        QListWidget::item:hover, QTableWidget::item:hover {{
            background-color: {colors.hover};
        }}
        
        QListWidget::item:selected, QTableWidget::item:selected {{
            background-color: {colors.primary};
            color: {colors.background};
        }}
        
        QHeaderView::section {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border: 1px solid {colors.border};
            padding: {theme.padding}px;
            font-weight: bold;
        }}
        
        /* Scroll Bars */
        QScrollBar:vertical {{
            background-color: {colors.surface};
            width: 16px;
            border: 1px solid {colors.border};
            border-radius: 8px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors.primary};
            min-height: 20px;
            border-radius: 7px;
            margin: 1px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors.secondary};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {colors.surface};
            height: 16px;
            border: 1px solid {colors.border};
            border-radius: 8px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors.primary};
            min-width: 20px;
            border-radius: 7px;
            margin: 1px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors.secondary};
        }}
        
        /* Progress Bars */
        QProgressBar {{
            border: 2px solid {colors.border};
            background-color: {colors.surface};
            text-align: center;
            color: {colors.text_primary};
            border-radius: {theme.border_radius // 2}px;
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors.primary};
            border-radius: {theme.border_radius // 2 - 1}px;
        }}
        
        /* Menu Bar and Menus */
        QMenuBar {{
            background-color: {colors.background};
            color: {colors.text_primary};
            border-bottom: 1px solid {colors.border};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: {theme.padding // 2}px {theme.padding}px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors.primary};
            color: {colors.background};
        }}
        
        QMenu {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            border-radius: {theme.border_radius}px;
        }}
        
        QMenu::item {{
            padding: {theme.padding // 2}px {theme.padding * 2}px;
        }}
        
        QMenu::item:selected {{
            background-color: {colors.primary};
            color: {colors.background};
        }}
        
        /* Tool Bar */
        QToolBar {{
            background-color: {colors.surface};
            border: 1px solid {colors.border};
            spacing: {theme.spacing // 2}px;
            padding: {theme.padding // 2}px;
        }}
        
        QToolButton {{
            background-color: transparent;
            color: {colors.text_primary};
            border: 1px solid transparent;
            padding: {theme.padding // 2}px;
            border-radius: {theme.border_radius // 2}px;
        }}
        
        QToolButton:hover {{
            background-color: {colors.hover};
            border: 1px solid {colors.primary};
        }}
        
        QToolButton:pressed {{
            background-color: {colors.primary};
            color: {colors.background};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {colors.surface};
            color: {colors.text_primary};
            border-top: 1px solid {colors.border};
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {colors.border};
        }}
        
        QSplitter::handle:horizontal {{
            width: 3px;
        }}
        
        QSplitter::handle:vertical {{
            height: 3px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {colors.primary};
        }}
        """
        
        # Add custom styles if any
        if theme.name in self.custom_styles:
            stylesheet += "\n" + self.custom_styles[theme.name]
            
        return stylesheet
        
    def save_custom_theme(self, theme_config: ThemeConfig):
        """Save a custom theme to file"""
        themes_dir = "themes"
        if not os.path.exists(themes_dir):
            os.makedirs(themes_dir)
            
        theme_file = os.path.join(themes_dir, f"{theme_config.name}.json")
        
        try:
            with open(theme_file, 'w') as f:
                json.dump(asdict(theme_config), f, indent=2)
            self.themes[theme_config.name] = theme_config
        except Exception as e:
            print(f"Failed to save custom theme: {e}")
            
    def get_available_themes(self) -> Dict[str, str]:
        """Get available themes as name -> display_name mapping"""
        return {name: theme.display_name for name, theme in self.themes.items()}


class ThemeCustomizerDialog(QDialog):
    """Dialog for customizing and creating themes"""
    
    theme_applied = pyqtSignal(str)  # theme_name
    
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = None
        self.color_buttons = {}
        self.setWindowTitle("Theme Customizer")
        self.setFixedSize(700, 600)
        self._setup_ui()
        self._load_current_theme()
        
    def _setup_ui(self):
        """Setup theme customizer UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Theme Customizer")
        title.setFont(QFont("JetBrains Mono", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget for different customization areas
        self.tab_widget = QTabWidget()
        
        # Colors tab
        colors_tab = self._create_colors_tab()
        self.tab_widget.addTab(colors_tab, "Colors")
        
        # Typography tab
        typography_tab = self._create_typography_tab()
        self.tab_widget.addTab(typography_tab, "Typography")
        
        # Layout tab
        layout_tab = self._create_layout_tab()
        self.tab_widget.addTab(layout_tab, "Layout")
        
        # Preview tab
        preview_tab = self._create_preview_tab()
        self.tab_widget.addTab(preview_tab, "Preview")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Base Theme:"))
        self.theme_combo = QComboBox()
        available_themes = self.theme_manager.get_available_themes()
        for name, display_name in available_themes.items():
            self.theme_combo.addItem(display_name, name)
        theme_layout.addWidget(self.theme_combo)
        buttons_layout.addLayout(theme_layout)
        
        buttons_layout.addStretch()
        
        save_btn = QPushButton("Save Theme")
        save_btn.clicked.connect(self._save_theme)
        buttons_layout.addWidget(save_btn)
        
        apply_btn = QPushButton("Apply Theme")
        apply_btn.clicked.connect(self._apply_theme)
        buttons_layout.addWidget(apply_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        # Connect signals
        self.theme_combo.currentTextChanged.connect(self._theme_selection_changed)
        
    def _create_colors_tab(self) -> QWidget:
        """Create colors customization tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        
        # Color customization controls
        color_fields = [
            ("background", "Background"),
            ("surface", "Surface"),
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("accent", "Accent"),
            ("text_primary", "Primary Text"),
            ("text_secondary", "Secondary Text"),
            ("border", "Border"),
            ("hover", "Hover"),
            ("focus", "Focus"),
            ("error", "Error"),
            ("warning", "Warning"),
            ("success", "Success"),
            ("info", "Info")
        ]
        
        for i, (field, label) in enumerate(color_fields):
            row = i // 2
            col = (i % 2) * 2
            
            label_widget = QLabel(f"{label}:")
            scroll_layout.addWidget(label_widget, row, col)
            
            color_btn = QPushButton()
            color_btn.setFixedSize(100, 30)
            color_btn.clicked.connect(lambda checked, f=field: self._choose_color(f))
            self.color_buttons[field] = color_btn
            scroll_layout.addWidget(color_btn, row, col + 1)
            
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        return widget
        
    def _create_typography_tab(self) -> QWidget:
        """Create typography customization tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Font family
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(font_group)
        
        font_family_layout = QHBoxLayout()
        font_family_layout.addWidget(QLabel("Font Family:"))
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems([
            "JetBrains Mono",
            "Fira Code", 
            "Source Code Pro",
            "Consolas",
            "Monaco",
            "Courier New"
        ])
        font_family_layout.addWidget(self.font_family_combo)
        font_layout.addLayout(font_family_layout)
        
        # Font size
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Font Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(12)
        font_size_layout.addWidget(self.font_size_spin)
        font_layout.addLayout(font_size_layout)
        
        layout.addWidget(font_group)
        layout.addStretch()
        
        return widget
        
    def _create_layout_tab(self) -> QWidget:
        """Create layout customization tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Border radius
        border_group = QGroupBox("Border Settings")
        border_layout = QVBoxLayout(border_group)
        
        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Border Radius:"))
        self.border_radius_spin = QSpinBox()
        self.border_radius_spin.setRange(0, 20)
        self.border_radius_spin.setValue(8)
        radius_layout.addWidget(self.border_radius_spin)
        border_layout.addLayout(radius_layout)
        
        layout.addWidget(border_group)
        
        # Spacing
        spacing_group = QGroupBox("Spacing Settings")
        spacing_layout = QVBoxLayout(spacing_group)
        
        spacing_layout_h = QHBoxLayout()
        spacing_layout_h.addWidget(QLabel("Spacing:"))
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setRange(5, 30)
        self.spacing_spin.setValue(10)
        spacing_layout_h.addWidget(self.spacing_spin)
        spacing_layout.addLayout(spacing_layout_h)
        
        padding_layout = QHBoxLayout()
        padding_layout.addWidget(QLabel("Padding:"))
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(5, 30)
        self.padding_spin.setValue(10)
        padding_layout.addWidget(self.padding_spin)
        spacing_layout.addLayout(padding_layout)
        
        layout.addWidget(spacing_group)
        
        # Effects
        effects_group = QGroupBox("Effects")
        effects_layout = QVBoxLayout(effects_group)
        
        self.shadow_cb = QCheckBox("Enable Shadows")
        self.shadow_cb.setChecked(True)
        effects_layout.addWidget(self.shadow_cb)
        
        self.animation_cb = QCheckBox("Enable Animations")
        self.animation_cb.setChecked(True)
        effects_layout.addWidget(self.animation_cb)
        
        layout.addWidget(effects_group)
        layout.addStretch()
        
        return widget
        
    def _create_preview_tab(self) -> QWidget:
        """Create preview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        preview_label = QLabel("Theme Preview")
        preview_label.setFont(QFont("JetBrains Mono", 14, QFont.Bold))
        preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(preview_label)
        
        # Preview content
        preview_frame = QFrame()
        preview_frame.setFrameStyle(QFrame.StyledPanel)
        preview_layout = QVBoxLayout(preview_frame)
        
        # Sample controls
        preview_layout.addWidget(QLabel("Sample Label"))
        
        sample_btn = QPushButton("Sample Button")
        preview_layout.addWidget(sample_btn)
        
        sample_edit = QLineEdit("Sample text input")
        preview_layout.addWidget(sample_edit)
        
        sample_cb = QCheckBox("Sample checkbox")
        sample_cb.setChecked(True)
        preview_layout.addWidget(sample_cb)
        
        sample_combo = QComboBox()
        sample_combo.addItems(["Option 1", "Option 2", "Option 3"])
        preview_layout.addWidget(sample_combo)
        
        layout.addWidget(preview_frame)
        
        # Update preview button
        update_btn = QPushButton("Update Preview")
        update_btn.clicked.connect(self._update_preview)
        layout.addWidget(update_btn)
        
        self.preview_frame = preview_frame
        return widget
        
    def _load_current_theme(self):
        """Load current theme into UI"""
        current_theme = self.theme_manager.get_current_theme()
        self.current_theme = current_theme
        
        # Set color buttons
        colors = current_theme.colors
        for field, button in self.color_buttons.items():
            color_value = getattr(colors, field)
            self._set_color_button(button, color_value)
            
        # Set other controls
        self.font_family_combo.setCurrentText(current_theme.font_family)
        self.font_size_spin.setValue(current_theme.font_size)
        self.border_radius_spin.setValue(current_theme.border_radius)
        self.spacing_spin.setValue(current_theme.spacing)
        self.padding_spin.setValue(current_theme.padding)
        self.shadow_cb.setChecked(current_theme.shadow_enabled)
        self.animation_cb.setChecked(current_theme.animation_enabled)
        
        self._update_preview()
        
    def _set_color_button(self, button, color_value):
        """Set color button appearance"""
        color = QColor(color_value)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_value};
                border: 2px solid #333;
                color: {'#ffffff' if color.lightness() < 128 else '#000000'};
                font-weight: bold;
            }}
        """)
        button.setText(color_value)
        
    def _choose_color(self, field):
        """Open color chooser dialog"""
        current_color = getattr(self.current_theme.colors, field)
        color = QColorDialog.getColor(QColor(current_color), self)
        
        if color.isValid():
            color_hex = color.name()
            setattr(self.current_theme.colors, field, color_hex)
            self._set_color_button(self.color_buttons[field], color_hex)
            self._update_preview()
            
    def _theme_selection_changed(self):
        """Handle theme selection change"""
        selected_theme_name = self.theme_combo.currentData()
        if selected_theme_name:
            selected_theme = self.theme_manager.get_theme(selected_theme_name)
            if selected_theme:
                self.current_theme = selected_theme
                self._load_current_theme()
                
    def _update_preview(self):
        """Update theme preview"""
        if not self.current_theme:
            return
            
        # Update current theme with UI values
        self.current_theme.font_family = self.font_family_combo.currentText()
        self.current_theme.font_size = self.font_size_spin.value()
        self.current_theme.border_radius = self.border_radius_spin.value()
        self.current_theme.spacing = self.spacing_spin.value()
        self.current_theme.padding = self.padding_spin.value()
        self.current_theme.shadow_enabled = self.shadow_cb.isChecked()
        self.current_theme.animation_enabled = self.animation_cb.isChecked()
        
        # Apply to preview frame
        stylesheet = self.theme_manager.create_stylesheet(self.current_theme.name)
        self.preview_frame.setStyleSheet(stylesheet)
        
    def _save_theme(self):
        """Save current theme"""
        theme_name, ok = QLineEdit().getText(self, "Save Theme", "Theme name:")
        if ok and theme_name:
            self.current_theme.name = theme_name.lower().replace(" ", "_")
            self.current_theme.display_name = theme_name
            self.theme_manager.save_custom_theme(self.current_theme)
            
    def _apply_theme(self):
        """Apply current theme"""
        if self.current_theme:
            self.theme_manager.set_theme(self.current_theme.name)
            self.theme_applied.emit(self.current_theme.name)


# Global theme manager instance  
theme_manager = ThemeManager()


# Export functionality
__all__ = [
    'ThemeColors',
    'ThemeConfig',
    'ThemeManager',
    'ThemeCustomizerDialog',
    'theme_manager'
]


if __name__ == "__main__":
    # Test theme customizer
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = ThemeCustomizerDialog(theme_manager)
    dialog.show()
    
    sys.exit(app.exec_())