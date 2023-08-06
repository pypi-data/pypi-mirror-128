import os
import time
import requests
from flask import *

app = Flask(__name__)

class web():
  def __init__(self, title: str="Hello world!"):
    self.site_title = title
    @app.route("/")
    def main(self):
      return f"""
<!DOCTYPE html> 
<html> 
<head><title>{title}</title></head>  
</html>
"""

  def start(self):
    app.run(host="0.0.0.0", port=8080)