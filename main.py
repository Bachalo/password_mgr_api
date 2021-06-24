from fastapi import  FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/", include_in_schema=False)
async def index():
    response = RedirectResponse(url="/docs")
    return response

@app.post("/register")
def register():
    return {"register": "me"}

@app.post("/login")
def login(request:Request):
    client_ip = request.client
    return {"hello": client_ip}

@app.post("/logout")
def logout():
    return {"logout": "me"}

@app.post("/add")
def add():
    return {"add": "me"}

@app.post("/remove")
def remove():
    return {"remove": "me"}

@app.post("/edit")
def edit():
    return {"edit": "me"}