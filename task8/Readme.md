# Real-time Sensor Monitoring

A real-time monitoring system built using **FastAPI**, **WebSockets**, and **Asynchronous Python** to stream sensor data, calculate statistics, and detect anomalies.

---

## Features

- **Asynchronous Data Streaming**
  - Simulated sensor data generator using `asyncio` and `yield`.
  - Continuous streaming of temperature and vibration metrics.

- **Real-time Processing**
  - Calculates **Moving Average** using a sliding window.
  - Implements **Z-Score** calculation for statistical analysis.

- **Anomaly Detection**
  - Detects statistical outliers (Z-Score > 2).
  - Triggers "CRITICAL" status for high-temperature readings (> 100°F).

- **WebSocket Integration**
  - Low-latency communication between server and clients.
  - Broadcasts JSON payloads containing current readings and processed results.

- **Live Dashboard**
  - Frontend interface to visualize incoming sensor data in real-time.

---

## Tech Stack

- **Python 3**
- **FastAPI**
- **WebSockets**
- **Asyncio**
- **Statistics** (Python standard library)

---

## Project Workflow

1. **Sensor Simulation**: `sensor_stream` generates random temperature and vibration data every second.
2. **WebSocket Connection**: Clients connect to the `/ws` endpoint to receive live updates.
3. **Data Processing**: `SensorProcessor` receives raw data, updates the moving window, and calculates the Z-Score.
4. **Status Evaluation**: The processor flags readings as `NORMAL`, `ANOMALY`, or `CRITICAL`.
5. **Broadcasting**: The FastAPI server sends the enriched data back to the client via WebSockets.

---

## Processing Logic

- **Moving Average**: Uses a `deque` with a fixed `window_size` to maintain recent history.
- **Anomaly Scoring**: `(Current - Average) / StdDev`. A high Z-score indicates a value significantly far from the mean.

---

## Installation

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```
