import cv2
import numpy as np

def gather_all_photos():
    """Placeholder function to gather photos from various sources if needed in the future."""
    pass

# Function to extract frames from a video and return a list of frames
def extract_frames(video_path, frame_skip=1):
    """
    Extract frames from a video.
    
    Parameters:
    video_path (str): Path to the video file.
    frame_skip (int): Number of frames to skip between extractions to speed up processing.
    
    Returns:
    frames (list): List of extracted frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []

    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Skip frames to speed up extraction
        if frame_count % frame_skip == 0:
            frames.append(frame)
        frame_count += 1

    cap.release()
    return frames

# Function to stitch frames together horizontally
def stitch_frames_horizontally(frames):
    """
    Stitch frames horizontally, resizing all frames to the smallest height.
    
    Parameters:
    frames (list): List of frames to be stitched.
    
    Returns:
    stitched_image (ndarray): Horizontally stitched image.
    """
    if not frames:
        print("No frames to stitch.")
        return None
    
    # Ensure all frames have the same height
    height = min(frame.shape[0] for frame in frames)
    resized_frames = [cv2.resize(frame, (int(frame.shape[1] * height / frame.shape[0]), height)) for frame in frames]
    
    # Stitch frames together
    stitched_image = cv2.hconcat(resized_frames)
    return stitched_image

# Function to stitch frames together vertically
def stitch_frames_vertically(frames):
    """
    Stitch frames vertically, resizing all frames to the smallest width.
    
    Parameters:
    frames (list): List of frames to be stitched.
    
    Returns:
    stitched_image (ndarray): Vertically stitched image.
    """
    if not frames:
        print("No frames to stitch.")
        return None
    
    # Ensure all frames have the same width
    width = min(frame.shape[1] for frame in frames)
    resized_frames = [cv2.resize(frame, (width, int(frame.shape[0] * width / frame.shape[1]))) for frame in frames]
    
    # Stitch frames together
    stitched_image = cv2.vconcat(resized_frames)
    return stitched_image

# Main script
if __name__ == "__main__":
    video_paths = ['/Users/masonkirby/Desktop/ShelfSight/PXL_20240820_031819843.mp4']  # Replace with your video file path
    output_path = 'stitched_image.jpg'  # Output file for the stitched image

    # Extract frames from the first video
    frames = extract_frames(video_paths[0], frame_skip=10)  # Adjust frame_skip as needed
    
    if not frames:
        print("No frames extracted from video.")
    else:
        # Choose the stitching method (horizontal or vertical)
        stitched_image = stitch_frames_horizontally(frames)

        # Uncomment this to stitch vertically instead:
        # stitched_image = stitch_frames_vertically(frames)

        # Save the stitched image if it's not None
        if stitched_image is not None:
            cv2.imwrite(output_path, stitched_image)
            print(f"Stitched image saved to {output_path}")
        else:
            print("Stitching failed.")
