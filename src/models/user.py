from db import db
from sqlalchemy.orm import validates
import bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @validates('username')
    def validate_username_format(self, key, value):
        if len(value) < 4:
            return {'message': 'invalid username'}
        return value

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    def password_setter(self, password):
        if len(password) < 4:
            raise ValueError('password too short')
        self.password = password
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'user name': self.username,
            'user id': self.id}

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    
    

