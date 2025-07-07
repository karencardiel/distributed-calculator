# worker2.py - Multiplication/Division Operations (CORREGIDO)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    operations = data.get("operations", [])
    worker_name = data.get("worker_name", "Worker2")
    results = []
    
    for operation in operations:
        op = operation["op"]  # Mantener como string
        a = float(operation["a"])  # Convertir a float para decimales
        b = float(operation.get("b", 1))  # Convertir a float, default 1 si no existe
        
        try:
            if op == "mul":
                result = a * b
            elif op == "div":
                result = a / b if b != 0 else None
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
    print("Worker2 (Multiplication/Division) starting on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=True)