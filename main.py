from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sshLib
import uvicorn

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
  global sshObj
  responce = {}
  responce['operation'] = 'startConnection'
  sshObj = sshLib.SSHController(ip, user, password)
  if sshObj.startConection() == 1:
    responce['msg'] = "Error on connection"
    return responce
  
  sshObj.sendCommand("enable\n")
  sshObj.sendCommand("pass\n")
  sshObj.sendCommand("terminal lengt 0\n")
  responce['msg'] = "none"
  return responce

@app.post("/sendCommand")
def sendCommand(commad: str):
  #commad = commad.replace('-', ' ')
  commad = commad+'\n'
  responce = {}
  print(commad)
  responce['operation'] = 'sendCommand'
  responce['msg'] = sshObj.sendCommand(commad, 4)
  return responce

@app.get("/endConnection")
def endConnection():
  sshObj.endConnection()


if __name__ == '__main__':
    uvicorn.run(app, host="192.168.0.137", port=8000)