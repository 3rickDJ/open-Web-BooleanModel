#Importamos las librerias necesarias
import nltk
from nltk.stem import SnowballStemmer
import re
import unidecode
nltk.download('snowball_data', quiet=True) # Snowball stemmer data

#Funcion para notacion polaca inversa
def inverse_polish(query):
    #En query guardamos el resultado de aplicarle la funcion a query (por el usuario)
    query = clean_query(query)
    #Operadores para las consultas "!" = negacion , "u" = union, "n"= interseccion, los "()" son utilizados para los operadores es decir !(Hola) 
    operators = ["!", "u", "n", "(", ")"]
    #Capturamos los operadores y palabras (caracteres alfanumericos)
    pattern = r'([()!un])|(\b\w+\b)'
    #Encontramos todas las coincidencias del pattern en la cadena query, devolviendo tuplas con operadores o palabras
    matches = re.findall(pattern, query)
    #Seleccionamos el primer elemento si está presente (un operador) o el segundo elemento si el primer elemento está ausente (una palabra).
    #Esto convierte las tuplas de operadores y palabras en una lista mixta de operadores y palabras.
    query = [match[0] or match[1] for match in matches]
    #Aqui almacenamos la expresion en notacion polaca inversa
    polish = []
    #Lista para almacenar datos auxilares para la conversion de la notacion
    queue = []
    for i in query:
        # si es ) sacar de queue y meter en polish hasta encontrar (
        if i == ")":
            op = queue.pop()
            #Mientras que op sea diferente de ( 
            while op != "(":
                #Añadimos a la lista polish los elementos
                polish.append(op)
                #Eliminamos (y retornamos) el ultimo elemento de la lista 
                op = queue.pop()
        # si es operador meter en queue
        elif i in operators:
            queue.append(i)
        # si es otro meter en polish
        else:
            polish.append(i)

    # Añadimos el ultimo operando al finalizar si la expresion no esta encerrada por parentesis
    if queue:
        polish.append(queue.pop())
    return polish

#Aplicamos el proceso de stemming a la lista en notacion polaca inversa
def stem_polish_query(polish):
    stemmer = SnowballStemmer("spanish")
    #Recorremos cada elemento en la lista polish
    for i, term in enumerate(polish):
        #Si nuestro termino no es un operador logico
        if term not in ["!", "u", "n"]:
            #Aplicamos el stemming a ese elemento
            polish[i] = stemmer.stem(term)
    return polish
#convertimos la consulta infija en notacion polaca inversa
def postfix(query):
    return stem_polish_query(inverse_polish(query))

def clean_query(raw_query):
    # Removemos acentos
    # Descomponemos simbolos Unicode
    decomposed_string = unidecode.unidecode(raw_query)
    #Removemos signos de puntacion
    pattern = r'[^a-zA-Z()!un]'
    no_punctuation_string = re.sub(pattern, ' ', decomposed_string)
    # Eliminamos los espacios en blanco al inicio y final con strip y convertimos los caracteres a minusculas
    return no_punctuation_string.strip().lower()

