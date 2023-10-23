from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, json
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest

from ..utils import db
from ..models.all_table import Users
from ..models.all_table import Course
from ..models.all_table import Enrollment

enrollment_ns = Namespace('enrollment', description='Namespace for Enrollment')
course_ns = Namespace('course', description='Namespace for course')
users_ns = Namespace('users', description='Namespace for users')

user_model = users_ns.model(
    'Users',{
        'user_id':fields.Integer(description = "ini adalah user id"),
        'username':fields.String(description = "ini adalah username"),
        'email':fields.String(description = "ini adalah email"),
        'password':fields.String(description = "ini adalah password"),
    }
)
course_model = course_ns.model(
    'Course',{
        'course_id':fields.Integer(description = "ini adalah course id"),
        'course_name':fields.String(description = "ini adalah course name"),
        'price':fields.Integer(description = "ini adalah price"),
        'enrollment_date' : fields.DateTime(description = "ini adalah enrollment date")
        
    }
)
enrollment_model = enrollment_ns.model(
    'Enrollment',{
        'enrollment_id':fields.Integer(description = "ini adalah Enrollment id"),
        'user_id':fields.Integer(description = "ini adalah user id"),
        'course_id':fields.Integer(description = "ini adalah course id"),
        
    }
),course_ns.model(
    'Course',{
        'course_id':fields.Integer(description = "ini adalah course id"),
        'course_name':fields.String(description = "ini adalah course name"),
        'price':fields.Integer(description = "ini adalah price"),
        'enrollment_date' : fields.DateTime(description = "ini adalah enrollment date")
        
    }
),users_ns.model(
    'Users',{
        'user_id':fields.Integer(description = "ini adalah user id"),
        'username':fields.String(description = "ini adalah username"),
        'email':fields.String(description = "ini adalah email"),
        'password':fields.String(description = "ini adalah password"),
    }
)


@enrollment_ns.route('/')
class EnrollmentGetPost(Resource):
    @enrollment_ns.marshal_list_with(enrollment_model)
    @course_ns.marshal_list_with(course_model)
    @users_ns.marshal_list_with(user_model)
    @enrollment_ns.doc(
        description = "Get all Enrollments"
    )

    def get (self):
        """Get All Enrollment Data"""
        try:
            # data_user = Users.query.filter_by(user_id = '').first()
            # data_course = Course.query.all()
            # data_enrollment = Enrollment.query.all()
            # all_data = data_user + data_course + data_enrollment
            # all_user = Users.query.all()
            # user = Users.query.get(1)
            # user_course = user.course.all()

            all_data = db.session.query(
                Enrollment.enrollment_id,
                Enrollment.user_id,
                Enrollment.course_id,
                Course.course_name,
                Course.price,
                Course.enrollment_date,
                Users.username
            ).join(Users, Users.user_id == Enrollment.user_id).join(Course, Course.course_id == Enrollment.course_id).all()

            data = []
            for row in all_data:
                enrollment_id, user_id, course_id, course_name, price, enrollment_date, username = row
                data.append({
                    'enrollment_id': enrollment_id,
                    'user_id': user_id,
                    'course_id': course_id,
                    'course_name': course_name,
                    'price': price,
                    'enrollment_date': enrollment_date,
                    'username': username
                })
            
            print("Data berhasil diambil : ", data)

            return data, HTTPStatus.OK
        except Exception as e:
            # br = BadRequest('Data tidak ditemukan')
            # br.data = 
            print("Error : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    # @enrollment_ns.expect(enrollment_model) 
    # @enrollment_ns.marshal_with(enrollment_model) 
    # @enrollment_ns.doc(
    # description = "Create new Enrollment" 
    # )
    # def post(self):
    #     """Create New Enrollment"""
    #     try:
    #         new_enrollment = request.get_json()
    #         print(f"data{new_enrollment}")
            
    #         new_input_enrollment = Enrollment(
    #             course_name = new_enrollment.get('course_name'),
    #             price = new_enrollment.get('price'),
    #             enrollment_date = new_enrollment.get('enrollment_date')
            
    #         )
    #         db.session.add(new_input_enrollment)
    #         db.session.commit()
            
    #         return [], HTTPStatus.CREATED
            
            
    #     except Exception as e:
    #         print("Error Post : ", e)
    #         return [], HTTPStatus.BAD_REQUEST
        

@enrollment_ns.route('/<int:enrollment_id>')
class EnrollmentGetPutDelete(Resource): 
    @enrollment_ns.marshal_list_with(enrollment_model)
    @course_ns.marshal_list_with(course_model)
    @users_ns.marshal_list_with(user_model)
    @enrollment_ns.doc(
        description = "Get enrollment by Id",
        params = {
            "enrollment_id" : "an Id a given enrollment for method PUT by Id",
            "user_id" : "an id a given users for method PUT by Id",
            "course_id" : "an id a given users for method PUT by Id",
        }
            
    )
    
    def get(self, enrollment_id, user_id, course_id):
        '''Get Enrollment Data by Id unique'''
        
        #cara get datanya
        try:
            enrollment_by_id = Enrollment.query.get_or_404(enrollment_id)
            user_by_id = Users.query.get_or_404(user_id)
            course_by_id = Course.query.get_or_404(course_id)

            all_data = enrollment_by_id + course_by_id + user_by_id

            # print("data berhasil : ", all_data.course_name)
            # print("data berhasil : ", all_data.price)
            # print("data berhasil : ", all_data.enrollment_date)

            return all_data,HTTPStatus.OK
        
        except Exception as e:
            print("Error Get by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    # #SEKARANG BUAT YANG PUT
    # @enrollment_ns.expect(enrollment_model)
    # @enrollment_ns.marshal_with(enrollment_model) #ini pake with karena 1 aja, ga semua data
    # @enrollment_ns.doc(
    #     description = "Update enrollment by Id",
    #     #jangan lupa parameternya
    #     params = {
    #         "enrollment_id" : "an Id a given enrollment for method PUT by Id",
    #         "user_id" : "an id a given users for method PUT by Id",
    #         "course_id" : "an id a given users for method PUT by Id",
    #     }
    # )
    # def put(self, enrollment_id, user_by_id, course_by_id):
    #     """ Update Enrollment Data by Id unique"""
    #     try:
    #         enrollment_to_update = Enrollment.query.get_or_404(enrollment_id) #Ambil datanya
    #         #ini ngambil datanya dari database
            
    #         data = enrollment_ns.payload #ambil payloadnya
    #         #ini ngambil data dari kiriman user / user input
            
    #         enrollment_to_update.course_name = data['course_name']
    #         enrollment_to_update.price = data['price']
    #         enrollment_to_update.enrollment_date = data['enrollment_date']
            
    #         #jangan lupa commit
            
    #         db.session.commit()
            
    #         return [], HTTPStatus.OK
            
    #     except Exception as e:
    #         print("Error Update by id : ", e)
    #         return [], HTTPStatus.BAD_REQUEST
        
    #LANJUT KE DELETE
    @enrollment_ns.marshal_with(enrollment_model) #ini pake with karena 1 aja, ga semua data
    @enrollment_ns.doc(
        description = "Delete enrollment by Id",
        #jangan lupa parameternya
        params = {
            "enrollment_id" : "an Id a given enrollment for method PUT by Id"
        }
    )
    def delete(self, enrollment_id):
        """ Delete Enrollment Data by Id unique"""
        
        #caranya mirip2 seperti get 
        try:
                
            enrollment_to_delete = Enrollment.query.get_or_404(enrollment_id)
            
            db.session.delete(enrollment_to_delete)
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST