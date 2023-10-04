#Importamos las librerias necesarios para leer los documentos y el texto en UNICODE
import re #regex
import unicodedata 
import fitz
#Funcion para leer el contendio de la ruta dada por el usuario
def read_content(path):
    #Si el documento termina con pdf entonces ocupamos la funcion read_pdf
    if path.endswith('.pdf'):
        return read_pdf(path)
    #Si no es un archivo con terminacion txt y ocuparemos la funcion read_txt
    elif path.endswith('.txt'):
        return read_txt(path)
    #Algun otro archivo no lo leeremos
    else:
        raise Exception('Tipo de archivo de soportado.')
    
#Leer archivos txt
def read_txt(path):
    #Abrimos el archivo en modo lectura
    with open(path, 'r') as file:
        #Leemos el contenido lo devolvemos como una cadena de texto
        return file.read()

#Leer achivos pdf
def read_pdf(path):
    #Ocupamos la libreria fitz para su lectura
    file = fitz.open(path)
    #Creamos una lista para obtener el texto
    content = []
    #Iteramos en cada pagina de nuestro archivo
    for page in file:
        #Agregamos el contenido de cada pagina a la lista
        content.append(page.get_text())
    #Retornamos el contenido de todas las paginas unidas en una solca cadena de texto
    return ''.join(content)

def clean_content(content):
        # Removemos los acentos
        #Descomponemos los simbolos Unicode
        normalized_string = unicodedata.normalize('NFKD',  content)
        #Si un glyhp esta compuesto, usaremos la forma base 
        no_composed_string = ''.join([c for c in normalized_string if not unicodedata.combining(c)])
        # Removemos signos de puntuacion
        no_punctuation_string = re.sub(r'[^\w]+', ' ', no_composed_string)
        # Eliminamos los espacios en blanco al inicio y final con strip y convertimos los caracteres a minusculas
        return no_punctuation_string.strip().lower()

class Document:
    def __init__(self, path_to_doc):
        #Guardamos la ruta del documento como un atributo de referencia
        self.path = path_to_doc
        # Llamamos a la funcion read_content (para leer el contenido), luego a clean_content (para limpiar el documento de caracteres especiales)
        #Y lo asignamos a sel.content
        self.content = clean_content( read_content(self.path) )
