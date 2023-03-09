from fastapi import FastAPI
app = FastAPI()

@app.get("/test")
def test():
  print("is working")