from datetime import timedelta
from os import environ
from pathlib import Path

from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

base_settings = (
    "components/common.py",
    "components/database.py",
    "components/cors.py",
    "components/google_drive.py",
    "components/rest.py",
    "components/email.py",
    "components/jwt.py"
)

include(*base_settings)
