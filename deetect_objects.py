import cv2
import torch
import pytesseract
import sqlite3
import base64
import numpy as np
from ultralytics import YOLO
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load the pre-trained YOLOv5 model
model = YOLO("yolov5n.pt")  # Using a smaller model for speed

# Connect to SQLite database
conn = sqlite3.connect('store_products.db')
c = conn.cursor()

# Create table for storing product info
c.execute('''CREATE TABLE IF NOT EXISTS products
             (product_id INTEGER PRIMARY KEY,
              product_image BLOB,
              label_text TEXT)''')
conn.commit()


def detect_products(frame):
    results = model(frame)
    detections = []

    for result in results:
        for bbox in result.boxes:
            x1, y1, x2, y2 = map(int, bbox.xyxy[0])
            confidence = float(bbox.conf[0])
            label = int(bbox.cls[0])
            detections.append((x1, y1, x2, y2, confidence, label))

    return detections


def extract_text_from_label(frame, bbox):
    x1, y1, x2, y2, _, _ = bbox
    label_region = frame[y1:y2, x1:x2]
    text = pytesseract.image_to_string(label_region)
    return text


def associate_product_with_label(product_bbox, label_bboxes):
    product_center = (
        (product_bbox[0] + product_bbox[2]) // 2,
        (product_bbox[1] + product_bbox[3]) // 2
    )
    min_distance = float('inf')
    associated_label = None

    for label_bbox in label_bboxes:
        label_center = (
            (label_bbox[0] + label_bbox[2]) // 2,
            (label_bbox[1] + label_bbox[3]) // 2
        )
        distance = np.linalg.norm(
            np.array(product_center) - np.array(label_center)
        )

        if distance < min_distance:
            min_distance = distance
            associated_label = label_bbox

    return associated_label


def store_in_database(frame, product_bbox, label_text):
    product_image = frame[
        product_bbox[1]:product_bbox[3], product_bbox[0]:product_bbox[2]
    ]
    _, buffer = cv2.imencode('.jpg', product_image)
    product_image_binary = base64.b64encode(buffer).decode('utf-8')

    c.execute(
        "INSERT INTO products (product_image, label_text) VALUES (?, ?)", 
        (product_image_binary, label_text)
    )
    conn.commit()


async def process_frame(frame, loop, executor):
    product_detections = await loop.run_in_executor(
        executor, detect_products, frame
    )
    label_detections = await loop.run_in_executor(
        executor, detect_products, frame
    )

    for product_bbox in product_detections:
        associated_label_bbox = await loop.run_in_executor(
            executor, associate_product_with_label, 
            product_bbox, label_detections
        )

        if associated_label_bbox:
            label_text = await loop.run_in_executor(
                executor, extract_text_from_label, 
                frame, associated_label_bbox
            )
            await loop.run_in_executor(
                executor, store_in_database, 
                frame, product_bbox, label_text
            )

            x1, y1, x2, y2, _, _ = product_bbox
            cv2.rectangle(
                frame, (x1, y1), (x2, y2), 
                (0, 255, 0), 2
            )
            cv2.putText(
                frame, label_text, 
                (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 0, 0), 2
            )

    return frame


async def main():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=4)
    cap = cv2.VideoCapture(0)
    frame_skip = 5
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            processed_frame = await process_frame(frame, loop, executor)
            cv2.imshow('YOLOv5 Product Detection with OCR', processed_frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()


if __name__ == "__main__":
    asyncio.run(main())
