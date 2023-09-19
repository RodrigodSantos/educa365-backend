from flask_restful import fields
from datetime import datetime

class DateFormat(fields.Raw):
    def format(self, value):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value.strftime("%Y-%m-%d")