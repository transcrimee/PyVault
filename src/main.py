# Copyright (c) 2026 Nora Rose
# Licensed under MIT License

import os
import sys
import sys
import json
import glob
import uuid
from pathlib import Path

class functions:
    pass


class UserSession:

    def __init__(self):
        self.dir = Path("profile")
        self.dir.mkdir(parents=True, exist_ok=True)
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
        

    def login(self):
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
            input("--> ")
        except KeyboardInterrupt: 
           exit()

     
    

class Client:
      
      def __init__(self):
        self.session = UserSession()
        self.subfunctions = functions()

      def client(self):
        self.session.login()

if __name__ == "__main__": 
    application = Client()
    application.client()
