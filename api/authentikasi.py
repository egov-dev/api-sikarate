from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from .query.q_autentikasi import get_login, get_user_by_id


auth_ns = Namespace('auth', description='Endpoint Autentikasi Admin dan User')

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description="email"),
    'password': fields.String(required=True, description="password")
})


@auth_ns.route('/me')
class MeResource(Resource):
    @jwt_required()
    def get(self):
        """Ambil data user dari JWT token"""
        user_id = get_jwt_identity()
        try:
            user = get_user_by_id(user_id)
            if not user:
                return {"status": "error", "message": "User tidak ditemukan"}, 404
            return {"data": user}, 200
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Server error"}, 500
        
@auth_ns.route('/protected')
class ProtectedResource(Resource):
    def get(self):
        """Akses: (admin/mentor/peserta), Cek token masih valid"""
        return {'status': 'Token masih valid'}, 200
    

@auth_ns.route('/contoh-data')
class ContohDataResource(Resource):
    @jwt_required()
    def get(self):
        """Contoh data yang dikirimkan api"""
        return{
            'id_laporan': 1,
            'nama_pelapor': 'user1',
            'lokasi_kebakaran': 'mataram'
        }
    
@auth_ns.route('/login')
class LoginAdminResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Akses: (admin/user), login menggunakan email + password"""
        payload = request.get_json()

        if not payload['email'] or not payload['password']:
            return {'status': "Fields can't be blank"}, 400

        try:
            get_jwt_response = get_login(payload)
            if get_jwt_response is None:
                return {'status': "Invalid email or password"}, 401
            return get_jwt_response, 200
        except SQLAlchemyError as e:
            auth_ns.logger.error(f"Database error: {str(e)}")
            return {'status': "Internal server error"}, 500
