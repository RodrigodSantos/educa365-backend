from flask_restful import Resource, marshal
from helpers.database import db

from model.educandoResponsavel import EducandoResponsavel, educandoResponsaveisFields

class EducandoResponsaveis(Resource):
    def get(self):
        educandoResponsavel = EducandoResponsavel.query.all()
        return marshal(educandoResponsavel, educandoResponsaveisFields), 200
    def delete(self):
        db.session.query(EducandoResponsavel).delete()
        db.session.commit()
        return []
