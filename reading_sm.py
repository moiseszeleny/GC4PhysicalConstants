import gzip
import json
import re
import pandas as pd
from sympy import symbols, sympify, Eq
from typing import Dict, List, Tuple, Any


class StandardModelProcessor:
    """Procesador de datos del Modelo Estándar desde archivos JSON comprimidos."""
    
    def __init__(self, json_filename: str):
        self.json_filename = json_filename
        self.symbols_dict = self._create_symbols()
        self.data = self._load_data()
    
    def _create_symbols(self) -> Dict[str, Any]:
        """Crea y retorna un diccionario con los símbolos de SymPy necesarios."""
        # Definir símbolos comunes del Modelo Estándar
        symbol_names = ['alpha', 'm_Z', 'm_mu', 'delta', 'theta_12', 'theta_13', 
                    'theta_23', 'm_d', 'm_c', 'm_b', 'm_s', 'm_W', 'alpha_S']
        
        symbols_obj = symbols(' '.join(symbol_names))
        if isinstance(symbols_obj, tuple):
            return dict(zip(symbol_names, symbols_obj))
        else:
            return {symbol_names[0]: symbols_obj}
    
    def _load_data(self) -> Dict:
        """Carga los datos desde el archivo JSON comprimido."""
        try:
            with gzip.open(self.json_filename, 'r') as fin:
                return json.loads(fin.read().decode('utf-8'))
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {self.json_filename}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar JSON desde: {self.json_filename}")
    
    def clean_latex_expr(self, expr: str) -> str:
        """Convierte expresiones LaTeX a sintaxis de Python/SymPy."""
        # Reemplaza exponentes LaTeX ^{...} con **(...) 
        expr = re.sub(r'\^\{([^}]+)\}', r'**(\1)', expr)
        # Reemplaza subíndices LaTeX _{...} con _...
        expr = re.sub(r'_\{([^}]+)\}', r'_\1', expr)
        return expr.replace('\\', '').strip()
    
    def process_equation(self, equation_str: str) -> Tuple[Any, str]:
        """
        Procesa una ecuación string y la convierte en objeto SymPy Eq.
        
        Returns:
            Tuple de (ecuación_sympy, mensaje_error)
        """
        try:
            if '=' not in equation_str:
                return equation_str, "No contiene símbolo de igualdad"
            
            lhs, rhs = equation_str.split('=', 1)  # Split solo en el primer '='
            lhs_clean = self.clean_latex_expr(lhs)
            rhs_clean = self.clean_latex_expr(rhs)
            
            lhs_sympy = sympify(lhs_clean)
            rhs_sympy = sympify(rhs_clean, locals=self.symbols_dict)
            
            return Eq(lhs_sympy, rhs_sympy), ""
            
        except Exception as e:
            return equation_str, str(e)
    
    def process_data_section(self, section_key: str) -> List[List]:
        """Procesa una sección específica de los datos."""
        if section_key not in self.data:
            raise KeyError(f"Sección '{section_key}' no encontrada en los datos")
        
        section_data = self.data[section_key]
        processed_data = []
        errors_count = 0
        
        for i, array in enumerate(section_data):
            if len(array) < 4:
                print(f"Advertencia: Array {i} tiene menos de 4 elementos")
                continue
            
            equation, error_msg = self.process_equation(array[0])
            
            if error_msg:
                print(f"Error procesando ecuación {i}: {array[0]}")
                print(f"  Error: {error_msg}")
                errors_count += 1
            
            processed_array = [equation, array[1], array[2], array[3]]
            processed_data.append(processed_array)
        
        print(f"Procesamiento completado: {errors_count} errores de {len(section_data)} ecuaciones")
        return processed_data
    
    def create_dataframe(self, processed_data: List[List]) -> pd.DataFrame:
        """Crea un DataFrame de pandas con los datos procesados."""
        table_data = []
        
        for i, array in enumerate(processed_data):
            row = {
                'Index': i,
                'Equation': str(array[0]),
                'Error': array[1],
                'Predicted': array[2], 
                'Target': array[3]
            }
            table_data.append(row)
        
        return pd.DataFrame(table_data)
    
    def display_results(self, df: pd.DataFrame) -> None:
        """Muestra los resultados en formato de tabla con estadísticas."""
        print("Tabla de ecuaciones y valores del Modelo Estándar:")
        print("=" * 80)
        print(df.to_string(index=False))
        print(f"\nTotal de ecuaciones procesadas: {len(df)}")
        
        # Mostrar estadísticas básicas de los valores numéricos
        numeric_cols = ['Error', 'Predicted', 'Target']
        if all(col in df.columns for col in numeric_cols):
            print("\nEstadísticas de los valores:")
            print(df[numeric_cols].describe())
        
        # Análisis adicional
        if 'Error' in df.columns and 'Target' in df.columns:
            df['Relative_Error'] = abs(df['Error']) / abs(df['Target']) * 100
            print(f"\nError relativo promedio: {df['Relative_Error'].mean():.2f}%")


def main():
    """Función principal del programa."""
    try:
        # Crear procesador y procesar datos
        processor = StandardModelProcessor('standard_model_snippets.json.gz')
        processed_data = processor.process_data_section('7')
        
        # Crear y mostrar tabla
        df = processor.create_dataframe(processed_data)
        processor.display_results(df)
        
    except Exception as e:
        print(f"Error en la ejecución principal: {e}")


if __name__ == "__main__":
    main()