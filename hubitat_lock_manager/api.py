from flask import Flask, request, jsonify
from hubitat_lock_manager.datastore import DataStore

app = Flask(__name__)

data_store = DataStore(connection=None)  # Initialize with actual connection

@app.route('/create_key_code', methods=['POST'])
def create_key_code():
    params = request.json
    result = data_store.create(params)
    return jsonify(result)

@app.route('/read_key_code', methods=['POST'])
def read_key_code():
    params = request.json
    result = data_store.read(params)
    return jsonify(result)

@app.route('/update_key_code', methods=['POST'])
def update_key_code():
    params = request.json
    result = data_store.update(params)
    return jsonify(result)

@app.route('/delete_key_code', methods=['POST'])
def delete_key_code():
    params = request.json
    result = data_store.delete(params)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
