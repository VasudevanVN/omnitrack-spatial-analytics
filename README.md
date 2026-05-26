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
