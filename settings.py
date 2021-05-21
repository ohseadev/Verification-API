import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DBuser = os.getenv('DBuser')
DBpass = os.getenv('DBpass')
DBurl = os.getenv('DBurl')
