from split_settings.tools import optional, include
from os import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

base_settings = [
    "components/common.py",
    "components/database.py",
    "components/cors.py",
    "components/cookies.py",
    "components/google_drive.py"
]

include(*base_settings)
