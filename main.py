from fastapi import FastAPI
import os

app = FastAPI()

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
  return "<h1>Hola"+response+"</h1>"