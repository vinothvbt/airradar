#!/usr/bin/env python3
"""
Distance Calculation Engine for WiFi Security Radar Suite
Advanced algorithms for calculating distance from WiFi signal parameters
"""

import math
import logging
from typing import Dict, Optional, Tuple
from config_manager import config_manager

logger = logging.getLogger(__name__)

class DistanceCalculationEngine:
    """Engine for calculating distances from WiFi signal parameters"""
    
    def __init__(self):
        self.config = config_manager
        self.params = config_manager.get_distance_formula_params()
        self.freq_corrections = config_manager.get_frequency_corrections()
        
        # Physical constants
        self.LIGHT_SPEED = 299792458  # m/s
        self.DEFAULT_TX_POWER = 20    # dBm (typical router)
        
    def calculate_distance(self, signal_dbm: float, frequency_mhz: int, 
                          tx_power_dbm: Optional[float] = None) -> float:
        """
        Calculate distance using multiple methods and return best estimate
        
        Args:
            signal_dbm: Received signal strength in dBm
            frequency_mhz: WiFi frequency in MHz
            tx_power_dbm: Transmit power in dBm (optional)
            
        Returns:
            Estimated distance in meters
        """
        try:
            # Use provided tx_power or estimate based on frequency
            if tx_power_dbm is None:
                tx_power_dbm = self._estimate_tx_power(frequency_mhz)
            
            # Calculate using Free Space Path Loss
            fspl_distance = self._calculate_fspl_distance(
                signal_dbm, frequency_mhz, tx_power_dbm
            )
            
            # Calculate using Log-Normal Path Loss Model
            log_normal_distance = self._calculate_log_normal_distance(
                signal_dbm, frequency_mhz, tx_power_dbm
            )
            
            # Calculate using ITU Indoor Model (for indoor environments)
            itu_distance = self._calculate_itu_indoor_distance(
                signal_dbm, frequency_mhz, tx_power_dbm
            )
            
            # Combine estimates using weighted average
            weights = {"fspl": 0.3, "log_normal": 0.5, "itu": 0.2}
            
            combined_distance = (
                weights["fspl"] * fspl_distance +
                weights["log_normal"] * log_normal_distance +
                weights["itu"] * itu_distance
            )
            
            # Apply environmental and signal quality corrections
            corrected_distance = self._apply_corrections(
                combined_distance, signal_dbm, frequency_mhz
            )
            
            # Ensure reasonable bounds
            final_distance = max(0.5, min(2000.0, corrected_distance))
            
            logger.debug(f"Distance calculation: FSPL={fspl_distance:.1f}m, "
                        f"LogNormal={log_normal_distance:.1f}m, ITU={itu_distance:.1f}m, "
                        f"Final={final_distance:.1f}m")
            
            return round(final_distance, 1)
            
        except Exception as e:
            logger.error(f"Distance calculation failed: {e}")
            return self._fallback_distance_estimate(signal_dbm)
    
    def _calculate_fspl_distance(self, signal_dbm: float, frequency_mhz: int, 
                                tx_power_dbm: float) -> float:
        """Calculate distance using Free Space Path Loss formula"""
        try:
            # Path Loss = Tx Power - Rx Power
            path_loss_db = tx_power_dbm - signal_dbm
            
            # FSPL formula: PL(dB) = 20*log10(d) + 20*log10(f) + 20*log10(4π/c)
            # Rearranged: d = 10^((PL - 20*log10(f) - 20*log10(4π/c)) / 20)
            
            frequency_hz = frequency_mhz * 1e6
            constant = 20 * math.log10(4 * math.pi / self.LIGHT_SPEED)
            frequency_loss = 20 * math.log10(frequency_hz)
            
            distance_log = (path_loss_db - frequency_loss - constant) / 20
            distance = 10 ** distance_log
            
            return max(0.1, distance)
            
        except (ValueError, ZeroDivisionError) as e:
            logger.error(f"FSPL calculation error: {e}")
            return 50.0
    
    def _calculate_log_normal_distance(self, signal_dbm: float, frequency_mhz: int, 
                                     tx_power_dbm: float) -> float:
        """Calculate distance using Log-Normal Path Loss Model"""
        try:
            # Log-Normal Model: PL(d) = PL(d0) + 10*n*log10(d/d0) + X_σ
            # Where n is path loss exponent, d0 is reference distance
            
            path_loss_db = tx_power_dbm - signal_dbm
            
            # Get environment parameters
            env_params = self.params.get("environmental_factors", {}).get("indoor", {})
            n = env_params.get("path_loss_exponent", 2.0)  # Path loss exponent
            d0 = env_params.get("reference_distance", 1.0)   # Reference distance (m)
            pl_d0 = env_params.get("reference_loss", 40.0)   # Path loss at d0 (dB)
            
            # Adjust reference loss for frequency
            frequency_ghz = frequency_mhz / 1000.0
            if frequency_ghz > 5.0:
                pl_d0 += 5  # Higher loss at 5GHz
            
            # Solve for distance: d = d0 * 10^((PL - PL(d0)) / (10*n))
            distance_log = (path_loss_db - pl_d0) / (10 * n)
            distance = d0 * (10 ** distance_log)
            
            return max(0.1, distance)
            
        except (ValueError, ZeroDivisionError) as e:
            logger.error(f"Log-Normal calculation error: {e}")
            return 50.0
    
    def _calculate_itu_indoor_distance(self, signal_dbm: float, frequency_mhz: int, 
                                     tx_power_dbm: float) -> float:
        """Calculate distance using ITU Indoor Propagation Model"""
        try:
            # ITU-R P.1238 Indoor propagation model
            # L = 20*log10(f) + N*log10(d) + Lf(n) - 28
            # Where N depends on frequency, Lf(n) is floor penetration loss
            
            path_loss_db = tx_power_dbm - signal_dbm
            frequency_ghz = frequency_mhz / 1000.0
            
            # Frequency-dependent coefficients
            if frequency_ghz < 5.0:
                N = 28  # 2.4 GHz coefficient
            else:
                N = 30  # 5 GHz coefficient
            
            # Floor penetration loss (assume single floor)
            Lf = 15  # dB for one floor
            
            # Solve for distance
            # d = 10^((L - 20*log10(f) - Lf + 28) / N)
            frequency_term = 20 * math.log10(frequency_ghz * 1000)
            distance_log = (path_loss_db - frequency_term - Lf + 28) / N
            distance = 10 ** distance_log
            
            return max(0.1, distance)
            
        except (ValueError, ZeroDivisionError) as e:
            logger.error(f"ITU Indoor calculation error: {e}")
            return 50.0
    
    def _estimate_tx_power(self, frequency_mhz: int) -> float:
        """Estimate transmit power based on frequency and regulations"""
        frequency_ghz = frequency_mhz / 1000.0
        
        if 2400 <= frequency_mhz <= 2500:
            # 2.4 GHz band - typical home router
            return 20.0  # dBm (100 mW)
        elif 5000 <= frequency_mhz <= 6000:
            # 5 GHz band - can be higher power
            return 23.0  # dBm (200 mW)
        else:
            # Default assumption
            return 20.0  # dBm
    
    def _apply_corrections(self, base_distance: float, signal_dbm: float, 
                          frequency_mhz: int) -> float:
        """Apply environmental and signal quality corrections"""
        corrected_distance = base_distance
        
        # Signal quality corrections (worse signal = likely more obstacles)
        signal_range = self.config.get_signal_range_info(signal_dbm)
        if signal_range:
            corrected_distance *= signal_range.multiplier
        
        # Frequency-specific corrections
        frequency_corrections = self.freq_corrections
        for band_name, band_config in frequency_corrections.items():
            freq_min = band_config.get("min", 0)
            freq_max = band_config.get("max", 999999)
            multiplier = band_config.get("multiplier", 1.0)
            
            if freq_min <= frequency_mhz <= freq_max:
                corrected_distance *= multiplier
                break
        
        # Environmental factor corrections based on signal characteristics
        if signal_dbm < -80:
            # Very weak signal suggests multiple obstacles or long distance
            corrected_distance *= 1.5
        elif signal_dbm > -40:
            # Very strong signal suggests close proximity or direct line of sight
            corrected_distance *= 0.8
        
        return corrected_distance
    
    def _fallback_distance_estimate(self, signal_dbm: float) -> float:
        """Simple fallback distance estimation when advanced methods fail"""
        # Simple rule-of-thumb: every 6dB of path loss doubles distance
        # Assuming -30dBm at 1m as reference
        reference_signal = -30  # dBm
        reference_distance = 1.0  # meters
        
        if signal_dbm >= reference_signal:
            return reference_distance
        
        path_loss = reference_signal - signal_dbm
        # Each 6dB represents doubling of distance
        distance_multiplier = 2 ** (path_loss / 6.0)
        
        return reference_distance * distance_multiplier
    
    def calculate_angle_from_mac(self, mac_address: str) -> float:
        """Calculate consistent angle from MAC address for radar positioning"""
        try:
            if not mac_address:
                return 0.0
            
            # Use hash of MAC for consistent but pseudo-random positioning
            mac_hash = hash(mac_address)
            angle = (mac_hash % 360)
            
            # Ensure angle is positive
            return float(abs(angle))
            
        except Exception as e:
            logger.error(f"Angle calculation error: {e}")
            return 0.0
    
    def get_signal_quality_description(self, signal_dbm: float) -> str:
        """Get human-readable signal quality description"""
        if signal_dbm >= -30:
            return "Excellent"
        elif signal_dbm >= -50:
            return "Very Good"
        elif signal_dbm >= -60:
            return "Good"
        elif signal_dbm >= -70:
            return "Fair"
        elif signal_dbm >= -80:
            return "Poor"
        else:
            return "Very Poor"
    
    def estimate_max_range(self, frequency_mhz: int, tx_power_dbm: float = None) -> float:
        """Estimate maximum theoretical range for given parameters"""
        if tx_power_dbm is None:
            tx_power_dbm = self._estimate_tx_power(frequency_mhz)
        
        # Assume minimum receivable signal of -100 dBm
        min_signal = -100
        max_distance = self.calculate_distance(min_signal, frequency_mhz, tx_power_dbm)
        
        return max_distance
    
    def get_calculation_info(self, signal_dbm: float, frequency_mhz: int) -> Dict[str, str]:
        """Get detailed information about distance calculation"""
        tx_power = self._estimate_tx_power(frequency_mhz)
        path_loss = tx_power - signal_dbm
        
        return {
            "signal_strength": f"{signal_dbm} dBm",
            "frequency": f"{frequency_mhz} MHz",
            "estimated_tx_power": f"{tx_power} dBm",
            "path_loss": f"{path_loss} dB",
            "signal_quality": self.get_signal_quality_description(signal_dbm),
            "frequency_band": "2.4 GHz" if 2400 <= frequency_mhz <= 2500 else "5 GHz" if 5000 <= frequency_mhz <= 6000 else "Other"
        }


# Global distance calculation engine instance
distance_engine = DistanceCalculationEngine()
