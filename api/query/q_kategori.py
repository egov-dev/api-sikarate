from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..utils.config import get_connection
from datetime import datetime

def tambah_kategori(data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            result = conn.execute(text("""
                INSERT INTO kategori (nama, status, created_at, updated_at)
                VALUES (:nama, 1, NOW(), NOW())
                RETURNING id_kategori
            """), {"nama": data['nama']})
            return result.fetchone()[0]
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return None


def get_all_kategori():
    engine = get_connection()
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT * FROM kategori WHERE status = 1")
        ).mappings().all()
        
        kategori_list = []
        for row in result:
            kategori = dict(row)
            for key, value in kategori.items():
                if isinstance(value, datetime):
                    kategori[key] = value.isoformat()
            kategori_list.append(kategori)
        return kategori_list

# def get_all_kategori():
#     try:
#         engine = get_connection()
#         with engine.begin() as conn:
#             # Test query simple dulu
#             conn.execute(text("SELECT 1"))
#             print("✅ Database connected successfully")

#             # Query data kategori
#             result = conn.execute(
#                 text("SELECT * FROM kategori WHERE status = 1")
#             ).mappings().all()

#             kategori_list = []
#             for row in result:
#                 kategori = dict(row)
#                 for key, value in kategori.items():
#                     if isinstance(value, datetime):
#                         kategori[key] = value.isoformat()
#                 kategori_list.append(kategori)

#             return kategori_list
#     except SQLAlchemyError as e:
#         print(f"❌ Database connection/query failed: {str(e)}")
#         return []


def get_kategori_by_id(id_kategori):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            query = text("SELECT * FROM kategori WHERE id_kategori = :id AND status = 1")
            result = conn.execute(query, {"id": id_kategori}).mappings().fetchone()
            if result:
                kategori = dict(result)
                for key, value in kategori.items():
                    if isinstance(value, datetime):
                        kategori[key] = value.isoformat()
                return kategori
            else:
                return None
        except SQLAlchemyError as e:
            print("DB error:", e)
            return None
                
        

def update_kategori(id_kategori, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            conn.execute(text("""
                UPDATE kategori
                SET nama = :nama,
                    updated_at = NOW()
                WHERE id_kategori = :id AND status = 1
            """), {
                "id": id_kategori,
                "nama": data['nama']
            })
            return True
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False


def hapus_kategori(id_kategori):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            query = text("""
                 UPDATE kategori
                    SET status = 0
                WHERE id_kategori = :id
            """)
            result = conn.execute(query, {"id": id_kategori})
            return result.rowcount > 0  # True kalau ada yg kehapus
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False
