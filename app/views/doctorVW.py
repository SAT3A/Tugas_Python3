import json
from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, make_response
from http import HTTPStatus
from flask_jwt_extended import jwt_required, create_access_token, jwt_manager

from ..utils import db
from ..models.hospital import Dokter

dokter_ns = Namespace('dokter', description='Namespace for dokter')

dokter_model = dokter_ns.model(
    'Dokter',{
        'id_dokter ':fields.Integer(description = "ini adalah id dokter"),
        'nama_dokter':fields.String(description = "ini adalah nama dokter"),
        'spesialisasi':fields.String(description = "ini adalah spesialisasi dokter"),
    }
)

@dokter_ns.route('/')
class DoctorGetPost(Resource):
    @dokter_ns.marshal_list_with(dokter_model)
    @dokter_ns.doc(
        description = "Get all Doctor"
    )
    def get (self):
        """Get All Data Doctor"""

        try:
            data_dokter = Dokter.query.all()
            print("data berhasil diambil : ", data_dokter)
            return data_dokter, HTTPStatus.OK
        except Exception as e:
            print("Error : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @dokter_ns.expect(dokter_model) 
    @dokter_ns.marshal_with(dokter_model) 
    @dokter_ns.doc(
    description = "Create new data Doctor" 
    )
    def post(self):
        """Create New Data Doctor"""
        try:
            new_doctor = request.get_json()
            print(f"data{new_doctor}")
            
            new_input_doctor = Dokter(
                nama_dokter = new_doctor.get('nama_dokter'),
                spesialisasi = new_doctor.get('spesialisasi'),
            )
            db.session.add(new_input_doctor)
            db.session.commit()
            
            return [], HTTPStatus.CREATED
        
        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@dokter_ns.route('/<int:id_dokter>')
class DoctorGetPutDelete(Resource): 
    @dokter_ns.marshal_with(dokter_model) 
    @dokter_ns.doc(
        description = "Get Doctor by Id",
        params = {
            "id_dokter" : "an Id a given user for method PUT by Id"
        }
            
    )
    
    def get(self, id_dokter):
        '''Get Doctor Data by Id unique'''
        #cara get datanya
        try:
            data_by_id = Dokter.query.get_or_404(id_dokter)
            print("data berhasil : ", data_by_id.nama_dokter)
            return data_by_id, HTTPStatus.OK
        
        except Exception as e:
            print("Error Get by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #SEKARANG BUAT YANG PUT / UPDATE
    @dokter_ns.expect(dokter_model)
    @dokter_ns.marshal_with(dokter_model) #ini pake with karena 1 aja, ga semua data
    @dokter_ns.doc(
        description = "Update dokter data by Id",
        #jangan lupa parameternya
        params = {
            "id_dokter" : "an Id a given user for method PUT by Id"
        }
    )
    def put(self, id_dokter):
        """ Update Doctor Data by Id unique"""
        try:
            doctor_to_update = Dokter.query.get_or_404(id_dokter) #Ambil datanya
            #ini ngambil datanya dari database
            
            data = dokter_ns.payload #ambil payloadnya
            #ini ngambil data dari kiriman user / user input
            
            doctor_to_update.nama_dokter = data['nama_dokter']
            doctor_to_update.spesialisasi = data['spesialisasi']
            
            #jangan lupa commit
            
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error Update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #LANJUT KE DELETE
    @dokter_ns.marshal_with(dokter_model) #ini pake with karena 1 aja, ga semua data
    @dokter_ns.doc(
        description = "Delete Doctor Data by Id",
        #jangan lupa parameternya
        params = {
            "id_dokter" : "an Id a given user for method PUT by Id"
        }
    )
    def delete(self, id_dokter):
        """ Delete Patient Data by Id unique"""
        
        #caranya mirip2 seperti get 
        try:
                
            patient_to_delete = Dokter.query.get_or_404(id_dokter)
            
            db.session.delete(patient_to_delete)
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error delete by id : ", e)
            return "Data tidak ditemukan", [], HTTPStatus.BAD_REQUEST