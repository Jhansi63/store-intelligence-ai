# DESIGN.md

# Store Intelligence AI - Design Document

## Overview

Store Intelligence AI is an AI-powered retail analytics platform that analyzes CCTV footage to monitor customer movement, occupancy, dwell time, and store activity. The system provides actionable insights through an interactive dashboard.

## System Architecture

The solution consists of four major components:

1. Video Processing Layer

   * Reads CCTV footage.
   * Extracts frames for analysis.

2. Detection & Tracking Layer

   * Uses YOLOv8 for person detection.
   * Tracks individuals across frames.
   * Filters duplicate detections.

3. Analytics Layer

   * Calculates footfall.
   * Tracks customer movement.
   * Measures dwell time.
   * Generates store metrics.

4. Dashboard Layer

   * Displays KPIs and analytics.
   * Visualizes trends and store performance.
   * Supports business decision making.

## Data Flow

CCTV Video → YOLOv8 Detection → Person Tracking → Event Generation → SQLite Storage → Dashboard Analytics

## Edge Case Handling

### Staff Exclusion

The system is designed to support staff filtering by maintaining separate tracking identities and excluding known staff members from customer analytics.

### Re-Entry Handling

If a customer exits and re-enters the store, a new event sequence is generated while maintaining accurate footfall calculations.

### Occlusions

Temporary detection losses are handled through object tracking to reduce duplicate counting.

### Crowded Scenes

Tracking IDs help maintain customer consistency in high-density environments.

## AI-Assisted Decisions

AI tools were used during development to:

* Generate initial code structures.
* Assist in debugging and troubleshooting.
* Improve dashboard design.
* Draft project documentation.
* Suggest architecture improvements.
* Review implementation approaches.

All generated outputs were reviewed, modified, tested, and validated before integration into the final solution.

## Design Trade-Offs

* YOLOv8n was selected for faster inference over larger models.
* SQLite was selected for simplicity and lightweight deployment.
* Streamlit was used to accelerate dashboard development.
* Modular architecture improves maintainability and scalability.

## Future Improvements

* Real-time multi-camera support.
* Advanced customer behavior analytics.
* Staff identification using face recognition.
* Cloud deployment with distributed processing.
