import cv2
import threading
import time

# Define a list to store the camera capture objects
cameras = []

# Define a function to capture images from each camera
def capture_image(camera_id, results, index):
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Camera {camera_id} could not be opened.")
        return
    
    # Warm up the camera for better image quality
    time.sleep(0.1)
    
    # Capture a single frame
    ret, frame = cap.read()
    if ret:
        results[index] = frame
        print(f"Image captured from camera {camera_id}.")
    else:
        print(f"Failed to capture image from camera {camera_id}.")
    
    cap.release()

# Main function to capture images from all cameras simultaneously
def capture_from_all_cameras(camera_ids):
    threads = []
    results = [None] * len(camera_ids)  # Placeholder to store the captured frames

    for index, camera_id in enumerate(camera_ids):
        thread = threading.Thread(target=capture_image, args=(camera_id, results, index))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return results

if __name__ == "__main__":
    # Define the camera IDs (adjust according to the number of connected cameras)
    camera_ids = [0, 1, 2, 3]  # Example: 4 cameras connected

    # Capture images from all cameras
    captured_frames = capture_from_all_cameras(camera_ids)

    # Optionally display or save the captured images
    for idx, frame in enumerate(captured_frames):
        if frame is not None:
            # Display the captured image
            cv2.imshow(f"Camera {camera_ids[idx]}", frame)
            
            # Save the captured image
            cv2.imwrite(f"camera_{camera_ids[idx]}.jpg", frame)
    
    # Wait for key press to close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
