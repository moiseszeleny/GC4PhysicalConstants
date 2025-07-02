import gzip
import json
import re
from sympy import symbols, sympify, Eq

def clean_latex_expr(expr):
    """Convierte expresiones LaTeX a sintaxis de Python/SymPy"""
    # Reemplaza exponentes LaTeX ^{...} con **(...) 
    expr = re.sub(r'\^\{([^}]+)\}', r'**(\1)', expr)
    # Reemplaza subíndices LaTeX _{...} con _...
    expr = re.sub(r'_\{([^}]+)\}', r'_\1', expr)
    return expr.replace('\\', '').strip()

jsonfilename = 'standard_model_snippets.json.gz'
with gzip.open(jsonfilename, 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))

# Define todos los símbolos que podrías necesitar
alpha, m_Z, m_mu, delta = symbols('alpha m_Z m_mu delta')
local_dict = {'alpha': alpha, 'm_Z': m_Z, 'm_mu': m_mu, 'delta': delta}

data6 = data['6']
for array in data6:
    try:
        lhs, rhs = array[0].split('=')
        lhs = sympify(clean_latex_expr(lhs))
        rhs = sympify(clean_latex_expr(rhs), locals=local_dict)
        array[0] = Eq(lhs, rhs)
    except Exception as e:
        print(f"Error procesando: {array[0]}")
        print(f"Error: {e}")
        continue

# Crear una tabla con los datos
import pandas as pd

# Preparar los datos para la tabla
table_data = []
for i, array in enumerate(data6):
    row = {
        'Index': i,
        'Equation': str(array[0]),
        'Error': array[1],
        'Predicted': array[2], 
        'Target': array[3]
    }
    table_data.append(row)

# Crear DataFrame y mostrar la tabla
df = pd.DataFrame(table_data)
print("Tabla de ecuaciones y valores del Modelo Estándar:")
print("=" * 80)
print(df.to_string(index=False))
print(f"\nTotal de ecuaciones procesadas: {len(df)}")

# Mostrar estadísticas básicas de los valores numéricos
print("\nEstadísticas de los valores:")
print(df[['Error', 'Predicted', 'Target']].describe())