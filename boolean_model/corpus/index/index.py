#Importamos nuesta tabla hash
from .hash_table import HashTable
#Crearemos un indice invertido para los terminos stems en el corpus
def index(stems, corpus):
    # Indexa el corpus dado
    dictionary = HashTable()
    #Iteramos en cada termino stem
    for stem in stems:
        #Si el termino esta presente en el documento se añade la ruta del documento a la lista
        dictionary[stem] = set( [ process_data.path for process_data in corpus if stem in process_data.stems ] )
    # Devolvemos el diccionario con el indice invertido
    return dictionary

#Generamos una matriz de presencia o ausencia para los terminos stems en el corpus
def presence_matrix(corpus, stems):
    stems = list(stems)
    # Creamos la matriz con la primera fila que contiene los terminos stems
    matrix = [['documento'] + stems]
    #Para cada documento en el corpus creamos una fila
    for process_data in corpus:
        #Si esta presente el termino entonces colocamos un 1 si no un 0
        matrix.append([process_data.name] + [ "YES" if stem in process_data.stems else "NO" for stem in stems ] )
    # Devolvemos la matriz
    return matrix
