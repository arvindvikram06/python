import asyncio
from sensor import sensor_stream
from processor import SensorProcessor

async def main():
    processor = SensorProcessor()

    async for data in sensor_stream():
        result = processor.process(data)

        print(
            f"{data['timestamp']} | Temp: {data['temperature']} | "
            f"Avg: {result['moving_avg']} | "
            f"Z: {result['z_score']} | "
            f"Status: {result['status']}"
        )

asyncio.run(main())