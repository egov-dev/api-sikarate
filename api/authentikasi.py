from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource


auth_ns = Namespace('auth', description='Endpoint Autentikasi Admin dan User')

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