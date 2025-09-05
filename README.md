# Real-Time Traffic Light Detection

This project uses OpenCV and Python to detect the state of traffic lights in real-time from a video feed or file. It leverages color segmentation in the HSV color space and includes deployment instructions using Docker and Flask.

## Features

-   Real-time detection of Red, Yellow, and Green traffic lights.
-   Processes video from both webcam and file inputs.
-   Object validation using size and shape constraints.
-   Live visualization with bounding boxes and labels.
-   Deployable as a command-line tool, Docker container, or a web application.

---

## Folder Structure

```
traffic-light-detection/
├── src/                  # Source code
│   ├── detector.py       # Core detection logic and CLI runner
│   └── app.py            # Flask web application
├── templates/
│   └── index.html        # HTML for the web app
├── Dockerfile            # Docker configuration
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

---

## Local Setup and Usage

### 1. Installation

Clone the repository and install the required dependencies.

```bash
git clone <your-repo-url>
cd traffic-light-detection
pip install -r requirements.txt
```

### 2. Command-Line Usage

You can run the detector on a live webcam feed or a video file.

**Using Webcam:**
```bash
python src/detector.py
```

**Using a Video File:**
```bash
python src/detector.py --input data/videos/traffic_day.mp4
```

---

## Deployment

### Docker

See instructions in the Docker section below.

### Web Application (Flask)

To view the live feed in your browser:

1.  Run the Flask application:
    ```bash
    python src/app.py
    ```
2.  Open your web browser and navigate to `http://127.0.0.1:5000`.
