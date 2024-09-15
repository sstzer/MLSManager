import requests
import utils
from pathlib import Path

res = requests.get("https://api.modrinth.com/v2/version").json()
utils.add_record(Path("1.json"),res)