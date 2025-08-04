#!/usr/bin/env python3
"""
Test UI Micro-Interactions
Demonstrates the enhanced animations and interactions in WiFi Security Radar Suite
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from ui_animations import (animation_manager, EnhancedWidget, StatusIndicator, 
                               ProgressIndicator, EnhancedButton)
    from main_launcher import EnhancedButton
    ANIMATIONS_AVAILABLE = True
    print("✅ Animation framework loaded successfully")
except ImportError as e:
    print(f"❌ Animation framework failed to load: {e}")
    ANIMATIONS_AVAILABLE = False
    
    # Fallback classes
    class EnhancedWidget(QWidget):
        pass
    class StatusIndicator(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(20, 20)
        def set_status(self, status):
            pass
    class ProgressIndicator(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedHeight(6)
        def set_progress_animated(self, progress, duration=300):
            pass
    class EnhancedButton(QPushButton):
        pass

class MicroInteractionDemo(QMainWindow):
    """Demo window showcasing micro-interactions"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Radar - Micro-Interactions Demo")
        self.setFixedSize(800, 600)
        self._setup_ui()
        self._apply_theme()
        self._setup_demo_animations()
    
    def _setup_ui(self):
        """Setup demo UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("🎯 WiFi Security Radar Suite")
        title.setFont(QFont("JetBrains Mono", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Micro-Interactions & Animations Demo")
        subtitle.setFont(QFont("JetBrains Mono", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Status indicators row
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status Indicators:"))
        
        self.status_idle = StatusIndicator()
        self.status_idle.set_status("idle")
        status_layout.addWidget(self.status_idle)
        
        self.status_scanning = StatusIndicator()
        self.status_scanning.set_status("scanning")
        status_layout.addWidget(self.status_scanning)
        
        self.status_connected = StatusIndicator()
        self.status_connected.set_status("connected")
        status_layout.addWidget(self.status_connected)
        
        self.status_error = StatusIndicator()
        self.status_error.set_status("error")
        status_layout.addWidget(self.status_error)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Progress indicator
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("Progress Animation:"))
        self.progress = ProgressIndicator()
        progress_layout.addWidget(self.progress)
        layout.addLayout(progress_layout)
        
        # Enhanced buttons
        buttons_layout = QVBoxLayout()
        
        self.hover_btn = EnhancedButton("Hover Me - Enhanced Animations")
        self.hover_btn.setFont(QFont("JetBrains Mono", 11))
        buttons_layout.addWidget(self.hover_btn)
        
        self.scale_btn = EnhancedButton("Click for Scale Animation")
        self.scale_btn.setFont(QFont("JetBrains Mono", 11))
        self.scale_btn.clicked.connect(self._demo_scale_animation)
        buttons_layout.addWidget(self.scale_btn)
        
        self.color_btn = EnhancedButton("Color Transition Demo")
        self.color_btn.setFont(QFont("JetBrains Mono", 11))
        self.color_btn.clicked.connect(self._demo_color_transition)
        buttons_layout.addWidget(self.color_btn)
        
        self.progress_btn = EnhancedButton("Animate Progress")
        self.progress_btn.setFont(QFont("JetBrains Mono", 11))
        self.progress_btn.clicked.connect(self._demo_progress_animation)
        buttons_layout.addWidget(self.progress_btn)
        
        layout.addLayout(buttons_layout)
        
        # Info
        info = QLabel("""
🎮 Interactions Available:
• Hover over buttons for glow effects
• Click buttons for ripple animations  
• Scale and color transitions
• Smooth progress animations
• Pulsing status indicators
• Professional feedback throughout
        """)
        info.setFont(QFont("JetBrains Mono", 9))
        info.setAlignment(Qt.AlignLeft)
        layout.addWidget(info)
        
        layout.addStretch()
    
    def _apply_theme(self):
        """Apply hacker theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A0A;
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel {
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
            }
            QPushButton {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 12px 20px;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
                font-weight: bold;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #00FF00;
                color: #000000;
                border: 2px solid #00AA00;
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
            }
            QPushButton:pressed {
                background-color: #00AA00;
                color: #000000;
            }
        """)
    
    def _setup_demo_animations(self):
        """Setup demo animations"""
        if ANIMATIONS_AVAILABLE:
            # Start entrance animation
            fade_anim = animation_manager.create_fade_animation(self, duration=800)
            fade_anim.start()
    
    def _demo_scale_animation(self):
        """Demo scale animation"""
        if ANIMATIONS_AVAILABLE:
            scale_anim = animation_manager.create_scale_animation(
                self.scale_btn, duration=300, start_scale=1.0, end_scale=1.1
            )
            
            def reverse_scale():
                reverse_anim = animation_manager.create_scale_animation(
                    self.scale_btn, duration=300, start_scale=1.1, end_scale=1.0
                )
                reverse_anim.start()
            
            scale_anim.finished.connect(reverse_scale)
            scale_anim.start()
    
    def _demo_color_transition(self):
        """Demo color transition"""
        if ANIMATIONS_AVAILABLE:
            from PyQt5.QtGui import QColor
            color_anim = animation_manager.create_color_transition(
                self.color_btn, duration=500,
                start_color=QColor(30, 30, 30),
                end_color=QColor(255, 100, 0)
            )
            
            def reverse_color():
                reverse_anim = animation_manager.create_color_transition(
                    self.color_btn, duration=500,
                    start_color=QColor(255, 100, 0),
                    end_color=QColor(30, 30, 30)
                )
                reverse_anim.start()
            
            color_anim.finished.connect(reverse_color)
            color_anim.start()
    
    def _demo_progress_animation(self):
        """Demo progress animation"""
        if hasattr(self.progress, 'set_progress_animated'):
            import random
            target = random.uniform(0.3, 1.0)
            self.progress.set_progress_animated(target, duration=1000)
        else:
            print("Progress animation not available")

def main():
    """Run the demo"""
    app = QApplication(sys.argv)
    app.setApplicationName("WiFi Radar Micro-Interactions Demo")
    
    # Set virtual display if needed
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':99.0'
    
    demo = MicroInteractionDemo()
    demo.show()
    
    print("🚀 Micro-interactions demo started!")
    print("📱 Window should display with enhanced animations")
    print("🎯 Try hovering and clicking buttons to see animations")
    
    # Auto-close after 10 seconds for testing
    QTimer.singleShot(10000, app.quit)
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())