from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math

# Direcciones de los workers especializados
WORKERS = {
    "arithmetic": "http://localhost:5001/process",  # suma y resta
    "multiplication": "http://localhost:5002/process",  # multiplicación y división
    "advanced": "http://localhost:5003/process"  # exponenciación y raíz cuadrada
}

app = Flask(__name__)
CORS(app)

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    operations = data.get("operations", [])
    
    # Clasificar operaciones por tipo
    arithmetic_ops = []
    multiplication_ops = []
    advanced_ops = []
    
    for i, operation in enumerate(operations):
        op = operation["op"]
        operation["index"] = i  # Mantener el índice original
        
        if op in ["add", "sub"]:
            arithmetic_ops.append(operation)
        elif op in ["mul", "div"]:
            multiplication_ops.append(operation)
        elif op in ["pow", "sqrt"]:
            advanced_ops.append(operation)
    
    results = [None] * len(operations)  # Lista para mantener el orden
    
    # Enviar operaciones a workers especializados
    worker_groups = [
        (arithmetic_ops, "arithmetic", "Worker1"),
        (multiplication_ops, "multiplication", "Worker2"), 
        (advanced_ops, "advanced", "Worker3")
    ]
    
    for ops, worker_type, worker_name in worker_groups:
        if ops:
            try:
                res = requests.post(WORKERS[worker_type], 
                                  json={"operations": ops, "worker_name": worker_name})
                worker_results = res.json()
                
                # Colocar resultados en la posición correcta
                for i, result in enumerate(worker_results):
                    original_index = ops[i]["index"]
                    results[original_index] = result
                    
            except Exception as e:
                print(f"Error communicating with {worker_name}: {e}")
                for op in ops:
                    results[op["index"]] = {"result": None, "error": f"Worker {worker_name} unavailable"}
    
    return jsonify(results)

if __name__ == '__main__':
    print("Coordinator starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
