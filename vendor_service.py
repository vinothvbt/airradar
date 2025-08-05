#!/usr/bin/env python3
"""
Vendor Detection Service for WiFi Security Radar Suite
Handles MAC OUI to vendor mapping with dynamic updates
"""

import json
import requests
import logging
import re
from typing import Dict
from pathlib import Path
from datetime import datetime, timedelta
from config_manager import config_manager

logger = logging.getLogger(__name__)


class VendorDetectionService:
    """Service for detecting device vendors from MAC addresses"""

    def __init__(self):
        self.oui_database = {}
        self.config = config_manager.get_vendor_config()
        self.local_db_path = Path(
            self.config.get(
                "local_database",
                "oui_database.json"))
        self.update_interval = self.config.get("update_interval_days", 30)

        self._load_vendor_database()

    def _load_vendor_database(self):
        """Load vendor database from local file or download if needed"""
        try:
            # Check if local database exists and is recent
            if self._should_update_database():
                logger.info("Updating vendor database...")
                self._download_oui_database()

            # Load local database
            if self.local_db_path.exists():
                with open(self.local_db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.oui_database = data.get("oui_mappings", {})
                    logger.info(
                        f"Loaded {len(self.oui_database)} vendor mappings")
            else:
                # Use fallback database
                self._load_fallback_database()

        except Exception as e:
            logger.error(f"Error loading vendor database: {e}")
            self._load_fallback_database()

    def _should_update_database(self) -> bool:
        """Check if database should be updated"""
        if not self.local_db_path.exists():
            return True

        try:
            stat = self.local_db_path.stat()
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            return datetime.now() - last_modified > timedelta(days=self.update_interval)
        except Exception:
            return True

    def _download_oui_database(self):
        """Download OUI database from IEEE website"""
        try:
            url = self.config.get(
                "oui_database_source",
                "https://standards-oui.ieee.org/oui/oui.txt")
            logger.info(f"Downloading OUI database from {url}")

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Parse the OUI database
            oui_mappings = self._parse_oui_text(response.text)

            # Save to local file
            database_data = {
                "last_updated": datetime.now().isoformat(),
                "source": url,
                "oui_mappings": oui_mappings
            }

            with open(self.local_db_path, 'w', encoding='utf-8') as f:
                json.dump(database_data, f, indent=2)

            self.oui_database = oui_mappings
            logger.info(
                f"Downloaded and saved {
                    len(oui_mappings)} vendor mappings")

        except requests.RequestException as e:
            if "name resolution" in str(e).lower() or "network" in str(e).lower():
                logger.warning("Network unavailable for OUI database update - using fallback")
            else:
                logger.error(f"Error downloading OUI database: {e}")
            self._load_fallback_database()
        except Exception as e:
            logger.error(f"Error processing OUI database: {e}")
            self._load_fallback_database()

    def _parse_oui_text(self, oui_text: str) -> Dict[str, str]:
        """Parse IEEE OUI text format"""
        oui_mappings = {}
        current_oui = None

        for line in oui_text.split('\n'):
            line = line.strip()

            # Look for OUI assignment lines
            if '(hex)' in line:
                parts = line.split('(hex)')
                if len(parts) >= 2:
                    oui = parts[0].strip().replace('-', ':')
                    vendor = parts[1].strip()
                    if oui and vendor:
                        oui_mappings[oui] = vendor

            # Also look for company names on following lines
            elif current_oui and line and not line.startswith('\t'):
                # This might be a continuation of vendor name
                if current_oui in oui_mappings and len(line) < 100:
                    existing_vendor = oui_mappings[current_oui]
                    if len(
                            existing_vendor) < 20:  # Only append if current name is short
                        oui_mappings[current_oui] = f"{existing_vendor} {line}"

        return oui_mappings

    def _load_fallback_database(self):
        """Load fallback vendor database from configuration"""
        try:
            # Load from config.json fallback vendors
            fallback_vendors = self.config.get("fallback_vendors", {})
            
            # If no fallback in config, use the common OUIDs from old format
            if not fallback_vendors:
                fallback_vendors = self.config.get("fallback_vendors", {}).get("common_ouis", {})
            
            self.oui_database = fallback_vendors.copy()
            logger.info(f"Loaded {len(self.oui_database)} fallback vendor mappings")
            
            # If still empty, add some common ones manually
            if not self.oui_database:
                self.oui_database = {
                    "00:1B:63": "Apple Inc.",
                    "00:50:56": "VMware Inc.", 
                    "08:00:27": "Oracle VirtualBox",
                    "00:0C:29": "VMware Inc.",
                    "00:25:90": "Samsung Electronics",
                    "00:26:BB": "Apple Inc.",
                    "AC:DE:48": "Intel Corporation",
                    "00:1A:92": "ARRIS Group, Inc."
                }
                logger.info(f"Using built-in fallback database with {len(self.oui_database)} entries")
                
        except Exception as e:
            logger.error(f"Error loading fallback database: {e}")
            self.oui_database = {}

    def get_vendor(self, mac_address: str) -> str:
        """Get vendor name for MAC address"""
        try:
            if not mac_address or len(mac_address) < 8:
                return "Unknown"

            # Extract OUI (first 3 octets)
            oui = self._normalize_oui(mac_address[:8])

            # Look up in database
            vendor = self.oui_database.get(oui)
            if vendor:
                return self._clean_vendor_name(vendor)

            # Try with different separators
            for separator in ['-', '']:
                alt_oui = oui.replace(':', separator)
                vendor = self.oui_database.get(alt_oui)
                if vendor:
                    return self._clean_vendor_name(vendor)

            return "Unknown"

        except Exception as e:
            logger.error(f"Error getting vendor for {mac_address}: {e}")
            return "Unknown"

    def _normalize_oui(self, oui: str) -> str:
        """Normalize OUI format"""
        # Remove any non-hex characters except colons and hyphens
        cleaned = re.sub(r'[^0-9a-fA-F:\-]', '', oui)

        # Convert to uppercase and ensure colon separation
        if ':' not in cleaned and '-' not in cleaned:
            # Add colons if missing
            if len(cleaned) >= 6:
                cleaned = f"{cleaned[0:2]}:{cleaned[2:4]}:{cleaned[4:6]}"
        elif '-' in cleaned:
            cleaned = cleaned.replace('-', ':')

        return cleaned.upper()

    def _clean_vendor_name(self, vendor: str) -> str:
        """Clean and format vendor name"""
        if not vendor:
            return "Unknown"

        # Remove common suffixes and clean up
        vendor = vendor.strip()

        # Remove common corporate suffixes
        suffixes_to_remove = [
            ', INC.', ', INC', ', LLC', ', LTD.', ', LTD',
            ', CORP.', ', CORP', ', CO.', ', CO',
            'CORPORATION', 'INCORPORATED', 'LIMITED'
        ]

        vendor_upper = vendor.upper()
        for suffix in suffixes_to_remove:
            if vendor_upper.endswith(suffix):
                vendor = vendor[:-len(suffix)].strip()
                break

        # Capitalize properly
        vendor = vendor.title()

        # Handle special cases
        if vendor.lower().startswith('apple'):
            return "Apple Inc."
        elif vendor.lower().startswith('cisco'):
            return "Cisco Systems"
        elif vendor.lower().startswith('microsoft'):
            return "Microsoft Corporation"

        return vendor[:50]  # Limit length

    def get_vendor_info(self, mac_address: str) -> Dict[str, str]:
        """Get detailed vendor information"""
        vendor = self.get_vendor(mac_address)
        oui = self._normalize_oui(mac_address[:8])

        return {
            "vendor": vendor,
            "oui": oui,
            "mac_address": mac_address,
            "is_known": vendor != "Unknown"
        }

    def search_vendors(self, search_term: str) -> Dict[str, str]:
        """Search for vendors by name"""
        results = {}
        search_lower = search_term.lower()

        for oui, vendor in self.oui_database.items():
            if search_lower in vendor.lower():
                results[oui] = vendor

        return results

    def update_database(self):
        """Force update of vendor database"""
        self._download_oui_database()

    def get_database_info(self) -> Dict[str, str]:
        """Get information about the vendor database"""
        info = {
            "total_vendors": str(len(self.oui_database)),
            "database_file": str(self.local_db_path),
            "exists": str(self.local_db_path.exists())
        }

        if self.local_db_path.exists():
            try:
                stat = self.local_db_path.stat()
                info["last_modified"] = datetime.fromtimestamp(
                    stat.st_mtime).isoformat()
                info["file_size"] = f"{stat.st_size / 1024:.1f} KB"
            except Exception:
                pass

        return info


# Global vendor detection service instance
vendor_service = VendorDetectionService()

# Alias for backward compatibility
VendorService = VendorDetectionService
