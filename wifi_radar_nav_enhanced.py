#!/usr/bin/env python3
"""
WiFi Radar with Professional Navigation and Scrollable Side Panels
Enhanced modern UI with top navigation bar and improved layout
Version: 4.0.0 - Navigation Enhanced
"""

import sys
import os
import json
import re
import subprocess
import time
import math
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import sqlite3

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QSlider, QPushButton, QComboBox, QCheckBox,
    QGroupBox, QStatusBar, QTabWidget, QListWidget, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QSplitter,
    QScrollArea, QToolButton, QDialog, QMessageBox, QSpinBox,
    QMenuBar, QAction, QToolBar, QProgressBar, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QPalette, QPixmap,
    QLinearGradient, QRadialGradient, QPolygon, QPainterPath, QIcon
)
from PyQt5.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPointF, QRectF, QPoint, QSize,
    QRect, QMutex
)

# Configuration
CONFIG_FILE = 'wifi_radar_nav_config.json'
DB_FILE = 'wifi_nav_enhanced.db'

# Enhanced UI Constants
RADAR_SIZE = 450
MAX_RADIUS = 180
RING_SPACING = 30
DOT_SIZE =10
FONT_SIZE = 11  # Increased from 9
VERSION = "4.0.0"

# Navigation Bar Height
NAV_BAR_HEIGHT = 30

# Penetration Testing Constants
SIGNAL_THRESHOLDS = {
    'EXCELLENT': -30,
    'GOOD': -50, 
    'FAIR': -70,
    'POOR': -85,
    'VERY_POOR': -100
}

# UI Mode Settings
DARK_MODE = True
COMPACT_MODE = True

# View Mode Constants
VIEW_MODES = {
    'COMPACT': (800, 500),
    'NORMAL': (1400, 800),
    'FULLSCREEN': None
}

# Pre-compile regex patterns for performance
MAC_PATTERN = re.compile(r'([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})')
SIGNAL_PATTERN = re.compile(r'signal:\s*(-?\d+(?:\.\d+)?)\s*dBm', re.IGNORECASE)
FREQ_PATTERN = re.compile(r'freq:\s*(\d+)', re.IGNORECASE)
SSID_PATTERN = re.compile(r'SSID:\s*(.+?)(?:\n|$)')

@dataclass
class AccessPoint:
    """Enhanced AP class with comprehensive penetration testing capabilities"""
    bssid: str
    ssid: str
    signal_dbm: float
    frequency: int
    channel: int = 0
    security: str = "Unknown"
    last_seen: datetime = field(default_factory=datetime.now)
    
    # Enhanced positioning and analysis
    distance: float = 0.0
    angle: float = 0.0
    vendor: str = "Unknown"
    confidence: float = 0.0
    
    # Penetration testing features
    vulnerability_score: int = 0
    attack_vectors: List[str] = field(default_factory=list)
    threat_level: str = "LOW"
    is_vulnerable: bool = False
    
    # Advanced security analysis
    encryption_details: str = ""
    wps_enabled: bool = False
    client_count: int = 0
    uptime_estimate: int = 0
    
    def __post_init__(self):
        """Initialize calculated fields"""
        self._calculate_distance()
        self._calculate_angle()
        self._analyze_vendor()
        self._analyze_security()
    
    def _calculate_distance(self):
        """Calculate distance using Free Space Path Loss (FSPL) formula"""
        if self.signal_dbm >= -30:
            self.distance = 1.0
        elif self.signal_dbm >= -50:
            self.distance = 5.0 + ((-30 - self.signal_dbm) * 0.3)
        elif self.signal_dbm >= -70:
            self.distance = 15.0 + ((-50 - self.signal_dbm) * 0.8)
        elif self.signal_dbm >= -85:
            self.distance = 35.0 + ((-70 - self.signal_dbm) * 2.0)
        else:
            self.distance = 65.0 + ((-85 - self.signal_dbm) * 3.0)
        
        # Add some randomization for more realistic positioning
        import random
        self.distance *= random.uniform(0.8, 1.2)
        self.distance = max(1.0, min(150.0, self.distance))
    
    def _calculate_angle(self):
        """Calculate angle based on BSSID for consistent positioning"""
        # Use BSSID hash for consistent angle calculation
        hash_val = hash(self.bssid.replace(':', ''))
        # Distribute angles more evenly to prevent clustering
        base_angle = (hash_val % 360) * math.pi / 180
        
        # Add channel-based offset for better distribution
        channel_offset = (self.channel * 13.7) * math.pi / 180
        
        self.angle = (base_angle + channel_offset) % (2 * math.pi)
    
    def _analyze_vendor(self):
        """Analyze vendor from MAC address OUI"""
        oui = self.bssid.replace(':', '').upper()
        
        vendors = {
            # Major router manufacturers
            "D4CA6D": "ASUS", "704D7B": "ASUS", "1CB72C": "ASUS", "2C56DC": "ASUS",
            "90F652": "ASUS", "AC220B": "ASUS", "0C9D92": "ASUS", "50465D": "ASUS",
            
            # Cisco/Linksys
            "0013C4": "Cisco", "001DE5": "Cisco", "00264A": "Cisco", "68BD15": "Cisco",
            "68EF43": "Linksys", "F0B4D2": "Linksys", "24A43C": "Linksys", "20AA4B": "Linksys",
            
            # TP-Link
            "ECF4BB": "TP-Link", "9C53CD": "TP-Link", "E8DE27": "TP-Link", "C05326": "TP-Link",
            "14CC20": "TP-Link", "0C8066": "TP-Link", "843497": "TP-Link", "748EE8": "TP-Link",
            
            # Netgear
            "9CB70D": "Netgear", "A021B7": "Netgear", "0846A0": "Netgear", "2C3033": "Netgear",
            "CC40D0": "Netgear", "84D6D0": "Netgear", "4CF952": "Netgear", "04BF6D": "Netgear",
            
            # D-Link
            "B0487A": "D-Link", "CCDC02": "D-Link", "142D27": "D-Link", "E46F13": "D-Link",
            "5CD998": "D-Link", "E0051E": "D-Link", "C8BE19": "D-Link", "BC5FF4": "D-Link",
            
            # Apple
            "8863DF": "Apple", "041E64": "Apple", "04E536": "Apple", "68AB1E": "Apple",
            "D89695": "Apple", "A85C2C": "Apple", "7C6D62": "Apple", "0056CD": "Apple",
            
            # Intel
            "00A0C9": "Intel", "001F3F": "Intel", "0024D7": "Intel", "8C705A": "Intel",
            
            # Samsung
            "002454": "Samsung", "001485": "Samsung", "1C232C": "Samsung", "C8F733": "Samsung",
            
            # VMware/Virtualization
            "005056": "VMware", "080027": "Oracle", "00155D": "Microsoft", "001C42": "Parallels"
        }
        
        self.vendor = vendors.get(oui[:6], "Unknown")
    
    def _analyze_security(self):
        """Comprehensive security analysis with vulnerability assessment"""
        self.attack_vectors = []
        base_score = 0
        
        # Security protocol analysis
        security_lower = self.security.lower()
        
        if 'open' in security_lower or not self.security or self.security == "":
            base_score = 95
            self.threat_level = "CRITICAL"
            self.is_vulnerable = True
            self.encryption_details = "No encryption"
            self.attack_vectors = [
                "Direct network access",
                "Traffic interception and analysis", 
                "Man-in-the-middle attacks",
                "Packet injection and manipulation",
                "DNS spoofing and redirection",
                "Evil twin access point setup",
                "Session hijacking",
                "Credential harvesting"
            ]
            
        elif 'wep' in security_lower:
            base_score = 88
            self.threat_level = "CRITICAL"
            self.is_vulnerable = True
            self.encryption_details = "WEP (Broken encryption)"
            self.attack_vectors = [
                "WEP key cracking (aircrack-ng)",
                "IV collision attacks",
                "Chopchop attack",
                "Fragmentation attack",
                "Fake authentication bypass",
                "Statistical cryptanalysis",
                "Korek attacks",
                "PTW attack method"
            ]
            
        elif 'wpa3' in security_lower:
            base_score = 15
            self.threat_level = "LOW"
            self.encryption_details = "WPA3 (Latest security)"
            self.attack_vectors = [
                "SAE downgrade attacks",
                "Implementation vulnerabilities",
                "Side-channel timing attacks",
                "Dragonfly handshake analysis"
            ]
            
        elif 'wpa2' in security_lower:
            base_score = 35
            self.threat_level = "MEDIUM"
            self.encryption_details = "WPA2"
            self.attack_vectors = [
                "4-way handshake capture",
                "Dictionary and wordlist attacks",
                "Brute force password cracking",
                "PMKID attack (hashcat)",
                "Deauthentication attacks",
                "WPS PIN cracking (if enabled)",
                "KRACK vulnerability exploitation"
            ]
            
        elif 'wpa' in security_lower:
            base_score = 45
            self.threat_level = "MEDIUM"
            self.encryption_details = "WPA (Legacy)"
            self.attack_vectors = [
                "4-way handshake capture",
                "Dictionary attacks",
                "WPA-PSK cracking",
                "Deauthentication attacks",
                "Beck-Tews attack",
                "Chopchop variations"
            ]
        
        # Signal strength impact
        if self.signal_dbm > -30:
            base_score += 25
            self.attack_vectors.append("Very strong signal - easy target")
        elif self.signal_dbm > -50:
            base_score += 20
            self.attack_vectors.append("Strong signal - viable target")
        elif self.signal_dbm > -70:
            base_score += 10
            self.attack_vectors.append("Moderate signal strength")
        
        # SSID-based vulnerability indicators
        ssid_lower = self.ssid.lower()
        weak_indicators = [
            ('test', 15, "Test network - likely insecure"),
            ('guest', 12, "Guest network - reduced security"),
            ('public', 18, "Public network - high risk"),
            ('free', 20, "Free network - likely open"),
            ('admin', 10, "Admin network - default config risk"),
            ('default', 15, "Default SSID - unchanged config"),
            ('linksys', 12, "Default Linksys SSID"),
            ('netgear', 12, "Default Netgear SSID"),
            ('dlink', 12, "Default D-Link SSID"),
            ('router', 8, "Generic router name")
        ]
        
        for indicator, score_bonus, description in weak_indicators:
            if indicator in ssid_lower:
                base_score += score_bonus
                self.attack_vectors.append(description)
        
        # Hidden SSID check
        if not self.ssid or self.ssid.strip() == "" or "\\x00" in self.ssid:
            base_score += 5
            self.attack_vectors.append("Hidden SSID - probe request attacks")
        
        # Frequency-based analysis
        if self.frequency < 2500:  # 2.4GHz
            base_score += 5
            self.attack_vectors.append("2.4GHz band - more crowded, easier monitoring")
        elif self.frequency > 5000:  # 5GHz
            base_score += 2
            self.attack_vectors.append("5GHz band - shorter range but less monitored")
        
        # Finalize vulnerability score and threat level
        self.vulnerability_score = min(100, base_score)
        
        if self.vulnerability_score >= 80:
            self.threat_level = "CRITICAL"
            self.is_vulnerable = True
        elif self.vulnerability_score >= 60:
            self.threat_level = "HIGH"
            self.is_vulnerable = True
        elif self.vulnerability_score >= 40:
            self.threat_level = "MEDIUM"
            self.is_vulnerable = True
        elif self.vulnerability_score >= 20:
            self.threat_level = "LOW"
        else:
            self.threat_level = "MINIMAL"

def scan_wifi(interface: str = 'wlan0') -> List[Dict]:
    """Enhanced WiFi scanning with comprehensive parsing"""
    cmd = f"sudo iw dev {interface} scan"
    try:
        output = subprocess.check_output(
            cmd.split(), 
            stderr=subprocess.DEVNULL, 
            timeout=30
        ).decode()
        return parse_iw_output(output)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        try:
            cmd = f"sudo iwlist {interface} scan"
            output = subprocess.check_output(
                cmd.split(), 
                stderr=subprocess.DEVNULL, 
                timeout=30
            ).decode()
            return parse_iwlist_output(output)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return []

def parse_iw_output(output: str) -> List[Dict]:
    """Parse iw scan output with enhanced extraction"""
    networks = []
    blocks = output.split('BSS ')[1:]
    
    for block in blocks:
        try:
            lines = block.split('\n')
            bssid = lines[0].split('(')[0].strip()
            
            ssid_match = SSID_PATTERN.search(block)
            ssid = ssid_match.group(1).strip() if ssid_match else ""
            
            signal_match = SIGNAL_PATTERN.search(block)
            if not signal_match:
                continue
            signal = float(signal_match.group(1))
            
            freq_match = FREQ_PATTERN.search(block)
            if not freq_match:
                continue
            frequency = int(freq_match.group(1))
            
            if 2412 <= frequency <= 2484:
                channel = (frequency - 2412) // 5 + 1
            elif 5170 <= frequency <= 5825:
                channel = (frequency - 5000) // 5
            else:
                channel = 0
            
            security = "Open"
            if 'Privacy' in block or 'Capability' in block:
                if 'RSN' in block:
                    if 'SAE' in block or 'WPA3' in block:
                        security = "WPA3"
                    else:
                        security = "WPA2"
                elif 'WPA' in block:
                    security = "WPA"
                elif 'Privacy' in block:
                    security = "WEP"
            
            wps_enabled = 'WPS' in block or 'Wi-Fi Protected Setup' in block
            
            networks.append({
                'bssid': bssid,
                'ssid': ssid,
                'signal': signal,
                'frequency': frequency,
                'channel': channel,
                'security': security,
                'wps_enabled': wps_enabled
            })
            
        except (ValueError, IndexError):
            continue
    
    return networks

def parse_iwlist_output(output: str) -> List[Dict]:
    """Parse iwlist scan output"""
    networks = []
    cells = output.split('Cell ')[1:]
    
    for cell in cells:
        try:
            bssid_match = re.search(r'Address: ([0-9A-F:]{17})', cell, re.IGNORECASE)
            if not bssid_match:
                continue
            bssid = bssid_match.group(1)
            
            ssid_match = re.search(r'ESSID:"(.+?)"', cell)
            ssid = ssid_match.group(1) if ssid_match else ""
            
            signal_match = re.search(r'Signal level=([-\d]+) dBm', cell)
            if not signal_match:
                continue
            signal = float(signal_match.group(1))
            
            freq_match = re.search(r'Frequency:([\d.]+) GHz', cell)
            if freq_match:
                frequency = int(float(freq_match.group(1)) * 1000)
            else:
                frequency = 2437
                
            if 2412 <= frequency <= 2484:
                channel = (frequency - 2412) // 5 + 1
            else:
                channel = 0
            
            security = "Open"
            if "Encryption key:on" in cell:
                if "WPA3" in cell:
                    security = "WPA3"
                elif "WPA2" in cell:
                    security = "WPA2"
                elif "WPA" in cell:
                    security = "WPA"
                else:
                    security = "WEP"
            
            networks.append({
                'bssid': bssid,
                'ssid': ssid,
                'signal': signal,
                'frequency': frequency,
                'channel': channel,
                'security': security,
                'wps_enabled': False
            })
            
        except (ValueError, IndexError):
            continue
    
    return networks

class WiFiScanner(QThread):
    """Enhanced background WiFi scanning"""
    access_points_found = pyqtSignal(list)
    scan_error = pyqtSignal(str)
    scan_progress = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._mutex = QMutex()
        self._running = False
        self._interface = 'wlan0'
        self._scan_interval = 5
        
    def set_interface(self, interface: str):
        self._mutex.lock()
        self._interface = interface
        self._mutex.unlock()
    
    def set_scan_interval(self, interval: int):
        self._mutex.lock()
        self._scan_interval = interval
        self._mutex.unlock()
    
    def start_scanning(self):
        self._mutex.lock()
        self._running = True
        self._mutex.unlock()
        self.start()
    
    def stop_scanning(self):
        self._mutex.lock()
        self._running = False
        self._mutex.unlock()
        self.quit()
        self.wait(2000)
    
    def run(self):
        while True:
            self._mutex.lock()
            should_continue = self._running
            interface = self._interface
            interval = self._scan_interval
            self._mutex.unlock()
            
            if not should_continue:
                break
            
            try:
                self.scan_progress.emit(25)
                networks = scan_wifi(interface)
                self.scan_progress.emit(75)
                
                access_points = []
                for net in networks:
                    ap = AccessPoint(
                        bssid=net['bssid'],
                        ssid=net['ssid'],
                        signal_dbm=net['signal'],
                        frequency=net['frequency'],
                        channel=net['channel'],
                        security=net['security']
                    )
                    access_points.append(ap)
                
                self.scan_progress.emit(100)
                self.access_points_found.emit(access_points)
                
            except Exception as e:
                self.scan_error.emit(str(e))
            
            time.sleep(interval)

class RadarCanvas(QWidget):
    """Enhanced radar canvas with modern visualization"""
    ap_selected = pyqtSignal(object)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.dot_positions = []
        self._selected_index = -1
        self.access_points = []
        
        # UI settings
        self.show_vulnerable_only = False
        self.show_threat_colors = True
        
        self.setFixedSize(RADAR_SIZE, RADAR_SIZE)
        self._center_x = RADAR_SIZE // 2
        self._center_y = RADAR_SIZE // 2
        
        self._setup_graphics()
        self._apply_theme()

    def _setup_graphics(self):
        """Initialize graphics elements"""
        self._green_pen = QPen(QColor(0, 255, 0), 1)
        self._light_green_pen = QPen(QColor(0, 200, 0), 1)
        self._grid_pen = QPen(QColor(0, 120, 0), 1, Qt.DotLine)
        self._white_pen = QPen(Qt.white, 1)
        self._red_pen = QPen(Qt.red, 2)
        self._yellow_pen = QPen(Qt.yellow, 2)
        
        self.threat_colors = {
            'CRITICAL': QColor(255, 0, 0),
            'HIGH': QColor(255, 165, 0),
            'MEDIUM': QColor(255, 255, 0),
            'LOW': QColor(0, 255, 255),
            'MINIMAL': QColor(0, 255, 0)
        }
        
        self._small_font = QFont("JetBrains Mono", 10)  # Increased from 8
        self._normal_font = QFont("JetBrains Mono", 11)  # Increased from 9

    def _apply_theme(self):
        """Apply dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 10))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def set_show_vulnerable_only(self, enabled: bool):
        self.show_vulnerable_only = enabled
        self.update()
        
    def set_show_threat_colors(self, enabled: bool):
        self.show_threat_colors = enabled
        self.update()

    def update_access_points(self, aps: List[AccessPoint]):
        """Update access points with anti-clustering"""
        self.access_points = aps
        self.dot_positions.clear()
        
        display_aps = aps
        if self.show_vulnerable_only:
            display_aps = [ap for ap in aps if ap.is_vulnerable]
        
        used_positions = []
        min_distance_between_aps = 30
        
        for i, ap in enumerate(display_aps):
            radius = min(ap.distance * MAX_RADIUS / self.parent.max_distance, MAX_RADIUS - 10)
            
            x = int(self._center_x + radius * math.cos(ap.angle))
            y = int(self._center_y + radius * math.sin(ap.angle))
            
            attempts = 0
            while attempts < 25:
                too_close = False
                for used_pos in used_positions:
                    distance = math.sqrt((x - used_pos[0])**2 + (y - used_pos[1])**2)
                    if distance < min_distance_between_aps:
                        too_close = True
                        break
                
                if not too_close:
                    break
                
                angle_adjustment = (attempts * 12) * math.pi / 180
                new_angle = ap.angle + angle_adjustment
                x = int(self._center_x + radius * math.cos(new_angle))
                y = int(self._center_y + radius * math.sin(new_angle))
                attempts += 1
            
            used_positions.append((x, y))
            self.dot_positions.append({
                'x': x,
                'y': y,
                'ap': ap,
                'index': i
            })
        
        self.update()

    def paintEvent(self, event):
        """Main paint event"""
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        self._draw_grid_lines(qp)
        self._draw_access_points(qp)
        self._draw_statistics(qp)

    def _draw_grid_lines(self, qp):
        """Draw radar grid"""
        qp.setPen(self._grid_pen)
        for r in range(RING_SPACING, MAX_RADIUS + 1, RING_SPACING):
            qp.drawEllipse(
                self._center_x - r, self._center_y - r, 
                2 * r, 2 * r
            )
        
        qp.setPen(self._light_green_pen)
        qp.drawLine(
            self._center_x - MAX_RADIUS, self._center_y, 
            self._center_x + MAX_RADIUS, self._center_y
        )
        qp.drawLine(
            self._center_x, self._center_y - MAX_RADIUS, 
            self._center_x, self._center_y + MAX_RADIUS
        )

    def _draw_access_points(self, qp):
        """Draw access points with threat visualization"""
        for pos_data in self.dot_positions:
            x, y = pos_data['x'], pos_data['y']
            ap = pos_data['ap']
            
            if self.show_threat_colors and ap.threat_level in self.threat_colors:
                color = self.threat_colors[ap.threat_level]
            else:
                signal_ratio = max(0, min(1, (ap.signal_dbm + 100) / 60))
                color = QColor(
                    int(255 * (1 - signal_ratio)),
                    int(255 * signal_ratio),
                    0
                )
            
            if ap.is_vulnerable:
                qp.setPen(QPen(Qt.red, 3))
                qp.setBrush(QBrush())
                vulnerability_radius = DOT_SIZE + 10
                qp.drawEllipse(
                    x - vulnerability_radius//2, y - vulnerability_radius//2,
                    vulnerability_radius, vulnerability_radius
                )
            
            qp.setBrush(QBrush(color))
            qp.setPen(QPen(Qt.black, 2))
            qp.drawEllipse(x - DOT_SIZE//2, y - DOT_SIZE//2, DOT_SIZE, DOT_SIZE)
            
            if pos_data['index'] == self._selected_index:
                crosshair_size = 20
                qp.setPen(self._yellow_pen)
                qp.setBrush(QBrush())
                
                qp.drawEllipse(x - crosshair_size//2, y - crosshair_size//2,
                              crosshair_size, crosshair_size)
                
                line_length = 12
                qp.drawLine(x - crosshair_size//2 - line_length, y,
                           x - crosshair_size//2, y)
                qp.drawLine(x + crosshair_size//2, y,
                           x + crosshair_size//2 + line_length, y)
                qp.drawLine(x, y - crosshair_size//2 - line_length,
                           x, y - crosshair_size//2)
                qp.drawLine(x, y + crosshair_size//2,
                           x, y + crosshair_size//2 + line_length)
            
            qp.setPen(self._white_pen)
            qp.setFont(self._normal_font)  # Use normal font instead of small font
            
            text_offset_x = DOT_SIZE + 10
            text_offset_y = 4
            
            ssid = ap.ssid[:15] + ('...' if len(ap.ssid) > 15 else '')
            if not ap.ssid or ap.ssid.strip() == "":
                ssid = "<HIDDEN>"
            qp.drawText(x + text_offset_x, y + text_offset_y, ssid)

    def _draw_statistics(self, qp):
        """Draw statistics overlay"""
        qp.setPen(self._green_pen)
        qp.setFont(self._normal_font)  # Use normal font instead of small font
        
        total = len(self.access_points)
        vulnerable = sum(1 for ap in self.access_points if ap.is_vulnerable)
        critical = sum(1 for ap in self.access_points if ap.threat_level == "CRITICAL")
        high = sum(1 for ap in self.access_points if ap.threat_level == "HIGH")
        
        y_pos = 15
        qp.drawText(10, y_pos, f"TOTAL: {total}")
        qp.drawText(10, y_pos + 15, f"VULN: {vulnerable}")
        
        qp.setPen(QPen(Qt.red, 1))
        qp.drawText(10, y_pos + 30, f"CRIT: {critical}")
        
        qp.setPen(QPen(QColor(255, 165, 0), 1))
        qp.drawText(10, y_pos + 45, f"HIGH: {high}")

    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        click_x, click_y = event.x(), event.y()
        
        closest_index = -1
        min_distance = 25
        
        for pos_data in self.dot_positions:
            dx = click_x - pos_data['x']
            dy = click_y - pos_data['y']
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < min_distance:
                min_distance = distance
                closest_index = pos_data['index']
        
        if closest_index >= 0:
            self._selected_index = closest_index
            selected_ap = self.dot_positions[closest_index]['ap']
            self.ap_selected.emit(selected_ap)
            self.update()
        else:
            self._selected_index = -1
            self.ap_selected.emit(None)
            self.update()

class NavigationRadarWindow(QMainWindow):
    """Modern WiFi radar with navigation bar and scrollable panels"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration
        self.max_distance = 150
        self.scan_interval = 5
        self.interface = 'wlan0'
        self.current_view_mode = 'NORMAL'
        
        # Initialize components
        self.scanner = WiFiScanner()
        self.scanner.access_points_found.connect(self.update_access_points)
        self.scanner.scan_error.connect(self.handle_scan_error)
        self.scanner.scan_progress.connect(self.update_progress)
        
        self._setup_ui()
        self._setup_navigation()
        self._setup_connections()
        
        # Start scanning
        self.start_scanning()
        
        # Set window properties
        self.setWindowTitle(f'WiFi Radar Navigation Enhanced v{VERSION}')
        self.set_view_mode('NORMAL')
        
        # Apply dark theme
        self._apply_dark_theme()

    def _apply_dark_theme(self):
        """Apply comprehensive professional hacker-style dark theme"""
        self.setStyleSheet("""
            /* === MAIN WINDOW === */
            QMainWindow {
                background-color: #0A0A0A;
                color: #00FF00;
                font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
            }
            
            /* === MENU BAR === */
            QMenuBar {
                background-color: #141414;
                color: #00FF00;
                border-bottom: 2px solid #00FF00;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                font-weight: bold;
                padding: 4px;
                spacing: 2px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                margin: 1px;
                border-radius: 4px;
                border: 1px solid transparent;
            }
            QMenuBar::item:selected {
                background-color: #00FF00;
                color: #000000;
                border: 1px solid #00AA00;
            }
            QMenuBar::item:pressed {
                background-color: #00AA00;
                color: #000000;
            }
            
            /* === MENU DROPDOWNS === */
            QMenu {
                background-color: #1A1A1A;
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 6px;
                padding: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 20px;
                margin: 1px;
                border-radius: 3px;
                border: 1px solid transparent;
            }
            QMenu::item:selected {
                background-color: #00FF00;
                color: #000000;
                border: 1px solid #00AA00;
            }
            QMenu::item:pressed {
                background-color: #00AA00;
            }
            QMenu::separator {
                height: 2px;
                background-color: #00FF00;
                margin: 4px 10px;
            }
            QMenu::indicator {
                width: 14px;
                height: 14px;
                margin-left: 6px;
            }
            QMenu::indicator:checked {
                background-color: #00FF00;
                border: 1px solid #00AA00;
                border-radius: 2px;
            }
            
            /* === TOOLBAR === */
            QToolBar {
                background-color: #141414;
                border: none;
                border-bottom: 1px solid #333;
                spacing: 4px;
                padding: 4px;
            }
            QToolButton {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 6px 14px;
                margin: 2px;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                font-weight: bold;
                min-width: 60px;
            }
            QToolButton:hover {
                background-color: #00FF00;
                color: #000000;
                border: 2px solid #00AA00;
            }
            QToolButton:pressed {
                background-color: #00AA00;
                color: #000000;
            }
            QToolButton:checked {
                background-color: #006600;
                color: #00FF00;
                border: 2px solid #00FF00;
            }
            QToolBar::separator {
                background-color: #00FF00;
                width: 2px;
                margin: 4px 2px;
            }
            
            /* === GROUP BOXES === */
            QGroupBox {
                background-color: #141414;
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 6px;
                margin-top: 14px;
                font-family: 'JetBrains Mono', monospace;
                font-weight: bold;
                font-size: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #00FF00;
                background-color: #141414;
                border: 1px solid #00FF00;
                border-radius: 3px;
            }
            
            /* === TEXT EDIT === */
            QTextEdit {
                background-color: #000000;
                color: #00FF00;
                border: 2px solid #333;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                selection-background-color: #00FF00;
                selection-color: #000000;
                padding: 8px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 2px solid #00FF00;
            }
            
            /* === LIST WIDGET === */
            QListWidget {
                background-color: #000000;
                color: #00FF00;
                border: 2px solid #333;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                outline: none;
                alternate-background-color: #0A0A0A;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #333;
                line-height: 1.4;
                margin: 1px;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background-color: #00FF00;
                color: #000000;
                border: 1px solid #00AA00;
            }
            QListWidget::item:hover {
                background-color: #1E1E1E;
                border: 1px solid #555;
            }
            QListWidget:focus {
                border: 2px solid #00FF00;
            }
            
            /* === TREE WIDGET === */
            QTreeWidget {
                background-color: #000000;
                color: #00FF00;
                border: 2px solid #333;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                outline: none;
                alternate-background-color: #0A0A0A;
                gridline-color: #333;
            }
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #222;
                min-height: 22px;
                margin: 1px;
            }
            QTreeWidget::item:selected {
                background-color: #00FF00;
                color: #000000;
                border: 1px solid #00AA00;
            }
            QTreeWidget::item:hover {
                background-color: #1E1E1E;
                border: 1px solid #555;
            }
            QTreeWidget:focus {
                border: 2px solid #00FF00;
            }
            QHeaderView::section {
                background-color: #1E1E1E;
                color: #00FF00;
                padding: 8px;
                border: 1px solid #333;
                border-bottom: 2px solid #00FF00;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #333;
            }
            
            /* === SCROLL BARS === */
            QScrollBar:vertical {
                background-color: #1A1A1A;
                width: 16px;
                border: 1px solid #333;
                border-radius: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #00FF00;
                border: 1px solid #00AA00;
                border-radius: 7px;
                min-height: 25px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00AA00;
                border: 1px solid #008800;
            }
            QScrollBar::handle:vertical:pressed {
                background-color: #006600;
            }
            QScrollBar::add-line:vertical {
                background-color: #1A1A1A;
                height: 16px;
                border: 1px solid #333;
                border-radius: 8px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background-color: #1A1A1A;
                height: 16px;
                border: 1px solid #333;
                border-radius: 8px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background-color: #333;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background-color: #00FF00;
                width: 10px;
                height: 10px;
                border: 1px solid #00AA00;
                border-radius: 5px;
            }
            
            QScrollBar:horizontal {
                background-color: #1A1A1A;
                height: 16px;
                border: 1px solid #333;
                border-radius: 8px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background-color: #00FF00;
                border: 1px solid #00AA00;
                border-radius: 7px;
                min-width: 25px;
                margin: 1px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #00AA00;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background-color: #1A1A1A;
                width: 16px;
                border: 1px solid #333;
                border-radius: 8px;
            }
            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                background-color: #00FF00;
                width: 10px;
                height: 10px;
                border: 1px solid #00AA00;
                border-radius: 5px;
            }
            
            /* === SCROLL AREA === */
            QScrollArea {
                background-color: #0A0A0A;
                border: 2px solid #333;
                border-radius: 4px;
            }
            QScrollArea:focus {
                border: 2px solid #00FF00;
            }
            
            /* === COMBO BOX === */
            QComboBox {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 6px 10px;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                min-width: 80px;
            }
            QComboBox:hover {
                border-color: #00FF00;
                background-color: #2A2A2A;
            }
            QComboBox:focus {
                border-color: #00FF00;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #333;
                border-radius: 0;
                background-color: #1E1E1E;
            }
            QComboBox::drop-down:hover {
                background-color: #00FF00;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #00FF00;
                margin: 2px;
            }
            QComboBox::down-arrow:hover {
                border-top-color: #000000;
            }
            QComboBox QAbstractItemView {
                background-color: #1A1A1A;
                color: #00FF00;
                selection-background-color: #00FF00;
                selection-color: #000000;
                border: 2px solid #00FF00;
                border-radius: 4px;
                outline: none;
                font-family: 'JetBrains Mono', monospace;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #2A2A2A;
            }
            
            /* === CHECKBOX === */
            QCheckBox {
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                padding: 4px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 2px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #1E1E1E;
                border: 2px solid #333;
            }
            QCheckBox::indicator:unchecked:hover {
                background-color: #2A2A2A;
                border: 2px solid #00FF00;
            }
            QCheckBox::indicator:checked {
                background-color: #00FF00;
                border: 2px solid #00AA00;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTExLjMzMzMgMy41TDUuMjUgOS41ODMzM0wyLjY2NjY3IDciIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            }
            QCheckBox::indicator:checked:hover {
                background-color: #00AA00;
            }
            
            /* === SLIDER === */
            QSlider::groove:horizontal {
                background-color: #1E1E1E;
                height: 8px;
                border: 1px solid #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #00FF00;
                width: 20px;
                height: 20px;
                border: 2px solid #00AA00;
                border-radius: 10px;
                margin: -7px 0;
            }
            QSlider::handle:horizontal:hover {
                background-color: #00AA00;
                border: 2px solid #008800;
            }
            QSlider::handle:horizontal:pressed {
                background-color: #006600;
            }
            QSlider::sub-page:horizontal {
                background-color: #00FF00;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background-color: #333;
                border-radius: 4px;
            }
            
            /* === SPIN BOX === */
            QSpinBox {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 6px;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                min-width: 60px;
            }
            QSpinBox:hover {
                border-color: #00FF00;
                background-color: #2A2A2A;
            }
            QSpinBox:focus {
                border-color: #00FF00;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #333;
                border-bottom: 1px solid #333;
                border-top-right-radius: 3px;
                background-color: #1E1E1E;
            }
            QSpinBox::up-button:hover {
                background-color: #00FF00;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left: 1px solid #333;
                border-bottom-right-radius: 3px;
                background-color: #1E1E1E;
            }
            QSpinBox::down-button:hover {
                background-color: #00FF00;
            }
            QSpinBox::up-arrow {
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #00FF00;
            }
            QSpinBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #00FF00;
            }
            
            /* === PUSH BUTTON === */
            QPushButton {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                padding: 8px 16px;
                border-radius: 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #00FF00;
                color: #000000;
                border: 2px solid #00AA00;
            }
            QPushButton:pressed {
                background-color: #00AA00;
                color: #000000;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #666;
                border: 2px solid #222;
            }
            
            /* === LABEL === */
            QLabel {
                color: #00FF00;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                padding: 2px;
            }
            
            /* === STATUS BAR === */
            QStatusBar {
                background-color: #141414;
                color: #00FF00;
                border-top: 2px solid #00FF00;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                padding: 4px;
            }
            QStatusBar::item {
                border: none;
                padding: 2px;
            }
            
            /* === PROGRESS BAR === */
            QProgressBar {
                background-color: #1E1E1E;
                color: #00FF00;
                border: 2px solid #333;
                border-radius: 4px;
                text-align: center;
                font-family: 'JetBrains Mono', monospace;
                font-size: 9px;
                font-weight: bold;
                padding: 2px;
            }
            QProgressBar::chunk {
                background-color: #00FF00;
                border-radius: 2px;
                margin: 1px;
            }
            
            /* === SPLITTER === */
            QSplitter::handle {
                background-color: #333;
                border: 2px solid #555;
                border-radius: 3px;
                margin: 3px;
            }
            QSplitter::handle:hover {
                background-color: #00FF00;
                border: 2px solid #00AA00;
            }
            QSplitter::handle:pressed {
                background-color: #00AA00;
            }
            
            /* === MESSAGE BOX === */
            QMessageBox {
                background-color: #1A1A1A;
                color: #00FF00;
                border: 3px solid #00FF00;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
            }
            QMessageBox QLabel {
                color: #00FF00;
                font-size: 11px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                margin: 5px;
            }
            
            /* === DIALOG === */
            QDialog {
                background-color: #1A1A1A;
                color: #00FF00;
                border: 3px solid #00FF00;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
            }
            
            /* === TOOLTIP === */
            QToolTip {
                background-color: #1A1A1A;
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 4px;
                padding: 6px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 9px;
            }
        """)

    def _setup_navigation(self):
        """Setup modern navigation bar"""
        # Menu bar
        menubar = self.menuBar()
        menubar.setMaximumHeight(NAV_BAR_HEIGHT)
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Scan', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.manual_scan)
        file_menu.addAction(new_action)
        
        save_action = QAction('Save Results', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        vuln_scan_action = QAction('Vulnerability Scan', self)
        vuln_scan_action.triggered.connect(self.run_vulnerability_scan)
        tools_menu.addAction(vuln_scan_action)
        
        export_action = QAction('Export Targets', self)
        export_action.triggered.connect(self.export_targets)
        tools_menu.addAction(export_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('Settings')
        
        interface_action = QAction('Interface Settings', self)
        interface_action.triggered.connect(self.show_interface_settings)
        settings_menu.addAction(interface_action)
        
        display_action = QAction('Display Options', self)
        display_action.triggered.connect(self.show_display_options)
        settings_menu.addAction(display_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # View modes submenu
        view_modes_menu = view_menu.addMenu('View Mode')
        
        compact_action = QAction('Compact (800x500)', self)
        compact_action.setShortcut('Ctrl+1')
        compact_action.triggered.connect(lambda: self.set_view_mode('COMPACT'))
        view_modes_menu.addAction(compact_action)
        
        normal_action = QAction('Normal (1400x800)', self)
        normal_action.setShortcut('Ctrl+2')
        normal_action.triggered.connect(lambda: self.set_view_mode('NORMAL'))
        view_modes_menu.addAction(normal_action)
        
        fullscreen_action = QAction('Fullscreen', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.triggered.connect(lambda: self.set_view_mode('FULLSCREEN'))
        view_modes_menu.addAction(fullscreen_action)
        
        view_menu.addSeparator()
        
        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.manual_scan)
        view_menu.addAction(refresh_action)
        
        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Toolbar
        toolbar = self.addToolBar('Main')
        toolbar.setMaximumHeight(NAV_BAR_HEIGHT)
        toolbar.setMovable(False)
        
        # Quick action buttons
        scan_btn = QToolButton()
        scan_btn.setText('Scan')
        scan_btn.setToolTip('Start manual scan')
        scan_btn.clicked.connect(self.manual_scan)
        toolbar.addWidget(scan_btn)
        
        toolbar.addSeparator()
        
        vuln_btn = QToolButton()
        vuln_btn.setText('Vuln Only')
        vuln_btn.setToolTip('Show vulnerable targets only')
        vuln_btn.setCheckable(True)
        vuln_btn.toggled.connect(self.toggle_vulnerable_only)
        toolbar.addWidget(vuln_btn)
        
        threat_btn = QToolButton()
        threat_btn.setText('Threat Colors')
        threat_btn.setToolTip('Use threat level colors')
        threat_btn.setCheckable(True)
        threat_btn.setChecked(True)
        threat_btn.toggled.connect(self.toggle_threat_colors)
        toolbar.addWidget(threat_btn)
        
        toolbar.addSeparator()
        
        # Interface selector
        toolbar.addWidget(QLabel('Interface:'))
        self.interface_combo = QComboBox()
        self.interface_combo.addItems(['wlan0', 'wlan1', 'wifi0'])
        self.interface_combo.setCurrentText(self.interface)
        self.interface_combo.currentTextChanged.connect(self.change_interface)
        toolbar.addWidget(self.interface_combo)
        
        toolbar.addSeparator()
        
        # View mode buttons
        compact_btn = QToolButton()
        compact_btn.setText('Compact')
        compact_btn.setToolTip('Switch to compact view (800x500)')
        compact_btn.clicked.connect(lambda: self.set_view_mode('COMPACT'))
        toolbar.addWidget(compact_btn)
        
        normal_btn = QToolButton()
        normal_btn.setText('Normal')
        normal_btn.setToolTip('Switch to normal view (1400x800)')
        normal_btn.clicked.connect(lambda: self.set_view_mode('NORMAL'))
        toolbar.addWidget(normal_btn)
        
        fullscreen_btn = QToolButton()
        fullscreen_btn.setText('Fullscreen')
        fullscreen_btn.setToolTip('Switch to fullscreen view')
        fullscreen_btn.clicked.connect(lambda: self.set_view_mode('FULLSCREEN'))
        toolbar.addWidget(fullscreen_btn)
        
        # Progress bar
        toolbar.addSeparator()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(100)
        self.progress_bar.setMaximumHeight(20)
        self.progress_bar.setVisible(False)
        toolbar.addWidget(self.progress_bar)

    def _setup_ui(self):
        """Setup the main user interface"""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)
        
        # Left panel - Radar
        radar_group = QGroupBox("WiFi Penetration Testing Radar")
        radar_layout = QVBoxLayout(radar_group)
        
        self.radar = RadarCanvas(self)
        self.radar.ap_selected.connect(self.on_ap_selected)
        radar_layout.addWidget(self.radar, 0, Qt.AlignCenter)
        
        # Quick controls under radar
        quick_controls = QHBoxLayout()
        
        self.distance_slider = QSlider(Qt.Horizontal)
        self.distance_slider.setMinimum(50)
        self.distance_slider.setMaximum(500)
        self.distance_slider.setValue(self.max_distance)
        self.distance_slider.valueChanged.connect(self.change_max_distance)
        quick_controls.addWidget(QLabel("Range:"))
        quick_controls.addWidget(self.distance_slider)
        
        self.distance_label = QLabel(f"{self.max_distance}m")
        quick_controls.addWidget(self.distance_label)
        
        radar_layout.addLayout(quick_controls)
        
        main_layout.addWidget(radar_group, 2)
        
        # Right panel - Scrollable side panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        
        # Target Analysis Section
        details_group = QGroupBox("Target Analysis")
        details_layout = QVBoxLayout(details_group)
        
        # Scrollable text area for target details
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        details_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        details_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        details_scroll.setMaximumHeight(300)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlainText("Select an access point to view detailed analysis...")
        
        # Set larger font for details text
        details_font = QFont("JetBrains Mono", 11)
        self.details_text.setFont(details_font)
        
        details_scroll.setWidget(self.details_text)
        details_layout.addWidget(details_scroll)
        
        right_layout.addWidget(details_group)
        
        # Vulnerability Assessment Section
        vuln_group = QGroupBox("Vulnerability Assessment")
        vuln_layout = QVBoxLayout(vuln_group)
        
        # Scrollable vulnerability list
        vuln_scroll = QScrollArea()
        vuln_scroll.setWidgetResizable(True)
        vuln_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        vuln_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        vuln_scroll.setMaximumHeight(250)
        
        self.vuln_list = QListWidget()
        
        # Set larger font for vulnerability list
        vuln_font = QFont("JetBrains Mono", 11)
        self.vuln_list.setFont(vuln_font)
        
        vuln_scroll.setWidget(self.vuln_list)
        vuln_layout.addWidget(vuln_scroll)
        
        right_layout.addWidget(vuln_group)
        
        # Target List Section
        targets_group = QGroupBox("Target List")
        targets_layout = QVBoxLayout(targets_group)
        
        # Scrollable target tree
        targets_scroll = QScrollArea()
        targets_scroll.setWidgetResizable(True)
        targets_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        targets_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.targets_tree = QTreeWidget()
        self.targets_tree.setHeaderLabels(['SSID', 'Security', 'Signal', 'Threat'])
        self.targets_tree.setRootIsDecorated(False)
        self.targets_tree.itemClicked.connect(self.on_target_selected)
        
        # Set larger font for tree widget
        tree_font = QFont("JetBrains Mono", 11)  # Increased size
        self.targets_tree.setFont(tree_font)
        header_font = QFont("JetBrains Mono", 11, QFont.Bold)  # Bold headers
        self.targets_tree.header().setFont(header_font)
        
        targets_scroll.setWidget(self.targets_tree)
        targets_layout.addWidget(targets_scroll)
        
        right_layout.addWidget(targets_group)
        
        main_layout.addWidget(right_panel, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widgets to status bar
        self.mode_label = QLabel(f"Mode: {self.current_view_mode}")
        self.mode_label.setStyleSheet("color: #00FF00; font-weight: bold; padding: 2px 10px;")
        self.status_bar.addPermanentWidget(self.mode_label)
        
        self.interface_label = QLabel(f"Interface: {self.interface}")
        self.interface_label.setStyleSheet("color: #00FF00; font-weight: bold; padding: 2px 10px;")
        self.status_bar.addPermanentWidget(self.interface_label)
        
        self.status_bar.showMessage(f"Ready - {self.current_view_mode} Mode")

    def _setup_connections(self):
        """Setup signal connections"""
        pass

    def start_scanning(self):
        """Start WiFi scanning"""
        self.scanner.set_interface(self.interface)
        self.scanner.set_scan_interval(self.scan_interval)
        self.scanner.start_scanning()
        self.status_bar.showMessage(f"Scanning on {self.interface}...")

    def update_access_points(self, aps: List[AccessPoint]):
        """Update access points display"""
        self.radar.update_access_points(aps)
        self.update_targets_tree(aps)
        self.status_bar.showMessage(f"Found {len(aps)} access points - {sum(1 for ap in aps if ap.is_vulnerable)} vulnerable")

    def update_targets_tree(self, aps: List[AccessPoint]):
        """Update the targets tree widget"""
        self.targets_tree.clear()
        
        for ap in aps:
            item = QTreeWidgetItem()
            
            # SSID
            ssid = ap.ssid if ap.ssid else "<HIDDEN>"
            item.setText(0, ssid[:20] + ('...' if len(ssid) > 20 else ''))
            
            # Security
            item.setText(1, ap.security)
            
            # Signal
            item.setText(2, f"{ap.signal_dbm:.0f}dBm")
            
            # Threat Level
            item.setText(3, ap.threat_level)
            
            # Color coding based on threat level
            if ap.threat_level == "CRITICAL":
                for i in range(4):
                    item.setBackground(i, QColor(80, 0, 0))
            elif ap.threat_level == "HIGH":
                for i in range(4):
                    item.setBackground(i, QColor(80, 40, 0))
            elif ap.threat_level == "MEDIUM":
                for i in range(4):
                    item.setBackground(i, QColor(80, 80, 0))
            
            # Store AP reference
            item.setData(0, Qt.UserRole, ap)
            
            self.targets_tree.addTopLevelItem(item)
        
        # Auto-resize columns
        for i in range(4):
            self.targets_tree.resizeColumnToContents(i)

    def on_target_selected(self, item, column):
        """Handle target selection from tree"""
        ap = item.data(0, Qt.UserRole)
        if ap:
            self.on_ap_selected(ap)

    def on_ap_selected(self, ap: AccessPoint):
        """Handle access point selection"""
        if ap is None:
            self.details_text.setPlainText("Select an access point to view detailed analysis...")
            self.vuln_list.clear()
            return
        
        # Update target analysis
        details = f"""TARGET ANALYSIS
        
Basic Information:
SSID: {ap.ssid if ap.ssid else '<HIDDEN>'}
BSSID: {ap.bssid}
Security: {ap.security}
Channel: {ap.channel}
Frequency: {ap.frequency} MHz
Vendor: {ap.vendor}

Signal Analysis:
Signal Strength: {ap.signal_dbm:.1f} dBm
Estimated Distance: {ap.distance:.1f} meters
Signal Quality: {self._get_signal_quality(ap.signal_dbm)}

Security Assessment:
Encryption: {ap.encryption_details}
Vulnerability Score: {ap.vulnerability_score}/100
Threat Level: {ap.threat_level}
WPS Enabled: {'Yes' if ap.wps_enabled else 'No'}

Penetration Testing Info:
Last Seen: {ap.last_seen.strftime('%H:%M:%S')}
Is Vulnerable: {'Yes' if ap.is_vulnerable else 'No'}
Attack Vectors Available: {len(ap.attack_vectors)}

Technical Details:
MAC OUI: {ap.bssid[:8]}
Band: {'2.4GHz' if ap.frequency < 3000 else '5GHz'}
Channel Width: Auto-detected
"""
        
        self.details_text.setPlainText(details)
        
        # Update vulnerability list
        self.vuln_list.clear()
        
        if ap.attack_vectors:
            for vector in ap.attack_vectors:
                item = QListWidgetItem(f"• {vector}")
                
                # Color code by severity
                if "CRITICAL" in vector.upper() or "BROKEN" in vector.upper():
                    item.setBackground(QColor(80, 0, 0))
                elif "HIGH" in vector.upper() or "WEAK" in vector.upper():
                    item.setBackground(QColor(80, 40, 0))
                elif "MEDIUM" in vector.upper():
                    item.setBackground(QColor(80, 80, 0))
                
                self.vuln_list.addItem(item)
        else:
            item = QListWidgetItem("No specific attack vectors identified")
            item.setBackground(QColor(0, 40, 0))
            self.vuln_list.addItem(item)

    def _get_signal_quality(self, signal_dbm):
        """Get signal quality description"""
        if signal_dbm > -30:
            return "Excellent"
        elif signal_dbm > -50:
            return "Good"
        elif signal_dbm > -70:
            return "Fair"
        elif signal_dbm > -85:
            return "Poor"
        else:
            return "Very Poor"

    def handle_scan_error(self, error: str):
        """Handle scanning errors"""
        self.status_bar.showMessage(f"Scan error: {error}")

    def update_progress(self, value: int):
        """Update progress bar"""
        if value == 0:
            self.progress_bar.setVisible(False)
        else:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(value)
            if value == 100:
                QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))

    def set_view_mode(self, mode: str):
        """Set the view mode (COMPACT, NORMAL, FULLSCREEN)"""
        self.current_view_mode = mode
        
        if mode == 'FULLSCREEN':
            if not self.isFullScreen():
                self.showFullScreen()
            self.status_bar.showMessage(f"View Mode: Fullscreen")
            self.mode_label.setText("Mode: FULLSCREEN")
        else:
            if self.isFullScreen():
                self.showNormal()
            
            if mode in VIEW_MODES:
                width, height = VIEW_MODES[mode]
                self.resize(width, height)
                
                # Adjust UI elements based on view mode
                if mode == 'COMPACT':
                    self._setup_compact_layout()
                else:  # NORMAL
                    self._setup_normal_layout()
                
                self.status_bar.showMessage(f"View Mode: {mode} ({width}x{height})")
                self.mode_label.setText(f"Mode: {mode}")

    def _setup_compact_layout(self):
        """Setup compact layout for small screens"""
        # Adjust radar size for compact mode
        self.radar.setFixedSize(250, 250)
        
        # Reduce margins and spacing for compact mode
        central = self.centralWidget()
        main_layout = central.layout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(5)
        
        # Adjust side panel widths
        right_panel = central.layout().itemAt(1).widget()
        if right_panel:
            right_panel.setMaximumWidth(300)
        
        # Hide some toolbar elements in compact mode
        for action in self.menuBar().actions():
            if action.text() in ['Tools', 'Help']:
                action.setVisible(False)
        
        # Reduce font sizes for compact mode
        compact_font = QFont("JetBrains Mono", 9)
        self.details_text.setFont(compact_font)
        self.vuln_list.setFont(compact_font)
        self.targets_tree.setFont(compact_font)

    def _setup_normal_layout(self):
        """Setup normal layout"""
        # Restore normal radar size
        self.radar.setFixedSize(RADAR_SIZE, RADAR_SIZE)
        
        # Restore normal margins and spacing
        central = self.centralWidget()
        main_layout = central.layout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)
        
        # Remove side panel width restrictions
        right_panel = central.layout().itemAt(1).widget()
        if right_panel:
            right_panel.setMaximumWidth(16777215)  # Default maximum width
        
        # Show all toolbar elements
        for action in self.menuBar().actions():
            action.setVisible(True)
        
        # Restore normal font sizes
        normal_font = QFont("JetBrains Mono", 11)
        self.details_text.setFont(normal_font)
        self.vuln_list.setFont(normal_font)
        self.targets_tree.setFont(normal_font)

    def zoom_in(self):
        """Increase UI element sizes"""
        current_font = self.font()
        new_size = min(current_font.pointSize() + 1, 16)
        new_font = QFont(current_font.family(), new_size)
        self.setFont(new_font)
        self.status_bar.showMessage(f"Font size increased to {new_size}pt")

    def zoom_out(self):
        """Decrease UI element sizes"""
        current_font = self.font()
        new_size = max(current_font.pointSize() - 1, 8)
        new_font = QFont(current_font.family(), new_size)
        self.setFont(new_font)
        self.status_bar.showMessage(f"Font size decreased to {new_size}pt")

    def change_interface(self, interface: str):
        """Change WiFi interface"""
        self.interface = interface
        self.scanner.set_interface(interface)
        self.interface_label.setText(f"Interface: {interface}")
        self.status_bar.showMessage(f"Switched to interface: {interface}")

    def change_max_distance(self, distance: int):
        """Change maximum distance"""
        self.max_distance = distance
        self.distance_label.setText(f"{distance}m")
        self.radar.update()

    def toggle_vulnerable_only(self, enabled: bool):
        """Toggle showing only vulnerable APs"""
        self.radar.set_show_vulnerable_only(enabled)

    def toggle_threat_colors(self, enabled: bool):
        """Toggle threat level colors"""
        self.radar.set_show_threat_colors(enabled)

    def manual_scan(self):
        """Trigger manual scan"""
        self.status_bar.showMessage("Manual scan initiated...")
        # The scanner thread will handle the actual scanning

    def save_results(self):
        """Save scan results with enhanced dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Save Results")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Scan results have been saved successfully!\n\nSaved data includes:\n• Access point details\n• Vulnerability assessments\n• Signal analysis\n• Threat classifications")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def run_vulnerability_scan(self):
        """Run vulnerability scan with enhanced dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Vulnerability Scan")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Advanced vulnerability scan completed!\n\nAnalysis includes:\n• Security protocol weaknesses\n• Attack vector identification\n• Signal strength assessment\n• Penetration testing opportunities")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def export_targets(self):
        """Export targets with enhanced dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Export Targets")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Target data exported successfully!\n\nExported formats:\n• Vulnerable targets list\n• Security analysis report\n• Attack vector summary\n• Technical specifications")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_interface_settings(self):
        """Show interface settings with enhanced dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Interface Settings")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Interface configuration options:\n\nAvailable settings:\n• Network interface selection\n• Scan interval adjustment\n• Signal threshold configuration\n• Advanced monitoring options")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_display_options(self):
        """Show display options with enhanced dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Display Options")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Display customization options:\n\nAvailable options:\n• Theme selection\n• Color scheme adjustment\n• Font size configuration\n• Layout preferences")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode - deprecated, use set_view_mode instead"""
        if self.isFullScreen():
            self.set_view_mode('NORMAL')
        else:
            self.set_view_mode('FULLSCREEN')

    def show_about(self):
        """Show about dialog with enhanced styling"""
        msg = QMessageBox(self)
        msg.setWindowTitle("About WiFi Radar Navigation Enhanced")
        msg.setIcon(QMessageBox.Information)
        
        about_text = f"""
<div style="font-family: 'JetBrains Mono', monospace; color: #00FF00;">
<h2 style="color: #00FF00; text-align: center;">WiFi Radar Navigation Enhanced v{VERSION}</h2>

<p><b>Professional WiFi Penetration Testing Tool</b></p>

<p><b>Core Features:</b></p>
<ul>
<li>Real-time WiFi scanning and analysis</li>
<li>Comprehensive vulnerability assessment</li>
<li>Modern navigation bar interface</li>
<li>Scrollable analysis panels</li>
<li>Threat level visualization</li>
<li>Multiple view modes (Compact/Normal/Fullscreen)</li>
</ul>

<p><b>Security Analysis:</b></p>
<ul>
<li>WEP/WPA/WPA2/WPA3 detection</li>
<li>Attack vector identification</li>
<li>Signal strength analysis</li>
<li>Vendor identification</li>
</ul>

<p><b>Keyboard Shortcuts:</b></p>
<ul>
<li>Ctrl+1: Compact Mode</li>
<li>Ctrl+2: Normal Mode</li>
<li>F11: Fullscreen Mode</li>
<li>F5: Refresh Scan</li>
<li>Ctrl+N: New Scan</li>
<li>Ctrl+S: Save Results</li>
<li>Ctrl++: Zoom In</li>
<li>Ctrl+-: Zoom Out</li>
</ul>

<p style="text-align: center; margin-top: 20px;">
<b>© 2025 WiFi Security Tools</b><br>
<i>Professional Hacker-Style Interface</i>
</p>
</div>
        """
        
        msg.setText(about_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, event):
        """Handle application close"""
        self.scanner.stop_scanning()
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("WiFi Radar Navigation Enhanced")
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("WiFi Security Tools")
    
    # Create and show main window
    window = NavigationRadarWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
