# Copyright (c) 2026 Nora Rose
# Licensed under MIT License

import os
import sys
import sys
import json
import glob
import uuid
import hashlib
from pathlib import Path
from stylelibrary import color
from stylelibrary import style

class functions:
    pass


class UserSession:

    def __init__(self):
        self.subfunctions = functions()
        self.dir = Path("profile")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.username = self.load_user(choice="")
        self.options = {
        "Make Profile": "create",
        "Remove Profile": "delete",
        "Exit": "exit"
       }


    def list_profiles_and_options(self):
        return (
           [f.name for f in self.dir.iterdir()],
           [key for key, value in self.options.items()]
        )  
        

    def login(self, choice):
        print("---- User Session Login ----")
        #print(f"Available profiles: {', '.join(self.list_profiles_and_options())}")
        profiles, options = self.list_profiles_and_options()
        for key, value in enumerate(profiles, start=1):
          print(f"{key}. {value}")
        print("---- ----------- ----")
        for key, value in enumerate(options, start=1):
          print(f"{key}. {value}")
        try:
         while True:
            choice = input("--> ")
            if not choice.endswith(".json"):
              choice += ".json"
            if choice in profiles:
              print("---- ----- Verification ----- ----")
              password = input("Password: ")
              with open(f"profile/{choice}", "r") as file:
                   data = json.load(file)
              hash = hashlib.sha256(password.encode()).hexdigest()
              if hash == data.get("password_hash"):
               print(style.bold_style(color.rgb_text(0, 255, 0, " Login Successful! ")))
               self.main_menu()
               return True
              else:
               print(style.bold_style(color.rgb_text(255, 0, 0,  " Invalid Password. ")))
               return False
        
        except KeyboardInterrupt: 
           exit()    

    def load_user(self, choice): # This method checks if the username.json file exists. If it does, it reads the file and loads the username from it. If the file does not exist, it prompts the user to enter a username, validates that it's not empty, and then saves it to username.json for future use. The method returns the username, which is stored in the instance variable self.username.
     if os.path.exists(choice):
       with open(choice, "r") as f:
           data = json.load(f)
           self.username = data.get("username", "User")   

    def main_menu(self):
      print(f"{self.username}")
      print("test")
      input("test")
              


if __name__ == "__main__": 
    usersession = UserSession()
    usersession.login(choice="")
