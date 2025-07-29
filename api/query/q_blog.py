from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..utils.config import get_connection
from datetime import datetime

def insert_artikel(id_user, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            result = conn.execute(text("""
                INSERT INTO artikel (id_user, judul, isi, id_kategori, status, created_at, updated_at)
                VALUES (:id_user, :judul, :isi, :id_kategori, 1, NOW(), NOW())
                RETURNING id_artikel
            """), {
                "id_user": id_user,
                "judul": data['judul'],
                "isi": data['isi'],
                "id_kategori": data['id_kategori']
            })
            return result.fetchone()[0]
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return None


def get_all_artikel():
    engine = get_connection()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT a.*, k.nama as kategori
            FROM artikel a
            JOIN kategori k ON a.id_kategori = k.id_kategori
            WHERE a.status = 1
        """)).mappings().all()

        artikel_list = []
        for row in result:
            artikel = dict(row)
            for key, value in artikel.items():
                if isinstance(value, datetime):
                    artikel[key] = value.isoformat()
            artikel_list.append(artikel)
        return artikel_list



def get_artikel_by_id(id_artikel):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            query = text("""
                SELECT a.*, k.nama AS kategori
                FROM artikel a
                JOIN kategori k ON a.id_kategori = k.id_kategori
                WHERE a.id_artikel = :id AND a.status = 1
            """)
            result = conn.execute(query, {"id": id_artikel}).mappings().fetchone()
            if result:
                artikel = dict(result)

                # Convert datetime to string (ISO format)
                for key, value in artikel.items():
                    if isinstance(value, datetime):
                        artikel[key] = value.isoformat()
                return artikel
            else:
                return None
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return None


def update_artikel(id_artikel, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            # Cek apakah 'status' disertakan
            if 'status' in data:
                query = text("""
                    UPDATE artikel
                    SET judul = :judul,
                        isi = :isi,
                        id_kategori = :id_kategori,
                        status = :status,
                        updated_at = NOW()
                    WHERE id_artikel = :id
                """)
                params = {
                    "id": id_artikel,
                    "judul": data['judul'],
                    "isi": data['isi'],
                    "id_kategori": data['id_kategori'],
                    "status": data['status']
                }
            else:
                query = text("""
                    UPDATE artikel
                    SET judul = :judul,
                        isi = :isi,
                        id_kategori = :id_kategori,
                        updated_at = NOW()
                    WHERE id_artikel = :id
                """)
                params = {
                    "id": id_artikel,
                    "judul": data['judul'],
                    "isi": data['isi'],
                    "id_kategori": data['id_kategori']
                }
            conn.execute(query, params)
            return True
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False



def hapus_artikel(id_artikel):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            query = text("""
                DELETE FROM artikel
                WHERE id_artikel = :id
            """)
            result = conn.execute(query, {"id": id_artikel})
            return result.rowcount > 0  # True kalau ada yg kehapus
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False

