# 🤖 CAPTCHA Solver - Complete Setup Guide

Automated CAPTCHA solver using ADB, EasyOCR, and OpenCV. Works with both USB and wireless connections.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Connection Setup](#connection-setup)
  - [USB Connection](#usb-connection)
  - [Wireless Connection](#wireless-connection)
  - [Using Termux](#using-termux-optional)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- ✅ **Automatic CAPTCHA solving** using EasyOCR
- ✅ **USB and Wireless ADB** support
- ✅ **Virtual display mode** (phone screen stays OFF)
- ✅ **Detailed logging** for debugging
- ✅ **Easy configuration** via JSON file
- ✅ **Multiple device support**
- ✅ **Screenshot archiving** for analysis

---

## 📦 Requirements

### On Your Computer:
- **Windows 10/11** (or Linux/Mac with modifications)
- **Python 3.7+**
- **ADB (Android Debug Bridge)** - Included in `platform-tools` folder
- **(Optional) scrcpy** - For virtual display mode

### On Your Phone:
- **Android 7.0+**
- **USB Debugging enabled**
- **CAPTCHA Work app** (or your target app)

---

## 🚀 Installation

### Step 1: Install Python Dependencies

Run the setup script:
```batch
setup.bat
```

This will:
- Create a virtual environment
- Install all required packages (OpenCV, EasyOCR, etc.)
- Set up the project structure

**Manual installation (if needed):**
```batch
python -m venv captcha_env
captcha_env\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Install ADB

**Option A:** Use included platform-tools
- ADB is already in the `platform-tools` folder
- Add to PATH: `set PATH=%PATH%;D:\Android Platform tool\platform-tools`

**Option B:** Download latest ADB
1. Download from: https://developer.android.com/tools/releases/platform-tools
2. Extract and add to system PATH

**Verify ADB installation:**
```batch
adb version
```

### Step 3: Install scrcpy (Optional - for virtual display mode)

**Using Chocolatey:**
```batch
choco install scrcpy
```

**Manual installation:**
1. Download from: https://github.com/Genymobile/scrcpy/releases
2. Extract and add to PATH
3. Verify: `scrcpy --version`

---

## 🔌 Connection Setup

### USB Connection (Recommended for first setup)

#### Step 1: Enable Developer Options
1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. You'll see "You are now a developer!"

#### Step 2: Enable USB Debugging
1. Go to **Settings** → **System** → **Developer Options**
2. Enable **USB Debugging**
3. Enable **Stay Awake** (optional but helpful)

#### Step 3: Connect Your Phone
1. Connect phone via USB cable
2. Select **File Transfer** or **MTP** mode
3. Accept the **USB debugging** prompt on your phone
4. Check "Always allow from this computer" ✓

#### Step 4: Verify Connection
```batch
check_connection.bat
```

You should see your device listed:
```
List of devices attached
ABC123456789    device
```

---

### Wireless Connection (No cable needed!)

#### Method 1: Using USB First (Easiest)

1. **Connect via USB** and verify with `adb devices`

2. **Enable TCP/IP mode:**
   ```batch
   adb tcpip 5555
   ```

3. **Find your phone's IP address:**
   - **Settings** → **About Phone** → **Status** → **IP Address**
   - Or use: **Settings** → **Wi-Fi** → Tap your network → IP Address
   - Example: `192.168.1.100`

4. **Connect wirelessly:**
   ```batch
   adb connect 192.168.1.100:5555
   ```

5. **Disconnect USB cable** (you're now wireless!)

6. **Verify:**
   ```batch
   adb devices
   ```
   Should show:
   ```
   192.168.1.100:5555    device
   ```

7. **Update config.json** (optional):
   ```json
   "adb": {
       "device_serial": "192.168.1.100:5555"
   }
   ```

#### Method 2: Using Wireless ADB (Android 11+)

1. Go to **Developer Options**
2. Enable **Wireless Debugging**
3. Tap **Wireless Debugging** → **Pair device with pairing code**
4. On your computer:
   ```batch
   adb pair 192.168.1.100:XXXXX
   ```
   Enter the pairing code shown on phone

5. Connect:
   ```batch
   adb connect 192.168.1.100:XXXXX
   ```

---

### Using Termux (Optional)

You can use Termux on your phone as an alternative to ADB from computer:

#### Step 1: Install Termux
- Download from: https://f-droid.org/packages/com.termux/
- **DO NOT** use Play Store version (outdated)

#### Step 2: Install ADB in Termux
```bash
pkg update
pkg install android-tools
```

#### Step 3: Enable Wireless ADB from Termux
```bash
setprop service.adb.tcp.port 5555
stop adbd
start adbd
```

#### Step 4: Connect from Computer
```batch
adb connect localhost:5555
```

---

## ⚙️ Configuration

### Edit `config.json`

```json
{
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
    }
}
```

### Finding Coordinates

#### Method 1: Using ADB (Easy)
1. Enable **Pointer Location** in Developer Options
2. Touch the screen where you want coordinates
3. Look at the top of screen for coordinates

#### Method 2: Using Screenshot
1. Take screenshot: `adb shell screencap -p /sdcard/screen.png`
2. Pull it: `adb pull /sdcard/screen.png`
3. Open in image editor and note pixel coordinates

#### Method 3: Using Developer Options
1. Enable **Show Taps** and **Pointer Location**
2. Record screen while tapping
3. Review video for exact coordinates

### Finding Package and Activity Name

```batch
# Open the CAPTCHA app on your phone, then run:
adb shell dumpsys window windows | findstr "mCurrentFocus"
```

Output example:
```
mCurrentFocus=Window{abc123 u0 com.captchawork/com.captchawork.MainActivity}
```
- Package: `com.captchawork`
- Activity: `com.captchawork.MainActivity` (use `.MainActivity` in config)

---

## 🎮 Usage

### Test Mode (Solve ONE captcha)
```batch
test_solver.bat
```

### Standard Mode (USB connection, screen visible)
```batch
run_solver.bat
```

### Virtual Display Mode (Phone screen OFF)
```batch
run_solver_virtual.bat
```

### With Arguments
```batch
# Run for 10 iterations only
run_solver.bat --iterations 10

# Show scrcpy window in virtual mode
run_solver_virtual.bat --show-window
```

### Command Line Options
```batch
# Standard solver
python src\captcha_solver_adb.py --help
python src\captcha_solver_adb.py --test
python src\captcha_solver_adb.py --iterations 50

# Virtual display solver
python src\captcha_solver_virtual.py --help
python src\captcha_solver_virtual.py --test
python src\captcha_solver_virtual.py --show-window
```

---

## 📊 Logs and Screenshots

- **Logs:** `logs/captcha_solver_YYYYMMDD_HHMMSS.log`
- **Screenshots:** `screenshots/screen_HHMMSS.png`
- **Cropped CAPTCHAs:** `screenshots/captcha_crop_HHMMSS.png`

View real-time logs:
```batch
type logs\captcha_solver_*.log
```

---

## 🔧 Troubleshooting

### "No devices connected"
- Check USB cable (try different cable/port)
- Verify USB Debugging is enabled
- Accept the USB debugging prompt on phone
- Try: `adb kill-server` then `adb start-server`
- For wireless: Ensure phone and computer on same WiFi

### "App won't open"
- Verify package name in config.json
- Check activity name (use dumpsys command above)
- Ensure CAPTCHA app is installed
- Grant necessary permissions to the app

### "Can't extract CAPTCHA text"
- Check captcha_crop coordinates in config.json
- Look at `screenshots/captcha_crop_*.png` to verify crop region
- Adjust crop coordinates to capture only CAPTCHA text
- Try increasing delays in config.json

### "Wrong text submitted"
- OCR accuracy varies - check confidence scores in logs
- Try preprocessing in config (adjust min_confidence)
- Ensure CAPTCHA region is clear (no overlapping elements)
- Check lighting/contrast of CAPTCHA images

### "scrcpy not found"
- Install scrcpy: `choco install scrcpy`
- Or download from: https://github.com/Genymobile/scrcpy/releases
- Add scrcpy to PATH

### "Multiple devices connected"
- Disconnect other devices
- Or specify device in config.json:
  ```json
  "adb": {
      "device_serial": "ABC123456789"
  }
  ```

### Wireless Connection Drops
- Phone goes to sleep → Enable "Stay Awake" in Developer Options
- WiFi turns off → Disable battery optimization for WiFi
- Reconnect: `adb connect YOUR_IP:5555`

---

## 🎯 Tips for Best Performance

1. **Use Wireless Connection** - No cable wear, more flexibility
2. **Enable Virtual Display Mode** - Saves phone battery
3. **Adjust Delays** - Faster phone = shorter delays
4. **Monitor Logs** - Watch for patterns in failures
5. **Test Coordinates** - Use test mode first
6. **Keep Phone Plugged In** - For long sessions
7. **Close Other Apps** - For better performance

---

## 📱 Your Phone Info

After connecting, you can check:

```batch
# Phone model
adb shell getprop ro.product.model

# Android version
adb shell getprop ro.build.version.release

# Screen resolution
adb shell wm size

# Screen density
adb shell wm density
```

---

## 🚀 Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] Run `setup.bat`
- [ ] Enable USB Debugging on phone
- [ ] Connect phone via USB
- [ ] Run `check_connection.bat`
- [ ] Edit `config.json` with your app details
- [ ] Run `test_solver.bat` to verify
- [ ] Run `run_solver.bat` or `run_solver_virtual.bat`

---

## 📝 Next Steps

Once everything is working:

1. **Configure for wireless** - No more cables!
2. **Adjust coordinates** - Fine-tune for accuracy
3. **Optimize delays** - Speed up solving
4. **Monitor performance** - Check logs regularly
5. **Set up automation** - Run at specific times

---

## 💡 Need Help?

1. Check logs in `logs/` folder
2. Verify screenshots in `screenshots/` folder
3. Test with `test_solver.bat` first
4. Check config.json settings
5. Verify ADB connection with `check_connection.bat`

---

**Ready to solve CAPTCHAs? Run `setup.bat` to begin! 🚀**
