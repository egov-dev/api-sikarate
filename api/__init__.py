from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from .authentikasi import auth_ns

api = Flask(__name__)
CORS(api)

load_dotenv()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Masukkan token JWT Anda dengan format: **Bearer &lt;JWT&gt;**'
    }
}

# Swagger API instance
restx_api = Api(
    api, 
    version="1.0", 
    title="SIKARATE", 
    description="Dokumentasi API SIKARATE", 
    doc="/documentation",
    authorizations=authorizations,
    security='Bearer Auth'
)

restx_api.add_namespace(auth_ns, path="/auth")