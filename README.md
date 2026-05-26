# omnitrack-spatial-analytics
# OmniTrack: Real-Time Spatial Video Analytics Infrastructure

OmniTrack is a computer vision and spatial analytics product designed for automated warehouse logistics and industrial safety monitoring. The system ingests video feeds, tracks high-value assets (machinery, forklifts, workers), and calculates real-time geometric geofence violations to prevent workplace hazards.

## 🚀 Live Production Demo
👉 **[CLICK HERE TO ACCESS THE LIVE APP](PASTE_YOUR_STREAMLIT_URL_HERE)** *(Please download the sample clip from the repo or use any mp4 transit video to test)*

## 🛠️ Key Technical Features
* **Multi-Object Tracking (MOT):** Implements temporal tracking IDs leveraging deep learning abstractions to persistently monitor assets under occlusions.
* **Computational Geofencing:** Utilizes `Shapely` polygon structures to run real-time coordinate intersection calculations on object base midpoints.
* **Performance-Optimized Baseline:** Backed by an optimized YOLO nano-architecture to achieve low-latency processing and minimal CPU memory overhead.
* **Live Telemetry Engine:** Translates spatial intersection events into a fluid frontend logging data pipeline.

## 📦 Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/VasudevanVN/omnitrack-spatial-analytics.git](https://github.com/VasudevanVN/omnitrack-spatial-analytics.git)
   cd omnitrack-spatial-analytics
2. **Install Infrastructure Dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Execute the Application Engine:**
   ```bash
   streamlit run app.py
## 🔬 System Architecture Logic

**The application pipeline breaks down into three distinct asynchronous processing steps:**
*1 Object Detection & Tracking: Frames are normalized to $640 \times 480$ pixel matrices and parsed by YOLO to output   temporal bounding box coordinates.
*2 Spatial Coordinate Transform: The engine extracts the base midpoint of the bounding box vector:
                                *$$\text{Point} = \left(\frac{x_1 + x_2}{2}, y_2\right)$$
*3 Geometric Membership Evaluation: A Shapely polygon execution loop evaluates whether the calculated Point vector intersects the static boundary vertices using ray-casting spatial algorithms.
