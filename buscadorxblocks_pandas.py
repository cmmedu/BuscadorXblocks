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

# Función para buscar y contar la palabra clave
def find_keyword(xml_file, nombre_xblock_buscado):
    keyword_ids = []
    keyword_found = False
    with open(xml_file, 'r', encoding='utf-8') as file:
        for line in file:
            if nombre_xblock_buscado in line:
                match = re.search(r'url_name="([^"]+)"', line)
                if match:
                    keyword_ids.append(match.group(1))
                if not keyword_found:
                    keyword_found = True
    return keyword_ids

# Carpeta donde se encuentran los archivos XML
folder_path = './'  # Cambia esto a la ubicación de tu carpeta

# Definir la palabra clave a buscar
nombre_xblock_buscado = 'dialogsquestionsxblock'

# Crear un DataFrame para almacenar los resultados
data = {'Nombre': [], 'ID [' + nombre_xblock_buscado + '] encontrados': []}

# Recorre los archivos XML en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        xml_file = os.path.join(folder_path, filename)
        title = extract_title(xml_file)
        if title is not None:
            keyword_ids = find_keyword(xml_file, nombre_xblock_buscado)
            if keyword_ids:
                data['Nombre'].append(title)
                data['ID [' + nombre_xblock_buscado + '] encontrados'].append(', '.join(keyword_ids))

# Convertir el diccionario a un DataFrame de Pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
df.to_excel('resultados.xlsx', index=False)
print("Resultados guardados en 'resultados.xlsx'")
