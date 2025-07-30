from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from .query.q_kategori import (
    tambah_kategori, get_all_kategori, get_kategori_by_id,
    update_kategori, hapus_kategori
)

kategori_ns = Namespace('kategori', description='Manajemen Kategori')

kategori_input_model = kategori_ns.model('KategoriInput', {
    'nama': fields.String(required=True, description='Nama Kategori')
})

kategori_model = kategori_ns.model('Kategori', {
    'id_kategori': fields.Integer(readOnly=True),
    'nama': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String
})


@kategori_ns.route('/')
class KategoriListResource(Resource):
    @jwt_required()
    @kategori_ns.expect(kategori_input_model)
    def post(self):
        """Tambah kategori baru"""
        try:
            data = request.get_json()
            new_id = tambah_kategori(data)
            if new_id:
                return {"message": "Kategori berhasil ditambahkan", "id_kategori": new_id}, 201
            return {"message": "Gagal tambah kategori"}, 500
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


    def get(self):
        """Ambil semua kategori"""
        try:
            data = get_all_kategori()
            if not data:
                return {
                    'status': 'empty',
                    'message': 'Tidak ada artikel yang tersedia'
                }, 404
            return {"data": data}, 200
        except SQLAlchemyError as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil kategori: {str(e)}'
            }, 500


@kategori_ns.route('/<int:id_kategori>')
class KategoriResource(Resource):
    def get(self, id_kategori):
        """Ambil kategori berdasarkan ID"""
        kategori = get_kategori_by_id(id_kategori)
        if kategori:
            return {"data": kategori}, 200
        return {"message": "Kategori tidak ditemukan"}, 404


    @jwt_required()
    @kategori_ns.expect(kategori_input_model)
    def put(self, id_kategori):
        """Update kategori berdasarkan ID"""
        try:
            data = request.get_json()
            success = update_kategori(id_kategori, data)
            if success:
                return {"message": "Kategori berhasil diperbarui"}, 200
            return {"message": "Gagal update kategori"}, 500
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


    @jwt_required()
    def delete(self, id_kategori):
        """Hapus kategori"""
        try:
            success = hapus_kategori(id_kategori)
            if success:
                return {"message": f"Kategori dengan ID {id_kategori} berhasil dihapus"}, 200
            return {"message": "Kategori tidak ditemukan ID {id_kategori}"}, 404
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500
