from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/")
def page():
    return FileResponse('testingPage.html')
