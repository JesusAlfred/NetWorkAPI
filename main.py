from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sshLib
import uvicorn

class Command(BaseModel):
    command: str

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

@app.get("/updateDevicesList")
def updateDevicesList(initialRouter: str, user: str, password: str, enablep:str = ""):
  tempSSHObj = sshLib.SSHController(initialRouter, user, password)
  sshObj.sendCommand("enable\n")
  sshObj.sendCommand(enablep + "\n")
  sendCommand("terminal len 0\n")
  out = tempSSHObj.sendCommand("show cdp neighbors")
  print(out)

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
def startConnection(ip: str, user: str, password: str, enablep: str):
  global sshObj
  response = {}
  response['operation'] = 'startConnection'
  sshObj = sshLib.SSHController(ip, user, password)
  if sshObj.startConection() == 1:
    response['msg'] = "Error on connection"
    return response
  
  sshObj.sendCommand("enable\n")
  sshObj.sendCommand(enablep + "\n")
  sendCommand("terminal len 0\n")
  response['msg'] = "true"
  return response

@app.post("/sendCommand/")
def sendCommand(c: Command):
  c.command = c.command+'\n'
  response = {}
  print(c.command)
  response['operation'] = 'sendCommand'
  response['msg'] = sshObj.sendCommand(c.command)
  return response

@app.get("/endConnection")
def endConnection():
  sshObj.endConnection()


import netifaces as ni
import winreg as wr
from pprint import pprint

def get_connection_name_from_guid(iface_guids):
  reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
  reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
  try:
    reg_subkey = wr.OpenKey(reg_key, iface_guids + r'\Connection')
    iface_name = wr.QueryValueEx(reg_subkey, 'Name')[0]
    return iface_name
  except FileNotFoundError:
    return '(unknown)'
    pass

def toValidKey(s):
  return s.replace(" ", "")

if __name__ == '__main__':
  import netifaces
  interfaces = []
  print("Select interface to run the API")
  count = 0
  for iface in netifaces.interfaces():
    iface_details = netifaces.ifaddresses(iface)
    if netifaces.AF_INET in iface_details:
      interfaces.append({
        'name': toValidKey(get_connection_name_from_guid(iface)),
        'MAC': iface_details[-1000][0]['addr'],
        'IPv4': iface_details[2][0]['addr'],
        'IPv6': iface_details[23][0]['addr']
      })
      print(str(count) + ') ' + interfaces[count]['name'] + "\tip: " + interfaces[count]['IPv4'])
      count+=1
  selection = -1
  while selection < 0:
    selection = int(input())
    if selection >= count:
      print("select a valid option")
      selection = -1
  host = interfaces[selection]['IPv4']
  uvicorn.run(app, host=host, port=8000)

