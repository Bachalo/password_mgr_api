### API for my first extension
- It's meant to be password manager.
- Im making this api in python with fastapi and sqlite3 libraries.
- Master passwords are hashed using sha256 and salted.
- User can keep track of logged in deveices.
- Thanks to storing users ip we can do all the operations without users username or password. (Need to check for better method)


todo List
 - [DONE] Adding new passwords. 
 - [DONE] Removing passwords.
 - [DONE] Editing passowords.
 - [] Make sure to make this api as secure as possible.
 - [DONE] List users passwords for specified variable.

Warnings:
- Remember to not delete any files it bugs with heroku and it shows different error about buildpacks
