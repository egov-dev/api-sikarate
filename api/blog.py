from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from .utils.decorator import role_required

from .query.q_blog import (
    get_all_artikel, get_artikel_by_id,
    insert_artikel, update_artikel, hapus_artikel
)


blog_ns = Namespace('blog', description='Manajemen Artikel')

artikel_input_model = blog_ns.model('ArtikelInput', {
    'id_kategori': fields.Integer(required=True),
    'judul': fields.String(required=True),
    'isi': fields.String(required=True)
})

artikel_update_model = blog_ns.model('ArtikelUpdate', {
    'id_kategori': fields.Integer(required=True),
    'judul': fields.String(required=True),
    'isi': fields.String(required=True)
})


@blog_ns.route('/')
class ArtikelListResource(Resource):
    def get(self):
        """Ambil semua artikel"""
        try:
            data = get_all_artikel()
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
        


    @role_required('admin')
    @blog_ns.expect(artikel_input_model) 
    def post(self):
        """Buat artikel baru"""
        user_id = get_jwt_identity()
        if not user_id:
            return {'message': 'User ID tidak ditemukan di token'}, 400
        payload = request.get_json()
        print("Payload:", payload)

        required_fields = ['id_kategori', 'judul', 'isi']
        for field in required_fields:
            if field not in payload:
                return {'message': f'Field {field} tidak ada di body'}, 400
        try:
            insert_artikel(
    user_id,
    {
        'id_kategori': payload['id_kategori'],
        'judul': payload['judul'],
        'isi': payload['isi']  
    })
            return {'message': 'Artikel berhasil dibuat'}, 201
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


@blog_ns.route('/<int:id_artikel>')
class ArtikelResource(Resource):
    def get(self, id_artikel):
        """Ambil artikel berdasarkan ID"""
        artikel = get_artikel_by_id(id_artikel)
        if not artikel:
            return {'message': 'Artikel tidak ditemukan'}, 404
        return {'data': artikel}, 200


    @role_required('admin')
    @blog_ns.expect(artikel_update_model)
    def put(self, id_artikel):
        """Update artikel berdasarkan ID"""
        payload = request.get_json()
        try:
            update_artikel(
            id_artikel,
            {
                'judul': payload['judul'],
                'isi': payload['isi'],
                'id_kategori': payload['id_kategori']
            }
        )
            return {'message': 'Artikel berhasil diperbarui'}, 200
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500



    @role_required('admin')
    def delete(self, id_artikel):
        """Hapus artikel berdasarkan ID"""
        try:
            success = hapus_artikel(id_artikel)
            if success:
                return {'message': f'Artikel dengan ID {id_artikel} berhasil dihapus'}, 200
            else:
                return {'message': f'Artikel dengan ID {id_artikel} tidak ditemukan'}, 404
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500

