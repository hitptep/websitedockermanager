import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(message)

if __name__ == '__main__':
    start_server = websockets.serve(echo, 'localhost', 8795)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
