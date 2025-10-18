"""
CAPTCHA Solver with ADB Integration
Connects to Android device via ADB, captures screenshots, reads CAPTCHAs using EasyOCR,
and automatically submits answers.
"""

import subprocess
import time
import os
import logging
import json
from datetime import datetime
from pathlib import Path
import sys

try:
    import cv2
    import numpy as np
    import easyocr
except ImportError as e:
    print(f"Error: Missing required package. Please run: pip install -r requirements.txt")
    print(f"Specific error: {e}")
    sys.exit(1)

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "config.json"
LOG_DIR = PROJECT_DIR / "logs"
SCREENSHOT_DIR = PROJECT_DIR / "screenshots"

# Create necessary directories
LOG_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)

# Set up logging
LOG_FILE = LOG_DIR / f"captcha_solver_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def load_config():
    """Load configuration from config.json"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        default_config = {
            "captcha_work": {
                "package": "com.captchawork",
                "activity": ".MainActivity"
            },
            "coordinates": {
                "input_field_x": 540,
                "input_field_y": 1400,
                "submit_button_x": 540,
                "submit_button_y": 1700,
                "captcha_crop": {
                    "x1": 100,
                    "y1": 800,
                    "x2": 980,
                    "y2": 1200
                }
            },
            "delays": {
                "after_tap": 0.5,
                "after_text": 0.5,
                "after_submit": 2.0,
                "after_close": 0.5,
                "after_open": 3.0,
                "before_screenshot": 1.0
            },
            "ocr": {
                "min_confidence": 0.3,
                "languages": ["en"]
            },
            "adb": {
                "command": "adb",
                "device_serial": null,
                "wireless_port": 5555
            }
        }
        
        # Save default config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        logging.info(f"Created default config file: {CONFIG_FILE}")
        return default_config

# Load configuration
CONFIG = load_config()

class ADBController:
    """Handles all ADB operations"""
    
    def __init__(self):
        self.adb_command = CONFIG['adb']['command']
        self.device_serial = CONFIG['adb']['device_serial']
        
    def get_adb_prefix(self):
        """Get ADB command prefix with device serial if specified"""
        if self.device_serial:
            return [self.adb_command, "-s", self.device_serial]
        return [self.adb_command]
    
    def check_connection(self):
        """Check if device is connected"""
        try:
            result = subprocess.run(
                self.get_adb_prefix() + ["devices"],
                capture_output=True,
                text=True,
                check=True
            )
            
            devices = [line for line in result.stdout.split('\n') 
                      if line and not line.startswith('List') and '\tdevice' in line]
            
            if not devices:
                logging.error("No devices connected via ADB")
                return False
            
            if len(devices) > 1 and not self.device_serial:
                logging.warning(f"Multiple devices connected: {len(devices)}")
                logging.info("Please specify device_serial in config.json")
                for device in devices:
                    logging.info(f"  - {device.split()[0]}")
                return False
            
            device_id = devices[0].split()[0]
            logging.info(f"Connected to device: {device_id}")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"ADB connection check failed: {e}")
            return False
    
    def capture_screenshot(self, output_path):
        """Capture screenshot from device"""
        try:
            logging.info("Capturing screenshot...")
            time.sleep(CONFIG['delays']['before_screenshot'])
            
            # Capture screenshot to device
            subprocess.run(
                self.get_adb_prefix() + ["shell", "screencap", "-p", "/sdcard/screenshot.png"],
                check=True
            )
            
            # Pull screenshot to computer
            subprocess.run(
                self.get_adb_prefix() + ["pull", "/sdcard/screenshot.png", str(output_path)],
                check=True,
                capture_output=True
            )
            
            logging.info(f"Screenshot saved to: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to capture screenshot: {e}")
            return False
    
    def tap(self, x, y):
        """Tap at specific coordinates"""
        try:
            subprocess.run(
                self.get_adb_prefix() + ["shell", "input", "tap", str(x), str(y)],
                check=True
            )
            time.sleep(CONFIG['delays']['after_tap'])
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to tap at ({x}, {y}): {e}")
            return False
    
    def input_text(self, text):
        """Input text via ADB"""
        try:
            # Clean text (remove special characters that might cause issues)
            cleaned_text = ''.join(c for c in text if c.isalnum())
            
            # First clear any existing text
            subprocess.run(
                self.get_adb_prefix() + ["shell", "input", "keyevent", "KEYCODE_MOVE_END"],
                check=True
            )
            for _ in range(20):  # Delete up to 20 characters
                subprocess.run(
                    self.get_adb_prefix() + ["shell", "input", "keyevent", "KEYCODE_DEL"],
                    check=True
                )
            
            # Input new text
            subprocess.run(
                self.get_adb_prefix() + ["shell", "input", "text", cleaned_text],
                check=True
            )
            
            time.sleep(CONFIG['delays']['after_text'])
            logging.info(f"Entered text: '{cleaned_text}'")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to input text: {e}")
            return False
    
    def open_app(self, package, activity):
        """Open an app via ADB"""
        try:
            logging.info(f"Opening app: {package}")
            subprocess.run(
                self.get_adb_prefix() + ["shell", "am", "start", "-n", f"{package}/{activity}"],
                check=True
            )
            time.sleep(CONFIG['delays']['after_open'])
            logging.info("App opened successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to open app: {e}")
            return False
    
    def close_app(self, package):
        """Close an app via ADB"""
        try:
            logging.info(f"Closing app: {package}")
            subprocess.run(
                self.get_adb_prefix() + ["shell", "am", "force-stop", package],
                check=True
            )
            time.sleep(CONFIG['delays']['after_close'])
            logging.info("App closed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to close app: {e}")
            return False

class CaptchaOCR:
    """Handles CAPTCHA text extraction using EasyOCR"""
    
    def __init__(self):
        logging.info("Initializing EasyOCR...")
        self.reader = easyocr.Reader(
            CONFIG['ocr']['languages'],
            gpu=False  # Set to True if you have CUDA GPU
        )
        logging.info("EasyOCR initialized successfully")
    
    def extract_captcha(self, image_path):
        """Extract CAPTCHA text from screenshot"""
        try:
            # Load image
            img = cv2.imread(str(image_path))
            if img is None:
                logging.error(f"Failed to load image: {image_path}")
                return None
            
            # Crop to CAPTCHA region
            crop_config = CONFIG['coordinates']['captcha_crop']
            captcha_region = img[
                crop_config['y1']:crop_config['y2'],
                crop_config['x1']:crop_config['x2']
            ]
            
            # Save cropped region for debugging
            crop_path = SCREENSHOT_DIR / f"captcha_crop_{datetime.now().strftime('%H%M%S')}.png"
            cv2.imwrite(str(crop_path), captcha_region)
            
            # Preprocess image
            gray = cv2.cvtColor(captcha_region, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding to make text clearer
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Use EasyOCR to extract text
            results = self.reader.readtext(thresh)
            
            if not results:
                logging.warning("No text detected in CAPTCHA")
                return None
            
            # Get text with highest confidence
            best_result = max(results, key=lambda x: x[2])
            text, confidence = best_result[1], best_result[2]
            
            logging.info(f"Detected CAPTCHA: '{text}' (confidence: {confidence:.2f})")
            
            if confidence < CONFIG['ocr']['min_confidence']:
                logging.warning(f"Low confidence: {confidence:.2f} < {CONFIG['ocr']['min_confidence']}")
            
            return text.strip()
            
        except Exception as e:
            logging.error(f"Error extracting CAPTCHA: {e}")
            return None

class CaptchaSolver:
    """Main CAPTCHA solver logic"""
    
    def __init__(self):
        self.adb = ADBController()
        self.ocr = CaptchaOCR()
        self.stats = {
            'solved': 0,
            'failed': 0,
            'start_time': datetime.now()
        }
    
    def solve_one_captcha(self):
        """Solve one CAPTCHA"""
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
        """Run solver continuously"""
        logging.info("=" * 60)
        logging.info("CAPTCHA SOLVER STARTED")
        logging.info("=" * 60)
        logging.info(f"Log file: {LOG_FILE}")
        logging.info(f"Config file: {CONFIG_FILE}")
        logging.info("")
        
        # Check ADB connection
        if not self.adb.check_connection():
            logging.error("Failed to connect to device. Please check:")
            logging.error("  1. USB debugging is enabled on your phone")
            logging.error("  2. Your phone is connected via USB or wireless ADB")
            logging.error("  3. You've accepted the USB debugging prompt")
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
                
                # Small delay between iterations
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("")
            logging.info("=" * 60)
            logging.info("CAPTCHA SOLVER STOPPED BY USER")
            logging.info(f"Total solved: {self.stats['solved']}")
            logging.info(f"Total failed: {self.stats['failed']}")
            logging.info(f"Runtime: {elapsed:.1f} minutes")
            logging.info("=" * 60)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CAPTCHA Solver with ADB')
    parser.add_argument('--iterations', type=int, help='Max iterations (default: infinite)')
    parser.add_argument('--test', action='store_true', help='Test mode (solve one CAPTCHA only)')
    
    args = parser.parse_args()
    
    solver = CaptchaSolver()
    
    if args.test:
        logging.info("Running in TEST mode (one CAPTCHA only)")
        solver.solve_one_captcha()
    else:
        solver.run_continuous(max_iterations=args.iterations)

if __name__ == "__main__":
    main()
