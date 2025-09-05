import cv2
import numpy as np
import argparse

# --- 1. Argument Parsing ---
# Set up argument parser to handle command-line inputs
parser = argparse.ArgumentParser(description='Real-time Traffic Light Detection')
parser.add_argument('--input', type=str, help='Path to the video file. If not provided, webcam will be used.')
args = parser.parse_args()

# --- 2. Color Range Definitions in HSV ---
# Define the lower and upper bounds for Red, Yellow, and Green colors in the HSV space.
# These values might need tuning based on lighting conditions and camera specifics.
color_ranges = {
    'red': {
        # Red can wrap around the hue spectrum, so two ranges are often needed.
        'lower1': np.array([0, 120, 70]),
        'upper1': np.array([10, 255, 255]),
        'lower2': np.array([170, 120, 70]),
        'upper2': np.array([180, 255, 255])
    },
    'yellow': {
        'lower': np.array([20, 100, 100]),
        'upper': np.array([30, 255, 255])
    },
    'green': {
        'lower': np.array([40, 70, 70]),
        'upper': np.array([90, 255, 255])
    }
}

def process_frame(frame):
    """
    Processes a single video frame to detect and classify traffic lights.

    Args:
        frame: The input video frame (as a NumPy array).

    Returns:
        The frame with annotations (bounding boxes and labels).
    """
    # --- 3. HSV Conversion ---
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    detected_lights = []

    for color_name, ranges in color_ranges.items():
        # --- 4. Color Segmentation and Masking ---
        if color_name == 'red':
            mask1 = cv2.inRange(hsv_frame, ranges['lower1'], ranges['upper1'])
            mask2 = cv2.inRange(hsv_frame, ranges['lower2'], ranges['upper2'])
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv_frame, ranges['lower'], ranges['upper'])

        # --- Morphological Operations to clean up the mask ---
        # Erode to remove small noise, Dilate to close gaps
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # --- 5. Contour Detection ---
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # --- 6. Validate Detected Regions (Size/Shape Constraints) ---
            area = cv2.contourArea(contour)
            
            # Filter by area to avoid detecting small, irrelevant objects
            if area > 100: 
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by aspect ratio to find circle-like or light-like shapes
                aspect_ratio = float(w) / h
                if 0.5 < aspect_ratio < 1.5:
                    detected_lights.append({
                        'box': (x, y, w, h),
                        'color': color_name,
                        'area': area
                    })

    # --- 7. Classify Traffic Light State & Handle Overlaps ---
    # This simple logic picks the largest detected light of a certain color.
    # More sophisticated logic could be used for complex scenes.
    if detected_lights:
        # Find the single most prominent light based on contour area
        most_prominent_light = max(detected_lights, key=lambda x: x['area'])
        
        # --- 8. Draw Bounding Boxes and Labels ---
        x, y, w, h = most_prominent_light['box']
        color_name = most_prominent_light['color']
        
        # Define drawing color based on detected light state
        draw_color = {
            'red': (0, 0, 255),
            'yellow': (0, 255, 255),
            'green': (0, 255, 0)
        }.get(color_name, (255, 255, 255))
        
        # Draw the bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
        
        # Put the label
        label = f"Traffic Light: {color_name.upper()}"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, draw_color, 2)

    return frame


def main():
    # --- 1. Set up video capture ---
    if args.input:
        cap = cv2.VideoCapture(args.input)
        if not cap.isOpened():
            print(f"Error: Could not open video file {args.input}")
            return
    else:
        cap = cv2.VideoCapture(0) # Use webcam 0
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

    while cap.isOpened():
        # --- 2. Implement frame-by-frame processing pipeline ---
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        processed_frame = process_frame(frame)

        # --- 9. Display live video feed with annotations ---
        cv2.imshow('Traffic Light Detection', processed_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()