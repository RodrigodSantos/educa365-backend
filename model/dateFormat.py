from flask_restful import fields
import datetime

class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime("%Y-%m-%d")