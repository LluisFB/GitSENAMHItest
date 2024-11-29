#ESTE CODIGO FUE ESCRITO PARA USARSE EN COLAB, PERO YA LO PUEDEN ADECUAR 
from google.colab import drive
import csv
drive.mount('/content/drive')


#EL ARCHIVO trujillo.txt ES SOLO UN COPIAR PEGAR DEL TEXT:LIST DE LA WEB DE LA UNIV, DE WYOMING,
#TAMBIEN LO AGREGARÉ AL GIT COMO REFERENCIA

#Abrir el excel de prensa de la SPM
# Define la ruta del archivo
file_path = '/content/drive/My Drive/Colab Notebooks/trujillo.txt'

#CODIGO PARA GENERAR LOS DATOS DE LOS NIVELES A PARTIR DEL ARCHIVO trujillo.txt
# Definir la función parse_sounding
def parse_sounding(input_txt, output_txt, output_csv):
    with open(input_txt, 'r') as f:
        lines = f.readlines()

    # Encontrar la sección de los datos atmosféricos
    data_started = False
    data_lines = []

    for line in lines:
        if line.strip() == "-----------------------------------------------------------------------------":
            data_started = True
        elif data_started:
            if line.strip() == "":
                break  # Terminó la sección de datos
            else:
                data_lines.append(line.strip())

    # Procesar los datos de cada línea
    processed_data = []
    for line in data_lines:
        parts = line.split()
        
        try:
            # Extraer los valores (presión, altura, temperatura, punto de rocío, humedad relativa, dirección y velocidad)
            PRES_hPa = float(parts[0])  # presión en hectopascales
            HGHT = float(parts[1])  # altura (no se necesita conversión)
            TEMP_C = float(parts[2])  # temperatura en grados Celsius
            DWPT_C = float(parts[3])  # punto de rocío en grados Celsius
            RELH = int(parts[4])  # humedad relativa
            DRCT = float(parts[6]) # dirección del viento en grados
            SKNT = float(parts[7]) # velocidad del viento en nudos

            # Convertir la presión de hPa a Pa
            PRES = PRES_hPa * 100

            # Convertir temperaturas de Celsius a Kelvin y nudos a metros/segundo
            TEMP_K = TEMP_C + 273.15
            DWPT_K = DWPT_C + 273.15
            SKNT_MS = SKNT * 0.5144

            # Los valores no conocidos se reemplazan por -888888.00000
            W_U = -888888.00000
            W_V = -888888.00000
            THICK = -888888.00000

            # Formatear la línea para Little_R
            formatted_line = [
                f"{PRES:13.5f}",
                "      0",
                f"{HGHT:13.5f}",
                "      0",
                f"{TEMP_K:13.5f}",
                "      0",
                f"{DWPT_K:13.5f}",
                "      0",
                f"{SKNT_MS:13.5f}",
                "      0",
                f"{DRCT:13.5f}",
                "      0",
                f"{W_U:13.5f}", #VIENTO U
                "      0",
                f"{W_V:13.5f}", #VIENTO V
                "      0",
                f"{RELH:13.5f}", 
                "      0",
                f"{THICK:13.5f}", #THICKNESS
                "      0",
            ]
            processed_data.append(formatted_line)
        except ValueError:
            continue  # Si la línea no tiene suficientes datos, se omite

    # Guardar los datos procesados en el archivo de texto
    with open(output_txt, 'w') as f:
        for line in processed_data:
            f.write(''.join(line) + '\n')


# Uso de la función para procesar el archivo
output_txt = '/content/drive/My Drive/Colab Notebooks/sounding_output.txt'
parse_sounding(file_path, output_txt, output_csv)


#AHORA TENEMOS QUE GENERAR LA CABECERA, ESTA SE HACE A PARTIR DE LA CABECERA DE EJEMPLO DE LA WEB
#POR LO QUE PRIMERO ESTOY SEPARANDO LOS CAMPOS DE LA CABECERA PARA ENTENDER MEJOR SU ESTRUCTURA

# Cabecera de ejemplo
header = ("            39.78000          -104.8600072469                                   "
          "DENVER/STAPLETON INT., CO. / U.S.A.     FM-35 TEMP                              "
          "GTS (ROHK) UKUS09 KWBC 051200 RRA                 1626.00000         1   "
          "-888888   -888888       890   -888888         T         F         F   "
          "-888888   -888888      20080205120000-888888.00000      0-888888.00000      0"
          "-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0"
          "-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0"
          "-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0")

# Definición de los campos con sus posiciones y longitudes
fields = [
    ("Latitude", 0, 20),                # F20.5
    ("Longitude", 20, 40),              # F20.5
    ("ID", 40, 80),                     # A40
    ("Name", 80, 120),                  # A40
    ("Platform", 120, 160),             # A40
    ("Source", 160, 200),               # A40
    ("Elevation", 200, 220),            # F20.5
    ("Valid_fields", 220, 230),         # I10
    ("Num_errors", 230, 240),           # I10
    ("Num_warnings", 240, 250),         # I10
    ("Sequence_number", 250, 260),      # I10
    ("Num_duplicates", 260, 270),       # I10
    ("Is_sounding", 270, 280),          # L (10 caracteres)
    ("Is_bogus", 280, 290),             # L (10 caracteres)
    ("Discard", 290, 300),              # L (10 caracteres)
    ("Unix_time", 300, 310),            # I10
    ("Julian_day", 310, 320),           # I10
    ("Date", 320, 340),                 # A20
    ("SLP_QC", 340, 360),               # F13.5 + I7
    ("Ref_Pressure_QC", 360, 380),      # F13.5 + I7
    ("Ground_Temp_QC", 380, 400),       # F13.5 + I7
    ("SST_QC", 400, 420),               # F13.5 + I7
    ("SFC_Pressure_QC", 420, 440),      # F13.5 + I7
    ("Precip_QC", 440, 460),            # F13.5 + I7
    ("Daily_Max_T_QC", 460, 480),       # F13.5 + I7
    ("Daily_Min_T_QC", 480, 500),       # F13.5 + I7
    ("Night_Min_T_QC", 500, 520),       # F13.5 + I7
    ("3hr_Pres_Change_QC", 520, 540),   # F13.5 + I7
    ("24hr_Pres_Change_QC", 540, 560),  # F13.5 + I7
    ("Cloud_Cover_QC", 560, 580),       # F13.5 + I7
    ("Ceiling_QC", 580, 600),           # F13.5 + I7
    ("Precipitable_Water_QC", 600, 620) # F13.5 + I7
]

# Extraer los campos
parsed_data = {}
for field_name, start, end in fields:
    value = header[start:end]
    parsed_data[field_name] = value.strip()

# Mostrar el resultado
for field, value in parsed_data.items():
    print(f"{field}:{value}")

#lUEGO ES IMPORTANTE EXTRAER LOS DATOS QUE IRAN EN LA CABECERA, DEL ARCHIVO trujillo.txt

import re

# Ruta del archivo de texto
file_path = '/content/drive/My Drive/Colab Notebooks/trujillo.txt'

# Leer el archivo
with open(file_path, 'r') as file:
    data = file.read()

# Función para extraer información
def extraer_campos(data):
    campos = {}

    # ID y Nombre de la estación
    id_nombre = re.search(r'^(\d+)\s+([\w\s]+)\sObservations', data, re.MULTILINE)
    if id_nombre:
        campos['ID'] = id_nombre.group(1).strip()
        campos['Nombre'] = id_nombre.group(2).strip()

    # Latitud, Longitud, Elevación
    latitud = re.search(r'Station latitude:\s*([-\d.]+)', data)
    longitud = re.search(r'Station longitude:\s*([-\d.]+)', data)
    elevacion = re.search(r'Station elevation:\s*([-\d.]+)', data)

    if latitud:
        campos['Latitud'] = float(latitud.group(1))
    if longitud:
        campos['Longitud'] = float(longitud.group(1))
    if elevacion:
        campos['Elevación'] = float(elevacion.group(1))

    # Observation time
    obs_time = re.search(r'Observation time:\s*([\d/]+)', data)
    if obs_time:
        campos['Observation Time'] = obs_time.group(1)

    # Agua precipitable
    agua_precipitable = re.search(r'Precipitable water \[mm\] for entire sounding:\s*([\d.]+)', data)
    if agua_precipitable:
        campos['Agua Precipitable'] = float(agua_precipitable.group(1))

    return campos

# Extraer campos
campos_extraidos = extraer_campos(data)

# Imprimir resultados
for campo, valor in campos_extraidos.items():
    print(f"{campo}: {valor}")


#AHORA SI PODEMOS CREAR LA CABECERA O HEADER, USE UN PEQUEÑO ATAJO, PORQUE NO ME SALIA BIEN 
#LOS DATOS EXTRAIDOS DE TRUJILLO PARA QUE ENTREN EN LA CABECERA, POR LO QUE TUVE QUE VOLVER A 
#ESCRIBIRLO COMO UN NUEVO DICCIONARIO :'V


# Función para formatear valores
def formatear_valor(valor, tipo, longitud):
    if tipo == "F":
        # Ajustar para F20.5: 20 caracteres totales con 5 decimales
        return f"{float(valor):{longitud - 5}.{5}f}".rjust(longitud)
    elif tipo == "I":
        return f"{int(valor):{longitud}d}"
    elif tipo == "A":
        return f"{str(valor):<{longitud}}"
    elif tipo == "L":  # Texto lógico de longitud fija
        return f"{str(valor):>{longitud}}"
    else:
        raise ValueError("Tipo desconocido.")

# Datos de Trujillo
datos_trujillo = {
    "Latitude": -8.04,          # Latitud de Trujillo
    "Longitude": -79.06,        # Longitud de Trujillo
    "Elevation": 128.0,         # Elevación de Trujillo
    "Date": "20241127120000",   # Formato A20
}

# Variables editables para la cabecera
NAME = "TRUJILLO/MARTINEZ INT., LA LIB. / PERU"  # Editable
PLATFORM = "FM-35 TEMP"  # No cambiar
SOURCE = "GTS SENAMHI PERU"  # Editable

# Campos constantes de la cabecera
CONSTANT_FIELDS = {
    "Valid_fields": 1,
    "Num_errors": -888888,
    "Num_warnings": -888888,
    "Sequence_number": 890,
    "Num_duplicates": -888888,
    "Is_sounding": "T",
    "Is_bogus": "F",
    "Discard": "F",
    "Unix_time": -888888,
    "Julian_day": -888888,
    "SLP_QC": (-888888.0, 0),
    "Ref_Pressure_QC": (-888888.0, 0),
    "Ground_Temp_QC": (-888888.0, 0),
    "SST_QC": (-888888.0, 0),
    "SFC_Pressure_QC": (-888888.0, 0),
    "Precip_QC": (-888888.0, 0),
    "Daily_Max_T_QC": (-888888.0, 0),
    "Daily_Min_T_QC": (-888888.0, 0),
    "Night_Min_T_QC": (-888888.0, 0),
    "3hr_Pres_Change_QC": (-888888.0, 0),
    "24hr_Pres_Change_QC": (-888888.0, 0),
    "Cloud_Cover_QC": (-888888.0, 0),
    "Ceiling_QC": (-888888.0, 0),
    "Precipitable_Water_QC": (-888888.0, 0),
}

# Construcción de la cabecera
header = (
    formatear_valor(datos_trujillo["Latitude"], "F", 20)
    + formatear_valor(datos_trujillo["Longitude"], "F", 20)
    + formatear_valor("72469", "A", 40)  # ID (valor fijo)
    + formatear_valor(NAME, "A", 40)
    + formatear_valor(PLATFORM, "A", 40)
    + formatear_valor(SOURCE, "A", 40)
    + formatear_valor(datos_trujillo["Elevation"], "F", 20)
    + formatear_valor(CONSTANT_FIELDS["Valid_fields"], "I", 10)
    + formatear_valor(CONSTANT_FIELDS["Num_errors"], "I", 10)
    + formatear_valor(CONSTANT_FIELDS["Num_warnings"], "I", 10)
    + formatear_valor(CONSTANT_FIELDS["Sequence_number"], "I", 10)
    + formatear_valor(CONSTANT_FIELDS["Num_duplicates"], "I", 10)
    + formatear_valor(CONSTANT_FIELDS["Is_sounding"], "L", 10)
    + formatear_valor(CONSTANT_FIELDS["Is_bogus"], "L", 10)
    + formatear_valor(CONSTANT_FIELDS["Discard"], "L", 10)
    + formatear_valor(CONSTANT_FIELDS["Unix_time"], "I", 10)
    + formatear_valor(CONSTANT_FIELDS["Julian_day"], "I", 10)
    + formatear_valor(datos_trujillo["Date"], "A", 20)
    + "".join(
        formatear_valor(CONSTANT_FIELDS[campo][0], "F", 13)
        + formatear_valor(CONSTANT_FIELDS[campo][1], "I", 7)
        for campo in [
            "SLP_QC",
            "Ref_Pressure_QC",
            "Ground_Temp_QC",
            "SST_QC",
            "SFC_Pressure_QC",
            "Precip_QC",
            "Daily_Max_T_QC",
            "Daily_Min_T_QC",
            "Night_Min_T_QC",
            "3hr_Pres_Change_QC",
            "24hr_Pres_Change_QC",
            "Cloud_Cover_QC",
            "Ceiling_QC",
            "Precipitable_Water_QC",
        ]
    )
)

# Imprimir la cabecera resultante
print(header)


#////////////////////////////////////////////////////////////////////////////////////////////
#AHORA QUE YA TENEMOS DATOS Y CABECERA, PODEMOS JUNTARNOS EN UN SOLO ARCHIVO DE SALIDA


# Abrir el archivo existente y leer su contenido
file_path = '/content/drive/My Drive/Colab Notebooks/sounding_output.txt'

# Abrimos el archivo en modo lectura para obtener el contenido original
with open(file_path, 'r') as file:
    lines = file.readlines()

# Ahora abrimos el archivo en modo escritura, y escribimos la cabecera en la primera línea
with open('/content/drive/My Drive/Colab Notebooks/output_Little_R.txt', 'w') as output_file:
    # Escribir la cabecera como primera línea
    output_file.write(header + "\n")
    
    # Escribir el contenido original del archivo, manteniendo las líneas después de la cabecera
    output_file.writelines(lines)


#LISTO, EL ARCHIVO FINAL SE LLAMA output_Little_R.txt Y TIENE PRIMERO LA CABECERA, Y LUEGO LOS DATOS

