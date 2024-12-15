import os
import uvicorn
import websockets
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from calculate import calculate


app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Принимаем подключение
    try:
        while True:
            sentMessage = await websocket.receive_json()  # Ожидаем сообщение от клиента
            print(f"Получено сообщение: {sentMessage}")
            calculate(sentMessage)
            # Отправляем ответ клиенту
            await websocket.send_json(
                {'xy': 'orbit/xy_orbit_animation.gif',
                 'xz': 'orbit/xz_orbit_animation.gif',
                 'yz': 'orbit/yz_orbit_animation.gif'})

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
