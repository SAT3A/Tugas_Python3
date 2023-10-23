import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..utils import db

class Users(db.Model):
    __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    email = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(50), nullable = False)
    enrollments = db.relationship('Enrollment', backref='users', lazy=True)
    
    def __repr__(self):
        return f'<users{self.username}>'
    
class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('course.course_id'), primary_key=True)
    
    def __repr__(self):
        
        return f'<enrollment{self.course_name}>'    


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer(), primary_key = True)
    course_name = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    enrollment_date = db.Column(db.DateTime, nullable=False)

    #relasi
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

    def __repr__(self):
        return f'<course{self.course_name}>'
    


