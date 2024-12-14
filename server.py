# Install flask dan librouteros jika belum
# pip install flask librouteros

from flask import Flask, jsonify, request
from librouteros import connect
from librouteros.exceptions import TrapError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Fungsi untuk terhubung dengan Mikrotik
def connect_to_mikrotik():
    # Ubah dengan informasi login perangkat Mikrotik
    host = '192.168.56.4'  # IP Mikrotik
    username = 'admin'
    password = ''

    try:
        api = connect(username=username, password=password, host=host)
        return api
    except TrapError as e:
        print(f"Error connecting to Mikrotik: {e}")
        return None

def get_api():
    api = connect_to_mikrotik()
    if api is None:
        return None
    return api

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

@app.route('/api/address', methods=['GET'])
def get_ip_address():
    api = connect_to_mikrotik()
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        ip_address_data = []
        # Ambil data dari ip/route/print Mikrotik
        for address in api('/ip/address/print'):
            ip_address_data.append(address)
        return jsonify(ip_address_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        api.close()  # Pastikan koneksi tertutup setelah selesai

@app.route('/api/address/<id>', methods=['GET'])
def get_ip_address_by_id(id):
    api = connect_to_mikrotik()
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        # Cari IP Address berdasarkan ID
        for address in api('/ip/address/print'):
            if address.get('.id') == id:
                return jsonify(address), 200
        return jsonify({"error": "Address not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        api.close()

# @app.route('/api/address/<id>', methods=['OPTIONS'])
# def handle_options(id):
#     return '', 200

@app.route('/api/address/<id>', methods=['PATCH'])
def update_ip_address(id):
    api = connect_to_mikrotik()
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        # Ambil data dari permintaan
        data = request.json
        new_address = data.get('address')
        interface = data.get('interface')
        disabled = data.get('disabled', False)
        network = data.get('network')

        if not id or not new_address or not interface:
            return jsonify({"error": "Address, interface, and id are required"}), 400

        # Langkah 1: Cari ID dari alamat IP yang ada
        addresses = list(api('/ip/address/print'))
        ip_found = None
        for address in addresses:
            if address['.id'] == id:
                ip_found = address
                break

        if ip_found:
            # Langkah 2: Update IP address dengan perintah 'set' untuk IP yang sudah ada
            response = list(api('/ip/address/set', **{
                '.id': id,
                'address': new_address,
                'interface': interface,
                'disabled': disabled,
                'network': network,  # Anda bisa mengirimkan parameter ini jika perlu
            }))
            print(f"IP address {new_address} berhasil diperbarui pada interface {interface}.")
            print("Response:", response)  # Menampilkan response dari server

            # Langkah 3: Cek IP address setelah perubahan
            addresses_after = list(api('/ip/address/print'))
            print("Daftar IP setelah perubahan:", addresses_after)
            
            return jsonify({"message": "IP address updated successfully"}), 200
        else:
            return jsonify({"error": "IP address not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        api.close()

@app.route('/api/address', methods=['POST'])
def add_ip_address():
    api = connect_to_mikrotik()  # Menghubungkan ke Mikrotik
    if api is None:
        return jsonify({"error": "Could not connect to Mikrotik"}), 500

    try:
        # Ambil data dari permintaan
        data = request.json
        new_address = data.get('address')
        interface = data.get('interface')
        disabled = data.get('disabled', False)
        network = data.get('network')

        # Validasi input
        if not new_address or not interface:
            return jsonify({"error": "Address and interface are required"}), 400

        # Langkah 1: Menambahkan alamat IP baru ke Mikrotik
        response = list(api('/ip/address/add', **{
            'address': new_address,
            'interface': interface,
            'disabled': disabled,
            'network': network  # Parameter opsional
        }))
        
        # Langkah 2: Cek apakah penambahan berhasil
        print(f"IP address {new_address} berhasil ditambahkan pada interface {interface}.")
        print("Response:", response)  # Menampilkan respons dari server

        # Langkah 3: Cek IP address setelah penambahan
        addresses_after = list(api('/ip/address/print'))
        print("Daftar IP setelah penambahan:", addresses_after)
        
        return jsonify({"message": "IP address added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        api.close()  # Menutup koneksi

# @app.route('/api/address/remove_by_id/<string:id>', methods=['DELETE'])
# def remove_ip_address_by_id(id):
#     api = connect_to_mikrotik()
#     if api is None:
#         return jsonify({"error": "Could not connect to Mikrotik"}), 500

#     try:
#         # Hapus IP address berdasarkan .id
#         print(f"Removing IP address with .id: {id}")
#         api(cmd='/ip/address/remove', **{'.id': id})

#         return jsonify({"message": f"IP address with .id {id} removed successfully"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         api.close()

if __name__ == '__main__':
    app.run(debug=True)
