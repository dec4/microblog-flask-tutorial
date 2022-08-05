"""
Create instance of class Flask
"""
from flask import Flask

app = Flask(__name__)

from app import routes  # bottom import as a workaround to circular imports
