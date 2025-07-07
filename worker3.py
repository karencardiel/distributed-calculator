# worker3.py - Advanced Math Operations (CORREGIDO)
from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    operations = data.get("operations", [])
    worker_name = data.get("worker_name", "Worker3")
    results = []
    
    for operation in operations:
        op = operation["op"]  # Mantener como string
        a = float(operation["a"])  # Convertir a float para decimales
        b = float(operation.get("b", 0)) if operation.get("b") is not None else None
        
        try:
            if op == "pow":
                result = a ** b
            elif op == "sqrt":
                result = math.sqrt(a) if a >= 0 else None
            else:
                result = None
                
            # Incluir información del worker que procesó la operación
            operation_str = f"{a} {op}" if op == "sqrt" else f"{a} {op} {b}"
            results.append({
                "result": result,
                "processed_by": worker_name,
                "operation": operation_str
            })
            
        except Exception as e:
            operation_str = f"{a} {op}" if op == "sqrt" else f"{a} {op} {b}"
            results.append({
                "result": None,
                "processed_by": worker_name,
                "error": str(e),
                "operation": operation_str
            })
    
    return jsonify(results)

if __name__ == '__main__':
    print("Worker3 (Advanced Math) starting on port 5003...")
    app.run(host='0.0.0.0', port=5003, debug=True)