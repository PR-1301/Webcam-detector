# 📹 Webcam Motion Detector & Alert System

A real-time motion detection and surveillance application built with Python, OpenCV, and Streamlit. The system continuously monitors a webcam feed, detects movement, captures snapshots of entering objects, and sends instant email alerts with attachments in background threads.

---

## Key Features

- **Real-Time Motion Detection**: Uses background frame differencing, Gaussian blurring, and contour analysis in OpenCV to detect motion accurately.
- **Automated Email Alerts**: Automatically captures and selects the clearest snapshot during motion and sends an email notification via SMTP (Gmail) upon the subject leaving/settling.
- **Multithreaded Architecture**: Utilizes Python `threading.Thread` so sending emails and file cleanup don't block or stutter the live camera feed.
- **Streamlit Web UI (`project9.py`)**: An alternative web-based dashboard displaying the live camera feed with real-time day and time overlays.
- **Automated Cleanup**: Automatically purges temporary snapshot files after alerts are dispatched.

---

## How It Works

1. **Baseline Capture**: The first captured frame is converted to grayscale and blurred to serve as the reference background.
2. **Delta & Thresholding**: Calculates absolute difference between subsequent frames and the baseline. If pixel difference exceeds the threshold, it is marked as movement.
3. **Contour Filtering**: Filters out micro-movements/noise (minimum contour area of 5000 pixels) and draws a bounding rectangle around the moving object.
4. **Snapshot Selection**: Saves frame snapshots sequentially to an `images/` directory and picks the mid-point image during motion for best clarity.
5. **State Transition & Notification**: Detects when motion transitions from active (`1`) to inactive (`0`) and triggers `send_email` in a background daemon thread.

---

## Project Structure

```text
Webcam-detector/
├── main.py          # Main OpenCV motion detection & email trigger script
├── emailing.py      # Email helper module using smtplib & EmailMessage
├── project9.py      # Streamlit web-based live camera stream with timestamp
├── images/          # Temporary directory for captured frames (auto-created/cleaned)
└── README.md        # Project documentation
```

---

## Getting Started

### 1. Prerequisites

- Python 3.8+
- A working webcam / USB camera
- A Gmail account (with an **App Password** configured if 2-Factor Authentication is enabled)

### 2. Installation

Clone this repository and navigate to the project directory:

```bash
git clone https://github.com/<your-username>/Webcam-detector.git
cd Webcam-detector
```

Create and activate a virtual environment (recommended):

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install opencv-python pillow streamlit
```

Ensure the `images/` folder exists:

```bash
mkdir -p images
```

---

## Configuration

Open [`emailing.py`](file:///run/media/pr/New%20Volume/Webcam-detector/emailing.py) and configure your email credentials:

```python
username = "your_email@gmail.com"
password = "your_16_digit_app_password"  # Use Google App Password (not your primary password)
receiver = "receiver_email@gmail.com"
```

> [!TIP]
> **Generating a Google App Password:**
> 1. Go to your **Google Account** > **Security**.
> 2. Enable **2-Step Verification** (if not already enabled).
> 3. Search for **App passwords**, create a new one (e.g. name it "Webcam Detector"), and paste the 16-character code into `password`.

---

## Usage

### Option 1: Motion Detector & Email Alerts (`main.py`)

Run the core OpenCV detection script:

```bash
python main.py
```

- Two OpenCV windows will appear:
  - **My video (Dilation / Motion Delta)**: Shows thresholded motion contours.
  - **My video (Live Feed)**: Shows live camera feed with green bounding boxes around detected objects.
- Press <kbd>x</kbd> on the keyboard while focusing the video window to stop and quit the application.

### Option 2: Streamlit Live Web Feed (`project9.py`)

Run the web dashboard using Streamlit:

```bash
streamlit run project9.py
```

- Open the displayed local URL (typically `http://localhost:8501`) in your browser.
- Click **Start Camera** to view the live feed with active day-of-week and timestamp overlay.

---

## Customization & Tweaks

- **Sensitivity / Object Size**: Adjust the minimum contour area in [`main.py`](file:///run/media/pr/New%20Volume/Webcam-detector/main.py#L40) (default is `5000`):
  ```python
  if cv.contourArea(contour) < 5000:
      continue
  ```
- **Threshold Sensitivity**: Modify delta threshold sensitivity in [`main.py`](file:///run/media/pr/New%20Volume/Webcam-detector/main.py#L33) (default is `60`).
- **Camera Index**: If you have multiple webcams, change `cv.VideoCapture(0)` to `cv.VideoCapture(1)` or your preferred device index.

---

## License

This project is open-source and available under the [MIT License](LICENSE).
