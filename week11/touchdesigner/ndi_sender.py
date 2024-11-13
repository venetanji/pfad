
import numpy as np
import asyncio
import NDIlib as ndi

def send_frames(output_queue):
    
    ndi.initialize()
    
    send_settings = ndi.SendCreate()
    send_settings.ndi_name = "Python NDI Example"
    ndi_send = ndi.send_create(send_settings)
    video_frame = ndi.VideoFrameV2()         
    video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_RGBA
    img = np.zeros((1080, 1920, 4), dtype=np.uint8)
    video_frame = ndi.VideoFrameV2()
    video_frame.data = img
    
    running = True
    while running:
        if output_queue.qsize() > 1:            
            img[::] = output_queue.get_nowait()
        try:
            ndi.send_send_video_v2(ndi_send, video_frame)

        except Exception as e:
            print("error", e)
            break
        
async def generate_frames(input_queue, output_queue):
    for img in await input_queue.get():
        img = np.random.randint(0, 255, (1080, 1920, 4), dtype=np.uint8)
        output_queue.put_nowait(img)
        await asyncio.sleep(1)

async def read_frames(input_queue):
    while True:
        img = np.zeros((1080, 1920, 4), dtype=np.uint8)
        input_queue.put_nowait(img)
        await asyncio.sleep(1/60)        

async def main():
    global running
    running = False
    output_queue = asyncio.Queue()
    input_queue = asyncio.Queue()

    asyncio.get_running_loop().run_in_executor(None,send_frames, output_queue)
    #send_blocking = asyncio.to_thread(send_frames(output_queue))
    generate_task = asyncio.create_task(generate_frames(input_queue, output_queue))
    read_task = asyncio.create_task(read_frames(input_queue))
    
    
    try:
        await asyncio.gather(
            generate_task,
            read_task
        )
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        running = False

if __name__ == "__main__":
    asyncio.run(main())