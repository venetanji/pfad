import asyncio
import time
import pygame
from websockets import connect

FPS = 100
width, height = 700, 400

def pygame_event_loop(loop, event_queue):
    while True:
        event = pygame.event.wait()
        event_queue.put_nowait(event)

async def animation(screen):
    black = 0, 0, 0
    current_time = 0
    while True:
        last_time, current_time = current_time, time.time()
        await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick

        # "update logic here"
        screen.fill(black)
        pygame.display.flip()


async def handle_events(event_queue):
    while True:
        event = await event_queue.get()
        await asyncio.sleep(0.1)  # allow other tasks to run
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("space key pressed")
        else:
            print("event", event)
        
    asyncio.get_event_loop().stop()

async def handle_websocket():
    async with connect("ws://localhost:8765") as websocket:
        while True:
            await websocket.send("Hello, world!")
            response = await websocket.recv()
            print(response)
            await asyncio.sleep(1)


def main():
    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()

    pygame.init()
    pygame.display.set_caption("pygame+asyncio")
    screen = pygame.display.set_mode((width, height))

    pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
    animation_task = asyncio.ensure_future(animation(screen))
    event_task = asyncio.ensure_future(handle_events(event_queue))
    websocket_task = asyncio.ensure_future(handle_websocket())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        pygame_task.cancel()
        animation_task.cancel()
        event_task.cancel()
        websocket_task.cancel()

    pygame.quit()


if __name__ == "__main__":
    main()