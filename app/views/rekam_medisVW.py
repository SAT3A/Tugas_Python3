import json
from flask_restx import Namespace, Resource, fields
from flask import request
from flask import jsonify, make_response
from http import HTTPStatus
from flask_jwt_extended import jwt_required, create_access_token, jwt_manager

from ..utils import db
from ..models.hospital import Rekam_Medis
from ..models.hospital import Pasien

rekam_medis_ns = Namespace('rekam_medis', description='Namespace for rekam medis')

rekam_medis_model = rekam_medis_ns.model(
    'Rekam_Medis',{
        'id_rekam_medis':fields.Integer(description = "ini adalah id rekam medis"),
        'id_pasien':fields.Integer(description = "ini adalah id pasien"),
        'diagnosis':fields.String(description = "ini adalah diagnosis"),
        'tgl_periksa':fields.DateTime(description = "ini adalah tgl_periksa"),
    }
)

@rekam_medis_ns.route('/')
class RekamMedisGetPost(Resource):
    @rekam_medis_ns.marshal_list_with(rekam_medis_model)
    @rekam_medis_ns.doc(
        description = "Get all Medical Record"
    )
    def get (self):
        """Get All Medical Record"""

        try:
            data_rekam_medis = Rekam_Medis.query.all()
            data_pasien = Pasien.query.all()
            all_data = data_rekam_medis + data_pasien
            print("data berhasil diambil : ", all_data)
            return all_data, HTTPStatus.OK
        except Exception as e:
            print("Error : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    @rekam_medis_ns.expect(rekam_medis_model) 
    @rekam_medis_ns.marshal_with(rekam_medis_model) 
    @rekam_medis_ns.doc(
    description = "Create new Medical Record" 
    )
    def post(self):
        """Create New Medical Record"""
        try:
            new_medical_record = request.get_json()
            print(f"data{new_medical_record}")
            
            new_input_medical_record = Rekam_Medis(
                diagnosis = new_medical_record.get('diagnosis'),
                tgl_periksa = new_medical_record.get('tgl_periksa'),
                
            )
            db.session.add(new_input_medical_record)
            db.session.commit()
            
            return [], HTTPStatus.CREATED
        
        except Exception as e:
            print("Error Post : ", e)
            return [], HTTPStatus.BAD_REQUEST

@rekam_medis_ns.route('/<int:id_rekam_medis>')
class MedicalRecordGetPutDelete(Resource): 
    @rekam_medis_ns.marshal_with(rekam_medis_model) 
    @rekam_medis_ns.doc(
        description = "Get medical records by Id",
        params = {
            "id_rekam_medis" : "an Id a given user for method PUT by Id",
        }
    )
    
    def get(self, id_rekam_medis):
        '''Get Patient Data by Id unique'''
        #cara get datanya
        try:
            data_by_id = Rekam_Medis.query.get_or_404(id_rekam_medis)
            print("data berhasil : ", data_by_id.id_rekam_medis)
            return data_by_id, HTTPStatus.OK
        
        except Exception as e:
            print("Error Get by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #SEKARANG BUAT YANG PUT / UPDATE
    @rekam_medis_ns.expect(rekam_medis_model)
    @rekam_medis_ns.marshal_with(rekam_medis_model) #ini pake with karena 1 aja, ga semua data
    @rekam_medis_ns.doc(
        description = "Update Medical Records data by Id",
        #jangan lupa parameternya
        params = {
            "id_rekam_medis" : "an Id a given user for method PUT by Id"
        }
    )
    def put(self, id_rekam_medis):
        """ Update Medical Records by Id unique"""
        try:
            medical_record_to_update = Rekam_Medis.query.get_or_404(id_rekam_medis) #Ambil datanya
            #ini ngambil datanya dari database
            
            data = rekam_medis_ns.payload #ambil payloadnya
            #ini ngambil data dari kiriman user / user input
            
            medical_record_to_update.diagnosis = data['diagnosis']
            medical_record_to_update.tgl_periksa = data['tgl_periksa']
            
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error Update by id : ", e)
            return [], HTTPStatus.BAD_REQUEST
        
    #LANJUT KE DELETE
    @rekam_medis_ns.marshal_with(rekam_medis_model) #ini pake with karena 1 aja, ga semua data
    @rekam_medis_ns.doc(
        description = "Delete Medical Records by Id",
        #jangan lupa parameternya
        params = {
            "id_rekam_medis" : "an Id a given user for method PUT by Id"
        }
    )
    def delete(self, id_rekam_medis):
        """ Delete User Data by Id unique"""
        
        #caranya mirip2 seperti get 
        try:
                
            medical_record_to_delete = Rekam_Medis.query.get_or_404(id_rekam_medis)
            
            db.session.delete(medical_record_to_delete)
            db.session.commit()
            
            return [], HTTPStatus.OK
            
        except Exception as e:
            print("Error delete by id : ", e)
            return [], HTTPStatus.BAD_REQUEST