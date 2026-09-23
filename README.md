# Hand Gesture Volume Control

A real-time computer vision project that allows users to control their computer's system volume using hand gestures.

The project uses **MediaPipe Hand Tracking** to detect hand landmarks and **OpenCV** to process the webcam feed. The distance between the thumb and index finger is used to increase or decrease the system volume.

## Features

* Real-time hand detection using a webcam
* Tracks 21 hand landmarks using MediaPipe
* Detects the thumb and index finger
* Calculates the distance between the two fingers
* Maps finger distance to system volume
* Displays the current volume percentage
* Includes a real-time FPS counter
* Smooth hand landmark movement using interpolation
* Visual hand skeleton and fingertip markers
* Volume bar showing the current volume level
* Uses Pycaw to control Windows system audio

## How It Works

The basic workflow of the project is:

```text
Webcam
   ↓
OpenCV captures video
   ↓
MediaPipe detects hand
   ↓
21 hand landmarks are extracted
   ↓
Thumb + Index Finger positions are identified
   ↓
Distance between fingers is calculated
   ↓
Distance is mapped to volume range
   ↓
Pycaw changes Windows system volume
```

### Gesture Control

The distance between the **thumb tip** and **index finger tip** controls the volume:

* Move fingers closer → Lower volume
* Move fingers farther apart → Higher volume

When the fingers are very close together, a visual indicator appears on the screen.

## Technologies Used

* **Python**
* **OpenCV** — webcam capture and image processing
* **MediaPipe** — hand landmark detection
* **NumPy** — distance-to-volume interpolation
* **Pycaw** — Windows system volume control
* **Math** — calculating the distance between landmarks

## Project Structure

```text
Hand-Gesture-Volume-Control/
│
├── HandTrackingModule.py
├── VolumeHandControl.py
├── README.md
└── .gitignore
```

### `HandTrackingModule.py`

This module contains the custom `handDetector` class.

It is responsible for:

* Initializing MediaPipe Hands
* Detecting hands
* Extracting hand landmarks
* Drawing the hand skeleton
* Smoothing landmark movement
* Counting fingers
* Displaying fingertip markers
* Drawing the hand bounding box

### `VolumeHandControl.py`

This is the main application.

It:

1. Opens the webcam.
2. Detects the hand using `HandTrackingModule`.
3. Gets the thumb and index finger landmarks.
4. Calculates the distance between them.
5. Converts that distance into a volume level.
6. Changes the Windows system volume using Pycaw.
7. Displays the volume bar and FPS.

## Requirements

* Windows operating system
* Python 3.x
* Webcam
* Working microphone/camera permissions are not required for audio input, but webcam access is required.

### Python Libraries

Install the required libraries:

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the Project Folder

```bash
cd Hand-Gesture-Volume-Control
```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

### 4. Run the Project

```bash
python VolumeHandControl.py
```

A webcam window should open and display the detected hand.

## Usage

After starting the program:

1. Show one hand in front of the webcam.
2. Make sure the thumb and index finger are visible.
3. Move the thumb and index finger closer together to decrease the volume.
4. Move them farther apart to increase the volume.
5. The volume percentage is displayed on the screen.
6. Press **Q** to exit the application.

## Volume Mapping

The project maps the distance between the thumb and index finger to the system audio range.

The current distance range is:

```text
120 pixels → Minimum volume
300 pixels → Maximum volume
```

The distance is converted into the Windows audio volume range obtained through Pycaw.

## Visual Interface

The application displays:

* Hand skeleton
* Finger tip markers
* Connection line between thumb and index finger
* Center point between the fingers
* Volume percentage
* Vertical volume bar
* FPS counter
* Visual indicator when the fingers are very close

## Hand Tracking

MediaPipe provides 21 landmarks for each detected hand.

Some of the landmarks used by this project are:

```text
Landmark 0  → Wrist
Landmark 4  → Thumb tip
Landmark 8  → Index finger tip
Landmark 12 → Middle finger tip
Landmark 16 → Ring finger tip
Landmark 20 → Pinky tip
```

The project mainly uses landmarks **4** and **8** for volume control.

## Smoothing

To make the hand tracking more stable, the project applies landmark smoothing.

A smoothing factor is used to gradually move the detected landmark position toward the new position instead of immediately jumping to it.

This helps reduce small movements and makes the hand skeleton appear smoother.

## Important Note

This project uses **Pycaw**, which controls Windows system audio. Therefore, the volume-control functionality is intended for **Windows**.

The hand tracking portion can work independently, but the system-volume control code depends on Windows audio APIs.

## Possible Improvements

Some possible future improvements include:

* Add mute/unmute gesture
* Add media play/pause gestures
* Add next/previous track gestures
* Add brightness control
* Add gesture-based application controls
* Add a graphical user interface
* Improve gesture detection
* Add support for multiple hand gestures
* Add configurable minimum and maximum finger distances
* Improve performance and tracking stability

## Author

**Mehroz Shahid**

Computer Science Student
Interested in AI, Machine Learning, Computer Vision, and AI Engineering.
