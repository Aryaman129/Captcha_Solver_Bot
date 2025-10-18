# True Virtual Android Environment in Linux

This guide will help you set up a completely virtual Android environment in Linux where the CAPTCHA Work app runs without appearing on your phone's screen at all.

## Overview

We'll use one of these approaches:
1. **Android Emulator**: Run a virtual Android device on your Linux system
2. **Android-x86 in VM**: Run Android as a virtual machine
3. **Anbox**: Run Android apps directly in Linux

## Option 1: Android Emulator (Recommended)

### Prerequisites
- Linux (Ubuntu/Debian recommended)
- At least 4GB RAM
- 10GB free disk space

### Step 1: Install Required Packages
```bash
sudo apt update
sudo apt install openjdk-11-jdk android-sdk qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils python3 python3-pip
```

### Step 2: Set Up Environment Variables
```bash
echo 'export ANDROID_SDK_ROOT=/usr/lib/android-sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_SDK_ROOT/tools/bin:$ANDROID_SDK_ROOT/platform-tools' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Install System Images and Create Virtual Device
```bash
sdkmanager "platform-tools" "platforms;android-30" "system-images;android-30;google_apis;x86_64"
avdmanager create avd -n CaptchaDevice -k "system-images;android-30;google_apis;x86_64" -d "pixel"
```

### Step 4: Install Python Dependencies
```bash
pip3 install opencv-python easyocr numpy pillow
```

### Step 5: Get the CAPTCHA Work APK
You'll need to get the APK file for the CAPTCHA Work app. You can extract it from your phone using:
```bash
adb shell pm path com.captchawork
# This will output something like: package:/data/app/com.captchawork-1/base.apk
adb pull /data/app/com.captchawork-1/base.apk captcha_work.apk
```

### Step 6: Run the Headless Emulator
```bash
# Start the emulator without a window
emulator -avd CaptchaDevice -no-window -no-audio -no-boot-anim &

# Wait for it to boot
adb wait-for-device

# Install the CAPTCHA Work app
adb install captcha_work.apk

# Run our CAPTCHA solver script
python3 linux_captcha_solver.py
```

## Option 2: Android-x86 in VirtualBox

### Step 1: Install VirtualBox
```bash
sudo apt update
sudo apt install virtualbox
```

### Step 2: Download Android-x86
Download from [android-x86.org](https://www.android-x86.org/download.html)

### Step 3: Create a Virtual Machine
1. Open VirtualBox
2. Click "New"
3. Name: "Android"
4. Type: "Linux"
5. Version: "Other Linux (64-bit)"
6. Memory: 2048 MB
7. Create a virtual hard disk
8. Start the VM and select the Android-x86 ISO

### Step 4: Install Android-x86
Follow the installation prompts to install Android-x86 to the virtual hard disk.

### Step 5: Configure for Headless Operation
```bash
# Start the VM in headless mode
VBoxManage startvm "Android" --type headless

# Connect ADB to the VM (default port is 5555)
adb connect localhost:5555

# Install the CAPTCHA Work app
adb install captcha_work.apk

# Run our CAPTCHA solver script
python3 linux_captcha_solver.py
```

## Option 3: Anbox

### Step 1: Install Anbox
```bash
sudo apt update
sudo apt install anbox
```

### Step 2: Install the CAPTCHA Work App
```bash
adb install captcha_work.apk
```

### Step 3: Run the CAPTCHA Solver
```bash
python3 linux_captcha_solver.py
```

## Automating the Process

To make this run automatically at startup:

### Create a Systemd Service
```bash
sudo nano /etc/systemd/system/captcha-solver.service
```

Add the following content:
```
[Unit]
Description=CAPTCHA Solver Virtual Service
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/captcha_solver
ExecStart=/bin/bash -c '/path/to/run_headless_emulator.sh'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable captcha-solver.service
sudo systemctl start captcha-solver.service
```

## Troubleshooting

### Emulator Won't Start
```bash
# Check if KVM is available
kvm-ok

# If not, you may need to enable virtualization in BIOS/UEFI
```

### ADB Connection Issues
```bash
# Restart ADB server
adb kill-server
adb start-server
```

### App Installation Issues
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
