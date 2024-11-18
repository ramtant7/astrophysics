import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir,'..\static')
app.mount('/',StaticFiles(directory=st_abs_file_path, html=True))


@app.get("/api/calc/{id}")
async def index():
    print(id)
    return FileResponse('/index.html',media_type='text/html')

if __name__ =='__main__':
    uvicorn.run(app, host='0.0.0.0', port=8888)