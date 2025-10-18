# CAPTCHA Solver with Virtual Display (scrcpy)

This solution allows you to run the CAPTCHA solver with a virtual display using scrcpy. The app runs on your phone's processor, but the display is redirected to your computer, and your phone's screen can be turned off.

## How It Works

1. **scrcpy** creates a virtual display on your computer
2. The app runs on your phone's processor
3. The visual output is redirected to the virtual display (which is hidden)
4. Your phone's physical screen is turned off
5. All touch/input events are sent from the script to your phone

## Features

- **Phone Screen Off**: Your phone's screen is turned off, saving battery
- **Background Operation**: The process runs in the background
- **Same Functionality**: The CAPTCHA solver works exactly as before
- **Automatic Installation**: The script will automatically install scrcpy if needed

## Requirements

- Windows 10/11
- USB connection to your Android phone
- USB debugging enabled on your phone
- Python 3.7 or higher

## Usage

1. Connect your phone via USB
2. Run the batch file:
   ```
   run_rapid_solver.bat
   ```
3. The script will:
   - Check if scrcpy is installed and install it if needed
   - Start the virtual display
   - Turn off your phone's screen
   - Run the CAPTCHA solver

## What's Happening on Your Phone

- The app will still run on your phone's processor
- Your phone's screen will be turned off
- The app will open and close as before, but you won't see it
- Your phone will stay awake (but with screen off)

## Troubleshooting

### scrcpy Installation Issues

If the automatic installation fails:
1. Download scrcpy manually from: https://github.com/Genymobile/scrcpy/releases
2. Extract it to a folder
3. Add that folder to your PATH

### Phone Screen Still Turning On

Some phones have security settings that prevent the screen from being turned off via ADB. Try:
1. Go to Developer Options on your phone
2. Look for "Stay awake" or similar settings
3. Enable "Stay awake while charging"

### Connection Issues

If the script can't connect to your phone:
1. Make sure USB debugging is enabled
2. Try unplugging and reconnecting your phone
3. Accept any USB debugging prompts on your phone

## Advanced: Running as a Service

To run this as a Windows service:
1. Install the service:
   ```
   manage_captcha_service.bat install
   ```
2. Start the service:
   ```
   manage_captcha_service.bat start
   ```

This will allow the CAPTCHA solver to run completely in the background, even without a user logged in.
