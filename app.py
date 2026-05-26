import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from shapely.geometry import Polygon, Point

st.set_page_config(page_title="OmniTrack MVP", layout="wide")
st.title("OmniTrack: Real-Time Spatial Video Analytics Infrastructure")

# 1. Define Guarded Loading Dock (Polygon Geometry)
# Coordinates represent the localized geofence zone on a 640x480 frame
ZONE_COORDINATES = [(100, 150), (400, 150), (500, 400), (50, 400)]
ZONE_POLYGON = Polygon(ZONE_COORDINATES)

# 2. Cache the Model Initialization to save memory
@st.cache_resource
def load_model():
    # Utilizing nano-architecture for high-throughput, low-latency CPU inference
    return YOLO("yolo11n.pt") 

model = load_model()

# 3. Sidebar UI Configuration
st.sidebar.header("Configuration Panel")
uploaded_file = st.sidebar.file_uploader("Upload Logistics/Traffic Video", type=["mp4", "avi", "mov"])
conf_threshold = st.sidebar.slider("Model Confidence Gate", 0.0, 1.0, 0.4)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Analytical Video Feed")
    video_placeholder = st.empty()

with col2:
    st.subheader("Telemetry Log & Metrics")
    metric_placeholder = st.empty()
    log_placeholder = st.empty()

if uploaded_file is not None:
    # Save uploaded file temporarily to pass to OpenCV parser
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.read())
        
    cap = cv2.VideoCapture("temp_input.mp4")
    log_data = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.resize(frame, (640, 480))
        overlay = frame.copy()
        
        # Draw the geofenced Polygon Zone (Translucent Red)
        cv2.fillPoly(overlay, [np.array(ZONE_COORDINATES, dtype=np.int32)], (0, 0, 255))
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        cv2.polylines(frame, [np.array(ZONE_COORDINATES, dtype=np.int32)], True, (0, 0, 255), 2)
        
        # Execute Tracking Framework (Filters for people, cars, and trucks)
        results = model.track(frame, persist=True, conf=conf_threshold, classes=[0, 2, 7], verbose=False)
        
        inside_zone_count = 0
        active_ids = []
        
        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            class_indices = results[0].boxes.cls.cpu().numpy().astype(int)
            
            for box, track_id, cls_idx in zip(boxes, track_ids, class_indices):
                x1, y1, x2, y2 = box
                label = model.names[cls_idx]
                active_ids.append(track_id)
                
                # Calculate Base Midpoint Vector of the tracked object bounding box
                base_midpoint = Point((x1 + x2) / 2, y2)
                
                # Mathematical Geometry Intersection Check using Shapely
                is_inside = ZONE_POLYGON.contains(base_midpoint)
                
                # Set Visual Cues Based on Zone Membership
                color = (0, 255, 0) # Green for safe
                if is_inside:
                    color = (0, 0, 255) # Red for zone breach
                    inside_zone_count += 1
                    log_entry = f"ID {track_id} ({label}) breached Guarded Loading Dock."
                    if log_entry not in log_data[-5:]:
                        log_data.append(log_entry)
                
                # Render tracking identities and bounding boxes onto frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, f"ID {track_id}: {label}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Update Web UI Interface Elements Fluidly
        video_placeholder.image(frame, channels="BGR", use_container_width=True)
        
        metric_placeholder.markdown(f"""
        ### Active Metrics
        * **Total Objects Tracked:** {len(active_ids)}
        * **Objects inside Geofenced Zone:** {inside_zone_count}
        """)
        
        log_placeholder.text("\n".join(log_data[-10:]))
        
    cap.release()
else:
    st.info("Please upload a sample mp4 video file in the sidebar to run the system engine simulation.")