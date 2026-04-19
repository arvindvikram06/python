from fastapi import FastAPI, WebSocket
import asyncio

from sensor import sensor_stream
from processor import SensorProcessor

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    processor = SensorProcessor()

    async for data in sensor_stream():
        result = processor.process(data)

        response = {
            "timestamp": data["timestamp"],
            "temperature": data["temperature"],
            "moving_avg": result["moving_avg"],
            "z_score": result["z_score"],
            "status": result["status"]
        }

        await websocket.send_json(response)
        await asyncio.sleep(1)