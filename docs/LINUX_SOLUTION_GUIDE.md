# True Virtual Android Environment in Linux

This guide will help you set up a completely virtual Android environment in Linux where the CAPTCHA Work app runs without appearing on your phone's screen at all.

## Why Linux is the Best Solution

The Linux solution is superior because:

1. It runs a **true virtual Android environment** on your computer
2. Your phone is not involved at all - no app opening on your phone
3. The emulator can run headlessly (no visible window)
4. It's more stable and reliable than the Windows workarounds

## Setup Instructions

### Step 1: Boot into Linux

Since you mentioned you have Linux available, boot into your Linux system.

### Step 2: Download the Setup Files

Download these files from your Windows system to your Linux system:
- `linux_emulator_setup.sh`
- `linux_captcha_solver.py`

### Step 3: Run the Setup Script

```bash
# Make the script executable
chmod +x linux_emulator_setup.sh

# Run the setup script
./linux_emulator_setup.sh
```

This script will:
1. Install all required packages
2. Download and set up the Android SDK
3. Create a virtual Android device
4. Install Python dependencies
5. Create scripts to run the emulator headlessly

### Step 4: Get the CAPTCHA Work APK

You need to extract the CAPTCHA Work app from your phone:

```bash
# Connect your phone via USB
adb devices

# Find the package path
adb shell pm path com.captchawork

# Extract the APK (replace with the path from previous command)
adb pull /data/app/com.captchawork-1/base.apk captcha_work.apk
```

### Step 5: Run the Headless Emulator

```bash
# Run the emulator and CAPTCHA solver
./run_headless_emulator.sh
```

This will:
1. Start the Android emulator without a window
2. Install the CAPTCHA Work app
3. Run the CAPTCHA solver script

### Step 6: Set Up as a Service (Optional)

To run this automatically at startup:

```bash
# Edit the service file to use your username
nano captcha-solver.service

# Install the service
sudo cp captcha-solver.service /etc/systemd/system/
sudo systemctl enable captcha-solver.service
sudo systemctl start captcha-solver.service
```

## How It Works

1. **Virtual Android**: The emulator creates a complete Android environment
2. **Headless Mode**: No window is displayed on your screen
3. **Background Operation**: The service runs in the background
4. **No Phone Involvement**: Your phone is not used at all

## Troubleshooting

### Emulator Won't Start

```bash
# Check if KVM is available
kvm-ok

# If not, you may need to enable virtualization in BIOS/UEFI
```

### APK Installation Issues

```bash
# Check if the APK is valid
adb install -r captcha_work.apk
```

## Monitoring

To monitor the CAPTCHA solver:

```bash
# Check the log file
tail -f linux_captcha_solver.log

# Check the service status
sudo systemctl status captcha-solver.service
```

This solution gives you exactly what you're looking for - a truly virtual environment where the app doesn't appear on your phone at all.
