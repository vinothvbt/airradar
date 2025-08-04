#!/usr/bin/env python3
"""
UI Animations and Micro-Interactions Module
Provides enhanced animations, transitions, and interactive feedback for WiFi Security Radar Suite
"""

from PyQt5.QtCore import (QPropertyAnimation, QEasingCurve, QVariantAnimation, 
                          QSequentialAnimationGroup, QParallelAnimationGroup, 
                          QTimer, pyqtSignal, pyqtProperty, QObject, QPoint, QSize)
from PyQt5.QtWidgets import QWidget, QGraphicsEffect, QGraphicsOpacityEffect
from PyQt5.QtGui import QColor, QPalette, QFont
import math

class AnimationManager(QObject):
    """Centralized animation manager for coordinating UI micro-interactions"""
    
    def __init__(self):
        super().__init__()
        self.active_animations = []
        self.hover_animations = {}
        self.pulse_timers = {}
        
    def create_fade_animation(self, target, duration=300, start_opacity=0.0, end_opacity=1.0):
        """Create smooth fade in/out animation"""
        effect = QGraphicsOpacityEffect()
        target.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.active_animations.append(animation)
        return animation
    
    def create_scale_animation(self, target, duration=200, start_scale=1.0, end_scale=1.05):
        """Create smooth scale animation for hover effects"""
        animation = QPropertyAnimation(target, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        # Calculate scaled geometry
        original_rect = target.geometry()
        center = original_rect.center()
        
        # Start geometry
        start_rect = original_rect
        
        # End geometry (scaled)
        end_width = int(original_rect.width() * end_scale)
        end_height = int(original_rect.height() * end_scale)
        end_rect = original_rect
        end_rect.setSize(QSize(end_width, end_height))
        end_rect.moveCenter(center)
        
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        
        self.active_animations.append(animation)
        return animation
    
    def create_color_transition(self, target, duration=300, start_color=None, end_color=None):
        """Create smooth color transition animation"""
        if start_color is None:
            start_color = QColor(30, 30, 30)  # Default dark
        if end_color is None:
            end_color = QColor(0, 255, 0)     # Matrix green
            
        animation = QVariantAnimation()
        animation.setDuration(duration)
        animation.setStartValue(start_color)
        animation.setEndValue(end_color)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        def update_color(color):
            target.setStyleSheet(f"""
                background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                border: 2px solid rgb({min(255, color.red() + 50)}, {min(255, color.green() + 50)}, {min(255, color.blue() + 50)});
            """)
        
        animation.valueChanged.connect(update_color)
        self.active_animations.append(animation)
        return animation
    
    def create_pulse_animation(self, target, duration=1000):
        """Create pulsing glow effect for status indicators"""
        animation = QVariantAnimation()
        animation.setDuration(duration)
        animation.setStartValue(0.3)
        animation.setEndValue(1.0)
        animation.setLoopCount(-1)  # Infinite loop
        animation.setEasingCurve(QEasingCurve.InOutSine)
        
        def update_pulse(opacity):
            target.setStyleSheet(f"""
                background-color: rgba(0, 255, 0, {int(opacity * 255)});
                border: 2px solid rgba(0, 170, 0, {int(opacity * 255)});
                border-radius: 6px;
            """)
        
        animation.valueChanged.connect(update_pulse)
        self.active_animations.append(animation)
        return animation
    
    def create_slide_animation(self, target, duration=400, start_pos=None, end_pos=None, direction='left'):
        """Create slide-in/out animation for panels"""
        animation = QPropertyAnimation(target, b"pos")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutQuart)
        
        if start_pos is None:
            current_pos = target.pos()
            if direction == 'left':
                start_pos = QPoint(current_pos.x() - target.width(), current_pos.y())
            elif direction == 'right':
                start_pos = QPoint(current_pos.x() + target.width(), current_pos.y())
            elif direction == 'up':
                start_pos = QPoint(current_pos.x(), current_pos.y() - target.height())
            else:  # down
                start_pos = QPoint(current_pos.x(), current_pos.y() + target.height())
        
        if end_pos is None:
            end_pos = target.pos()
            
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        
        self.active_animations.append(animation)
        return animation
    
    def create_ripple_effect(self, target, click_pos, duration=600):
        """Create material design-style ripple effect"""
        ripple_widget = QWidget(target)
        ripple_widget.setStyleSheet("""
            background-color: rgba(0, 255, 0, 100);
            border-radius: 50px;
        """)
        
        # Position ripple at click point
        ripple_widget.setGeometry(click_pos.x() - 25, click_pos.y() - 25, 50, 50)
        ripple_widget.show()
        
        # Scale animation
        scale_animation = QPropertyAnimation(ripple_widget, b"geometry")
        scale_animation.setDuration(duration)
        scale_animation.setEasingCurve(QEasingCurve.OutQuart)
        
        final_size = min(target.width(), target.height()) * 2
        final_rect = ripple_widget.geometry()
        final_rect.setSize(QSize(final_size, final_size))
        final_rect.moveCenter(click_pos)
        
        scale_animation.setStartValue(ripple_widget.geometry())
        scale_animation.setEndValue(final_rect)
        
        # Fade animation
        fade_animation = self.create_fade_animation(ripple_widget, duration, 0.8, 0.0)
        
        # Clean up when animation finishes
        def cleanup():
            ripple_widget.deleteLater()
        
        fade_animation.finished.connect(cleanup)
        
        # Start animations
        scale_animation.start()
        fade_animation.start()
        
        return scale_animation, fade_animation
    
    def animate_view_mode_transition(self, target, new_size, duration=500):
        """Animate smooth view mode transitions"""
        # Create size animation
        size_animation = QPropertyAnimation(target, b"size")
        size_animation.setDuration(duration)
        size_animation.setStartValue(target.size())
        size_animation.setEndValue(new_size)
        size_animation.setEasingCurve(QEasingCurve.OutExpo)
        
        # Create opacity animation for smooth transition
        opacity_animation = self.create_fade_animation(target, duration // 2, 1.0, 0.8)
        
        # Restore opacity after resize
        def restore_opacity():
            restore_anim = self.create_fade_animation(target, duration // 2, 0.8, 1.0)
            restore_anim.start()
        
        opacity_animation.finished.connect(restore_opacity)
        
        # Start animations
        size_animation.start()
        opacity_animation.start()
        
        return size_animation, opacity_animation


class EnhancedWidget(QWidget):
    """Enhanced widget with built-in micro-interactions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation_manager = AnimationManager()
        self.hover_scale = 1.02
        self.original_style = ""
        self._setup_interactions()
    
    def _setup_interactions(self):
        """Setup default micro-interactions"""
        self.setAttribute(51)  # Qt.WA_Hover
        self.setMouseTracking(True)
    
    def enterEvent(self, event):
        """Enhanced hover enter with animations"""
        super().enterEvent(event)
        
        # Scale animation
        scale_anim = self.animation_manager.create_scale_animation(
            self, duration=150, end_scale=self.hover_scale
        )
        scale_anim.start()
        
        # Color transition
        color_anim = self.animation_manager.create_color_transition(
            self, duration=200,
            start_color=QColor(30, 30, 30),
            end_color=QColor(45, 45, 45)
        )
        color_anim.start()
    
    def leaveEvent(self, event):
        """Enhanced hover leave with animations"""
        super().leaveEvent(event)
        
        # Restore scale
        scale_anim = self.animation_manager.create_scale_animation(
            self, duration=150, start_scale=self.hover_scale, end_scale=1.0
        )
        scale_anim.start()
        
        # Restore color
        color_anim = self.animation_manager.create_color_transition(
            self, duration=200,
            start_color=QColor(45, 45, 45),
            end_color=QColor(30, 30, 30)
        )
        color_anim.start()
    
    def mousePressEvent(self, event):
        """Enhanced click with ripple effect"""
        super().mousePressEvent(event)
        
        # Create ripple effect
        self.animation_manager.create_ripple_effect(self, event.pos())


class StatusIndicator(EnhancedWidget):
    """Animated status indicator with pulsing effects"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = "idle"
        self.pulse_animation = None
        self.setFixedSize(20, 20)
        self._update_appearance()
    
    def set_status(self, status):
        """Set status and update animations"""
        self.status = status
        self._update_appearance()
    
    def _update_appearance(self):
        """Update appearance based on status"""
        if self.pulse_animation:
            self.pulse_animation.stop()
            
        if self.status == "scanning":
            # Start pulsing animation
            self.pulse_animation = self.animation_manager.create_pulse_animation(self, 800)
            self.pulse_animation.start()
        elif self.status == "connected":
            self.setStyleSheet("""
                background-color: #00ff00;
                border: 2px solid #00aa00;
                border-radius: 10px;
            """)
        elif self.status == "error":
            self.setStyleSheet("""
                background-color: #ff4444;
                border: 2px solid #cc2222;
                border-radius: 10px;
            """)
        else:  # idle
            self.setStyleSheet("""
                background-color: #666666;
                border: 2px solid #444444;
                border-radius: 10px;
            """)


class ProgressIndicator(EnhancedWidget):
    """Smooth animated progress bar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0.0
        self.setFixedHeight(6)
        self.setMinimumWidth(200)
    
    @pyqtProperty(float)
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        self._progress = max(0.0, min(1.0, value))
        self.update()
    
    def set_progress_animated(self, target_progress, duration=300):
        """Animate progress change"""
        animation = QPropertyAnimation(self, b"progress")
        animation.setDuration(duration)
        animation.setStartValue(self._progress)
        animation.setEndValue(target_progress)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
        return animation
    
    def paintEvent(self, event):
        """Custom paint with gradient progress bar"""
        from PyQt5.QtGui import QPainter, QLinearGradient
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        # Progress
        if self._progress > 0:
            progress_width = int(self.width() * self._progress)
            
            gradient = QLinearGradient(0, 0, progress_width, 0)
            gradient.setColorAt(0, QColor(0, 255, 0))
            gradient.setColorAt(1, QColor(0, 170, 0))
            
            painter.fillRect(0, 0, progress_width, self.height(), gradient)


# Global animation manager instance
animation_manager = AnimationManager()