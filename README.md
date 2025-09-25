# Coin Detection Project

This Python project detects coins from a camera feed and calculates the total amount.

## Installation

1. Clone the repo:
    ```
    git clone https://github.com/trevorzimmerman/usd-coin-counter.git
    cd usd-coin-counter
    ```
2. Create a virtual environment and activate it:
    ```
    python -m venv coinenv
    source coinenv/bin/activate  # On Windows: coinenv\Scripts\activate
    ```
3. Install dependencies:
    ```
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

## Notes

- This project was completed as the final research project for **CS7367: Machine Vision**.
- Uses `inference`, `supervision`, `OpenCV`, `requests`, and `numpy`.
- A virtual environment is recommended to avoid dependency conflicts.
