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

# Determinar la carpeta donde se encuentran los archivos XML
if os.path.exists('vertical'):
    folder_path = 'vertical/'
else:
    folder_path = './'

# Definir la palabra clave a buscar
nombre_xblock_buscado = 'dialogsquestionsxblock'

# Lista para almacenar los datos
data = []

# Recorre los archivos XML en la carpeta
max_title_length = 0
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        xml_file = os.path.join(folder_path, filename)
        title = extract_title(xml_file)
        if title is not None:
            max_title_length = max(max_title_length, len(title))
            keyword_ids = find_keyword(xml_file, nombre_xblock_buscado)
            if keyword_ids:
                row_data = {'Nombre': title}
                for i, keyword_id in enumerate(keyword_ids, start=1):
                    row_data[f'ID {i} [{nombre_xblock_buscado}]'] = keyword_id
                data.append(row_data)

# Convertir la lista de diccionarios a un DataFrame de Pandas
df = pd.DataFrame(data)

# Ajustar el ancho de la columna 'Nombre' al tamaño del texto más largo
column_widths = {'Nombre': max_title_length}
df_widths = pd.DataFrame(column_widths, index=[0])
df = pd.concat([df_widths, df], ignore_index=True)

# Guardar el DataFrame en un archivo Excel
df.to_excel('resultados.xlsx', index=False)
print("Resultados guardados en 'resultados.xlsx'")
