# CHOICES.md

# Technical Choices

## Model Selection

### YOLOv8n

YOLOv8n was selected because:

* Fast inference speed.
* Low computational requirements.
* Suitable for near real-time processing.
* Strong person detection performance.

Alternative models considered:

* YOLOv8s
* YOLOv8m

YOLOv8n provided the best balance between speed and accuracy for the challenge.

## Database Choice

### SQLite

Reasons:

* Lightweight.
* Zero configuration.
* Easy integration with Python.
* Suitable for challenge-scale workloads.

## Dashboard Framework

### Streamlit

Reasons:

* Rapid development.
* Interactive visualizations.
* Easy deployment.
* Minimal frontend complexity.

## Schema Design

Event-based architecture was selected.

Each event contains:

* event_id
* timestamp
* event_type
* person_id
* store_id

Benefits:

* Easy analytics generation.
* Scalable logging.
* Supports future event types.
* Compatible with JSONL format.

## API Architecture

REST-style APIs were chosen because:

* Simplicity.
* Easy frontend integration.
* Standard HTTP operations.
* Maintainable architecture.

## Project Structure

The project follows a modular architecture:

* app/ : Application logic
* pipeline/ : Detection and analytics pipeline
* dashboard/ : Visualization layer

Benefits:

* Separation of concerns.
* Easier maintenance.
* Better scalability.

## Logging Format

JSONL was selected because:

* One event per line.
* Easy streaming and parsing.
* Human readable.
* Efficient storage for event logs.

## Future Enhancements

* Real-time event streaming.
* Cloud-native deployment.
* Multi-store analytics.
* Advanced customer behavior prediction.
