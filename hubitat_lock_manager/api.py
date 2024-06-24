from flask import Flask, request, jsonify
from hubitat_lock_manager.hubitat_manager import HubitatManager
from hubitat_lock_manager.smart_lock import create_yale_assure_lever
from selenium import webdriver

app = Flask(__name__)

@app.route('/create_key_code', methods=['POST'])
def create_key_code():
    params = request.json
    driver = webdriver.Chrome(executable_path="path/to/chromedriver")
    smart_lock = create_yale_assure_lever(driver)
    manager = HubitatManager(driver=driver, smart_lock=smart_lock)
    result = manager.create_key_code(CreateKeyCodeParams(**params))
    manager.close()
    return jsonify(result)

@app.route('/read_key_code', methods=['POST'])
def read_key_code():
    params = request.json
    driver = webdriver.Chrome(executable_path="path/to/chromedriver")
    smart_lock = create_yale_assure_lever(driver)
    manager = HubitatManager(driver=driver, smart_lock=smart_lock)
    result = manager.read_key_code(ReadKeyCodeParams(**params))
    manager.close()
    return jsonify(result)

@app.route('/update_key_code', methods=['POST'])
def update_key_code():
    params = request.json
    driver = webdriver.Chrome(executable_path="path/to/chromedriver")
    smart_lock = create_yale_assure_lever(driver)
    manager = HubitatManager(driver=driver, smart_lock=smart_lock)
    result = manager.update_key_code(UpdateKeyCodeParams(**params))
    manager.close()
    return jsonify(result)

@app.route('/delete_key_code', methods=['POST'])
def delete_key_code():
    params = request.json
    driver = webdriver.Chrome(executable_path="path/to/chromedriver")
    smart_lock = create_yale_assure_lever
