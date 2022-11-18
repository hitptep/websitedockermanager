# coding: GB2312
import os,re,sys
import asyncio
import websockets

# execute command, and return the output
def execShell(shell):
    r = os.popen(shell)
    text = r.read()
    r.close()
    return text

def get_port(container):
    shell = "docker port "+container
    result = execShell(shell)
    port=re.findall('(?<=:::).*$', result)
    return port
    
# if __name__=="__main__":
#     print(get_port("portainer_agent"))


async def hello():
    async with websockets.connect('ws://localhost:8768') as websocket:
        port=get_port(sys.argv[1])
        await websocket.send(port)



asyncio.get_event_loop().run_until_complete(hello())

