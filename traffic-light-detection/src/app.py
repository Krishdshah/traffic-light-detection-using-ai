# src/app.py

from flask import Flask, render_template, Response
import cv2
from detector import process_frame # Import the processing function

app = Flask(__name__, template_folder='../templates')

# --- Video Capture ---
# You can switch this to a video file path if you prefer
VIDEO_SOURCE = 0 # 0 for webcam

def generate_frames():
    """Generates frames from the camera to be streamed."""
    camera = cv2.VideoCapture(VIDEO_SOURCE)
    if not camera.isOpened():
        raise RuntimeError("Could not start camera.")

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Process the frame using the imported function
            processed_frame = process_frame(frame)
            
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            
            # Yield the frame in the response format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the 'src' attribute of an img tag."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)