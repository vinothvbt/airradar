#!/usr/bin/env python3
"""
Real-time Graphs Module for WiFi Security Radar Suite
Provides real-time visualization of signal strength, network activity, and security metrics
"""

import sys
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import deque
import json

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QGroupBox, QTabWidget, QCheckBox, QSpinBox, QPushButton
)
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygon
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPointF, QRectF


class RealtimeGraphWidget(QWidget):
    """Base widget for real-time graph visualization"""
    
    def __init__(self, title="Graph", max_points=100):
        super().__init__()
        self.title = title
        self.max_points = max_points
        self.data_points = deque(maxlen=max_points)
        self.time_points = deque(maxlen=max_points)
        self.grid_enabled = True
        self.auto_scale = True
        self.min_value = 0
        self.max_value = 100
        
        # Styling
        self.background_color = QColor(10, 10, 10)
        self.grid_color = QColor(51, 51, 51)
        self.text_color = QColor(0, 255, 0)
        self.line_color = QColor(0, 255, 0)
        self.fill_color = QColor(0, 255, 0, 30)
        
        # Font
        self.font = QFont("JetBrains Mono", 8)
        
        self.setMinimumSize(400, 200)
        
    def add_data_point(self, value, timestamp=None):
        """Add a new data point to the graph"""
        if timestamp is None:
            timestamp = datetime.now()
            
        self.data_points.append(value)
        self.time_points.append(timestamp)
        
        # Auto-scale if enabled
        if self.auto_scale and self.data_points:
            self.min_value = min(self.data_points) - 5
            self.max_value = max(self.data_points) + 5
            
        self.update()
        
    def clear_data(self):
        """Clear all data points"""
        self.data_points.clear()
        self.time_points.clear()
        self.update()
        
    def paintEvent(self, event):
        """Paint the graph"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill background
        painter.fillRect(self.rect(), self.background_color)
        
        # Calculate drawing area
        margin = 40
        graph_rect = QRectF(
            margin, margin,
            self.width() - 2 * margin,
            self.height() - 2 * margin
        )
        
        # Draw title
        painter.setPen(self.text_color)
        painter.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
        painter.drawText(10, 25, self.title)
        
        # Draw grid if enabled
        if self.grid_enabled:
            self._draw_grid(painter, graph_rect)
            
        # Draw axes labels
        self._draw_axes_labels(painter, graph_rect)
        
        # Draw data if available
        if len(self.data_points) > 1:
            self._draw_data(painter, graph_rect)
            
    def _draw_grid(self, painter, rect):
        """Draw grid lines"""
        painter.setPen(QPen(self.grid_color, 1, Qt.DotLine))
        
        # Vertical grid lines
        for i in range(1, 10):
            x = rect.left() + (rect.width() * i / 10)
            painter.drawLine(x, rect.top(), x, rect.bottom())
            
        # Horizontal grid lines
        for i in range(1, 6):
            y = rect.top() + (rect.height() * i / 6)
            painter.drawLine(rect.left(), y, rect.right(), y)
            
    def _draw_axes_labels(self, painter, rect):
        """Draw axes labels"""
        painter.setPen(self.text_color)
        painter.setFont(self.font)
        
        # Y-axis labels (values)
        for i in range(6):
            value = self.max_value - (self.max_value - self.min_value) * i / 5
            y = rect.top() + (rect.height() * i / 5)
            painter.drawText(5, y + 5, f"{value:.1f}")
            
        # X-axis labels (time) - show last few timestamps
        if self.time_points:
            time_range = min(5, len(self.time_points))
            for i in range(time_range):
                if i < len(self.time_points):
                    timestamp = self.time_points[-(i+1)]
                    x = rect.right() - (rect.width() * i / (time_range - 1)) if time_range > 1 else rect.right()
                    time_str = timestamp.strftime("%H:%M:%S")
                    painter.drawText(x - 25, rect.bottom() + 15, time_str)
                    
    def _draw_data(self, painter, rect):
        """Draw the data line"""
        if not self.data_points or len(self.data_points) < 2:
            return
            
        # Create points for the line
        points = []
        data_list = list(self.data_points)
        
        for i, value in enumerate(data_list):
            x = rect.left() + (rect.width() * i / (len(data_list) - 1))
            y_ratio = (value - self.min_value) / (self.max_value - self.min_value) if self.max_value != self.min_value else 0.5
            y = rect.bottom() - (rect.height() * y_ratio)
            points.append(QPointF(x, y))
            
        # Draw fill area
        if len(points) > 1:
            fill_polygon = QPolygon()
            for point in points:
                fill_polygon.append(point.toPoint())
            fill_polygon.append(QPointF(rect.right(), rect.bottom()).toPoint())
            fill_polygon.append(QPointF(rect.left(), rect.bottom()).toPoint())
            
            painter.setBrush(QBrush(self.fill_color))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(fill_polygon)
            
        # Draw line
        painter.setPen(QPen(self.line_color, 2))
        painter.setBrush(Qt.NoBrush)
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])
            
        # Draw data points
        painter.setBrush(QBrush(self.line_color))
        for point in points:
            painter.drawEllipse(point, 3, 3)


class SignalStrengthGraph(RealtimeGraphWidget):
    """Real-time signal strength graph"""
    
    def __init__(self):
        super().__init__("Signal Strength (dBm)", max_points=50)
        self.min_value = -100
        self.max_value = -30
        self.auto_scale = False
        self.line_color = QColor(0, 255, 0)
        self.fill_color = QColor(0, 255, 0, 40)


class NetworkActivityGraph(RealtimeGraphWidget):
    """Real-time network activity graph"""
    
    def __init__(self):
        super().__init__("Network Activity (Networks Detected)", max_points=60)
        self.min_value = 0
        self.max_value = 50
        self.line_color = QColor(0, 150, 255)
        self.fill_color = QColor(0, 150, 255, 40)


class SecurityTrendGraph(RealtimeGraphWidget):
    """Real-time security threat level graph"""
    
    def __init__(self):
        super().__init__("Security Threat Level", max_points=40)
        self.min_value = 0
        self.max_value = 100
        self.line_color = QColor(255, 100, 0)
        self.fill_color = QColor(255, 100, 0, 40)


class RealtimeGraphsPanel(QWidget):
    """Panel containing multiple real-time graphs"""
    
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.signal_graph = SignalStrengthGraph()
        self.activity_graph = NetworkActivityGraph()
        self.security_graph = SecurityTrendGraph()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._generate_sample_data)
        
        # Data tracking
        self.current_networks = []
        self.last_update = datetime.now()
        
        self._setup_ui()
        self._apply_theme()
        
    def _setup_ui(self):
        """Setup the graphs panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Panel title
        title = QLabel("Real-time Monitoring Dashboard")
        title.setFont(QFont("JetBrains Mono", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Auto-update checkbox
        self.auto_update_cb = QCheckBox("Auto Update")
        self.auto_update_cb.setChecked(True)
        self.auto_update_cb.toggled.connect(self._toggle_auto_update)
        controls_layout.addWidget(self.auto_update_cb)
        
        # Update interval
        controls_layout.addWidget(QLabel("Interval (sec):"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 60)
        self.interval_spin.setValue(2)
        self.interval_spin.valueChanged.connect(self._update_interval_changed)
        controls_layout.addWidget(self.interval_spin)
        
        # Clear data button
        clear_btn = QPushButton("Clear Data")
        clear_btn.clicked.connect(self._clear_all_data)
        controls_layout.addWidget(clear_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Tab widget for different graphs
        self.tab_widget = QTabWidget()
        
        # Signal strength tab
        signal_tab = QWidget()
        signal_layout = QVBoxLayout(signal_tab)
        signal_layout.addWidget(self.signal_graph)
        self.tab_widget.addTab(signal_tab, "Signal Strength")
        
        # Network activity tab
        activity_tab = QWidget()
        activity_layout = QVBoxLayout(activity_tab)
        activity_layout.addWidget(self.activity_graph)
        self.tab_widget.addTab(activity_tab, "Network Activity")
        
        # Security trends tab
        security_tab = QWidget()
        security_layout = QVBoxLayout(security_tab)
        security_layout.addWidget(self.security_graph)
        self.tab_widget.addTab(security_tab, "Security Trends")
        
        layout.addWidget(self.tab_widget)
        
        # Start auto-update
        self._toggle_auto_update(True)
        
    def _apply_theme(self):
        """Apply consistent hacker theme"""
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel {
                color: #00ff00;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 2px solid #333;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #00ff00;
                padding: 8px 16px;
                margin: 2px;
                border: 1px solid #555;
            }
            QTabBar::tab:selected {
                background-color: #00ff00;
                color: #000000;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #003300;
                border: 1px solid #00ff00;
            }
            QCheckBox {
                color: #00ff00;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555;
                background-color: #1a1a1a;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #00ff00;
                background-color: #00ff00;
            }
            QSpinBox {
                border: 2px solid #555;
                background-color: #1a1a1a;
                color: #00ff00;
                padding: 4px;
                min-width: 60px;
            }
            QSpinBox:focus {
                border: 2px solid #00ff00;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: #00ff00;
                border: 2px solid #555;
                padding: 6px 12px;
                font-weight: bold;
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
        
    def _toggle_auto_update(self, enabled):
        """Toggle auto-update functionality"""
        if enabled:
            interval = self.interval_spin.value() * 1000  # Convert to milliseconds
            self.update_timer.start(interval)
        else:
            self.update_timer.stop()
            
    def _update_interval_changed(self, value):
        """Update the timer interval"""
        if self.update_timer.isActive():
            self.update_timer.stop()
            self.update_timer.start(value * 1000)
            
    def _clear_all_data(self):
        """Clear data from all graphs"""
        self.signal_graph.clear_data()
        self.activity_graph.clear_data()
        self.security_graph.clear_data()
        
    def _generate_sample_data(self):
        """Generate sample data for demonstration"""
        import random
        now = datetime.now()
        
        # Simulate signal strength (fluctuating around -60 dBm)
        signal_strength = -60 + random.randint(-20, 10)
        self.signal_graph.add_data_point(signal_strength, now)
        
        # Simulate network activity (random number of networks)
        network_count = random.randint(5, 25)
        self.activity_graph.add_data_point(network_count, now)
        
        # Simulate security threat level (based on network types)
        threat_level = random.randint(20, 80)
        self.security_graph.add_data_point(threat_level, now)
        
        # Emit data update signal
        self.data_updated.emit({
            'signal_strength': signal_strength,
            'network_count': network_count,
            'threat_level': threat_level,
            'timestamp': now
        })
        
    def update_with_real_data(self, networks_data):
        """Update graphs with real WiFi data"""
        if not networks_data:
            return
            
        now = datetime.now()
        
        # Calculate average signal strength
        signal_strengths = [ap.get('signal', -70) for ap in networks_data if 'signal' in ap]
        avg_signal = sum(signal_strengths) / len(signal_strengths) if signal_strengths else -70
        self.signal_graph.add_data_point(avg_signal, now)
        
        # Network count
        network_count = len(networks_data)
        self.activity_graph.add_data_point(network_count, now)
        
        # Security threat level (based on security types)
        threat_scores = []
        for ap in networks_data:
            security = ap.get('security', 'Unknown').upper()
            if 'OPEN' in security:
                threat_scores.append(95)
            elif 'WEP' in security:
                threat_scores.append(90)
            elif 'WPA3' in security:
                threat_scores.append(15)
            elif 'WPA2' in security:
                threat_scores.append(35)
            elif 'WPA' in security:
                threat_scores.append(50)
            else:
                threat_scores.append(40)
                
        avg_threat = sum(threat_scores) / len(threat_scores) if threat_scores else 40
        self.security_graph.add_data_point(avg_threat, now)
        
        # Emit data update
        self.data_updated.emit({
            'signal_strength': avg_signal,
            'network_count': network_count,
            'threat_level': avg_threat,
            'timestamp': now,
            'networks_data': networks_data
        })


# Export functionality for integration
__all__ = [
    'RealtimeGraphWidget',
    'SignalStrengthGraph', 
    'NetworkActivityGraph',
    'SecurityTrendGraph',
    'RealtimeGraphsPanel'
]


if __name__ == "__main__":
    # Test the graphs panel
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    panel = RealtimeGraphsPanel()
    panel.setWindowTitle("Real-time Graphs Test")
    panel.show()
    
    sys.exit(app.exec_())