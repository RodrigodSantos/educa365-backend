from helpers.database import db
from flask_restful import fields
blackListFields = {"id": fields.String, "token": fields.String, "exp": fields.DateTime}

class BlackList(db.Model):
  __tablename__ = "tb_blacklist"

  id = db.Column(db.Integer, primary_key=True)
  token = db.Column(db.String, nullable=False)
  exp = db.Column(db.TIMESTAMP, nullable=False)

  def __init__(self, token, exp):
    self.token = token
    self.exp = exp

  def __repr__(self):
    return f'BlackList {self.token}'