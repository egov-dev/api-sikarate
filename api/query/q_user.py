from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..utils.config import get_connection

def get_all_users():
    engine = get_connection()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id_user, email, nama, status = 1
            FROM users
        """)).mappings().all()
        return [dict(row) for row in result]

def get_user_by_id(id_user):
    engine = get_connection()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id_user, email, nama, status = 1
            FROM users
            WHERE id_user = :id_user
        """), {"id_user": id_user}).mappings().fetchone()
        return dict(result) if result else None

def insert_user(data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            result = conn.execute(text("""
                INSERT INTO users (email, password, nama, role, status)
                VALUES (:email, :password, :nama, :role, 1)
                RETURNING id_user
            """), data)
            return result.fetchone()[0]
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return None

def update_user(id_user, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            conn.execute(text("""
                UPDATE users
                SET email = :email,
                    password = :password,
                    nama = :nama,
                    status = 1
                WHERE id_user = :id_user
            """), {**data, "id_user": id_user})
            return True
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False

def hapus_user(id_user):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            result = conn.execute(text("""
                UPDATE user
                    SET status = 0
                WHERE id_user = :id
            """), {"id_user": id_user})
            return result.rowcount > 0
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False
