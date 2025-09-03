# 🏋️ Exercise Repetition & Set Counter using MediaPipe

This project uses **MediaPipe Pose** and **OpenCV** to automatically count exercise repetitions (e.g., squats) from a video and group them into **sets**.  
It detects human pose landmarks, applies simple rule-based logic, and overlays the live repetition and set count on the video.

---

## 🎯 Features
- Detects human pose using MediaPipe
- Tracks joint movement (e.g., hip, knee)
- Counts exercise repetitions using rule-based logic
- Groups repetitions into sets (default: 10 reps per set)
- Overlays reps and sets live on video
- Prints final repetition and set count in the console

---

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/exercise-repetition-counter.git
   cd exercise-repetition-counter
