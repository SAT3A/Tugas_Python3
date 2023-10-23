import json
from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, make_response
from http import HTTPStatus
from flask_jwt_extended import jwt_required, create_access_token, jwt_manager

from ..utils import db
from ..models.hospital import Pasien

pasien_ns = Namespace('pasien', description='Namespace for pasien')

pasien_model = pasien_ns.model(
    'Pasien',{
        'id_pasien':fields.Integer(description = "ini adalah id pasien"),
        'nama_pasien':fields.String(description = "ini adalah nama pasien"),
        'alamat':fields.String(description = "ini adalah alamat pasien"),
        'No_Rekam_Medis':fields.Integer(description = "ini adalah no rekam medis"),
    }
)

@pasien_ns.route('/')
class PatientGetPost(Resource):
    @pasien_ns.marshal_list_with(pasien_model)
    @pasien_ns.doc(
        description = "Get all patient"
    )
    def get (self):
        """Get All Data Pasien"""

        try:
            data_pasien = Pasien.query.all()
            print("data berhasil diambil : ", data_pasien)
            return data_pasien, HTTPStatus.OK
        except Exception as e:
            print("Error : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @pasien_ns.expect(pasien_model) 
    @pasien_ns.marshal_with(pasien_model) 
    @pasien_ns.doc(
    description = "Create new data patient" 
    )
    def post(self):
        """Create New Data patient"""
        try:
            new_patient = request.get_json()
            print(f"data{new_patient}")
            
            new_input_patient = Pasien(
                nama_pasien = new_patient.get('nama_pasien'),
                alamat = new_patient.get('alamat'),
                No_Rekam_Medis = new_patient.get('No_Rekam_Medis'),
            
            )
            db.session.add(new_input_patient)
            db.session.commit()
            
            return [], HTTPStatus.CREATED
        
        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@pasien_ns.route('/<int:id_pasien>')
class PatientGetPutDelete(Resource): 
    @pasien_ns.marshal_with(pasien_model) 
    @pasien_ns.doc(
        description = "Get patient by Id",
        params = {
            "id_pasien" : "an Id a given user for method PUT by Id"
        }
            
    )
    
    def get(self, id_pasien):
        '''Get Patient Data by Id unique'''
        #cara get datanya
        try:
            data_by_id = Pasien.query.get_or_404(id_pasien)
            print("data berhasil : ", data_by_id.nama_pasien)
            return data_by_id, HTTPStatus.OK
        
        except Exception as e:
            print("Error Get by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #SEKARANG BUAT YANG PUT / UPDATE
    @pasien_ns.expect(pasien_model)
    @pasien_ns.marshal_with(pasien_model) #ini pake with karena 1 aja, ga semua data
    @pasien_ns.doc(
        description = "Update patient data by Id",
        #jangan lupa parameternya
        params = {
            "id_pasien" : "an Id a given user for method PUT by Id"
        }
    )
    def put(self, id_pasien):
        """ Update Patient Data by Id unique"""
        try:
            patient_to_update = Pasien.query.get_or_404(id_pasien) #Ambil datanya
            #ini ngambil datanya dari database
            
            data = pasien_ns.payload #ambil payloadnya
            #ini ngambil data dari kiriman user / user input
            
            patient_to_update.nama_pasien = data['nama_pasien']
            patient_to_update.alamat = data['alamat']
            patient_to_update.No_Rekam_Medis = data['No_Rekam_Medis']
            
            #jangan lupa commit
            
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error Update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #LANJUT KE DELETE
    @pasien_ns.marshal_with(pasien_model) #ini pake with karena 1 aja, ga semua data
    @pasien_ns.doc(
        description = "Delete Patient Data by Id",
        #jangan lupa parameternya
        params = {
            "id_pasien" : "an Id a given user for method PUT by Id"
        }
    )
    def delete(self, id_pasien):
        """ Delete Patient Data by Id unique"""
        
        #caranya mirip2 seperti get 
        try:
                
            patient_to_delete = Pasien.query.get_or_404(id_pasien)
            
            db.session.delete(patient_to_delete)
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error delete by id : ", e)
            return "Data tidak ditemukan", [], HTTPStatus.BAD_REQUEST