# Wireless Hand-Tracking Controlled Robotic Hand

This project integrates a computer vision-based hand-tracking system with an ESP32-controlled robotic hand. The system works wirelessly by using a Python script on a PC to detect hand gestures in real time (via MediaPipe) and send finger status values via UDP over Wi‑Fi to an ESP32. The ESP32 receives the data, drives five servo motors accordingly, and displays a navigable OLED menu interface.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Setup and Configuration](#setup-and-configuration)
  - [Python Hand-Tracking and UDP Transmitter](#python-hand-tracking-and-udp-transmitter)
  - [ESP32 Arduino Code (UDP Receiver & Servo Control)](#esp32-arduino-code-udp-receiver--servo-control)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

This project consists of two main components:

1. **Python Script (Hand Tracking & UDP Transmitter):**  
   - Uses a webcam to capture real‑time video.
   - Utilizes Google’s MediaPipe library to detect hand landmarks.
   - Determines the “up” or “down” status for each finger based on landmark positions.
   - Visualizes dynamic overlays (rotating dots, arcs, trailing lines, status text) on the video feed.
   - Sends the computed finger status as a comma‑separated string via UDP to a specified IP and port.

2. **ESP32 Arduino Sketch (UDP Receiver, Servo Control & OLED Menu):**  
   - Connects to a Wi‑Fi network.
   - Sets up a UDP server to listen on a specific port (default: 8080) for incoming UDP packets.
   - Parses the received data (expected to be five comma‑separated integers) and adjusts five servo motors accordingly.
   - Displays an interactive OLED menu (with options like “Gesture Control”, “Glove Control”, and “Credits”) using push buttons for navigation.
   - Supports returning to the menu anytime via a dedicated back button interrupt.

---

## Features

- **Wireless Communication:**  
  The system operates wirelessly using UDP over Wi‑Fi, enabling remote control of the robotic hand.

- **Real‑Time Hand Tracking:**  
  The Python script leverages MediaPipe to extract hand landmarks and determine finger states with a mirror-like display.

- **Visual Feedback & Aesthetics:**  
  Engaging animations (rotating arcs, dots, and line trails) provide real‑time visual feedback on the PC screen.

- **Servo Motor Control:**  
  The ESP32 controls five servos corresponding to the thumb, index, middle, ring, and pinky fingers based on UDP data.

- **OLED Menu Interface:**  
  A simple interactive menu displayed on an OLED screen lets users switch modes or view credits. Navigation is implemented via four push buttons (up, down, select, back).

---

## Hardware Requirements

- **For the Python Transmitter:**
  - PC or laptop with a webcam.
  - Wi‑Fi network connection.

- **For the ESP32 Receiver:**
  - ESP32 development board.
  - 5 servo motors (for controlling the robotic hand).
  - OLED display (SSD1306 128×64 recommended) with I2C connection.
  - Four push buttons for menu navigation.
  - Breadboard, jumper wires, and appropriate power supply.

---

## Software Requirements

- **Python Environment:**
  - Python 3.7 or higher.
  - Libraries: OpenCV, MediaPipe, NumPy.
    ```bash
    pip install opencv-python mediapipe numpy
    ```
  - UDP communication handled by Python's built‑in `socket` module.

- **Arduino/ESP32 Environment:**
  - Arduino IDE (with ESP32 board package installed).
  - Required libraries:
    - WiFi (comes with ESP32 core)
    - Adafruit_SSD1306 and Adafruit_GFX
    - Wire
    - U8g2lib (if needed for additional OLED functions)
    - ESP32Servo
    - WiFiUdp (built into ESP32 core)

---

## Setup and Configuration

### Python Hand-Tracking and UDP Transmitter

1. **Wi‑Fi & UDP Settings:**
   - Open `python_hand_tracking_udp.py` and update:
     ```python
     ESP32_IP = 'your.esp32.ip.address'  # Replace with your ESP32's IP address
     ESP32_PORT = 8080                   # Replace with your ESP32's listening port
     ```

2. **Install Dependencies:**
   - Run:
     ```bash
     pip install opencv-python mediapipe numpy
     ```

3. **Running the Script:**
   - Execute the script from your terminal:
     ```bash
     python hand recognition.py
     ```
   - A window will display the webcam feed with overlaid animations. Press `'q'` to quit.

### ESP32 Arduino Code (UDP Receiver & Servo Control)

1. **Wi‑Fi Settings:**
   - In `esp_code.ino`, update:
     ```cpp
     const char* ssid = "your_SSID";
     const char* password = "your_PASSWORD";
     // Optionally update target IP if required (if using for specific UDP responses)
     ```

2. **Pin Configuration:**
   - Verify button and servo pin definitions match your wiring:
     - Servos: thumb on pin 32, index on 33, middle on 25, ring on 26, pinky on 27.
     - Buttons: defined on pins 14, 12, 2, and 13 (adjust if needed).

3. **OLED Connection:**
   - Ensure the OLED display’s I2C address (default 0x3C) and wiring (SDA, SCL) are correctly set.

4. **Library Installation:**
   - Install the required libraries via the Arduino Library Manager if not already present.

5. **Upload the Sketch:**
   - In the Arduino IDE, select your ESP32 board and port.
   - Compile and upload `esp_code.ino` to your ESP32.
   - Open the Serial Monitor to check Wi‑Fi connection and UDP server status.

---

## How It Works

1. **Python Side:**
   - Captures and processes the video feed from the webcam.
   - Uses MediaPipe to detect hand landmarks and determines finger statuses.
   - Creates real‑time visualizations (rotating dots, arcs, trails, status text).
   - Sends a comma‑separated string (e.g., "150,110,180,150,60") over UDP to the ESP32.

2. **ESP32 Side:**
   - Connects to Wi‑Fi and sets up a UDP server on the specified port.
   - Displays an interactive OLED menu that lets you choose modes.
   - In "Gesture Control" mode, continuously listens for UDP packets.
   - Parses the received data and writes the angles to the corresponding servo motors.
   - Supports returning to the main menu using a dedicated back button interrupt.

---

## Usage

1. **Start the Python Script:**  
   Run `hand recognition.py` on your PC to begin hand tracking and sending UDP messages.

2. **Run the ESP32 Code:**  
   Once the ESP32 is powered and connected to Wi‑Fi, it will display the main menu on the OLED. Use the push buttons to navigate:
   - Select **Gesture Control** to enter the mode that listens for UDP packets and drives servos.
   - **Glove Control** (coming soon) and **Credits** are additional menu options.

3. **Interacting:**  
   - When in Gesture Control mode, your hand gestures (captured by the Python script) will control the servos on the robotic hand wirelessly.
   - Press the back button at any time to return to the main menu.

---

## Troubleshooting

- **Wi‑Fi/UDP Issues:**
  - Ensure that both the PC and ESP32 are on the same network.
  - Verify the IP address and port settings in both the Python and Arduino code.
  
- **Hand Tracking:**
  - Adjust the MediaPipe confidence thresholds if hand detection is inconsistent.
  - Make sure the webcam has good lighting and a clear background.

- **Servo & OLED:**
  - Check the wiring for servos and the OLED display.
  - Ensure the ESP32’s power supply can handle the servo load.

- **Menu Navigation:**
  - Verify that the push buttons are correctly wired and that their GPIO definitions in the code match your setup.

---

## License

This project is licensed under the MIT License. See the [MIT](LICENSE) file for details.

---

## Acknowledgments

- **MediaPipe:**  
  For the hand-tracking solution.
- **OpenCV:**  
  For real-time video capture and image processing.
- **Youtube reference:** <br>
  https://www.youtube.com/watch?v=Fvg-v8FPcjg
- **Adafruit:**  
  For the SSD1306 and GFX libraries that simplify OLED interfacing.
- **ESP32 Community:**  
  For numerous tutorials and resources that have made wireless robotic control accessible.
