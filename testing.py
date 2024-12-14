from librouteros import connect

# Fungsi untuk menambahkan IP address baru
def add_ip(api, ip_address, interface):
    try:
        # Menambahkan IP address baru menggunakan perintah API yang benar
        response = list(api('/ip/address/add', address=ip_address, interface=interface))  # Mengkonsumsi generator
        print(f"IP address {ip_address} berhasil ditambahkan pada interface {interface}.")
        print("Response:", response)  # Menampilkan response dari server
        
        # Cek IP address yang baru ditambahkan
        addresses = list(api('/ip/address/print'))  # Mengambil daftar IP setelah penambahan
        print("Daftar IP setelah penambahan:", addresses)  # Debug: Menampilkan semua IP yang ada
    except Exception as e:
        print(f"Terjadi kesalahan saat menambahkan IP: {e}")

# Fungsi untuk mencari ID dari IP Address yang ada
def get_ip_id(api, old_ip):
    try:
        # Mengambil daftar IP address dalam bentuk list
        addresses = list(api('/ip/address/print'))  # Mengkonsumsi generator dan mengubahnya menjadi list
        print("Daftar IP Address yang ada:", addresses)  # Debug: Menampilkan semua IP yang ada
        
        # Mencari IP address yang sesuai dan mengembalikan ID-nya
        for address in addresses:
            if address['address'] == old_ip:
                print(f"ID ditemukan untuk IP {old_ip}: {address['.id']}")  # Debug: Menampilkan ID yang ditemukan
                return address['.id']  # Mengembalikan ID dari IP address
        return None  # Jika IP address tidak ditemukan
    except Exception as e:
        print(f"Terjadi kesalahan saat mencari ID IP: {e}")
        return None

# Fungsi untuk menghapus IP address di MikroTik menggunakan Command API
def delete_old_ip(api, old_ip):
    try:
        # Mendapatkan ID dari IP address yang ingin dihapus
        ip_id = get_ip_id(api, old_ip)
        
        if ip_id:
            # Menghapus IP address dengan ID yang ditemukan
            response = list(api('/ip/address/remove', numbers=ip_id))  # Mengkonsumsi generator
            print(f"IP address {old_ip} berhasil dihapus.")
            print("Response:", response)  # Menampilkan response dari server
            
            # Cek IP address setelah penghapusan
            addresses = list(api('/ip/address/print'))  # Mengambil daftar IP setelah penghapusan
            print("Daftar IP setelah penghapusan:", addresses)  # Debug: Menampilkan semua IP yang ada
        else:
            print(f"IP address {old_ip} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus IP: {e}")

# Contoh penggunaan
if __name__ == "__main__":
    mikrotik_ip = "192.168.56.4"  # Ganti dengan IP MikroTik Anda
    username = "admin"            # Ganti dengan username Anda
    password = ""         # Ganti dengan password Anda

    old_ip = "192.168.57.5/24"   # IP lama yang ingin dihapus (jika ada)
    new_ip = "192.168.57.7/24"   # IP baru yang ingin Anda set
    interface = "ether3"          # Interface yang akan dipakai (misal ether1)

    try:
        # Menghubungkan ke MikroTik
        api = connect(username=username, password=password, host=mikrotik_ip)

        # Menampilkan versi MikroTik
        version = api('/system/identity/print')
        print("Terhubung ke MikroTik dengan sukses. Versi perangkat:", version)

        # Hapus IP lama terlebih dahulu jika ada
        delete_old_ip(api, old_ip)

        # Tambahkan IP baru setelah IP lama dihapus
        add_ip(api, new_ip, interface)

    except Exception as e:
        print(f"Gagal terhubung ke MikroTik: {e}")
