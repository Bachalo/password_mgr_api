
# Password manager API

Super simple Python API used for my password manager.

 [Check it out](https://passwordmgrapi.herokuapp.com)
  (API is hosted on heroku might take a bit to spin up)

## Built with
I built it with Python using these libraries:
- FastApi
- Sqlite3

## Available endpoints

![Endpoints](https://i.ibb.co/xHqbfnC/001.png)
## Features
- Passwords for newly registered users are hashed and salted using sha256.
- Checks if user is logged in based on IP (This isn't probably the best solution).
