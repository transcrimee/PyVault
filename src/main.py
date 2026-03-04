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
import logging

logging.basicConfig(filename="application .log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class UserInput:
    def __init__(self):
        self.choice = ""

    def get_choice(self):
        return input("--> ")
  
class UserProfile:
    def __init__(self):
        self.choice = ""
       

    def update_from_input(self, user_input: UserInput):
        self.choice = user_input.choice

class functions:
   def __init__(self, data):
     self.logger = logging.getLogger(f"{__name__}.RepoManager")
     self.dir = Path("profile")
     self.dir.mkdir(parents=True, exist_ok=True)
     self.bank = Path("storage")
     self.bank.mkdir(parents=True, exist_ok=True)
     self.data = data

   def add_password(self, website, email, username, password, choice=""):
    try:
     while True:
       print(choice)
       path = os.path.join(self.dir, f"{choice}")
       if not os.path.exists(path):
           print(f"Error: Profile {path} not found.")
           return
       try:
         while True:
           with open(path, "r") as file:
                data = json.load(file)
           file_name = data.get("file_name", "")
           bank_file_path = os.path.join(self.bank, f"{file_name}.json")
           if os.path.exists(bank_file_path) and file_name:
            try:
              while True:
               with open(bank_file_path, "r") as file: 
                data_list = json.load(file)
               unique_id = str(uuid.uuid4()) # This will create a unique ID for each password
               new_data = [{"id": unique_id, "website": website, "email": email, "username": username, "password": password}] # This is the data set that grabs user data then appends it under it
               data_list.append(new_data) 
               with open(bank_file_path, "w") as f: # Writing the user data in storage - the file name of password storage
                json.dump(data_list, f, indent=4)
               print(f"Thanks, {username}! Your Account Details (ID: {unique_id}) been saved")
               return
            except (json.JSONDecodeError, IOError) as e:
             print(f"Error processing profile file: {e}")
             self.logger.critical(f"Error processing profile file: {type(e).__name__}", exc_info=True)
             break
           else:
            print(f"Error file path not found: {path}")
            self.logger.critical(f"Error could not find the file path: {type(e).__name__}", exc_info=True) 
            break
       except (json.JSONDecodeError, IOError) as e:
         print(f"Error processing profile file: {e}")
         self.logger.critical(f"Error processing profile file: {type(e).__name__}", exc_info=True)
         break
    except KeyboardInterrupt:
      exit()

   def remove_password(self, id_input, choice=""):
    path = os.path.join(self.dir, f"{choice}")
    if not os.path.exists(path):
      print(f"Error: Profile {path} not found.")      
      self.logger.critical(f"Profile was not found: {path}")
      return
    with open(path, "r") as f:
     data = json.load(f)
    file_name = data.get("file_name")
    bank_file_path = os.path.join(self.bank, f"{file_name}.json")
    print(bank_file_path)
    if os.path.exists(bank_file_path):
     with open(bank_file_path, 'r') as f:
      data_list = json.load(f)
      updated_list = [
                inner_list for inner_list in data_list 
                if inner_list[0].get('id') != id_input
            ]
     if len(updated_list) < len(data_list):
      with open(bank_file_path, "w") as f:
        json.dump(updated_list, f, indent=4)
      print(f"Success: Entry with ID {id_input} has been removed.")
      self.logger.info(f"Success with removing {id_input}")
    else:
      print("ID not found.")
      self.logger.warning("User ID could not be found :(")
    

 
   def display_all(self, choice=""):
     profile_path = os.path.join(self.dir, f"{choice}.json")
     if os.path.exists(profile_path):
      with open(profile_path, "r") as f:
       data = json.load(f)
      file_name = data.get("file_name")
      print(file_name)
      bank_file_path = os.path.join(self.bank, f"{file_name}.json")
      print(bank_file_path)
      if os.path.exists(bank_file_path):
       with open(bank_file_path, "r") as f:  
        data = json.load(f)
      keys = ["website", "email", "username", "password"]
      display = [sub[0].get(k) for sub in data for k in keys]
      print(display)
        

   #-----------------------------------#

   def make_profile(self):
    try:
     while True:
      print("Please enter your profile name")
      profile_name = input("Enter: ")
      while profile_name == "": #Simple check to make sure username is not empty because it just be weird 
        print("Please enter your profile name")
        profile_name = input("Enter: ")
      print("Please pick or make a Username")
      username = input("Enter your username: ")
      while username == "": #Simple check to make sure username is not empty because it just be weird   
         print("Please pick or make a Username")
         username = input("Enter your username: ")
      print("Make Password with 4-30 characters one special character is required")
      password = input("Enter your password: ")
      while password == "":
         print("Make Password with 4-30 characters one special character is required")
         password = input("Enter your password: ")
      password_hash = hashlib.sha256(f"{password}".encode()).hexdigest()  
      print("Make Password with 4-30 characters one special character is required")
      file_name = input("Enter your file name for your password: ")
      while password == "": #Simple check to make sure username is not empty because it just be weird 
        print("It seems that your file name for your password was empty please re-enter it!")
        file_name = input("Enter your file name for your password: ")
      with open(self.dir/f"{profile_name}.json", "w") as f: # Creates the username.json and ready to writes the username into it 
       json.dump({"profile_name": profile_name, "username": username, "password_hash": password_hash, "file_name": file_name}, f, indent=4) # Dumps the username into the json file
       empty_data = []
       filename = f"{self.bank}/{file_name}.json"
       with open(filename, 'w') as f_obj:
        json.dump(empty_data, f_obj)           
        print(f"Thanks, {username}! Your username has been saved")
        print(f"Created empty JSON file: {filename}") 
    except KeyboardInterrupt:
      exit()
   def remove_profile(self):
      print("Please enter the profile name you want to remove")
      try:
        while True:
          profile_name = input("Enter: ")
          profile_path = os.path.join(self.dir, f"{profile_name}.json")
          if os.path.exists(profile_path):
           try:
            while True:
             with open(profile_path, "r") as file:
                   data = json.load(file)
             file_name = data.get("file_name", "")
             bank_file_path = os.path.join(self.bank, f"{file_name}.json")
             if os.path.exists(bank_file_path) and file_name:
                     os.remove(bank_file_path)
             os.remove(profile_path)
             print(f"Successfully removed profile: {profile_name}")
             break 
           except (json.JSONDecodeError, IOError) as e:
            print(f"Error processing profile file: {e}")

          else:    
            print(f"Path not found: {profile_name}")
      except KeyboardInterrupt:
        exit()


class UserSession:

    def __init__(self,  input_data: UserInput):
        self.logger = logging.getLogger(f"{__name__}.RepoManager")
        self.input_data = input_data
        self.subfunctions = functions(data="")
        self.dir = Path("profile")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.username = self.load_user()
        self.options = {
        "Make Profile": "create",
        "Remove Profile": "delete",
        "Exit": "exit"
       }
        self.menu_options = {
        "Add Password": "create",
        "Remove Password": "delete",
        "Display ALL!!": "display",
        "Exit": "exit"
       }
        self.choice = ""
        
    
    def update_from_input(self, user_input: UserInput):
        self.choice = user_input.choice
       

    def get_profile_path(self, choice):
        return os.path.join(self.dir, f"{choice}.json")


    def list_profiles_and_options(self):
        return (
           [f.name for f in self.dir.iterdir()],
           [key for key, value in self.options.items()]
        )  
        
    def get_profile_path(self, choice):
        return os.path.join(self.dir, f"{choice}.json")

    def login(self, choice):
        print("---- User Session Login ----")
        #print(f"Available profiles: {', '.join(self.list_profiles_and_options())}")
        profiles, options = self.list_profiles_and_options()
        for i, name  in enumerate(profiles, start=1):
          print(f"{i}. {name}")
        print("---- ----------- ----")
        for i, opt in enumerate(options, start=1):
          print(f"{i}. {opt}")
        try:
         while True:
            input_data = UserInput()
            profile = UserProfile()
            profile.update_from_input(input_data)
            self.choice = input_data.get_choice() 

            if not self.choice.isdigit():
  
              if not self.choice.endswith('.json'):
                self.choice += '.json'

              filename = self.choice if self.choice.endswith('.json') else f"{self.choice}.json"
            
              if filename in profiles:
           
                      print("---- ----- Verification ----- ----")
                      try:
                        while True:
                         password = input("Password: ")
                         with open(f"profile/{filename}", "r") as file:
                          data = json.load(file)
                         hash = hashlib.sha256(password.encode()).hexdigest()
                         if hash == data.get("password_hash"):
                          print(style.bold_style(color.rgb_text(0, 255, 0, " Login Successful! ")))
                          self.logger.info(f"User Login Successful! as {filename}")

                          self.load_user(choice=self.choice)
                          self.main_menu(choice=self.choice)
                          return True
                         else:
                          print(style.bold_style(color.rgb_text(255, 0, 0,  " Invalid Password. ")))
                          self.logger.info(f"User could not Login Successful! as {filename} because of Invalid Password.")
                          return False
                      except TypeError:
                        print("TypeError: most likey because of Invalid Password.")
    
            #---------------------------------------------------------------------------------#
            elif self.choice.isdigit():
              idx = int(self.choice) - 1  # Convert "1" to index 0

              if 0 <= idx < len(options):
                selected_text = options[idx]
                print(f"Selected: {selected_text}")

                    # 2. Logic based on what was selected
                if selected_text == "Make Profile":
                  self.subfunctions.make_profile()
                  break
                elif selected_text == "Remove Profile":
                  self.subfunctions.remove_profile()
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
               if selected_text == "Add Password":
                  website = input("Enter -> Website Name ")
                  email = input("Enter -> Email Used ")
                  username = input("Enter -> Username ")
                  password = input("Enter -> Password ")
                  try:
                   self.subfunctions.add_password(website, email, username, password, self.choice)
                  except TimeoutError:
                    break
               elif selected_text == "Remove Password":
                  id_input = input("Enter -> ID ")
                  self.subfunctions.remove_password(id_input, self.choice)
                  
               elif  selected_text == "Display ALL!":
                   self.subfunctions.display_all(website, email, username, password, self.choice)
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
    input_data = UserInput()  # Create an instance of UserInput
    usersession = UserSession(input_data)  # Pass the instance to UserSession
    usersession.login(input_data)
    subfunctions = functions
    subfunctions.add_password(website="", email="", username="", password="", input_data="")
