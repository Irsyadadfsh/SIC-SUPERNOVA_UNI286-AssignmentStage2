from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import logging
from pymongo.server_api import ServerApi


# Inisialisasi Flask
app = Flask(_name_)
CORS(app)
# Konfigurasi Logging
logging.basicConfig(level=logging.INFO)

# MongoDB Connection
uri = "mongodb://irsyadadfiansha09:IBDcgkq570BGXPtY@cluster-supernova.vipeb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-Supernova"
DB_NAME = "UNI286"
COLLECTION_NAME = "supernova"

try:
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logging.info("Koneksi MongoDB berhasil")
except Exception as e:
    logging.error(f"Error koneksi MongoDB: {e}")

# Endpoint untuk menyimpan data
@app.route('/save', methods=["POST"])
def save_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Ambil data dengan default jika kosong
        suhu = data.get("suhu")
        kelembaban = data.get("kelembaban")
        intensitas_cahaya = data.get("intensitas_cahaya", 0)

        # Validasi input
        if suhu is None or kelembaban is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Simpan ke database
        simpan = {"suhu": suhu, "kelembaban": kelembaban, "intensitas_cahaya": intensitas_cahaya}
        collection.insert_one(simpan)
        logging.info(f"Data berhasil disimpan: {simpan}")

        return jsonify({"message": "success"})
    
    except Exception as e:
        logging.error(f"Error saat menyimpan data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Jalankan server Flask
if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000)