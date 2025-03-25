# Thư viện web API và mã hóa Caesar
from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher 
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher
app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    text = data['plain_text']  # Lấy văn bản cần mã hóa từ request
    key = int(data['key'])     # Số bước dịch chữ cái (vd: A->B là 1 bước)
    return jsonify({'encrypted_message': caesar_cipher.encrypt_text(text, key)})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    text = data['cipher_text'] # Lấy văn bản mã hóa từ request
    key = int(data['key'])     # Dùng lại số bước đã dịch để giải mã
    return jsonify({'decrypted_message': caesar_cipher.decrypt_text(text, key)})
    
vigenere_cipher = VigenereCipher()  # Tạo đối tượng mã hóa Vigenere

@app.route('/api/vigenere/encrypt', methods=['POST']) 
def vigenere_encrypt():
    # API mã hóa: Nhận văn bản gốc + khóa, trả về văn bản đã mã hóa
    data = request.json
    plain_text = data['plain_text']  # Văn bản cần mã hóa
    key = data['key']                # Khóa mã hóa
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    # API giải mã: Nhận văn bản mã hóa + khóa, trả về văn bản gốc
    data = request.json
    cipher_text = data['cipher_text']  # Văn bản đã mã hóa
    key = data['key']                  # Khóa giải mã
    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})


# Khởi tạo đối tượng RailFenceCipher để xử lý mã hóa/giải mã
railfence_cipher = RailFenceCipher()

# API endpoint xử lý yêu cầu mã hóa
# Input JSON: {"plain_text": "văn bản cần mã hóa", "key": số rail}
@app.route('/api/railfence/encrypt', methods=['POST'])
def encrypt():
    # Lấy dữ liệu từ request JSON
    data = request.json
    plain_text = data['plain_text']  # Lấy văn bản cần mã hóa
    key = int(data['key'])          # Chuyển key thành số nguyên
    # Thực hiện mã hóa và trả về kết quả
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

# API endpoint xử lý yêu cầu giải mã
# Input JSON: {"cipher_text": "văn bản đã mã hóa", "key": số rail}
@app.route('/api/railfence/decrypt', methods=['POST'])
def decrypt():
    # Lấy dữ liệu từ request JSON
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})


# Import và khởi tạo đối tượng PlayFairCipher
playfair_cipher = PlayFairCipher()

# API endpoint tạo ma trận:
# Input: {key: string}
# Output: ma trận Playfair 5x5
@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.json
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({"playfair_matrix": playfair_matrix})

# API endpoint mã hóa:
# Input: {plain_text: string, key: string}
# Output: văn bản đã mã hóa
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    return jsonify({'encrypted_text': encrypted_text})

# API endpoint giải mã:
# Input: {cipher_text: string, key: string}  
# Output: văn bản gốc
@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    return jsonify({'decrypted_text': decrypted_text})


# Khởi tạo đối tượng TranspositionCipher
transposition_cipher = TranspositionCipher()

# API endpoint để mã hóa văn bản
@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    # Lấy dữ liệu JSON từ request
    data = request.get_json()
    # Lấy văn bản cần mã hóa và key
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    # Thực hiện mã hóa và trả về kết quả
    encrypted_text = transposition_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

# API endpoint để giải mã văn bản
@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    # Lấy dữ liệu JSON từ request
    data = request.get_json()
    # Lấy văn bản đã mã hóa và key
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    # Thực hiện giải mã và trả về kết quả
    decrypted_text = transposition_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Chạy server ở cổng 5000