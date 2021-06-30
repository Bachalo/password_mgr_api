from fastapi import  FastAPI, Request
from fastapi.responses import RedirectResponse
from database import Database
from models import UserInfo, LoginInfo, NewPassInfo, EditPassInfo

app = FastAPI()

db = Database("sql_database.db")
db.__init__(dbname="sql_database.db")

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@app.post("/register")
def register(userInfo: UserInfo):
    message = db.register(userInfo.name, userInfo.email, userInfo.password)
    return {"Message": message}

@app.post("/login")
def login(loginInfo: LoginInfo, request:Request):
    client_ip = request.client.host
    message = db.login(loginInfo.email, loginInfo.password, client_ip)
    return {"Message": message}

@app.post("/logout")
def logout(request: Request):
    client_ip = request.client.host
    message = db.logout(client_ip)
    return {"Message": message}

@app.post("/add")
def add(newPassInfo: NewPassInfo, request: Request):
    client_ip = request.client.host
    message = db.add(newPassInfo.password, newPassInfo.email, newPassInfo.url_address, client_ip)
    return {"Message": message}

@app.post("/remove")
def remove(newPassInfo: NewPassInfo, request: Request):
    client_ip = request.client.host
    message = db.remove(newPassInfo.password, newPassInfo.email, newPassInfo.url_address, client_ip)
    return {"Message": message}

@app.post("/edit")
def edit(editPassInfo: EditPassInfo, request: Request):
    client_ip = request.client.host
    message = db.edit(editPassInfo.url_address, editPassInfo.email, editPassInfo.password, editPassInfo.valueToChange, editPassInfo.newValue, client_ip)
    return {"Message": message}
