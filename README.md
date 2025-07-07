# Math Server Practice - Calculadora Distribuida

## 📋 Descripción del Proyecto

Este proyecto implementa un **servidor matemático distribuido** como parte de la práctica de **Server Architecture** del curso de **Data Engineering** (5° cuatrimestre Mayo - Agosto 2025). El sistema utiliza microservicios construidos con Flask para ejecutar operaciones matemáticas de manera distribuida.

### Objetivos de la Práctica
- Diseñar y desplegar un servidor matemático aplicando principios fundamentales de arquitectura de servidores
- Implementar un sistema distribuido con comunicación via REST APIs
- Aplicar conceptos de paralelismo, comunicación entre servicios y modularidad

## 🏗️ Arquitectura del Sistema

El sistema consta de:
- **1 Coordinador** que recibe operaciones y las distribuye
- **3 Workers especializados** que procesan tipos específicos de operaciones
- **Frontend web** para interactuar con el sistema

![Architecture Diagram](https://github.com/user-attachments/assets/aecac4b9-9650-4f2e-9eb4-fda9bb17971f)

## 🚀 Implementación Paso a Paso

### Paso 1: Código Base Proporcionado

La práctica comenzó con un **coordinador básico** que distribuía operaciones entre 2 workers genéricos:

```python
# Coordinador inicial (código base)
WORKERS = [
    "http://localhost:5001/process",
    "http://localhost:5002/process"
]

# Distribución simple por chunks
chunk_size = math.ceil(n / len(WORKERS))
for i, worker_url in enumerate(WORKERS):
    chunk = operations[i*chunk_size:(i+1)*chunk_size]
```

**Worker inicial (código base):**
```python
# Worker genérico que manejaba todas las operaciones
if op == "add":
    result = a + b
elif op == "sub":
    result = a - b
elif op == "mul":
    result = a * b
elif op == "div":
    result = a / b if b != 0 else None
```

### Paso 2: Extensión Requerida - Especialización de Workers

Siguiendo las instrucciones de la práctica, se extendió el código para:

#### 🔧 **Modificación del Coordinador** (`coordinator.py`)

```python
# Configuración de workers especializados
WORKERS = {
    "arithmetic": "http://localhost:5001/process",      # suma y resta
    "multiplication": "http://localhost:5002/process",  # multiplicación y división
    "advanced": "http://localhost:5003/process"         # exponenciación y raíz cuadrada
}

# Clasificación inteligente de operaciones
def classify_operations(operations):
    arithmetic_ops = []
    multiplication_ops = []
    advanced_ops = []
    
    for operation in operations:
        op = operation["op"]
        if op in ["add", "sub"]:
            arithmetic_ops.append(operation)
        elif op in ["mul", "div"]:
            multiplication_ops.append(operation)
        elif op in ["pow", "sqrt"]:
            advanced_ops.append(operation)
```

#### 🔧 **Worker 1 - Operaciones Aritméticas** (`worker1.py`)

**Especialización:** Suma y Resta
```python
# worker1.py - Puerto 5001
@app.route('/process', methods=['POST'])
def process():
    for operation in operations:
        if op == "add":
            result = a + b
        elif op == "sub":
            result = a - b
        
        results.append({
            "result": result,
            "processed_by": "Worker1",  # Indica el nodo que procesó
            "operation": f"{a} {op} {b}"
        })
```

#### 🔧 **Worker 2 - Multiplicación y División** (`worker2.py`)

**Especialización:** Multiplicación y División
```python
# worker2.py - Puerto 5002
@app.route('/process', methods=['POST'])
def process():
    for operation in operations:
        if op == "mul":
            result = a * b
        elif op == "div":
            result = a / b if b != 0 else None
        
        results.append({
            "result": result,
            "processed_by": "Worker2",  # Indica el nodo que procesó
            "operation": f"{a} {op} {b}"
        })
```

#### 🔧 **Worker 3 - Operaciones Avanzadas** (`worker3.py`)

**Especialización:** Exponenciación y Raíz Cuadrada
```python
# worker3.py - Puerto 5003
@app.route('/process', methods=['POST'])
def process():
    for operation in operations:
        if op == "pow":
            result = a ** b
        elif op == "sqrt":
            result = math.sqrt(a) if a >= 0 else None
        
        results.append({
            "result": result,
            "processed_by": "Worker3",  # Indica el nodo que procesó
            "operation": operation_str
        })
```

### Paso 3: Frontend Web Interactivo

Adicionalmente, se desarrolló un **frontend web** (`front.html`) que no estaba en los requisitos originales pero mejora significativamente la experiencia del usuario:

```html
<!-- Formulario para agregar operaciones -->
<form id="operationForm">
    <input type="number" id="numA" step="any" required>
    <select id="operation" required>
        <option value="add">Suma (+)</option>
        <option value="sub">Resta (-)</option>
        <option value="mul">Multiplicación (×)</option>
        <option value="div">División (÷)</option>
        <option value="pow">Potencia (^)</option>
        <option value="sqrt">Raíz cuadrada (√)</option>
    </select>
    <input type="number" id="numB" step="any" required>
</form>
```

### Paso 4: Estilos y Animaciones

Se implementó un sistema de estilos avanzado (`styles.css`) con:
- Animaciones CSS modernas
- Efectos hover interactivos
- Diseño responsivo
- Retroalimentación visual

## 🛠️ Tecnologías Utilizadas

| Tecnología | Rol |
|------------|-----|
| **Python** | Lógica de negocio y servicios |
| **Flask** | Framework web para servicios REST |
| **Requests** | Cliente HTTP para enviar tareas a workers |
| **JSON** | Formato de datos para comunicación |
| **HTML/CSS/JavaScript** | Frontend interactivo |
| **Flask-CORS** | Manejo de CORS para el frontend |

## 🔧 Instalación y Ejecución

### Prerrequisitos
```bash
pip install flask flask-cors requests
```

### Ejecución Local (siguiendo las instrucciones de la práctica)

1. **Ejecutar el coordinador:**
```bash
python3 coordinator.py
```

2. **Ejecutar los workers en terminales separadas:**
```bash
python3 worker1.py  # Puerto 5001
python3 worker2.py  # Puerto 5002
python3 worker3.py  # Puerto 5003
```

3. **Probar con curl (como en la práctica original):**
```bash
curl -X POST http://localhost:5000/compute \
-H "Content-Type: application/json" \
-d '{"operations":[{"op":"add","a":25,"b":32},{"op":"mul","a":13,"b":14},{"op":"sub","a":17,"b":59}]}'
```

**Salida esperada:**
```json
[
  {"result": 57, "processed_by": "Worker1", "operation": "25.0 add 32.0"},
  {"result": 182, "processed_by": "Worker2", "operation": "13.0 mul 14.0"},
  {"result": -42, "processed_by": "Worker1", "operation": "17.0 sub 59.0"}
]
```

4. **Usar el frontend web:**
```bash
# Abrir front.html en el navegador
open front.html
```

## 📊 Asignación de Nodos (Cumplimiento de Requisitos)

| Operación | Worker | Puerto | Especialización |
|-----------|---------|---------|-----------------|
| **Suma** (`add`) | Worker1 | 5001 | ✅ Operaciones aritméticas |
| **Resta** (`sub`) | Worker1 | 5001 | ✅ Operaciones aritméticas |
| **Multiplicación** (`mul`) | Worker2 | 5002 | ✅ Multiplicación y división |
| **División** (`div`) | Worker2 | 5002 | ✅ Multiplicación y división |
| **Exponenciación** (`pow`) | Worker3 | 5003 | ✅ Operaciones avanzadas |
| **Raíz cuadrada** (`sqrt`) | Worker3 | 5003 | ✅ Operaciones avanzadas |

## ✅ Requisitos Cumplidos

### Requisitos Obligatorios:
- [x] **Nodo Worker1** para suma y resta
- [x] **Nodo Worker2** para multiplicación y división  
- [x] **Nodo Worker3** para exponenciación y raíz cuadrada
- [x] **Coordinador modificado** para distribuir tareas a nodos apropiados

### Requisitos Opcionales:
- [x] **Indicación del nodo** que procesó cada resultado
- [x] **Manejo de errores** mejorado
- [x] **Validación de entrada** (división por cero, raíz negativa)
- [x] **Frontend web interactivo** (extra)

## 🔍 Ejemplos de Uso

### Ejemplo 1: Operaciones Mixtas
```bash
curl -X POST http://localhost:5000/compute \
-H "Content-Type: application/json" \
-d '{"operations":[
  {"op":"add","a":10,"b":5},
  {"op":"mul","a":4,"b":3},
  {"op":"pow","a":2,"b":8},
  {"op":"sqrt","a":16}
]}'
```

### Ejemplo 2: Usando el Frontend
1. Abrir `front.html` en el navegador
2. Agregar operaciones usando el formulario
3. Presionar "Calcular Todas las Operaciones"
4. Ver resultados con información del worker que procesó cada operación


## 📝 Conclusión

Esta práctica demuestra exitosamente la implementación de un **servidor matemático distribuido** que cumple con todos los objetivos planteados. El sistema exhibe:

- **Arquitectura distribuida** bien estructurada
- **Especialización de workers** por tipo de operación
- **Comunicación eficiente** via REST APIs
- **Manejo robusto de errores** y casos edge
- **Interfaz de usuario intuitiva** (bonus)

El proyecto proporciona una base sólida para entender conceptos avanzados de sistemas distribuidos y arquitecturas de microservicios.

---
**Student:** Karen Cardiel Olea<br>
**Professor:** M. Sc. Jorge J. Pedrozo Romero  
**Curso:** Data Engineering - 5° Cuatrimestre  
**Período:** Mayo - Agosto 2025
