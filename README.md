ShelfSight - Real-time Shelf Stock Detection Using Computer Vision and Machine Learning
ShelfSight is an AI-powered inventory management tool designed to automatically detect low stock or missing items on retail shelves. By utilizing OpenCV, YOLOv5, and Tesseract OCR, ShelfSight enables retailers to monitor inventory in real-time by analyzing video feeds or uploaded footage.

Features:
Object Detection with YOLOv5: Real-time detection of products on shelves to ensure accurate monitoring of stock levels.
Text Extraction with Tesseract OCR: Extract product labels from shelf tags to link detected items with specific products and their positions on the shelf.
Automatic Low Stock Detection: Identifies missing or low-stock items by analyzing the area above shelf labels, helping retailers act before stockouts occur.
Camera Integration: Automatically detects and integrates multiple cameras for real-time shelf monitoring, allowing for seamless tracking across multiple locations.
Video Processing: Allows users to upload videos for analysis, with automatic detection and frame stitching for large shelf sections.
Database Integration: Utilizes SQLite to store detected product data, images, labels, and stock status, allowing for easy retrieval and reporting.
Technical Stack:
Backend: Python with Flask to serve as the API, handle video uploads, and communicate with the computer vision models.
Computer Vision:
OpenCV: For image and video processing, frame extraction, and stitching.
YOLOv5: For real-time object detection of products on the shelves.
Tesseract OCR: For reading and interpreting text on shelf labels.
Frontend: Built with React, allowing users to upload videos, select connected cameras, and view product detection results.
Database: SQLite to store product detection results, including images, labels, and missing stock data.
Key Use Cases:
Retail Inventory Management: Automates shelf monitoring to prevent stockouts by alerting staff when items are missing from the shelf.
Real-Time Camera Monitoring: Supports integration with multiple cameras to provide real-time updates on product availability across various locations.
Video-Based Detection: Analyzes uploaded video footage to detect missing items and stitch frames together for a panoramic view of the shelf.
How It Works:
Camera or Video Input: Users can either upload a video or connect a camera. ShelfSight extracts frames for real-time or batch processing.
Product Detection: YOLOv5 detects objects (products) on the shelves. The system then associates the detected products with the labels extracted using Tesseract OCR.
Stock Analysis: ShelfSight evaluates each detected product and the space above its label to identify missing or low-stock items.
Storage and Reporting: All detected products, images, and stock statuses are stored in an SQLite database for reporting and future analysis.
Getting Started:
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/shelfsight.git
cd shelfsight
Install Dependencies: Install the Python and Node.js dependencies:

bash
Copy code
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
Run the Backend:

bash
Copy code
python app.py
Run the Frontend:

bash
Copy code
cd frontend
npm start
Upload Video or Connect Camera: Use the web UI to upload a video or select a connected camera to begin detection.

Screenshots
(Add screenshots showing detection results, stock analysis, and the UI for camera selection or video upload)

Roadmap:
Multi-camera Synchronization: Improve the system’s ability to synchronize and stitch frames from multiple cameras.
Advanced Low Stock Detection: Implement deeper learning models to better predict low-stock situations before items run out.
Cloud Database Integration: Migrate from SQLite to a cloud-based database for scalable storage across multiple retail stores.
Contributing:
We welcome contributions from the community. Feel free to open issues or submit pull requests to help improve ShelfSight.

License:
This project is licensed under the MIT License.
