from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..utils.config import get_connection
from datetime import datetime


def tambah_laporan(user_id, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            result = conn.execute(text("""
                INSERT INTO laporan (id_user, judul, lokasi, waktu_kejadian, jenis, deskripsi, status)
                VALUES (:id_user, :judul, :lokasi, :waktu_kejadian, :jenis, :deskripsi, 1)
                RETURNING id_laporan
            """), {
                "id_user": user_id,
                "judul": data['judul'],
                "lokasi": data['lokasi'],
                "waktu_kejadian": data['waktu_kejadian'],
                "jenis": data['jenis'],
                "deskripsi": data.get('deskripsi', ''),
            })
            return result.fetchone()[0]
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return None


def get_all_laporan():
    engine = get_connection()
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM laporan WHERE status = 1")).mappings().all()
        
        laporan_list = []
        for row in result:
            laporan = dict(row)
            for key, value in laporan.items():
                if isinstance(value, datetime):
                    laporan[key] = value.isoformat()
            laporan_list.append(laporan)
        return laporan_list

def get_laporan_by_user_id(user_id):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            result = conn.execute(text("""
                SELECT * FROM laporan
                WHERE id_user = :user_id AND status = 1
            """), {"user_id": user_id}).mappings().all()

            laporan_list = []
            for row in result:
                laporan = dict(row)
                for key, value in laporan.items():
                    if isinstance(value, datetime):
                        laporan[key] = value.isoformat()
                laporan_list.append(laporan)
            return laporan_list
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return []


def get_laporan_by_id(id_laporan):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            query = text("""
                SELECT a.*, u.nama AS pelapor
                FROM laporan a
                JOIN users u ON a.id_user = u.id_user
                WHERE a.id_laporan = :id
            """)
            result = conn.execute(query, {"id": id_laporan}).mappings().fetchone()

            if result:
                laporan = dict(result)
                for key, value in laporan.items():
                    if isinstance(value, datetime):
                        laporan[key] = value.isoformat()
                return laporan
        except SQLAlchemyError as e:
            print("Gagal ambil laporan:", e)
            return None



def update_laporan(id_laporan, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            conn.execute(text("""
                UPDATE laporan
                SET judul = :judul,
                    lokasi = :lokasi,
                    waktu_kejadian = :waktu_kejadian,
                    jenis = :jenis,
                    deskripsi = :deskripsi,
                WHERE id_laporan = :id AND status = 1
            """), {
                "id": id_laporan,
                "judul": data['judul'],
                "lokasi": data['lokasi'],
                "waktu_kejadian": data['waktu_kejadian'],
                "jenis": data['jenis'],
                "deskripsi": data.get('deskripsi', ''),
            })
            return True
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False


def hapus_laporan(id_laporan):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            query = text("""
                DELETE FROM laporan
                WHERE id_laporan = :id
            """)
            result = conn.execute(query, {"id": id_laporan})
            return result.rowcount > 0  
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False


def verifikasi_laporan(id_laporan, data):
    engine = get_connection()
    with engine.begin() as conn:
        try:
            cek = conn.execute(text("""
                SELECT id_laporan FROM laporan WHERE id_laporan = :id AND status = 1
            """), {"id": id_laporan}).fetchone()
            if not cek:
                return None
            
            conn.execute(text("""
                UPDATE laporan
                SET status_penanganan = :status_penanganan
                WHERE id_laporan = :id AND status = 1
            """), {
                "id": id_laporan,
                "status_penanganan": data.get('status_penanganan', '')
            })
            return True
        except SQLAlchemyError as e:
            print("DB Error:", e)
            return False