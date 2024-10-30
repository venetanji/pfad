import asyncio
from websockets.server import serve

async def respond(websocket):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"You sent: {message}")

async def constant_ping(websocket):
    while True:
        await asyncio.sleep(5)
        print("Sending ping...")
        await websocket.send("Ping!")

async def echo(websocket):
    tasks = [respond(websocket), constant_ping(websocket)]
    await asyncio.gather(*tasks)
    
async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())