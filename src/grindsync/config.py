# config.py
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
LC_SESSION_COOKIE = os.getenv("LC_SESSION_COOKIE")
LC_USERNAME = os.getenv("LC_USERNAME")
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")