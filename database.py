import sqlite3, os
from hasher import Hasher
from datetime import datetime


class Database:
    def __init__(self, dbname):
        self.dbname = dbname

        if os.path.isfile(dbname):
            con = sqlite3.connect(dbname)
        else:
            con = sqlite3.connect(dbname)
            cur = con.cursor()

            Q1 = """CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), email VARCHAR(50), password VARCHAR(50))"""
            cur.execute(Q1)

            Q2 = """CREATE TABLE LoggedInDeveices (id INTEGER PRIMARY KEY AUTOINCREMENT,ipadress TEXT VARCHAR(50) ,relation int ,FOREIGN KEY(relation) REFERENCES Users(id))"""
            cur.execute(Q2)

            Q3 = "CREATE TABLE Passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, appName VARCHAR(20), password VARCHAR(50), email VARCHAR(50) COLLATE NOCASE, url VARCHAR(75) COLLATE NOCASE, appTag VARCHAR(20) COLLATE NOCASE, dateAdded VARCHAR(30) COLLATE NOCASE, relation int COLLATE NOCASE, FOREIGN KEY(relation) REFERENCES Users(id)) "        
            cur.execute(Q3)

            
    
    def register(self, name, email, password):
            hashed_password = Hasher.hash_password(password)
            with sqlite3.connect(self.dbname) as con:
                cur = con.cursor()
                Q1 = "SELECT * FROM Users WHERE (name=? OR email=?)"
                cur.execute(Q1, (name, email))
                result = cur.fetchall()

                if len(result)==0:
                    sql = "INSERT INTO Users (name, email, password) VALUES (?, ?, ?)"

                    cur.execute(sql, (name, email, hashed_password))
                    message=""
                else:
                    message="Email and/or name already taken"

                if len(message)==0:
                    return "succesful"
                else:
                    return message



    def login(self,email,password, ip_address):
            with sqlite3.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users WHERE email=?", (email,))
                row = cur.fetchone()
                print(row)

                if row==None:
                    message="User does not exist please register"
                else:
                    hashed_password = row[3]

                    found_match = Hasher.verify(password, hashed_password)

                    if row[2] == email:
                        if found_match:
                            Q1 = "SELECT * FROM LoggedInDeveices WHERE (ipadress=? AND relation=?)"
                            
                            cur.execute(Q1, (ip_address, row[1]))

                            result = cur.fetchall()
                            
                            if  len(result)==0:
                                cur.execute("INSERT INTO LoggedInDeveices (ipadress, relation) VALUES (?, ?)", (ip_address, row[1]))
                                message=""
                            else:
                                message="You are already logged in"
                            
                        else:
                            message="password is incorrent"
                    else:
                        message= "The email is incorrect"
                
                if len(message)==0:
                    return "succesful"
                else:
                    return message
                

        
    def logout(self, ip_address):
        with sqlite3.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM LoggedInDeveices WHERE ipadress=?" ,(ip_address,))
            
            return "succesful"


    def add(self,appName, password, email, url_address, appTag, ip_address):
            with sqlite3.connect(self.dbname) as con:
                cur = con.cursor()
                Q1 = "SELECT * FROM LoggedInDeveices WHERE ipadress=?"
                cur.execute(Q1, (ip_address,))
                row = cur.fetchone()                
                Q2 = "SELECT * FROM Passwords WHERE (email=? and url=?)"
                cur.execute(Q2, (email, url_address))
                result = cur.fetchall()

                if len(result)==0:
                    print("Adding new password to table")

                    sql = "INSERT INTO Passwords (appName, password, email, url, appTag, dateAdded, relation) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    dateAdded = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    cur.execute(sql, (appName, password, email, url_address, appTag, dateAdded, row[2]))
                    message = ""
                else:
                    message= "Password already exists in table"

                if len(message)==0:
                    return "succesful"
                else:
                    return message



    def remove(self, password , email, url_address, ip_address):
        with sqlite3.connect(self.dbname) as con:
            cur = con.cursor()
            row = getUsername(cur, ip_address)
            print(row)
            relation = row[2]

            if len(relation)==0:
                message = "Please log in"
            else:
                Q2 = "SELECT * FROM Passwords WHERE (email=? and url=? and password=? and relation=?)"
                cur.execute(Q2, (email, url_address, password, relation))
                result = cur.fetchall()
                print(result)

                if len(result)==0:
                    message = "Password does not exist in database"
                else:
                    message = ""
                    sql = "DELETE FROM Passwords WHERE (email=? and url=? and password=? and relation=?)"
                    cur.execute(sql, (email, url_address, password, relation))
            
            if len(message)==0:
                return "succesful"
            else:
                return message
    


    def edit(self, id, oldPassInfo, newPassInfo, ip_address):
        with sqlite3.connect(self.dbname) as con:
            cur = con.cursor()
            row = getUsername(cur, ip_address)
            relation = row[2]

            print(oldPassInfo.email)


            if len(relation)==0:
                message = "Please log in"
            else:
                Q1 = "SELECT * FROM Passwords WHERE (email=? and url=? and password=? and relation=?)"
                cur.execute(Q1, (oldPassInfo.email, oldPassInfo.url_address, oldPassInfo.password, relation))
                result = cur.fetchall()

                if len(result)==0:
                    message="Password does not exist in database"
                else:
                    message =""
                    sql = "UPDATE Passwords SET appName=?, password=?, email=?, url=?, appTag=? WHERE (id=? and email=? and password=? AND url=?)"
                    cur.execute(sql, (newPassInfo.appName, newPassInfo.password, newPassInfo.email, newPassInfo.url_address, newPassInfo.appTag, id, oldPassInfo.email, oldPassInfo.password, oldPassInfo.url_address))

        
            if len(message)==0:
                return "succesful"
            else:
                return message
    
    def search(self, variable_name, ip_address):
        with sqlite3.connect(self.dbname) as con:
            cur = con.cursor()
            query = getUsername(cur, ip_address)
            
            if query is None:
                message = "Please log in"
            else:
                searchstr = '%'+variable_name+'%'
                Q1 = "SELECT * FROM Passwords WHERE (id like ? OR appName like ? OR email like ? OR url like ? OR appTag like ? OR password=?)"
                cur.execute(Q1, (searchstr, searchstr, searchstr, searchstr, searchstr, variable_name))
                rows = cur.fetchall()
                data = []
                for row in rows:
                    data.append({
                        "id": row[0],
                        "appNAme": row[1],
                        "password": row[2],
                        "email": row[3],
                        "url_address": row[4],
                        "appTag": row[5],
                        "dateAdded": row[6],
                        "username": row[7]
                    })
                message=""
            
            if len(message)==0:
                return data
            else:
                return message


    def getDetails(self, id, ip_address):
        with sqlite3.connect(self.dbname) as con:
            cur = con.cursor()
            query = getUsername(cur, ip_address)
            
            if query is None:
                message = "Please log in"
            else:
                Q1 = "SELECT * FROM Passwords WHERE (id=?)"
                cur.execute(Q1, (id,))
                row = cur.fetchone()
                if row==None:
                    message = "Password does not exist"
                else:
                    data = {
                        "id": row[0],
                        "appNAme": row[1],
                        "password": row[2],
                        "email": row[3],
                        "url_address": row[4],
                        "appTag": row[5],
                        "dateAdded": row[6],
                        "username": row[7]
                    }
                    message=""
            
            if len(message)==0:
                return data
            else:
                return message

def getUsername(cur, ip_address):
    cur.execute("SELECT * FROM LoggedInDeveices WHERE ipadress=?", (ip_address,))
    return cur.fetchone()
