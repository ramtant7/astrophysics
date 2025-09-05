import os
import uvicorn
import asyncio
import websockets
import hashlib
import random
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from calculate import calculate
from test61 import calculate3d
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

executor = ThreadPoolExecutor()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Принимаем подключение
    try:
        while True:
            sentMessage = await websocket.receive_json()  # Ожидаем сообщение от клиента
            print(f"Получено сообщение: {sentMessage}")

            loop = asyncio.get_event_loop()
            if sentMessage['Type'] == '2D':
                await loop.run_in_executor(executor, calculate, sentMessage)

                # Отправляем ответ клиенту
                await websocket.send_json(
                    {'xy': 'orbit/xy_orbit_animation.gif',
                     'xz': 'orbit/xz_orbit_animation.gif',
                     'yz': 'orbit/yz_orbit_animation.gif',
                     'Type': '2D'})

            elif sentMessage['Type'] == '3D':
                output_filename = await loop.run_in_executor(executor, calculate3d, sentMessage)
                # Отправляем ответ клиенту
                print(output_filename)
                await websocket.send_json(
                    {'xyz3D': output_filename,
                     'Type': '3D'})

            else:
                print('Error Type')
    except websockets.ConnectionClosed:
        print("Соединение закрыто.")

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir,'../static')
app.mount('/',StaticFiles(directory=st_abs_file_path, html=True))


@app.get("/api/calc/{id}")
async def index():
    print(id)
    return FileResponse('/index.html',media_type='text/html')




if __name__ =='__main__':
    uvicorn.run(app, host='0.0.0.0', port=8888)

def hash_sha3_256(password,salt):
    password = 'Pa$$w0r'
    saltpass = salt + password
    dk = hashlib.sha3_256(saltpass.encode())
    return dk

def salt():
    random.seed()
    salt = random.getrandbits(64).to_bytes(8, 'big').hex()
    return salt