import subprocess
import time

print("Starting Store Intelligence System...")

# Start FastAPI backend
backend = subprocess.Popen(
    [
        "python",
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload"
    ]
)

time.sleep(5)

# Start detection pipeline
pipeline = subprocess.Popen(
    [
        "python",
        "pipeline/detect.py"
    ]
)

time.sleep(5)

# Start Streamlit dashboard
dashboard = subprocess.Popen(
    [
        "streamlit",
        "run",
        "dashboard/dashboard.py"
    ]
)

print("System Running")
print("Backend: http://127.0.0.1:8000/docs")
print("Dashboard: http://localhost:8501")

backend.wait()
pipeline.wait()
dashboard.wait()