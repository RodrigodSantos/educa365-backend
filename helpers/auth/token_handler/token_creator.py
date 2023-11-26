from jwt import encode, decode
from datetime import datetime, timedelta
import time
from uuid import UUID

class TokenCreator:
  def __init__(self, token_key: str, exp_time_days: int, refresh_time_days: int):
    self.__TOKEN_KEY = token_key
    self.__EXP_TIME_DAYS = exp_time_days
    self.__REFRESH_TIME_DAYS = refresh_time_days

  def create(self, cargo: str, id: UUID):
    return self.__encode_token(cargo, id)

  def refresh(self, token: str):
    token_information = decode(token, key=self.__TOKEN_KEY, algorithms="HS256")
    token_cargo = token_information["cargo"]
    token_id = token_information["id"]
    exp_time = token_information["exp"]

    if ((exp_time - time.time()) / 86.400) < self.__REFRESH_TIME_DAYS:
      return self.__encode_token(token_cargo, token_id)

    return token

  def __encode_token(self, cargo: str, id: UUID):
      token = encode({
        "exp": datetime.utcnow() + timedelta(days=self.__EXP_TIME_DAYS),
        "cargo": cargo,
        "id": str(id)
      }, key=self.__TOKEN_KEY, algorithm='HS256')

      return token