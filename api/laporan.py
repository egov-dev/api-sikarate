from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from .query.q_laporan import (
    tambah_laporan, get_all_laporan, get_laporan_by_id,
    update_laporan, hapus_laporan, verifikasi_laporan
)

laporan_ns = Namespace('laporan', description='Manajemen Laporan')

laporan_input_model = laporan_ns.model('LaporanInput', {
    'judul': fields.String(required=True),
    'lokasi': fields.String(required=True),
    'waktu_kejadian': fields.String(required=True),
    'jenis': fields.String(required=True),
    'deskripsi': fields.String,
    'lampiran': fields.String,
    # 'status_penanganan': fields.String,
})

laporan_update_model = laporan_ns.model('LaporanUpdate', {
    'judul': fields.String(required=True),
    'lokasi': fields.String(required=True),
    'waktu_kejadian': fields.String(required=True),
    'jenis': fields.String(required=True),
    'deskripsi': fields.String,
    'lampiran': fields.String,
    # 'status_penanganan': fields.String,
})

laporan_verifikasi_model = laporan_ns.model('LaporanVerifikasi', {
    'status_penanganan': fields.String,})


@laporan_ns.route('/')
class LaporanListResource(Resource):
    @jwt_required()
    def get(self):
        """Ambil semua laporan"""
        try:
            data = get_all_laporan()
            if not data:
                return {
                    'status': 'empty',
                    'message': 'Tidak ada artikel yang tersedia'
                }, 404
            return {'data': data}, 200
        except SQLAlchemyError as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil data artikel: {str(e)}'
            }, 500


    @jwt_required()
    @laporan_ns.expect(laporan_input_model)
    def post(self):
        """Buat laporan baru"""
        user_id = get_jwt_identity()
        payload = request.get_json()

        required_fields = ['judul', 'lokasi', 'waktu_kejadian', 'jenis']
        for field in required_fields:
            if field not in payload:
                return {'message': f'Field {field} tidak ada di body'}, 400
        try:
            new_id = tambah_laporan(user_id, payload)
            if new_id:
                return {"message": "Laporan berhasil ditambahkan", "id_laporan": new_id}, 201
            return {"message": "Gagal tambah laporan"}, 500
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


@laporan_ns.route('/<int:id_laporan>')
class LaporanResource(Resource):
    @jwt_required()
    def get(self, id_laporan):
        """Ambil laporan berdasarkan ID"""
        laporan = get_laporan_by_id(id_laporan)
        if not laporan:
            return {'message': 'Laporan tidak ditemukan'}, 404
        return {'data': laporan}, 200


    @jwt_required()
    @laporan_ns.expect(laporan_update_model)
    def put(self, id_laporan):
        """Update laporan berdasarkan ID"""
        payload = request.get_json()
        try:
            success = update_laporan(id_laporan, payload)
            if success:
                return {"message": "Laporan berhasil diperbarui"}, 200
            return {"message": "Gagal update laporan"}, 500
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


    @jwt_required()
    def delete(self, id_laporan):
        """Hapus laporan berdasarkan ID"""
        try:
            success = hapus_laporan(id_laporan)
            if success:
                return {'message': f'laporan dengan ID {id_laporan} berhasil dihapus'}, 200
            else:
                return {'message': f'laporan dengan ID {id_laporan} tidak ditemukan'}, 404
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


    @jwt_required()
    @laporan_ns.expect(laporan_verifikasi_model)
    def put(self, id_laporan):
        """Verifikasi laporan berdasarkan ID"""
        payload = request.get_json()
        try:
            success = verifikasi_laporan(id_laporan, payload)
            if success is None:
                return {"message": "Laporan dengan ID tersebut tidak ditemukan"}, 404
            if success:
                return {"message": "Verifikasi laporan berhasil diperbarui"}, 200
            return {"message": "Gagal Verifikasi laporan"}, 500
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500