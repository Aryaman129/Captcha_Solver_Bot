"""
CAPTCHA Solver with Virtual Display (scrcpy)
Uses scrcpy to create a virtual display, keeping your phone screen off while solving CAPTCHAs
"""

import subprocess
import time
import os
import logging
import json
import sys
from pathlib import Path
from datetime import datetime
import threading

# Import the main solver components
try:
    from captcha_solver_adb import ADBController, CaptchaOCR, CONFIG, LOG_DIR, SCREENSHOT_DIR
except ImportError:
    print("Error: Could not import captcha_solver_adb.py")
    print("Make sure captcha_solver_adb.py is in the same directory")
    sys.exit(1)

# Set up logging
LOG_FILE = LOG_DIR / f"captcha_solver_virtual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class ScrcpyController:
    """Manages scrcpy virtual display"""
    
    def __init__(self):
        self.scrcpy_process = None
        self.scrcpy_command = "scrcpy"
        
    def check_scrcpy_installed(self):
        """Check if scrcpy is installed"""
        try:
            result = subprocess.run(
                [self.scrcpy_command, "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            logging.info(f"scrcpy found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.error("scrcpy is not installed or not in PATH")
            logging.error("Download from: https://github.com/Genymobile/scrcpy/releases")
            logging.error("Or install via: choco install scrcpy")
            return False
    
    def start_virtual_display(self, hidden=True):
        """Start scrcpy virtual display"""
        try:
            logging.info("Starting scrcpy virtual display...")
            
            scrcpy_args = [
                self.scrcpy_command,
                "--stay-awake",  # Keep device awake
                "--turn-screen-off",  # Turn off phone screen
                "--power-off-on-close",  # Turn screen back on when closing
            ]
            
            if hidden:
                scrcpy_args.extend([
                    "--no-window",  # No display window
                ])
            else:
                scrcpy_args.extend([
                    "--window-title", "CAPTCHA Solver Virtual Display",
                    "--window-borderless",
                    "--always-on-top",
                    "--window-x", "0",
                    "--window-y", "0",
                    "--window-width", "360",
                    "--window-height", "640",
                ])
            
            # Start scrcpy in background
            self.scrcpy_process = subprocess.Popen(
                scrcpy_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for scrcpy to initialize
            time.sleep(3)
            
            if self.scrcpy_process.poll() is None:
                logging.info("✓ Virtual display started successfully")
                logging.info("  Phone screen is now OFF")
                return True
            else:
                logging.error("Failed to start scrcpy")
                return False
                
        except Exception as e:
            logging.error(f"Error starting scrcpy: {e}")
            return False
    
    def stop_virtual_display(self):
        """Stop scrcpy virtual display"""
        if self.scrcpy_process:
            try:
                logging.info("Stopping virtual display...")
                self.scrcpy_process.terminate()
                self.scrcpy_process.wait(timeout=5)
                logging.info("✓ Virtual display stopped")
            except Exception as e:
                logging.error(f"Error stopping scrcpy: {e}")
                try:
                    self.scrcpy_process.kill()
                except:
                    pass

class VirtualCaptchaSolver:
    """CAPTCHA solver with virtual display"""
    
    def __init__(self, show_window=False):
        self.adb = ADBController()
        self.ocr = CaptchaOCR()
        self.scrcpy = ScrcpyController()
        self.show_window = show_window
        self.stats = {
            'solved': 0,
            'failed': 0,
            'start_time': datetime.now()
        }
    
    def solve_one_captcha(self):
        """Solve one CAPTCHA (same logic as ADB version)"""
        try:
            # Open the app
            package = CONFIG['captcha_work']['package']
            activity = package + CONFIG['captcha_work']['activity']
            
            if not self.adb.open_app(package, activity):
                return False
            
            # Capture screenshot
            screenshot_path = SCREENSHOT_DIR / f"screen_{datetime.now().strftime('%H%M%S')}.png"
            if not self.adb.capture_screenshot(screenshot_path):
                self.adb.close_app(package)
                return False
            
            # Extract CAPTCHA text
            captcha_text = self.ocr.extract_captcha(screenshot_path)
            if not captcha_text:
                logging.error("Failed to extract CAPTCHA text")
                self.adb.close_app(package)
                return False
            
            # Tap input field
            coords = CONFIG['coordinates']
            if not self.adb.tap(coords['input_field_x'], coords['input_field_y']):
                self.adb.close_app(package)
                return False
            
            # Input text
            if not self.adb.input_text(captcha_text):
                self.adb.close_app(package)
                return False
            
            # Tap submit button
            if not self.adb.tap(coords['submit_button_x'], coords['submit_button_y']):
                self.adb.close_app(package)
                return False
            
            time.sleep(CONFIG['delays']['after_submit'])
            
            # Close app
            self.adb.close_app(package)
            
            self.stats['solved'] += 1
            logging.info(f"✓ CAPTCHA solved successfully! Total: {self.stats['solved']}")
            return True
            
        except Exception as e:
            logging.error(f"Error solving CAPTCHA: {e}")
            self.stats['failed'] += 1
            return False
    
    def run_continuous(self, max_iterations=None):
        """Run solver continuously with virtual display"""
        logging.info("=" * 60)
        logging.info("CAPTCHA SOLVER WITH VIRTUAL DISPLAY")
        logging.info("=" * 60)
        logging.info(f"Log file: {LOG_FILE}")
        logging.info("")
        
        # Check scrcpy
        if not self.scrcpy.check_scrcpy_installed():
            return
        
        # Check ADB connection
        if not self.adb.check_connection():
            logging.error("Failed to connect to device")
            return
        
        # Start virtual display
        if not self.scrcpy.start_virtual_display(hidden=not self.show_window):
            return
        
        iteration = 0
        try:
            while True:
                iteration += 1
                
                # Calculate stats
                elapsed = (datetime.now() - self.stats['start_time']).total_seconds() / 60
                rate = self.stats['solved'] / elapsed if elapsed > 0 else 0
                
                logging.info("")
                logging.info("=" * 60)
                logging.info(f"Iteration: {iteration}")
                logging.info(f"Solved: {self.stats['solved']} | Failed: {self.stats['failed']}")
                logging.info(f"Runtime: {elapsed:.1f} min | Rate: {rate:.2f} CAPTCHAs/min")
                logging.info("=" * 60)
                
                # Solve one CAPTCHA
                self.solve_one_captcha()
                
                # Check if max iterations reached
                if max_iterations and iteration >= max_iterations:
                    logging.info(f"Reached max iterations: {max_iterations}")
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("")
            logging.info("=" * 60)
            logging.info("CAPTCHA SOLVER STOPPED BY USER")
            logging.info(f"Total solved: {self.stats['solved']}")
            logging.info(f"Total failed: {self.stats['failed']}")
            logging.info(f"Runtime: {elapsed:.1f} minutes")
            logging.info("=" * 60)
        finally:
            self.scrcpy.stop_virtual_display()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CAPTCHA Solver with Virtual Display')
    parser.add_argument('--iterations', type=int, help='Max iterations (default: infinite)')
    parser.add_argument('--show-window', action='store_true', help='Show scrcpy window')
    parser.add_argument('--test', action='store_true', help='Test mode (one CAPTCHA only)')
    
    args = parser.parse_args()
    
    solver = VirtualCaptchaSolver(show_window=args.show_window)
    
    if args.test:
        logging.info("Running in TEST mode")
        if solver.scrcpy.check_scrcpy_installed() and solver.adb.check_connection():
            solver.scrcpy.start_virtual_display(hidden=not args.show_window)
            time.sleep(2)
            solver.solve_one_captcha()
            solver.scrcpy.stop_virtual_display()
    else:
        solver.run_continuous(max_iterations=args.iterations)

if __name__ == "__main__":
    main()
