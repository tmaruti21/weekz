import cv2

def show_camera_feed():
    # Create a video capture object, with 0 indicating the default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video stream or file.")
        return

    # Loop continuously to read frames from the camera
    while True:
        # Read a frame: 'ret' is a boolean, 'frame' is the image array
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Display the resulting frame in a window named 'Camera Feed'
        cv2.imshow('Camera Feed', frame)

        # Wait for 1 millisecond for a key press
        # If the 'q' key is pressed, break from the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy all windows when the loop ends
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera_feed()
