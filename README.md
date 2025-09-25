# Coin Detection Project

This Python project detects coins from a camera feed and calculates the total amount.

## Installation

For **Linux / macOS**
   ```
   git clone https://github.com/trevorzimmerman/usd-coin-counter.git
   cd usd-coin-counter
   python3 -m venv coinenv
   source coinenv/bin/activate
   pip install -r requirements.txt
   ```
For **Windows (CMD / PowerShell)**
   ```
   git clone https://github.com/trevorzimmerman/usd-coin-counter.git
   cd usd-coin-counter
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   python -m venv coinenv
   .\coinenv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
   ```
   python main.py
   ```

### Connecting Your Android Phone

To use your Android phone as the camera feed:

1. Download **IP Webcam** from the Google Play Store.
2. Ensure the phone and computer are on the **same WiFi network**.
3. Open the app, go to **Video Preferences → Video Orientation**, and set to **Portrait**.
4. Go back to the main page and click **Start server**.
5. Enter the **IPv4 URL** displayed on the phone in the script input, e.g.:
    ```
    http://192.168.1.151:8080
    ```
6. This script was tested on a phone with **1920×1080 resolution**. Other resolutions may cause scaling issues with annotations.

## Output

All processed files are saved in the project folder:

- **Pictures:** `usd-coin-counter/pictures`  
- **Videos:** `usd-coin-counter/videos`  

Files are saved here depending on whether you record images or videos.

## Notes

- This project was completed as the final research project for **CS7367: Machine Vision**.
- Uses `inference`, `supervision`, `OpenCV`, `requests`, and `numpy`.
- A virtual environment is recommended to avoid dependency conflicts.

For viewing a demonstration of the coin detection script, including multiple runs and the Roboflow model QR code, please see the project page: [CS 7367 – Machine Vision Project Page](https://trevorzimmerman.github.io/university/cs7367-machine-vision.md)
