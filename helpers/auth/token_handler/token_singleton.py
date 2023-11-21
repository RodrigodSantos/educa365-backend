from .token_creator import TokenCreator

token_creator = TokenCreator(
  token_key='1234',
  exp_time_days=3,
  refresh_time_days=2
)