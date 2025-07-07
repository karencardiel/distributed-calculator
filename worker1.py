# worker1.py - Arithmetic Operations (CORREGIDO)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    operations = data.get("operations", [])
    worker_name = data.get("worker_name", "Worker1")
    results = []
    
    for operation in operations:
        op = operation["op"]  # Mantener como string
        a = float(operation["a"])  # Convertir a float para decimales
        b = float(operation.get("b", 0))  # Convertir a float, default 0 si no existe
        
        try:
            if op == "add":
                result = a + b
            elif op == "sub":
                result = a - b
            else:
                result = None
                
            # Incluir información del worker que procesó la operación
            results.append({
                "result": result,
                "processed_by": worker_name,
                "operation": f"{a} {op} {b}"
            })
            
        except Exception as e:
            results.append({
                "result": None,
                "processed_by": worker_name,
                "error": str(e),
                "operation": f"{a} {op} {b}"
            })
    
    return jsonify(results)

if __name__ == '__main__':
    print("Worker1 (Arithmetic) starting on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)