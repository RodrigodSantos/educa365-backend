from .token_creator import TokenCreator
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_KEY = os.getenv("TOKEN_KEY")
EXP_TIME_DAYS= int(os.getenv("EXP_TIME_DAYS"))
REFRESH_TIME_DAYS= int(os.getenv("REFRESH_TIME_DAYS"))

token_creator = TokenCreator(
  token_key=TOKEN_KEY,
  exp_time_days=EXP_TIME_DAYS,
  refresh_time_days=REFRESH_TIME_DAYS
)
