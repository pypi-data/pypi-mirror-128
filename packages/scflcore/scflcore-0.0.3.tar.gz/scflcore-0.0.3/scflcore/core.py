import os
import time
import requests

class CoreManager():
    def __init__(self, name=None, password=None):
        self.corename = name
        self.password = password
        if self.corename is None:
            self.corename = "CoreManagerV1"
        else:
            self.corename = name
            
    def request(self, url=None, json: bool=False):
        if url is not None:
          if json:
            response = requests.get(url)
            return response.json()
          else:
            response = requests.get(url)
            return response
        else:
            response = ""
            return response
        
    def sleep(self, seconds: float=1.0):
        return time.sleep(seconds)
    
    def manage(self, name=None, password=None):
        if self.name == "SScefaLI_dev" and self.password == "dev":
            return "managed"
        else:
            return "No acess"