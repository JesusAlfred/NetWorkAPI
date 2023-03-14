from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sshLib

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

#@app.post("/startConnection") temporaly get
@app.get("/startConnection")
def startConnection(ip: str, user: str, password: str):
  responce = {}
  responce['operation'] = 'startConnection'
  sshObj = sshLib.SSHController(ip, user, password)
  if sshObj.startConection() == 1:
    responce['msg'] = "Error on connection"
    return responce
  
  r = sshObj.sendCommand("")
  responce['msg'] = r
  return responce