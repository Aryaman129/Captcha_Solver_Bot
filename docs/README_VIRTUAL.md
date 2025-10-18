# CAPTCHA Solver with Virtual Display

This solution allows you to run the CAPTCHA solver in a virtual environment on your computer, while your phone's screen remains off. The app runs on your phone's processor but displays and interacts through your computer.

## Prerequisites

1. **Python 3.7+** installed on your computer
2. **ADB** (Android Debug Bridge) installed and in your PATH
3. **scrcpy** installed on your computer
4. **USB debugging** enabled on your Android phone
5. Required Python packages:
   - pywin32
   - opencv-python
   - easyocr
   - pure-python-adb

## Installation

### 1. Install scrcpy

#### Windows:
```
# Using Chocolatey
choco install scrcpy

# Or download from: https://github.com/Genymobile/scrcpy/releases
```

#### Linux:
```
sudo apt install scrcpy
```

### 2. Install Python Dependencies

```
pip install pywin32 opencv-python easyocr pure-python-adb
```

### 3. Connect Your Phone

1. Enable USB debugging on your phone
2. Connect your phone to your computer via USB
3. Accept the USB debugging prompt on your phone

### 4. Install the Service

Run the following command as Administrator:

```
manage_captcha_service.bat install
```

## Usage

### Starting the Service

```
manage_captcha_service.bat start
```

### Stopping the Service

```
manage_captcha_service.bat stop
```

### Checking Service Status

```
manage_captcha_service.bat status
```

### Testing Without Installing as a Service

```
manage_captcha_service.bat test
```

### Removing the Service

```
manage_captcha_service.bat remove
```

## How It Works

1. **Virtual Display**: scrcpy creates a virtual display on your computer
2. **App Runs on Phone**: The app still runs on your phone's processor
3. **Screen Redirection**: The visual output is redirected to the virtual display
4. **Phone Screen Off**: Your phone's physical screen is turned off
5. **Background Service**: The whole process runs as a Windows service

## Logs

Logs are stored in the following files:
- `captcha_service.log` - Service logs
- `captcha_solver_virtual.log` - CAPTCHA solver logs

## Troubleshooting

### Service Won't Start

1. Check if scrcpy is installed and in your PATH
2. Make sure your phone is connected and USB debugging is enabled
3. Check the logs for specific errors

### Phone Screen Doesn't Turn Off

1. Make sure your phone allows screen control via ADB
2. Some phones require additional permissions for screen control

### CAPTCHA Recognition Issues

1. Check the cropping dimensions in the code
2. Ensure the phone is in portrait mode
3. Check the logs for recognition confidence scores

## Wireless Operation

To use this wirelessly:

1. Connect your phone via USB
2. Run: `adb tcpip 5555`
3. Get your phone's IP address
4. Run: `adb connect YOUR_PHONE_IP:5555`
5. Disconnect the USB cable
6. Start the service

The service will maintain the wireless connection as long as your phone stays on the same WiFi network.
