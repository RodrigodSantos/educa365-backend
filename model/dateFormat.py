from flask_restful import fields

class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime("%Y-%m-%d")