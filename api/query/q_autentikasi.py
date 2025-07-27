from flask_jwt_extended import create_access_token
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..utils.config import get_connection


def get_user_by_id(user_id):
    engine = get_connection()
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT id_user, email, role, status
            FROM users
            WHERE id_user = :id_user AND status = 1
        """), {"id_user": user_id}).mappings().fetchone()
        return dict(result) if result else None

def get_login(payload):
    engine = get_connection()
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT id_user, email, password, role, status
                    FROM users
                    WHERE email = :email AND status = 1
                """),
                {"email": payload['email']}
            ).mappings().fetchone()

            if result:
                if result['password'] == payload['password']:
                    access_token = create_access_token(
                        identity=str(result['id_user']),
                        additional_claims={"role": result['role']}
                    )
                    return {
                        'access_token': access_token,
                        'message': 'login success',
                        'id_user': result['id_user'],
                        'email': result['email'],
                        'role': result['role']
                    }
        return None
    except SQLAlchemyError as e:
        print(f"Error occurred: {str(e)}")
        return {'msg': 'Internal server error'}
