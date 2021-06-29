from fastapi import  FastAPI, Request
from fastapi.responses import RedirectResponse
from database import Database
from models import UserInfo, LoginInfo, NewPassInfo

app = FastAPI()

db = Database("sql_database.db")
db.__init__(dbname="sql_database.db")

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@app.post("/register")
def register(userInfo: UserInfo):
    db.register(userInfo.name, userInfo.email, userInfo.password)
    return {"register": "me"}

@app.post("/login")
def login(loginInfo: LoginInfo, request:Request):
    client_ip = request.client.host
    db.login(loginInfo.email, loginInfo.password, client_ip)
    return {"hello": client_ip}

@app.post("/logout")
def logout(request: Request):
    client_ip = request.client.host
    db.logout(client_ip)
    return {"logout": client_ip}

@app.post("/add")
def add(newPassInfo: NewPassInfo,request: Request):
    client_ip = request.client.host
    db.add(newPassInfo.password, newPassInfo.email, newPassInfo.url, client_ip)
    return {"add": "me"}

@app.post("/remove")
def remove():
    return {"remove": "me"}

@app.post("/edit")
def edit():
    return {"edit": "me"}