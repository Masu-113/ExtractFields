"""
El siguiente script utiliza una plantilla de PDF con campos de formulario *detectables* y un archivo .csv
para generar múltiples documentos PDF que aún puede ser editados antes de ser imprimidos.
"""

import logging
import re
import csv
from fillpdf import fillpdfs
from typing import Literal
import argparse
import os


# Preparando los argumentos del script y su descripción
SCRIPT_DESCRIPTION = """
El siguiente script utiliza una plantilla de PDF con campos de formulario *detectables* y un archivo .csv
para generar múltiples documentos PDF que aún puede ser editados antes de ser imprimidos.

Se requiere de un archivo de plantilla PDF y opcionalmente se puede brindar la ruta de una carpeta para los resultados generados.

*Por defecto se genera un archivo .log en la raíz de la ejecución del script.

E.g.:

python main.py --pdf_template="local/new-form-test.pdf" --csv_file="local/test_data.csv" --pdf_output_dir="resultados"
"""

def template_file_exists(filepath: str):
    try:
        if not os.path.exists(filepath):
            raise argparse.ArgumentTypeError("El archivo de plantilla PDF debe tener una ruta válida")
        return filepath
    except argparse.ArgumentTypeError as e:
        raise argparse.ArgumentTypeError("El archivo de plantilla PDF debe tener una ruta válida")
    except Exception as e:
        print("Unexpected error: {}".format(e))

def getOBCheckDict(numberOfBand: int) -> dict:
    """
    Esta función se encarga de elegir cuál checkbox hay que marcar en el documento PDF.
    
    Las bandas significan:

    - 2: 5.150-5.250
    - 3: 5.250-5.350
    - 4: 5.470-5.725
    - 5: 5.725-5.850
    """
    outputDict = {}
    match numberOfBand:
        case 2:
            outputDict["þÿ\x00C\x00a\x00s\x00i\x00l\x00l\x00a\x00 \x00d\x00e\x00 \x00v\x00e\x00r\x00i\x00f\x00i\x00c\x00a\x00c\x00i\x00ó\x00n\x006"] = "Yes"
        case 3:
            outputDict["þÿ\x00C\x00a\x00s\x00i\x00l\x00l\x00a\x00 \x00d\x00e\x00 \x00v\x00e\x00r\x00i\x00f\x00i\x00c\x00a\x00c\x00i\x00ó\x00n\x007"] = "Yes"
        case 4:
            outputDict["þÿ\x00C\x00a\x00s\x00i\x00l\x00l\x00a\x00 \x00d\x00e\x00 \x00v\x00e\x00r\x00i\x00f\x00i\x00c\x00a\x00c\x00i\x00ó\x00n\x005"] = "Yes"
        case 5:
            outputDict["þÿ\x00C\x00a\x00s\x00i\x00l\x00l\x00a\x00 \x00d\x00e\x00 \x00v\x00e\x00r\x00i\x00f\x00i\x00c\x00a\x00c\x00i\x00ó\x00n\x008"] = "Yes"
    return outputDict

def  getATCheckDict (antennaType: int, apertura: str = "") -> dict:
    outputType = {}
    match antennaType:
        case 2:
           outputType["þÿ\x00C\x00a\x00s\x00i\x00l\x00l\x00a\x00 \x00d\x00e\x00 \x00v\x00e\x00r\x00i\x00f\x00i\x00c\x00a\x00c\x00i\x00ó\x00n\x001\x003"] = "Yes"
        case 3:
            outputType["þÿ\x00C\x00a\x00s\x00i\x00l\x00l\x00a\x00 \x00d\x00e\x00 \x00v\x00e\x00r\x00i\x00f\x00i\x00c\x00a\x00c\x00i\x00ó\x00n\x001\x002"] = "Yes"
            if apertura:
                outputType["Texto43"] = apertura
    return outputType


def getCoordValues(coordinates: str) -> list:
    """
    Función para extraer los 3 valores correspondientes a una coordenada: Grados, minutos y segundos.

    E.g.:

    getCoordValues(\'85°53'48"O\') = [85, 53, 48]
    """
    outputCoords = []
    regexPattern = r"\d+(?:\.\d+)?"
    match = re.findall(pattern=regexPattern, string=coordinates.strip())
    if match:
        outputCoords = match
    return outputCoords

def getCoordDict(coordinates: str, mode: Literal["lat_d", "lon_d", "lat_o", "lon_o"]) -> dict:
    """
    Esta función utiliza una coordenada en el formato de grados, minutos y segundos; luego, devuelve
    un diccionario con los valores en base a los campos a rellenar en el formulario.

    E.g.:

    getCoordDict(\'85°53'48"O\', mode="lon_o") = {"Texto22": "85", "Texto23": "53", "Texto24": "48"}
    """
    outputValues = {}
    coordValues = getCoordValues(coordinates)
    match mode:
        case "lat_o":
            outputValues = {
                "Texto19": coordValues[0],
                "Texto20": coordValues[1],
                "Texto21": coordValues[2]
            }
        case "lon_o":
            outputValues = {
                "Texto22": coordValues[0],
                "Texto23": coordValues[1],
                "Texto24": coordValues[2]
            }
        case "lat_d":
            outputValues = {
                "Texto35": coordValues[0],
                "Texto34": coordValues[1],
                "Texto33": coordValues[2]
            }
        case "lon_d":
            outputValues = {
                "Texto32": coordValues[0],
                "Texto31": coordValues[1],
                "Texto30": coordValues[2]
            }
    return outputValues

parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
# parser.add_argument('positional_arg', help='A positional argument')
parser.add_argument('--pdf_template', required=True, type=template_file_exists,help="Ruta de archivo de plantilla PDF a usar.")
parser.add_argument('--csv_file', required=True, type=template_file_exists,help="Ruta de archivo CSV a utilizar.")
parser.add_argument('--pdf_output_dir', default="results2", help="Carpeta donde se guardarán los resultados generados")

args = parser.parse_args()

if __name__ == "__main__":
    # Configuración de logger
    logging.basicConfig(
        format="%(asctime)-5s %(name)-3s:%(levelname)-8s:: %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler("main.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Iniciando script")
    if os.path.exists(args.pdf_output_dir):
        logging.info("Ya existe un directorio de resultados con ese nombre, se sobreescribirán los archivos")
    else:
        logging.info("Creando directorio de resultados")
        os.makedirs(args.pdf_output_dir)
    logging.info("Obteniendo datos del CSV: {}".format(args.csv_file))
    with open(args.csv_file, "r", encoding="utf-8") as csvFile:
        csvData = csv.reader(csvFile, delimiter=";")
        for row in csvData:
            numOfData  = int(row[0])
            lat_o_data = getCoordDict(row[4], mode="lat_o")
            lon_o_data = getCoordDict(row[3], mode="lon_o")
            lat_d_data = getCoordDict(row[6], mode="lat_d")
            lon_d_data = getCoordDict(row[5], mode="lon_d")
            freqBand   = getOBCheckDict(int(row[22]))
            typeAntena = getATCheckDict(int(row[22]), apertura = row[12].strip())    
            # Verificando si alguna coordenada no se leyó correctamente
            if len(lat_o_data) != 3:
                logging.critical("File Numbered {}: Error con Latitud de Origen")
            if len(lon_o_data) != 3:
                logging.critical("File Numbered {}: Error con Longitud de Origen")
            if len(lat_d_data) != 3:
                logging.critical("File Numbered {}: Error con Latitud de Destino")
            if len(lon_d_data) != 3:
                logging.critical("File Numbered {}: Error con Longitud de Destino")
            # Formando el diccionario para generar cambios en el pdf
            changes = {
                "Texto18": row[1].strip(),
                "Texto36": row[2].strip(),
                **lat_o_data,
                **lon_o_data,
                **lat_d_data,
                **lon_d_data,
                **freqBand,
                **typeAntena,
                "Texto26": row[11].strip(), #ASNMO
                "Texto27": row[8].strip(), #direccion de punto inicio
                "Texto28": row[11].strip(),  #ASNMF
                "Texto37": row[9], #direccion de punto final
                #-- CARACTERISTICAS DEL EQUIPO --
                "Texto39": row[13].strip(), #MARCA
                "Texto40": row[10].strip(), #MODELO
                #"Texto41":  POTENCIA
                #"Texto42":  TIPO MODULACION
                #-- CARACTERISTICAS DE ANTENA --
                #"Texto43":  ANGULO DE APERTURA
                #"Texto44":  GANANCIA
                #"Texto45":  POLARIZACION
                #"Texto46":  MODELO
                #"Texto47":  MARCA
                #"Texto48":  comentario
                #"Texto48": row[10].strip()
            }
            try:
                fillpdfs.write_fillable_pdf(
                    input_pdf_path=args.pdf_template,
                    output_pdf_path=os.path.join(args.pdf_output_dir, "output_{:0=4}.pdf".format(numOfData)),
                    data_dict=changes
                )
                logging.info("File Numbered {}: OK".format(numOfData))
            except Exception as e:
                logging.error("PDF generation failed for file numbered: {}".format(numOfData))
        logging.info("Script Ended")