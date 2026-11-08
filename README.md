 **Automotive Edge AI: Vision-Based Driver Drowsiness & Cognitive Load Monitor**

A real-time computer vision system built with Python and OpenCV designed for active driver safety monitoring and edge deployment simulation.

** Features**
- **Real-Time Face & Eye Tracking:** Uses OpenCV Haar Cascades (`haarcascade_frontalface_default.xml`, `haarcascade_eye.xml`) to isolate the driver's face and eye regions.
- **Drowsiness Alert Logic:** Monitors closed-eye duration and triggers visual safety warnings when fatigue thresholds are exceeded.
- **Live Performance Metrics:** Integrated real-time FPS counter optimized for edge-device tracking.
- **Windows DirectShow Integration (`CAP_DSHOW`):** Resolves camera indexing delays and conflicts for stable execution.

** Tech Stack**
- **Language:** Python 3.15
- **Libraries:** OpenCV (`cv2`), NumPy, Urllib

** Quick Start**
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/automotive_driver_monitor.git](https://github.com/YOUR_USERNAME/automotive_driver_monitor.git)
   cd automotive_driver_monitor
