import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"You sent: {message}")

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())