from flask import Flask, request, jsonify
from datetime import datetime as dt

app = Flask(__name__)
errors1 = []

@app.route('/temp', methods=['POST'])
def temp():
    data = request.get_json()
    
    try:
        device_id, epoch_ms, data_type, temperature = data['data'].split(':')
        device_id = int(device_id)
        epoch_ms = int(epoch_ms)
        temperature = float(temperature)

        if(data_type!="'Temperature'"):
            errors1.append(data['data'])
            return jsonify({"error": "bad request"}), 400 
        if temperature >= 90:
            formatted_time = dt.fromtimestamp(epoch_ms / 1000).strftime('%Y/%m/%d %H:%M:%S')
            return jsonify({"overtemp": True, "device_id": device_id, "formatted_time": formatted_time})
        else:
            return jsonify({"overtemp": False})
        
    except ValueError:
        errors1.append(data['data'])
        return jsonify({"error": "bad request"}), 400
    
    

@app.route('/errors', methods=['GET', 'DELETE'])
def errors():
    if request.method == 'GET':
        return jsonify({"errors": errors1})
    elif request.method == 'DELETE':
        errors1.clear()
        return jsonify({"success": True})

if __name__ == '__main__':
    app.run()
