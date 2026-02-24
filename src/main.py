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
   
   def add_password(self):
      print("test1234")


class UserSession:

    def __init__(self):
        self.subfunctions = functions()
        self.dir = Path("profile")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.username = self.load_user()
        self.options = {
        "Make Profile": "create",
        "Remove Profile": "delete",
        "Exit": "exit"
       }
        self.menu_options = {
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
               self.load_user(choice=choice)
               self.main_menu(choice=choice)
               return True
              else:
               print(style.bold_style(color.rgb_text(255, 0, 0,  " Invalid Password. ")))
               return False
        
        except KeyboardInterrupt: 
           exit()    

    def load_user(self, choice=""): # This method checks if the username.json file exists. If it does, it reads the file and loads the username from it. If the file does not exist, it prompts the user to enter a username, validates that it's not empty, and then saves it to username.json for future use. The method returns the username, which is stored in the instance variable self.username.
      if not choice:
         self.username = "Unknown"
         return self.username
      
      filepath = self.dir / choice

      if filepath.exists() and filepath.is_file():
         try:
               with open(filepath, "r") as file:
                  data = json.load(file)
                  self.username = data.get("username", "User")
                  print(f"Loaded user from: {filepath}")
                  self.main_menu()
         except (json.JSONDecodeError, PermissionError) as e:
            print(f"Error loading profile: {e}")
            self.username = "User"
      else:
        self.username = "Guest"  

      return self.username and exit()
          

    def main_menu_options(self):
       return(
       [key for key, value in self.menu_options.items()]
       )
    
    def main_menu(self, choice=""):
      print(f"{self.username}")
      print("---- ----- Menu ----- ----")
      options = self.main_menu_options()
      for key, value in enumerate(options, start=1):
          print(f"{key}. {value}")
      print("---- ----- Menu ----- ----")
      try:
         while True:   
          selection = input("Enter number: ")

            # 1. Validate if the input is a number and within range
          if selection.isdigit():
            idx = int(selection) - 1  # Convert "1" to index 0

            if 0 <= idx < len(options):
               selected_text = options[idx]
               print(f"Selected: {selected_text}")

                    # 2. Logic based on what was selected
               if selected_text == "Make Profile":
                  self.subfunctions.add_password()
                  break
               elif selected_text == "Exit":
                exit()
               else:
                print(f"Logic for {selected_text} not implemented yet.")
            else:
              print(style.bold_style(color.rgb_text(255, 0, 0, "Number out of range.")))
         else:
          print(style.bold_style(color.rgb_text(255, 0, 0, "Please enter a valid number.")))

      except KeyboardInterrupt:
        print("\nExiting...")
        exit()
    
    
              


if __name__ == "__main__": 
    usersession = UserSession()
    usersession.login(choice="")
    
