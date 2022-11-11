
import re
import os
import asyncio
from socket import socket
import websockets

def watchdog(ports):
    result_ports=[]
    for port in ports:
        server = socket.socket()
        flag = server.connect_ex(('127.0.0.1', int(port)))
        if flag:
            result_ports.append(port)
        return result_ports

async def watchdog(websocket, path):
    ports = await websocket.recv()
    print("success!")
    result_ports=watchdog(ports)
    await websocket.send(result_ports)

start_server = websockets.serve(watchdog, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

