from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
  print("is working")

@app.get("/ping")
def ping(ip: str):
  print("ping to:", ip)
  response = os.system("ping -n 1 -w 1000 " + ip + "> nul")
  if response == 0:
    print("Success")
  else:
    print("Error")
  
  return {"operation": "ping", "status":response}