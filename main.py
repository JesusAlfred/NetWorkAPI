from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/test")
def test():
  print("is working")

@app.get("/ping")
def ping(ip: str):
    print("ping to:", ip)