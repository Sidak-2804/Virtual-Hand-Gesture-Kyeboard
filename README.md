# Virtual Keyboard using Hand Tracking ✋💻

## Overview 🚀
This project implements a **virtual keyboard** using **hand tracking** with OpenCV and Mediapipe. It detects hand gestures through a webcam and simulates keyboard key presses, allowing users to type without a physical keyboard.

## Features ✨
- 🖐️ Real-time hand tracking using **Mediapipe**.
- ⌨️ Virtual keyboard displayed on the screen.
- 👆 Key press detection using index finger movement.
- 🔠 Uppercase and lowercase modes.
- 🔑 Special function keys: Space (`SP`), Clear (`CL`), and Mode Switch (`APR`).
- ⚡ Simulated key presses using **pynput** for real-time typing.

## Installation 🛠️
Ensure you have Python installed, then install the required dependencies:
```bash
pip install opencv-python mediapipe numpy pynput
```

## How It Works 🎥
1. 📸 The webcam captures real-time hand movement.
2. 🖖 **Mediapipe Hands** detects hand landmarks.
3. 📌 The program tracks the index finger tip position.
4. 🏹 When the index finger moves forward over a key, it is "pressed."
5. 📝 The selected key is displayed on the screen and simulated using **pynput**.
6. 🏆 Special functionalities:
   - 🔵 `SP` → Adds a space.
   - 🔴 `CL` → Clears the last typed character.
   - 🔄 `APR` → Switches between uppercase and lowercase.

## Usage ▶️
Run the script using:
```bash
python keyboard.py
```
Press **'q'** to exit the application. ❌

## Future Enhancements 🔮
- 🖐️ Support for multiple hand gestures.
- 🧠 Auto-correct and word suggestions.
- 🎨 Improved UI with better key visualization.
- 🔧 Customizable keyboard layouts.
