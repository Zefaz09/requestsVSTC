from fastapi import FastAPI
import httpx
from parse import getSchedule
import pymysql


App = FastAPI()
latestContent = None




@App.get("/check")
async def check():
    return "Coming soon..."
