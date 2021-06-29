import sqlite3, os
from hasher import Hasher

class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        con = sqlite3.connect(dbname)
        cur = con.cursor()

        Q1 = """CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), email VARCHAR(50), password VARCHAR(50))"""

        Q2 = """CREATE TABLE LoggedInDeveices (id INTEGER PRIMARY KEY AUTOINCREMENT,ipadress TEXT VARCHAR(50) ,relation int ,FOREIGN KEY(relation) REFERENCES Users(id))"""

        Q3 = "CREATE TABLE Passwords (id INTEGER PRIMARY KEY AUTOINCREMENT, password VARCHAR(50), email VARCHAR(50), url VARCHAR(75), relation int, FOREIGN KEY(relation) REFERENCES Users(id)) "        
        #cur.execute(Q3)

        #cur.execute(Q2)

        if os.path.isfile(dbname):
            print("Passing")
            pass
        else:
            pass

            

    
    def register(self, name, email, password):
            hashed_password = Hasher.hash_password(password)
            with sqlite3.connect(self.dbname) as con:
                cur = con.cursor()
                Q1 = "SELECT * FROM Users WHERE (name=? OR email=?)"
                cur.execute(Q1, (name, email))
                result = cur.fetchall()

                if (len(result))==0:
                    sql = "INSERT INTO Users (name, email, password) VALUES (?, ?, ?)"

                    cur.execute(sql, (name, email, hashed_password))
                else:
                    print("Email and/or name already taken")

    def login(self,email,password, ip_address):
            with sqlite3.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users WHERE email=?", (email,))
                row = cur.fetchone()
                hashed_password = row[3]

                found_match = Hasher.verify(password, hashed_password)

                if row[2] == email:
                    if found_match:
                        print("Logged in successfuly")
                        Q1 = "SELECT * FROM LoggedInDeveices WHERE (ipadress=? AND relation=?)"
                        
                        cur.execute(Q1, (ip_address, row[1]))

                        result = cur.fetchall()
                        # print (result)
                        if  len(result)==0:
                            cur.execute("INSERT INTO LoggedInDeveices (ipadress, relation) VALUES (?, ?)", (ip_address, row[1]))
                        else:
                            print("You are already logged in")
                        
                    else:
                        print("password is incorrent")
                else:
                    print("The email is incorrect")
                print (row)
                

        
    def logout(self, ip_address):
        with sqlite3.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM LoggedInDeveices WHERE ipadress=?" ,(ip_address,))
            print("Logged out")

    def add(self, password, email, url_address, ip_address):
            with sqlite3.connect(self.dbname) as con:
                cur = con.cursor()
                Q1 = "SELECT * FROM LoggedInDeveices WHERE ipadress=?"
                cur.execute(Q1, (ip_address,))
                row = cur.fetchall()
                print (row[1])

                
                Q2 = "SELECT * FROM Passwords WHERE (email=? and url=?)"
                cur.execute(Q2, (email, url_address))
                result = cur.fetchall()

                if len(result)==0:
                    print("Adding new password to table")

                    sql = "INSERT INTO Passwords (password, email, url, relation) VALUES (?, ?, ?, ?)"
                    #cur.execute(sql, (password, email, url_address, row[2]))
                else:
                    print("Password already exists in table")



    def remove(self, url, login, password):
        return 'lol'

    def edit(self, old_value, new_value):
        return 'lol'
