'''revoked_token_model.py'''
from application.app import db

class RevokedTokenModel(db.Model):
    '''class representing rovoked tokens table'''
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    json_token_identifier = db.Column(db.String(120))

    def save(self):
        '''commit and save data from object'''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, json_token_identifier):
        '''check if token is blacklisted'''
        query = cls.query.filter_by(
            json_token_identifier=json_token_identifier).first()
        return bool(query)
