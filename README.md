# Hand-Controlled Mouse Cursor

This Python script uses the Mediapipe library to detect hand gestures from a webcam feed and controls the mouse cursor accordingly. It allows cursor control and clicking on your computer using your hand movements.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI

## Controls
Cursor movement: Move your index finger around to contol the cursor
Mouse Click: Put your thumb close the the palm joint of the index finger to trigger click

## Notes
- Frames per second (fps) is displayed on the webcam screen.
- The cursor movement may be laggy due to the hand detection function in Mediapipe; The Mediapipe Python library is currently only available to run on the CPU on Windows 11 and therefore program runtime may be limited.
- Certain variables are recommended to be adjusted to suit personal preferences.
