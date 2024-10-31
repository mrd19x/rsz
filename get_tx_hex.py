import requests
import json

# Konfigurasi koneksi ke Electrum RPC
rpc_user = 'zia'
rpc_password = '123123'
rpc_url = 'http://127.0.0.1:7777'

def rpc_call(method, params):
    """Fungsi untuk melakukan panggilan RPC ke Electrum."""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": method,
        "params": params
    }
    
    try:
        response = requests.post(rpc_url, headers=headers, json=payload, auth=(rpc_user, rpc_password))
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil
        
        # Mengembalikan respons JSON
        return response.json()
    except requests.exceptions.HTTPError:
        return None
    except Exception:
        return None

def get_transaction_hex(txid):
    """Fungsi untuk mendapatkan data hex dari transaksi."""
    result = rpc_call('gettransaction', [txid])
    if result and 'result' in result:
        hex_data = result['result']
        if isinstance(hex_data, str):
            return hex_data
    return None

if __name__ == "__main__":
    txid = "0a855d267a1451407953b93c6b29118f00f4da90f98dcdca59a8fee2148906f2"  # Ganti dengan TXID yang diinginkan
    hex_data = get_transaction_hex(txid)
    
    if hex_data:
        print(hex_data)  # Hanya mencetak data hex
