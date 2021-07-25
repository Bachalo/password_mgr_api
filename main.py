from fastapi import  FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from database import Database
from models import DetailsPassInfo, UserInfo, LoginInfo, NewPassInfo, EditPassInfo, SearchPassInfo

app = FastAPI()

# SHIT TO ALLOW CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = Database("sql_database.db")
db.__init__(dbname="sql_database.db")

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@app.post("/register")
def register(userInfo: UserInfo):
    message = db.register(userInfo.name, userInfo.email, userInfo.password)
    return {"Response": message}

@app.post("/login")
def login(loginInfo: LoginInfo, request:Request):
    client_ip = request.client.host
    message = db.login(loginInfo.email, loginInfo.password, client_ip)
    return {"Response": message}

@app.post("/logout")
def logout(request: Request):
    client_ip = request.client.host
    message = db.logout(client_ip)
    return {"Response": message}

@app.post("/add")
def add(newPassInfo: NewPassInfo, request: Request):
    client_ip = request.client.host
    message = db.add(newPassInfo.appName, newPassInfo.password, newPassInfo.email, newPassInfo.url_address, newPassInfo.appTag, client_ip)
    return {"Response": message}

@app.post("/remove")
def remove(newPassInfo: NewPassInfo, request: Request):
    client_ip = request.client.host
    message = db.remove(newPassInfo.password, newPassInfo.email, newPassInfo.url_address, client_ip)
    return {"Response": message}

@app.post("/edit")
def edit(editPassInfo: EditPassInfo, request: Request):
    client_ip = request.client.host
    message = db.edit(editPassInfo.id , editPassInfo.oldPassInfo, editPassInfo.NewPassInfo, client_ip)
    return {"Response": message}

@app.get("/returnAll")
def search(request: Request):
    client_ip = request.client.host
    message = db.returnAll(client_ip)
    return message
    
@app.post("/getDetails")
def getDetails(detailsPassInfo: DetailsPassInfo, request: Request):
    client_ip = request.client.host
    message = db.getDetails(detailsPassInfo.searchId, client_ip)
    return message