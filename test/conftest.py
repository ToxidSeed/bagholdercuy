import pytest
from app import app

# Push app context globally for the entire pytest session
ctx = app.app_context()
ctx.push()

def pytest_unconfigure(config):
    ctx.pop()
