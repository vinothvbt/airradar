#!/usr/bin/env python3
"""
Enhanced GUI Integration Module for WiFi Security Radar Suite
Integrates new features (real-time graphs, export, accessibility, i18n) into existing interfaces
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QAction,
    QSplitter, QTabWidget, QMainWindow, QDockWidget, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence

# Import new modules
try:
    from realtime_graphs import RealtimeGraphsPanel
    from export_module import ExportDialog
    from accessibility import accessibility_manager, apply_accessibility_to_widget, AccessibilityDialog
    from internationalization import translation_manager, LanguageDialog, TranslatedWidget
    from enhanced_themes import theme_manager, ThemeCustomizerDialog
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Enhanced features not available: {e}")
    ENHANCED_FEATURES_AVAILABLE = False
    
    # Fallback classes
    class RealtimeGraphsPanel(QWidget):
        def __init__(self): 
            super().__init__()
            self.update_with_real_data = lambda x: None
    class ExportDialog(QWidget): 
        def __init__(self, *args): super().__init__()
    class AccessibilityDialog(QWidget): 
        def __init__(self, *args): super().__init__()
    class LanguageDialog(QWidget): 
        def __init__(self, *args): super().__init__()
    class ThemeCustomizerDialog(QWidget): 
        def __init__(self, *args): super().__init__()
    class TranslatedWidget:
        def __init__(self, *args): pass
        def tr(self, section, key, fallback=None): return fallback or key


class EnhancedFeatureIntegrator:
    """Integrates enhanced features into existing radar interfaces"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.graphs_panel = None
        self.accessibility_enabled = False
        self.graphs_dock = None
        
    def integrate_enhanced_features(self):
        """Integrate all enhanced features into the main window"""
        if not ENHANCED_FEATURES_AVAILABLE:
            print("Enhanced features not available, skipping integration")
            return
            
        try:
            # Add enhanced menu items
            self._add_enhanced_menus()
            
            # Setup real-time graphs
            self._setup_realtime_graphs()
            
            # Apply accessibility features
            self._apply_accessibility()
            
            # Apply current theme
            self._apply_theme()
            
            # Setup translation
            self._setup_translation()
            
            print("✅ Enhanced features integrated successfully")
            
        except Exception as e:
            print(f"⚠️ Error integrating enhanced features: {e}")
            
    def _add_enhanced_menus(self):
        """Add enhanced menu items to existing menu bar"""
        if not hasattr(self.main_window, 'menubar'):
            return
            
        menubar = self.main_window.menubar
        
        # Add View menu if it doesn't exist
        view_menu = None
        for action in menubar.actions():
            if action.text() == "View":
                view_menu = action.menu()
                break
                
        if not view_menu:
            view_menu = menubar.addMenu("View")
            
        # Add graphs action
        graphs_action = QAction("Real-time Graphs", self.main_window)
        graphs_action.setShortcut(QKeySequence("Ctrl+G"))
        graphs_action.triggered.connect(self._toggle_graphs_panel)
        view_menu.addAction(graphs_action)
        
        # Add Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        # Export action
        export_action = QAction("Export Data...", self.main_window)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._show_export_dialog)
        tools_menu.addAction(export_action)
        
        # Accessibility action
        accessibility_action = QAction("Accessibility...", self.main_window)
        accessibility_action.setShortcut(QKeySequence("Ctrl+Alt+A"))
        accessibility_action.triggered.connect(self._show_accessibility_dialog)
        tools_menu.addAction(accessibility_action)
        
        # Language action
        language_action = QAction("Language...", self.main_window)
        language_action.triggered.connect(self._show_language_dialog)
        tools_menu.addAction(language_action)
        
        # Theme customizer action
        theme_action = QAction("Customize Theme...", self.main_window)
        theme_action.triggered.connect(self._show_theme_dialog)
        tools_menu.addAction(theme_action)
        
    def _setup_realtime_graphs(self):
        """Setup real-time graphs panel"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return
            
        try:
            # Create graphs panel
            self.graphs_panel = RealtimeGraphsPanel()
            
            # Create dock widget for graphs
            self.graphs_dock = QDockWidget("Real-time Monitoring", self.main_window)
            self.graphs_dock.setWidget(self.graphs_panel)
            self.graphs_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
            
            # Add to main window
            self.main_window.addDockWidget(Qt.RightDockWidgetArea, self.graphs_dock)
            
            # Initially hide
            self.graphs_dock.hide()
            
            # Connect to data updates if scanner exists
            if hasattr(self.main_window, 'scanner'):
                if hasattr(self.main_window.scanner, 'scan_completed'):
                    self.main_window.scanner.scan_completed.connect(self._update_graphs_data)
                    
        except Exception as e:
            print(f"Error setting up graphs: {e}")
            
    def _apply_accessibility(self):
        """Apply accessibility features to the main window"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return
            
        try:
            # Apply accessibility to main window
            nav_handler = apply_accessibility_to_widget(self.main_window)
            self.accessibility_enabled = True
            
            # Store reference for later use
            self.main_window._nav_handler = nav_handler
            
        except Exception as e:
            print(f"Error applying accessibility: {e}")
            
    def _apply_theme(self):
        """Apply current theme to the main window"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return
            
        try:
            # Get current theme stylesheet
            stylesheet = theme_manager.create_stylesheet()
            
            # Apply to main window
            self.main_window.setStyleSheet(stylesheet)
            
            # Connect to theme changes
            theme_manager.theme_changed.connect(self._on_theme_changed)
            
        except Exception as e:
            print(f"Error applying theme: {e}")
            
    def _setup_translation(self):
        """Setup translation for the main window"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return
            
        try:
            # Connect to language changes
            translation_manager.language_changed.connect(self._on_language_changed)
            
        except Exception as e:
            print(f"Error setting up translation: {e}")
            
    def _toggle_graphs_panel(self):
        """Toggle visibility of graphs panel"""
        if self.graphs_dock:
            if self.graphs_dock.isVisible():
                self.graphs_dock.hide()
            else:
                self.graphs_dock.show()
                
    def _show_export_dialog(self):
        """Show export dialog"""
        if not ENHANCED_FEATURES_AVAILABLE:
            QMessageBox.information(self.main_window, "Feature Unavailable", 
                                   "Export feature is not available.")
            return
            
        try:
            # Get networks data from main window
            networks_data = []
            if hasattr(self.main_window, 'access_points'):
                networks_data = [
                    {
                        'ssid': ap.ssid,
                        'bssid': ap.bssid,
                        'security': ap.security,
                        'signal': ap.signal,
                        'channel': ap.channel,
                        'frequency': f"{ap.frequency} MHz" if ap.frequency else "Unknown",
                        'vendor': getattr(ap, 'vendor', 'Unknown'),
                        'last_seen': ap.timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(ap, 'timestamp') else "Unknown"
                    }
                    for ap in self.main_window.access_points
                ]
                
            dialog = ExportDialog(networks_data, self.main_window)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Export Error", f"Failed to open export dialog: {e}")
            
    def _show_accessibility_dialog(self):
        """Show accessibility settings dialog"""
        if not ENHANCED_FEATURES_AVAILABLE:
            QMessageBox.information(self.main_window, "Feature Unavailable", 
                                   "Accessibility settings are not available.")
            return
            
        try:
            dialog = AccessibilityDialog(accessibility_manager, self.main_window)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Accessibility Error", 
                               f"Failed to open accessibility dialog: {e}")
            
    def _show_language_dialog(self):
        """Show language selection dialog"""
        if not ENHANCED_FEATURES_AVAILABLE:
            QMessageBox.information(self.main_window, "Feature Unavailable", 
                                   "Language settings are not available.")
            return
            
        try:
            dialog = LanguageDialog(translation_manager, self.main_window)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Language Error", 
                               f"Failed to open language dialog: {e}")
            
    def _show_theme_dialog(self):
        """Show theme customizer dialog"""
        if not ENHANCED_FEATURES_AVAILABLE:
            QMessageBox.information(self.main_window, "Feature Unavailable", 
                                   "Theme customizer is not available.")
            return
            
        try:
            dialog = ThemeCustomizerDialog(theme_manager, self.main_window)
            dialog.theme_applied.connect(self._on_theme_changed)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Theme Error", 
                               f"Failed to open theme dialog: {e}")
            
    def _update_graphs_data(self, networks_data):
        """Update graphs with new network data"""
        if self.graphs_panel and ENHANCED_FEATURES_AVAILABLE:
            try:
                # Convert access points to format expected by graphs
                formatted_data = []
                if hasattr(networks_data, '__iter__'):
                    for ap in networks_data:
                        if hasattr(ap, 'bssid'):  # It's an AccessPoint object
                            formatted_data.append({
                                'ssid': ap.ssid,
                                'bssid': ap.bssid,
                                'security': ap.security,
                                'signal': ap.signal,
                                'channel': ap.channel,
                                'frequency': ap.frequency
                            })
                        elif isinstance(ap, dict):  # It's already a dict
                            formatted_data.append(ap)
                            
                self.graphs_panel.update_with_real_data(formatted_data)
                
            except Exception as e:
                print(f"Error updating graphs data: {e}")
                
    def _on_theme_changed(self, theme_name):
        """Handle theme change"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return
            
        try:
            # Apply new theme
            stylesheet = theme_manager.create_stylesheet(theme_name)
            self.main_window.setStyleSheet(stylesheet)
            
        except Exception as e:
            print(f"Error applying new theme: {e}")
            
    def _on_language_changed(self, language_code):
        """Handle language change"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return
            
        try:
            # Update window title and other translatable text
            # This would need to be implemented for each specific interface
            print(f"Language changed to: {language_code}")
            
        except Exception as e:
            print(f"Error handling language change: {e}")


class EnhancedMainWindow(QMainWindow):
    """Enhanced main window base class with integrated features"""
    
    def __init__(self):
        super().__init__()
        self.feature_integrator = EnhancedFeatureIntegrator(self)
        self.access_points = []  # Will be populated by scanner
        self._setup_enhanced_features()
        
    def _setup_enhanced_features(self):
        """Setup enhanced features"""
        # Wait for main window to be fully initialized
        QTimer.singleShot(100, self.feature_integrator.integrate_enhanced_features)
        
    def update_networks_data(self, access_points):
        """Update networks data and notify graphs"""
        self.access_points = access_points
        if hasattr(self.feature_integrator, '_update_graphs_data'):
            self.feature_integrator._update_graphs_data(access_points)


def enhance_existing_window(window):
    """Enhance an existing window with new features"""
    if not hasattr(window, 'feature_integrator'):
        integrator = EnhancedFeatureIntegrator(window)
        window.feature_integrator = integrator
        
        # Add method to update networks data
        def update_networks_data(access_points):
            window.access_points = access_points
            integrator._update_graphs_data(access_points)
        window.update_networks_data = update_networks_data
        
        # Integrate features
        integrator.integrate_enhanced_features()
        
    return window


# Export functionality
__all__ = [
    'EnhancedFeatureIntegrator',
    'EnhancedMainWindow', 
    'enhance_existing_window'
]


if __name__ == "__main__":
    # Test enhanced integration
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create a simple test window
    window = EnhancedMainWindow()
    window.setWindowTitle("Enhanced Features Test")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    
    sys.exit(app.exec_())