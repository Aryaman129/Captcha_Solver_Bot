# 🤖 Automated CAPTCHA Solver

**Intelligent CAPTCHA solving system using ADB, Computer Vision, and OCR**

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🌟 Overview

An automated CAPTCHA solving system that connects to your Android device, captures CAPTCHAs, reads them using EasyOCR, and automatically submits answers. Perfect for CAPTCHA-based earning apps, testing automation, or accessibility solutions.

### Key Features

✅ **Dual Mode Operation**
- Standard Mode: Works with USB/wireless ADB
- Virtual Display Mode: Phone screen stays OFF (uses scrcpy)

✅ **Intelligent OCR**
- EasyOCR for accurate text recognition
- Configurable confidence thresholds
- Multi-language support

✅ **Flexible Connection**
- USB connection support
- Wireless ADB (no cables!)
- Multi-device support
- Termux integration

✅ **Production Ready**
- Comprehensive logging
- Screenshot archival
- Error recovery
- Performance tracking

✅ **Easy Configuration**
- JSON-based config
- Adjustable coordinates
- Customizable delays
- Device-specific settings

---

## 📁 Project Structure

```
Android Platform tool/
├── src/
│   ├── captcha_solver_adb.py      # Main solver with ADB
│   └── captcha_solver_virtual.py  # Virtual display version
├── docs/                           # Additional documentation
├── logs/                           # Execution logs
├── screenshots/                    # Captured screenshots
├── platform-tools/                 # ADB tools
├── config.json                     # Configuration file
├── requirements.txt                # Python dependencies
├── SETUP.md                        # Detailed setup guide
├── setup.bat                       # Setup script
├── check_connection.bat            # ADB connection tester
├── run_solver.bat                  # Run standard solver
├── run_solver_virtual.bat          # Run virtual display solver
└── test_solver.bat                 # Test mode (1 captcha)
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```batch
setup.bat
```

This installs Python packages: OpenCV, EasyOCR, NumPy, etc.

### 2. Connect Your Phone

**USB Connection:**
- Enable USB Debugging on phone
- Connect via USB cable
- Accept USB debugging prompt

**Wireless Connection:**
```batch
adb tcpip 5555
adb connect YOUR_PHONE_IP:5555
```

### 3. Verify Connection

```batch
check_connection.bat
```

### 4. Configure for YOUR App

**⚠️ IMPORTANT: You MUST edit `config.json` before running!**

Edit `config.json` and replace the default values:

#### A. Find Your App's Package Name
```batch
# 1. Open your CAPTCHA app on your phone
# 2. Run this command:
adb shell dumpsys window windows | findstr "mCurrentFocus"

# Output example:
# mCurrentFocus=Window{abc123 u0 com.yourapp/com.yourapp.MainActivity}
#                                  ^^^^^^^^^ Package name
```

Update in config.json:
```json
"captcha_work": {
    "package": "com.yourapp",        ← Replace this
    "activity": ".MainActivity"       ← Replace this
}
```

#### B. Find Screen Coordinates
```batch
# Method 1: Enable Pointer Location
# 1. Go to Developer Options > Show Pointer Location
# 2. Tap on your screen where the input field is
# 3. Note the X and Y values shown at the top

# Method 2: Take a screenshot
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png
# Open in image editor and note pixel coordinates
```

Update in config.json:
```json
"coordinates": {
    "input_field_x": 540,     ← X coordinate of input field
    "input_field_y": 1400,    ← Y coordinate of input field
    "submit_button_x": 540,   ← X coordinate of submit button
    "submit_button_y": 1700,  ← Y coordinate of submit button
    "captcha_crop": {
        "x1": 100,  ← Left edge of CAPTCHA image
        "y1": 800,  ← Top edge of CAPTCHA image
        "x2": 980,  ← Right edge of CAPTCHA image
        "y2": 1200  ← Bottom edge of CAPTCHA image
    }
}
```

#### C. Adjust Timing (Optional)
If your phone is slow or fast, adjust delays:
```json
"delays": {
    "after_open": 3.0,      ← Wait time after opening app
    "after_submit": 2.0     ← Wait time after submitting
}
```

**See [SETUP.md](SETUP.md) for detailed configuration instructions**

### 5. Test

```batch
test_solver.bat
```

### 6. Run

```batch
# Standard mode (screen visible)
run_solver.bat

# Virtual display mode (screen OFF)
run_solver_virtual.bat
```

---

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with screenshots
- **[docs/](docs/)** - Additional guides and references

---

## ⚙️ Configuration

### config.json

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
    },
    "delays": {
        "after_tap": 0.5,
        "after_submit": 2.0,
        "after_open": 3.0
    }
}
```

### Finding Coordinates

1. Enable "Pointer Location" in Developer Options
2. Tap the screen where needed
3. Note coordinates from top of screen

---

## 🎮 Usage Examples

### Basic Usage

```batch
# Test with one CAPTCHA
test_solver.bat

# Run continuously
run_solver.bat

# Run for 50 iterations
run_solver.bat --iterations 50
```

### Virtual Display Mode

```batch
# Run with phone screen OFF
run_solver_virtual.bat

# Show scrcpy window (for debugging)
run_solver_virtual.bat --show-window
```

### Python Commands

```batch
# Activate environment
captcha_env\Scripts\activate

# Run standard solver
python src\captcha_solver_adb.py

# Run virtual solver
python src\captcha_solver_virtual.py --test
```

---

## 📊 Performance Tracking

The solver automatically tracks:
- CAPTCHAs solved
- Success/failure rate
- Solving speed (CAPTCHAs per minute)
- Runtime statistics

Check logs in `logs/` folder for detailed analytics.

---

## 🔧 Requirements

### Software
- Python 3.7+
- ADB (Android Debug Bridge)
- scrcpy (optional, for virtual display)

### Hardware
- Android 7.0+
- USB cable or WiFi connection
- Computer (Windows/Linux/Mac)

### Python Packages
- opencv-python
- easyocr
- numpy
- pillow

---

## 🛠️ Troubleshooting

### Connection Issues

**Device not found:**
```batch
# Restart ADB server
adb kill-server
adb start-server

# Check devices
adb devices
```

**Wireless connection drops:**
```batch
# Reconnect
adb connect YOUR_IP:5555

# Enable "Stay Awake" in Developer Options
```

### OCR Issues

**Low accuracy:**
- Adjust `captcha_crop` coordinates in config.json
- Check `screenshots/captcha_crop_*.png` files
- Increase `min_confidence` threshold

**Can't read CAPTCHA:**
- Verify crop region captures full CAPTCHA
- Check image quality in screenshots
- Adjust delays if CAPTCHA not fully loaded

### App Issues

**App won't open:**
```batch
# Find correct package/activity
adb shell dumpsys window windows | findstr "mCurrentFocus"
```

**Wrong coordinates:**
- Enable "Pointer Location" in Developer Options
- Use test mode to verify taps
- Check phone resolution: `adb shell wm size`

---

## 🎯 Tips for Best Results

1. **Use Virtual Display Mode** - Saves battery, runs in background
2. **Enable Wireless ADB** - More convenient, no cable wear
3. **Adjust Delays** - Tune for your phone's speed
4. **Monitor Logs** - Track performance and errors
5. **Fine-tune Coordinates** - Test with one CAPTCHA first
6. **Keep Phone Charged** - For long sessions

---

## 🔒 Privacy & Security

- All processing done locally (no cloud/internet)
- Screenshots stored locally only
- ADB connection is secure and local
- No data shared externally

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional OCR engines
- Machine learning integration
- GUI interface
- Mobile app version
- iOS support

---

## 📞 Support

- Check SETUP.md for detailed instructions
- Review logs for error details
- Test with `test_solver.bat` first
- Verify connection with `check_connection.bat`

---

## 🎓 Educational Purpose

This project is for educational and accessibility purposes. Please use responsibly and in accordance with the terms of service of any apps or services.

---

## 🚀 Future Enhancements

- [ ] GUI interface for easier configuration
- [ ] Machine learning for better accuracy
- [ ] Cloud deployment options
- [ ] Mobile app (run entirely on phone)
- [ ] iOS support
- [ ] Multi-threaded solving
- [ ] Database integration for analytics
- [ ] Web dashboard

---

**Ready to get started? Run `setup.bat` and check [SETUP.md](SETUP.md) for detailed instructions!**
