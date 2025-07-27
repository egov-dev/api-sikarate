from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource


auth_ns = Namespace('auth', description='Endpoint Autentikasi Admin dan User')

@auth_ns.route('/protected')
class ProtectedResource(Resource):
    def get(self):
        """Akses: (admin/mentor/peserta), Cek token masih valid"""
        return {'status': 'Token masih valid'}, 200