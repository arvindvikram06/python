import asyncio
from sensor import sensor_stream

async def main():
    async for data in sensor_stream():
        print(data)

asyncio.run(main())