import asyncio
import websockets
import urllib.parse

USERS = set()

def getargs(path):
    try:
        return path.split("?")[-1]
    except:
        return ""
    
async def register(websocket):
    USERS.add(websocket)
    print(USERS)
    
async def unregister(websocket):
    try:
        USERS.remove(websocket)
        await broadcast("%s saiu!" % websocket.values['name'][0])
    except:
        print("Erro ao remover usuário!")
    
async def broadcast(message):
    if USERS:  
        await asyncio.wait([user.send(message) for user in USERS])

async def serv(websocket, path):
    await register(websocket)
    websocket.values = urllib.parse.parse_qs(getargs(path))
    await broadcast("%s entrou!" % websocket.values['name'][0])
    while(1):
        try:
            message = await websocket.recv()
            await broadcast("%s : %s" %(websocket.values['name'][0],message))
        except:
            await unregister(websocket)
            break

        

start_server = websockets.serve(serv, "localhost", 8993)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()