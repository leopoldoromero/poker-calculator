import os
from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret

load_dotenv(".env")

APPLICATION_TITLE = "Poker Calculator"
OPENAPI_PATH = "/api/v1/openapi.json"
API_KEY = os.getenv("API_KEY", "*")

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "*"))
