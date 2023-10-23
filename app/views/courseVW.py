from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, json
from http import HTTPStatus
from flask_jwt_extended import jwt_required, create_access_token, JWTManager, jwt_manager, get_jwt_identity

from werkzeug.security import generate_password_hash, check_password_hash

from ..utils import db
from ..models.all_table import Users
from ..models.all_table import Course
from ..models.all_table import Enrollment


# authorizations = { #kedua
#     "jsonWebToken":{
#         "type":"apiKey",
#         "in":"header",
#         "name":"Authorization"
#     }
# }

course_ns = Namespace('course', description='Namespace for course') #ketiga

course_model = course_ns.model(
    'Course',{
        'course_id':fields.Integer(description = "ini adalah course id"),
        'course_name':fields.String(description = "ini adalah course name"),
        'price':fields.Integer(description = "ini adalah price"),
        'enrollment_date':fields.DateTime(description = "ini adalah enrollment date")
        
    }
)

@course_ns.route('/')
class CourseGetPost(Resource):

    #method_decorators = [jwt_required()] #pertama

    #@course_ns.doc(security="jsonWebToken")
    @course_ns.marshal_list_with(course_model)
    @course_ns.doc(
        description = "Get all Courses"
    )

    def get (self):
        """Get All Courses"""
        
        try:
            data_course = Course.query.all()
            print("data berhasil diambil : ", data_course)

            return data_course, HTTPStatus.OK
        except Exception as e:
            print("Error : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @course_ns.expect(course_model) 
    @course_ns.marshal_with(course_model) 
    @course_ns.doc(
    description = "Create new Course" 
    )
    def post(self):
        """Create New Course"""
        try:
            new_course = request.get_json()
            print(f"data{new_course}")
            
            new_input_course = Course(
                course_name = new_course.get('course_name'),
                price = new_course.get('price'),
                enrollment_date = new_course.get('enrollment_date')
                
            )
            db.session.add(new_input_course)
            db.session.commit()
            
            return [], HTTPStatus.CREATED
            
        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@course_ns.route('/<int:course_id>')
class CourseGetPutDelete(Resource): 
    @course_ns.marshal_with(course_model) 
    @course_ns.doc(
        description = "Get Course by Id",
        params = {
            "course_id" : "an Id a given Course for method PUT by Id"
        }
            
    )
    
    def get(self, course_id):
        '''Get Course Data by Id unique'''
        try:
            
            data_by_id = Course.query.get_or_404(course_id)
            print("data berhasil : ", data_by_id.course_name)
            return data_by_id, HTTPStatus.OK
        
        except Exception as e:
            print("Error Get by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    
    @course_ns.expect(course_model)
    @course_ns.marshal_with(course_model) 
    @course_ns.doc(
        description = "Update Course by Id",
        params = {
            "course_id" : "an Id a given course for method PUT by Id"
        }
    )
    def put(self, course_id):
        """ Update Course Data by Id unique"""
        try:
            course_to_update = Course.query.get_or_404(course_id) #Ambil datanya
            #ini ngambil datanya dari database
            
            data = course_ns.payload #ambil payloadnya
            #ini ngambil data dari kiriman user / user input
            
            course_to_update.course_name = data['course_name']
            course_to_update.price = data['price']
            course_to_update.enrollment_date = data['enrollment_date']

            
            #jangan lupa commit
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error Update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #LANJUT KE DELETE
    @course_ns.marshal_with(course_model) 
    @course_ns.doc(
        description = "Delete Course by Id",
        params = {
            "course_id" : "an Id a given course for method PUT by Id"
        }
    )
    def delete(self, course_id):
        """ Delete User Data by Id unique"""
        
        #caranya mirip2 seperti get 
        try:
                
            course_to_delete = Course.query.get_or_404(course_id)
            
            db.session.delete(course_to_delete)
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
    
    