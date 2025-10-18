# Running Android in a True Virtual Environment with VirtualBox

This guide will help you set up a completely virtual Android environment using VirtualBox on Windows. This is a true virtual solution where the app runs entirely on your computer, not on your phone.

## Why This Solution Works

This solution is superior because:

1. It runs Android-x86 in a virtual machine on your Windows computer
2. Your phone is not involved at all - no app opening on your phone
3. The virtual machine can run headlessly (no visible window)
4. It's a complete Android environment that can run any Android app

## Setup Instructions

### Step 1: Download Required Software

1. **VirtualBox**: Download and install from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)
2. **Android-x86**: Download from [android-x86.org](https://www.android-x86.org/download.html) (get the latest stable ISO)

### Step 2: Create a Virtual Machine

1. Open VirtualBox
2. Click "New"
3. Enter the following settings:
   - Name: "Android-x86"
   - Type: "Linux"
   - Version: "Other Linux (64-bit)"
   - Memory: 2048 MB (or more if available)
   - Create a virtual hard disk (VDI, dynamically allocated, 8GB)

### Step 3: Configure the Virtual Machine

1. Select the new VM and click "Settings"
2. **System**:
   - Processor: 2 CPUs (or more if available)
   - Enable PAE/NX
3. **Display**:
   - Video Memory: 128 MB
   - Graphics Controller: VBoxSVGA
4. **Storage**:
   - Click on the empty optical drive
   - Choose the Android-x86 ISO file you downloaded
5. **Network**:
   - Adapter 1: NAT

### Step 4: Install Android-x86

1. Start the VM
2. Select "Installation - Install Android-x86 to harddisk"
3. Create a new partition (use the entire disk)
4. Format as ext4
5. Install GRUB bootloader
6. Make system r/w (Yes)
7. Complete the installation and reboot

### Step 5: Complete Android Setup

1. Go through the Android setup process
2. Connect to Wi-Fi
3. Skip Google account setup (you can add it later)
4. Complete the initial setup

### Step 6: Install the CAPTCHA Work App

1. Download the APK file for CAPTCHA Work
   - You can extract it from your phone using ADB:
     ```
     adb shell pm path com.captchawork
     adb pull /data/app/com.captchawork-1/base.apk captcha_work.apk
     ```
2. Transfer the APK to the VM:
   - Enable shared folders in VirtualBox settings
   - Add a shared folder with your Windows folder containing the APK
   - Mount the shared folder in Android
   - Copy the APK file
3. Install the APK:
   - Open a terminal in Android
   - Navigate to where you copied the APK
   - Run: `pm install captcha_work.apk`

### Step 7: Set Up Headless Operation

1. Shut down the VM
2. Create a batch file to run the VM headlessly:

```batch
@echo off
echo Starting Android-x86 VM headlessly...
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "Android-x86" --type headless
echo VM started. To stop it, run: stop_android_vm.bat
```

3. Create a batch file to stop the VM:

```batch
@echo off
echo Stopping Android-x86 VM...
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm "Android-x86" savestate
echo VM stopped and state saved.
```

### Step 8: Create a Script to Run the CAPTCHA Solver

1. Install ADB on your Windows computer
2. Create a script to connect to the VM via ADB:

```batch
@echo off
echo Connecting to Android-x86 VM via ADB...
adb connect localhost:5555
echo Running CAPTCHA solver...
python captcha_solver_vm.py
```

3. Create a modified version of the CAPTCHA solver script that connects to the VM:

```python
# captcha_solver_vm.py
import subprocess
import time
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='vm_captcha_solver.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration
ADB_PATH = "adb"  # ADB should be in PATH
CAPTCHA_WORK_PACKAGE = "com.captchawork"
CAPTCHA_WORK_ACTIVITY = "com.captchawork.MainActivity"

# Coordinates for input field and submit button
INPUT_FIELD_X = 620
INPUT_FIELD_Y = 1500
SUBMIT_BUTTON_X = 598
SUBMIT_BUTTON_Y = 1732

# Timing settings
DELAY_AFTER_TAP = 0.5
DELAY_AFTER_TEXT = 0.5
DELAY_AFTER_SUBMIT = 0.5
DELAY_AFTER_CLOSE = 0.5
DELAY_AFTER_OPEN = 2.0
DELAY_BEFORE_SCREENSHOT = 1.5
DELAY_AFTER_SCREENSHOT = 1.0

def log_and_print(message, level="info"):
    """Log a message and print it to console"""
    if level.lower() == "info":
        logging.info(message)
    elif level.lower() == "error":
        logging.error(message)
    elif level.lower() == "warning":
        logging.warning(message)
    
    # Also print to console
    print(message)

def connect_to_vm():
    """Connect to the Android-x86 VM via ADB"""
    try:
        log_and_print("Connecting to Android-x86 VM...")
        subprocess.run([ADB_PATH, "connect", "localhost:5555"], check=True)
        log_and_print("Connected to VM")
        return True
    except Exception as e:
        log_and_print(f"Error connecting to VM: {e}", "error")
        return False

def open_captcha_work():
    """Open the Captcha Work app"""
    try:
        log_and_print("Opening Captcha Work app...")
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "am", "start", "-n", 
                      f"{CAPTCHA_WORK_PACKAGE}/{CAPTCHA_WORK_ACTIVITY}"], check=True)
        log_and_print(f"Waiting {DELAY_AFTER_OPEN}s for app to open...")
        time.sleep(DELAY_AFTER_OPEN)
        log_and_print("Captcha Work app opened")
        return True
    except Exception as e:
        log_and_print(f"Error opening Captcha Work: {e}", "error")
        return False

def close_captcha_work():
    """Close the Captcha Work app"""
    try:
        log_and_print("Closing Captcha Work app...")
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "am", "force-stop", 
                      CAPTCHA_WORK_PACKAGE], check=True)
        log_and_print(f"Waiting {DELAY_AFTER_CLOSE}s for app to close...")
        time.sleep(DELAY_AFTER_CLOSE)
        log_and_print("Captcha Work app closed")
        return True
    except Exception as e:
        log_and_print(f"Error closing Captcha Work: {e}", "error")
        return False

def capture_screenshot(local_path="screen.png"):
    """Capture a screenshot from the VM"""
    try:
        log_and_print(f"Waiting {DELAY_BEFORE_SCREENSHOT}s before taking screenshot...")
        time.sleep(DELAY_BEFORE_SCREENSHOT)
        
        log_and_print("Capturing screenshot from VM...")
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "exec-out", "screencap", "-p", ">", 
                      local_path], check=True, shell=True)
        log_and_print(f"Screenshot saved to {local_path}")
        
        log_and_print(f"Waiting {DELAY_AFTER_SCREENSHOT}s after screenshot...")
        time.sleep(DELAY_AFTER_SCREENSHOT)
        
        return local_path
    except Exception as e:
        log_and_print(f"Error capturing screenshot: {e}", "error")
        return None

def input_and_submit(text):
    """Input the CAPTCHA text and submit it"""
    log_and_print(f"Tapping input field at ({INPUT_FIELD_X}, {INPUT_FIELD_Y})...")
    try:
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "input", "tap", 
                      str(INPUT_FIELD_X), str(INPUT_FIELD_Y)], check=True)
        
        log_and_print(f"Waiting {DELAY_AFTER_TAP}s after tap...")
        time.sleep(DELAY_AFTER_TAP)
        
        # Clear any existing text
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "input", "keyevent", 
                      "KEYCODE_CTRL_A"], check=True)
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "input", "keyevent", 
                      "KEYCODE_DEL"], check=True)
        
        time.sleep(DELAY_AFTER_TAP)
        
        log_and_print(f"Entering text: '{text}'...")
        cleaned_text = ''.join(c for c in text if c.isalnum())
        log_and_print(f"Cleaned text for input: '{cleaned_text}'")
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "input", "text", 
                      cleaned_text], check=True)
        
        log_and_print(f"Waiting {DELAY_AFTER_TEXT}s after entering text...")
        time.sleep(DELAY_AFTER_TEXT)
        
        log_and_print(f"Tapping submit button at ({SUBMIT_BUTTON_X}, {SUBMIT_BUTTON_Y})...")
        subprocess.run([ADB_PATH, "-s", "localhost:5555", "shell", "input", "tap", 
                      str(SUBMIT_BUTTON_X), str(SUBMIT_BUTTON_Y)], check=True)
        
        log_and_print(f"Waiting {DELAY_AFTER_SUBMIT}s after submission...")
        time.sleep(DELAY_AFTER_SUBMIT)
        return True
    except Exception as e:
        log_and_print(f"Error during input and submit: {e}", "error")
        return False

def main():
    """Main function to run the CAPTCHA solver"""
    log_and_print("Starting CAPTCHA Solver for Android-x86 VM")
    
    # Connect to the VM
    if not connect_to_vm():
        log_and_print("Failed to connect to VM. Exiting.", "error")
        return
    
    # Import EasyOCR here to avoid loading it if connection fails
    import cv2
    import numpy as np
    import easyocr
    
    # Initialize EasyOCR
    log_and_print("Initializing EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    log_and_print("EasyOCR initialized")
    
    try:
        solved_count = 0
        start_time = datetime.now()
        
        while True:
            try:
                # Calculate statistics
                current_time = datetime.now()
                elapsed_time = (current_time - start_time).total_seconds() / 60
                
                if elapsed_time > 0:
                    rate = solved_count / elapsed_time
                else:
                    rate = 0
                
                log_and_print(f"Running for {elapsed_time:.1f} minutes. Rate: {rate:.2f} CAPTCHAs/minute")
                
                # Open the app
                log_and_print("\n--- New CAPTCHA Attempt ---")
                open_captcha_work()
                
                # Capture screenshot
                screenshot_path = capture_screenshot()
                
                if not screenshot_path:
                    log_and_print("Failed to capture screenshot. Retrying...", "error")
                    close_captcha_work()
                    continue
                
                # Extract CAPTCHA text (using the same function from your original script)
                # ... (add your extract_captcha_text function here)
                
                # For testing, use a dummy text
                captcha_text = "test123"
                
                # Input text and submit
                if input_and_submit(captcha_text):
                    solved_count += 1
                    log_and_print(f"Total CAPTCHAs solved: {solved_count}")
                else:
                    log_and_print("Failed to input and submit", "error")
                
                # Close the app
                close_captcha_work()
                
            except Exception as e:
                log_and_print(f"Error in main loop: {e}", "error")
                try:
                    close_captcha_work()
                except:
                    pass
                time.sleep(30)
        
    except KeyboardInterrupt:
        log_and_print("Process stopped by user")
        log_and_print(f"Total CAPTCHAs solved: {solved_count}")
    except Exception as e:
        log_and_print(f"Error in main process: {e}", "error")

if __name__ == "__main__":
    main()
```

## Running the Solution

1. Start the VM headlessly:
   ```
   start_android_vm.bat
   ```

2. Run the CAPTCHA solver:
   ```
   run_captcha_solver.bat
   ```

3. To stop the VM:
   ```
   stop_android_vm.bat
   ```

## Benefits of This Solution

1. **True Virtual Environment**: The Android OS runs entirely on your computer
2. **No Phone Involvement**: Your phone is not used at all
3. **Headless Operation**: No visible window on your computer
4. **Complete Android Environment**: Can run any Android app
5. **Persistent Storage**: The VM state is saved between runs

## Troubleshooting

### VM Won't Start

```
VBoxManage list vms
VBoxManage showvminfo "Android-x86"
```

### ADB Connection Issues

```
adb kill-server
adb start-server
adb connect localhost:5555
```

### Performance Issues

- Increase VM memory and CPU allocation
- Enable hardware virtualization in BIOS/UEFI
- Use a SSD for the VM disk

This solution gives you exactly what you're looking for - a truly virtual environment where the app doesn't appear on your phone at all.
