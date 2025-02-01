import cv2
import mediapipe as mp
import numpy as np
import socket

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open the webcam
cap = cv2.VideoCapture(0)

# Animation variables
rotation_angle = 0
dot_angle = 0

# Aesthetic color for white circles and other elements
circle_color = (255, 255, 255)  # White color for all circles and elements
rectangle_color = (255, 255, 255)  # White for the rectangle
status_text_color = (0, 0, 0)  # Black text

# Store previous hand position for line trails
previous_landmarks = None
line_trail = []

# Rotation variables for arcs
arc_rotation_angle = 0
arc_radius_values = [60, 80, 100]  # Radii for concentric arcs
arc_thickness = 1  # Thickness of the arc lines

# Set up Wi-Fi communication
ESP32_IP = 'ip address'  # Replace with your ESP32's IP address
ESP32_PORT = 8080         # Replace with your ESP32's listening port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for a mirror-like effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    result = hands.process(rgb_frame)

    # Get frame dimensions
    height, width, _ = frame.shape

    # Text to display in the top-left corner
    status_text = ""
    y_offset = 30  # Starting position for text

    # Initialize finger status array [thumb, index, middle, ring, pinky]
    finger_status_array = [0, 180, 180, 180, 180]  # Default to reverse angle when no hand is detected

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Check the status of each finger

            # Thumb Finger (checking tip and dip)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            thumb_tip_y = int(thumb_tip.y * height)
            thumb_dip_y = int(thumb_dip.y * height)
            if thumb_tip_y > thumb_dip_y:
                finger_status_array[0] = 150  # Thumb is down (reverse angle)
            else:
                finger_status_array[0] = 0  # Thumb is up

            # Index Finger
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
            index_tip_y = int(index_tip.y * height)
            index_dip_y = int(index_dip.y * height)
            if index_tip_y > index_dip_y:
                finger_status_array[1] = 0  # Index is down
            else:
                finger_status_array[1] = 110  # Index is up

            # Middle Finger
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
            middle_tip_y = int(middle_tip.y * height)
            middle_dip_y = int(middle_dip.y * height)
            if middle_tip_y > middle_dip_y:
                finger_status_array[2] = 0  # Middle is down
            else:
                finger_status_array[2] = 180  # Middle is up

            # Ring Finger
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
            ring_tip_y = int(ring_tip.y * height)
            ring_dip_y = int(ring_dip.y * height)
            if ring_tip_y > ring_dip_y:
                finger_status_array[3] = 0  # Ring is down
            else:
                finger_status_array[3] = 150  # Ring is up

            # Pinky Finger
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]
            pinky_tip_y = int(pinky_tip.y * height)
            pinky_dip_y = int(pinky_dip.y * height)
            if pinky_tip_y > pinky_dip_y:
                finger_status_array[4] = 60  # Pinky is down
            else:
                finger_status_array[4] = 120  # Pinky is up

            # Combine all finger statuses into one string for display
            status_text = "\n".join([f"{finger}: {'Up' if (state > 0 if finger != 'Thumb' else state == 0) else 'Down'}" 
                         for finger, state in zip(["Thumb", "Index", "Middle", "Ring", "Pinky"], finger_status_array)])
            print(finger_status_array)
            # Get coordinates of the hand bounding box
            x_min = min([lm.x for lm in hand_landmarks.landmark]) * width
            x_max = max([lm.x for lm in hand_landmarks.landmark]) * width
            y_min = min([lm.y for lm in hand_landmarks.landmark]) * height
            y_max = max([lm.y for lm in hand_landmarks.landmark]) * height

            # Calculate the center of the bounding box
            x_center = int((x_min + x_max) / 2)
            y_center = int((y_min + y_max) / 2)

            # Calculate the radius for the hand outline
            radius = int(max(x_max - x_min, y_max - y_min) / 2)

            # Rotation angle of the outermost elements
            rotation_angle += 3

            # Draw the outer rectangle with data (status text)
            text = f"Hand Status"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
            text_width, text_height = text_size

            cv2.rectangle(frame, 
                          (x_center - 100, y_center + 50), 
                          (x_center + 100 + text_width // 2, y_center + 90), 
                          rectangle_color, 1)  # Thinner line width

            cv2.putText(frame, text, 
                        (x_center - 80, y_center + 75), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, status_text_color, 1)

            # Draw rotating small inner circle dots
            for inner_angle in range(0, 360, 90):
                inner_rad = np.radians(inner_angle + dot_angle)
                dot_x = int(x_center + (radius - 40) * np.cos(inner_rad))
                dot_y = int(y_center + (radius - 40) * np.sin(inner_rad))
                cv2.circle(frame, (dot_x, dot_y), 5, status_text_color, -1)

            # Floating lines (threads) following hand movement
            if previous_landmarks is not None:
                for i in range(len(hand_landmarks.landmark)):
                    current_landmark = hand_landmarks.landmark[i]
                    prev_landmark = previous_landmarks[i]

                    # Convert normalized coordinates to pixel values
                    current_x = int(current_landmark.x * width)
                    current_y = int(current_landmark.y * height)
                    prev_x = int(prev_landmark.x * width)
                    prev_y = int(prev_landmark.y * height)

                    # Draw lines connecting previous position to current position
                    cv2.line(frame, (prev_x, prev_y), (current_x, current_y), circle_color, 1)

            # Store current landmarks for the next frame
            previous_landmarks = hand_landmarks.landmark

            # Draw rotating arcs around the hand (thin white arcs)
            for radius in arc_radius_values:
                arc_start_angle = arc_rotation_angle
                arc_end_angle = arc_start_angle + 180  # Arc spans 180 degrees (half circle)

                # Convert start and end angles to radians
                start_angle_rad = np.radians(arc_start_angle)
                end_angle_rad = np.radians(arc_end_angle)

                # Draw the arc using cv2.ellipse()
                cv2.ellipse(frame, 
                            (x_center, y_center),    # Center of the ellipse (hand center)
                            (radius, radius),        # Semi-major and semi-minor axes (same radius for circle)
                            0,                       # No rotation of the ellipse
                            arc_start_angle,         # Start angle
                            arc_end_angle,           # End angle
                            circle_color,            # White color for the arcs
                            arc_thickness)           # Thickness of the arc

            # Increment the arc rotation angle to rotate the arcs on the next frame
            arc_rotation_angle += 2  # Adjust rotation speed if needed

    # Send the finger status array to ESP32 over Wi-Fi
    try:
        message = ",".join(map(str, finger_status_array))
        sock.sendto(message.encode(), (ESP32_IP, ESP32_PORT))
    except Exception as e:
        print(f"Error sending data: {e}")

    # Display the status text on the frame
    for i, line in enumerate(status_text.split("\n")):
        cv2.putText(frame, line, 
                    (10, y_offset + (i * 30)),  # Stack text with an offset
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, status_text_color, 1)

    # Add the quit message on the top-right corner
    cv2.putText(frame, "Press 'Q' to quit", (width - 180, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_text_color, 1)

    # Show the frame with the hand and the circles/arcs
    cv2.imshow("Hand Tracking with Arcs", frame)

    # Check for exit key (press 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
sock.close()
