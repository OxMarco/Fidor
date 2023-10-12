import cv2

def main():
    # Assume these values
    focal_length = 950.4  # In pixel units, replace with your calibrated focal length
    known_width = 230.3  # Actual width of the object in some unit (e.g., cm)

    # Initialize camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Threshold the image (you can use other techniques like Canny edge detection)
        ret, thresh = cv2.threshold(gray, 127, 255, 0)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Proceed if at least one contour was found
        if contours:
            # Find largest contour
            largest_contour = max(contours, key=cv2.contourArea)

            # Get bounding box dimensions for the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Estimate distance
            distance = (known_width * focal_length) / w

            # Draw rectangle around the largest object and display distance
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Display the frame with distance estimation
        cv2.imshow('Distance Estimation', frame)

        # Stop the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
