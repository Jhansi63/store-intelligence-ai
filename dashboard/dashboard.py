import subprocess

import streamlit as st
import sqlite3
import pandas as pd
import tempfile
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Store Intelligence AI",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🛍️ Store Intelligence AI Dashboard")

st.markdown(
    "Upload CCTV footage and analyze store visitors using AI"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Upload CCTV Video")

uploaded_video = st.sidebar.file_uploader(
    "Choose Video",
    type=["mp4", "avi", "mov"]
)

# -----------------------------
# VIDEO DISPLAY
# -----------------------------
if uploaded_video is not None:

    st.sidebar.success("Video Uploaded")

    # Save temp file
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_file.write(uploaded_video.read())

    video_path = temp_file.name

    st.subheader("Uploaded Video")

    st.video(video_path)
    if st.button("Analyze Video"):
        # Clear old events
        conn = sqlite3.connect("store.db")

        cursor = conn.cursor()

        cursor.execute("DELETE FROM events")

        conn.commit()

        conn.close()

        st.success("Old events cleared")

        # Set uploaded video path
        os.environ["VIDEO_PATH"] = video_path

        # Run detection pipeline
        with st.spinner("Running AI Detection..."):
            result = subprocess.run(
                [
                    ".venv/Scripts/python.exe",
                    "pipeline/detect.py",
                    video_path
                ],
                capture_output=True,
                text=True
            )

        st.success("Video Analysis Completed")

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("store.db")

try:

    df = pd.read_sql_query(
        "SELECT * FROM events",
        conn
    )

    # -----------------------------
    # METRICS
    # -----------------------------
    unique_visitors = df["visitor_id"].nunique()

    total_events = len(df)

    purchase_count = len(
        df[df["event_type"] == "PURCHASE"]
    )

    conversion_rate = 0

    if unique_visitors > 0:
        conversion_rate = (
            purchase_count / unique_visitors
        ) * 100

    # -----------------------------
    # TOP METRICS
    # -----------------------------
    st.subheader("Store Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Unique Visitors",
        unique_visitors
    )

    col2.metric(
        "Total Events",
        total_events
    )

    col3.metric(
        "Conversion Rate",
        f"{conversion_rate:.2f}%"
    )

    # -----------------------------
    # CHART
    # -----------------------------
    st.subheader("Event Distribution")

    event_counts = df["event_type"].value_counts()

    st.bar_chart(event_counts)

    # -----------------------------
    # EVENT TABLE
    # -----------------------------
    st.subheader("Live Events")

    st.dataframe(df)

except Exception as e:

    st.warning("No events found yet")

    st.text(str(e))

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.markdown(
    "Built with YOLOv8 + FastAPI + Streamlit"
)