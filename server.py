# Install flask dan librouteros jika belum
# pip install flask librouteros

from flask import Flask, jsonify
from librouteros import connect
from librouteros.exceptions import TrapError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Fungsi untuk terhubung dengan Mikrotik
def connect_to_mikrotik():
    # Ubah dengan informasi login perangkat Mikrotik
    host = '192.168.56.2'  # IP Mikrotik
    username = 'admin'
    password = '123456'

    try:
        api = connect(username=username, password=password, host=host)
        return api
    except TrapError as e:
        print(f"Error connecting to Mikrotik: {e}")
        return None

# Endpoint untuk mengambil data interfaces
@app.route('/api/interfaces', methods=['GET'])
def get_interfaces():
    api = connect_to_mikrotik()
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        interfaces_data = []
        # Ambil data dari interface Mikrotik
        for interface in api('/interface/print'):
            interfaces_data.append(interface)
        return jsonify(interfaces_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        api.close()  # Pastikan koneksi tertutup setelah selesai

@app.route('/api/dhcp-clients', methods=['GET'])
def get_dhcp_clients():
    api = connect_to_mikrotik()
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        dhcp_clients_data = []
        # Ambil data dari DHCP Client Mikrotik
        for client in api('/ip/dhcp-client/print'):
            dhcp_clients_data.append(client)
        return jsonify(dhcp_clients_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        api.close()  # Pastikan koneksi tertutup setelah selesai

@app.route('/api/routes', methods=['GET'])
def get_routes():
    api = connect_to_mikrotik()
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        routes_data = []
        # Ambil data dari ip/route/print Mikrotik
        for route in api('/ip/route/print'):
            routes_data.append(route)
        return jsonify(routes_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        api.close()  # Pastikan koneksi tertutup setelah selesai

if __name__ == '__main__':
    app.run(debug=True)
