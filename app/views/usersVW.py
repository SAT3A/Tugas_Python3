from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, json
from http import HTTPStatus
from flask_jwt_extended import jwt_required, create_access_token, jwt_manager

from ..utils import db
from ..models.all_table import Users
from ..models.all_table import Course
from ..models.all_table import Enrollment

users_ns = Namespace('users', description='Namespace for users')

users_model = users_ns.model(
    'Users',{
        'user_id':fields.Integer(description = "ini adalah user id"),
        'username':fields.String(description = "ini adalah username"),
        'email':fields.String(description = "ini adalah email"),
        'password':fields.String(description = "ini adalah password"),
    }
)

@users_ns.route('/')
class UserGetPost(Resource):
       
    @users_ns.marshal_list_with(users_model)
    @users_ns.doc(
        description = "Get all users"
    )

    def get (self):
        """Get All Data Users"""

        try:
            data_users = Users.query.all()
            print("data berhasil diambil : ", data_users)


            return data_users, HTTPStatus.OK
        except Exception as e:
            print("Error : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @users_ns.expect(users_model) 
    @users_ns.marshal_with(users_model) 
    @users_ns.doc(
    description = "Create new user" 
    )
    def post(self):
        """Create New Data User"""
        try:
            new_user = request.get_json()
            print(f"data{new_user}")
            
            new_input_user = Users(
                username = new_user.get('username'),
                email = new_user.get('email'),
                password = new_user.get('password'),
            
            )
            db.session.add(new_input_user)
            db.session.commit()
            
            return [], HTTPStatus.CREATED
            
            
        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@users_ns.route('/<int:user_id>')
class UserGetPutDelete(Resource): 
    @users_ns.marshal_with(users_model) 
    @users_ns.doc(
        description = "Get user by Id",
        params = {
            "user_id" : "an Id a given user for method PUT by Id"
        }
            
    )
    
    def get(self, user_id):
        '''Get User Data by Id unique'''
        
        #cara get datanya
        try:
            data_by_id = Users.query.get_or_404(user_id)
            print("data berhasil : ", data_by_id.username)
            return data_by_id, HTTPStatus.OK
        
        except Exception as e:
            print("Error Get by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #SEKARANG BUAT YANG PUT
    @users_ns.expect(users_model)
    @users_ns.marshal_with(users_model) #ini pake with karena 1 aja, ga semua data
    @users_ns.doc(
        description = "Update user by Id",
        #jangan lupa parameternya
        params = {
            "user_id" : "an Id a given user for method PUT by Id"
        }
    )
    def put(self, user_id):
        """ Update User Data by Id unique"""
        try:
            user_to_update = Users.query.get_or_404(user_id) #Ambil datanya
            #ini ngambil datanya dari database
            
            data = users_ns.payload #ambil payloadnya
            #ini ngambil data dari kiriman user / user input
            
            user_to_update.username = data['username']
            user_to_update.email = data['email']
            user_to_update.password = data['password']
            
            #jangan lupa commit
            
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error Update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #LANJUT KE DELETE
    @users_ns.marshal_with(users_model) #ini pake with karena 1 aja, ga semua data
    @users_ns.doc(
        description = "Delete user by Id",
        #jangan lupa parameternya
        params = {
            "user_id" : "an Id a given user for method PUT by Id"
        }
    )
    def delete(self, user_id):
        """ Delete User Data by Id unique"""
        
        #caranya mirip2 seperti get 
        try:
                
            user_to_delete = Users.query.get_or_404(user_id)
            
            db.session.delete(user_to_delete)
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST