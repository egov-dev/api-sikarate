from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from .query.q_user import (
    get_all_users, get_user_by_id,
    insert_user, update_user, hapus_user
)

user_ns = Namespace('user', description='Manajemen User')

user_model = user_ns.model('User', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'nama': fields.String(required=True),
    'status': fields.Integer(required=True)
})

@user_ns.route('/')
class UserListResource(Resource):
    @jwt_required()
    def get(self):
        """Ambil semua data user"""
        try:
            data = get_all_users()
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
    @user_ns.expect(user_model)
    def post(self):
        """Tambah user baru"""
        payload = request.get_json()
        try:
            user_id = insert_user(payload)
            return {'message': 'User berhasil ditambahkan', 'id_user': user_id}, 201
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


@user_ns.route('/<int:id_user>')
class UserResource(Resource):
    @jwt_required()
    def get(self, id_user):
        """Ambil user berdasarkan ID"""
        user = get_user_by_id(id_user)
        if not user:
            return {'message': 'User tidak ditemukan'}, 404
        return {'data': user}, 200


    @jwt_required()
    @user_ns.expect(user_model)
    def put(self, id_user):
        """Perbarui data user berdasarkan ID"""
        payload = request.get_json()
        try:
            success = update_user(id_user, payload)
            if success:
                return {'message': 'User berhasil diperbarui'}, 200
            else:
                return {'message': 'User tidak ditemukan'}, 404
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500


    @jwt_required()
    def delete(self, id_user):
        """Hapus user berdasarkan ID"""
        try:
            success = hapus_user(id_user)
            if success:
                return {'message': f'User dengan ID {id_user} berhasil dihapus'}, 200
            else:
                return {'message': 'User tidak ditemukan'}, 404
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': str(e)}, 500
