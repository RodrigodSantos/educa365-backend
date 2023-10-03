from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.log import logger

import uuid

from model.educandoResponsavel import EducandoResponsavel, educandoResponsavelFields

class EducandoResponsavelId():
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass
