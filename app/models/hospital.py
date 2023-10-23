# import datetime
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from ..utils import db


# #TABLE PASIEN, BERELASI DENGAN REKAM MEDIS ONE-TO-ONE
# class Pasien(db.Model):
#     __tablename__ = 'pasien'
#     id_pasien = db.Column(db.Integer(), primary_key = True)
#     nama_pasien = db.Column(db.String(50), nullable = False, unique=True)
#     alamat = db.Column(db.String(50))
#     No_Rekam_Medis = db.Column(db.Integer(), nullable = False, unique=True)
#     profile = db.relationship('Rekam_Medis', backref='pasien', uselist=False, cascade='all, delete-orphan')
#     profile_pasien = db.relationship('Penugasan', backref='pasien', uselist=False, cascade='all, delete-orphan')

#     def __repr__(self):
#         return f'<pasien{self.nama_pasien}>'

# #TABLE REKAM MEDIS    
# class Rekam_Medis(db.Model):
#     __tablename__ = 'rekam_medis'
#     id_rekam_medis = db.Column(db.Integer(), primary_key = True)
#     id_pasien = db.Column(db.Integer(), db.ForeignKey('pasien.id_pasien'))
#     diagnosis = db.Column(db.String(50), nullable = False)
#     tgl_periksa = db.Column(db.DateTime, nullable = False)
#     rekam_medis_pasien = db.relationship('Penugasan', backref='rekam_medis', uselist=False, cascade='all, delete-orphan')

#     def __repr__(self):
#         return f'<rekam_medis{self.id_pasien}>'

# #TABLE DOKTER
# class Dokter(db.Model):
#     __tablename__ = 'dokter'
#     id_dokter = db.Column(db.Integer(), primary_key = True)
#     nama_dokter = db.Column(db.String(50), nullable = False)
#     spesialisasi = db.Column(db.String(50), nullable = False)

#     def __repr__(self):
#         return f'<dokter{self.nama_dokter}>'

# #TABLE KAMAR RAWAT
# class Kamar_Rawat(db.Model):
#     __tablename__ = 'kamar_rawat'
#     id_kamar = db.Column(db.Integer(), primary_key = True)
#     nama_kamar = db.Column(db.String(50), nullable = False)
#     jenis_kamar = db.Column(db.String(50), nullable = False)

#     def __repr__(self):
#         return f'<kamar_rawat{self.nama_kamar}>'

# #TABLE PENUGASAN BERELASI DENGAN TABLE KAMAR RAWAT DAN TABLE DOKTER MANY-TO-MANY
# class Penugasan(db.Model):
#      __tablename__ = 'penugasan'
#      id_penugasan = db.Column(db.Integer(), primary_key = True)
#      id_dokter = db.Column(db.Integer(), db.ForeignKey('dokter.id_dokter') ,primary_key = True)
#      id_kamar = db.Column(db.Integer(), db.ForeignKey('kamar_rawat.id_kamar'), primary_key = True)
#      id_pasien = db.Column(db.Integer(), db.ForeignKey('pasien.id_pasien'), primary_key = True)
#      id_rekam_medis = db.Column(db.Integer(), db.ForeignKey('rekam_medis.id_rekam_medis'), primary_key = True)
#      tanggal_penugasan = db.Column(db.DateTime, nullable = False)

#      def __repr__(self):
#         return f'<penugasan{self.tanggal_penugasan}>'