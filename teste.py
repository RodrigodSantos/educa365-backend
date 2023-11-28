import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_KEY = os.getenv("TOKEN_KEY")
EXP_TIME_DAYS = os.getenv("EXP_TIME_DAYS")
REFRESH_TIME_DAYS = os.getenv("REFRESH_TIME_DAYS")

print(TOKEN_KEY)
print(EXP_TIME_DAYS)
print(REFRESH_TIME_DAYS)
