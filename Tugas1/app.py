from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)
data_file = 'data.txt'

# Fungsi untuk menghitung hash
def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Mengambil isi file
@app.route('/data', methods=['GET'])
def get_data():
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return jsonify({'contents': lines, 'hash': calculate_hash(''.join(lines))})

# Menambahkan data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json.get('data')
    with open(data_file, 'a', encoding='utf-8') as f:
        f.write(new_data + '\n')
    return jsonify({'message': 'Data added successfully!'})

# Memperbarui data
@app.route('/data/<int:line_number>', methods=['PUT'])
def update_data(line_number):
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if line_number < 1 or line_number > len(lines):
        return jsonify({'error': 'Invalid line number!'}), 400
    new_data = request.json.get('data')
    lines[line_number - 1] = new_data + '\n'
    with open(data_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return jsonify({'message': 'Data updated successfully!'})

# Menghapus data
@app.route('/data/<int:line_number>', methods=['DELETE'])
def delete_data(line_number):
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if line_number < 1 or line_number > len(lines):
        return jsonify({'error': 'Invalid line number!'}), 400
    lines.pop(line_number - 1)
    with open(data_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return jsonify({'message': 'Data deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
