import os
import re
import pandas as pd

# Función para extraer el título de un archivo XML
def extract_title(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        match = re.search(r'display_name="([^"]+)"', first_line)
        if match:
            return match.group(1)
    return None

# Función para extraer el título y ID de un archivo XML
def extract_title_and_id(xml_file):
    results = []
    with open(xml_file, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'display_name="([^"]+)"', line)
            if match:
                display_name = match.group(1)
                if len(display_name) > 100:
                    # Buscar el ID del bloque
                    id_match = re.search(r'url_name="([^"]+)"', line)
                    block_id = id_match.group(1) if id_match else "No ID found"
                    results.append({
                        'display_name': display_name,
                        'block_id': block_id
                    })
    return results

# Determinar la carpeta donde se encuentran los archivos XML
if os.path.exists('vertical'):
    folder_path = 'vertical/'
else:
    folder_path = './'

# Lista para almacenar los datos
data = []

# Recorre los archivos XML en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        xml_file = os.path.join(folder_path, filename)
        title = extract_title(xml_file)
        if title is not None:
            results = extract_title_and_id(xml_file)
            for result in results:
                data.append({
                    'Nombre': title,
                    'ID del Bloque': result['block_id'],
                    'Display Name': result['display_name']
                })

# Convertir la lista de diccionarios a un DataFrame de Pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
df.to_excel('resultados_nombreslargos.xlsx', index=False)
print("Resultados guardados en 'resultados_nombreslargos.xlsx'")
