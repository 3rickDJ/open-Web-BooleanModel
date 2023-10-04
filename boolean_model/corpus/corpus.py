from .index import index
from .data_preprocessing import process_text
import os
from itertools import chain

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

#Funcion para leer el corpus desde la ruta dada
def read_corpus(path):
    # Asignamos los datos a las variables
    files, corpus, stems = read_data(path)
    #Verifica que corpus sea una lista de instancias de process_data
    assert isinstance(corpus, list), "The corpus must be a list of process_data instances."
    #Verifica que files sea una lista de cadenas que representan rutas de archivos
    assert isinstance(files, list), "The files must be a list of strings path to files."
    #Verifica que el primer elemento de corpus sea una instancia de process_data
    assert isinstance(corpus[0], process_text.ProcessData), "The corpus must be a list of process_data instances."
    #crea un índice invertido del corpus utilizando los términos derivados y los documentos del corpus.
    dictionary = index.index(stems, corpus)
    # Return the corpus.
    return dictionary, files

# Leemos los datos de la ruta dada
def read_data(path):
    files = read_file_paths(path)
    corpus = concurrent_read(files)
    stems = set( chain.from_iterable( [ process_data.get_stems() for process_data in corpus ] ) )
    tokens = collect_tokens(corpus)
    terms = collect_terms(corpus)
    write("tokens.txt", "\n".join(tokens))
    write("terms.txt", "\n".join(terms))
    write("stems.txt", "\n".join(stems))
    # Crea una matriz de presencia usando los términos derivados y el corpus.
    presence_matrix = index.presence_matrix(corpus, stems)
    # Guardamos la matriz de presencia en un archivo "presence_matrix.csv"
    write_matrix("presence_matrix.csv", presence_matrix)

    # Return the corpus.
    return files, corpus, stems

#Funcion para leer los archivos dados, en paralelo devolviendo una lista de estancias
def concurrent_read(files):
    with ThreadPoolExecutor(max_workers=len(files)) as executor:
        corpus = executor.map(lambda file: process_text.ProcessData(file), files)
        return list(corpus)

#Calcula los stems para cada documento en paralelo, deolviendolos para cada documento
def concurrent_stems(corpus):
    with ProcessPoolExecutor() as executor:
        stems = executor.map(get_stem_instance, corpus)
        return list(stems)

#Obtiene los stems de un objeto
def get_stem_instance(process_data):
    return process_data.get_stems()

#Actuliza los stems en el corpus con la list_stems
def update_corpus_stems(corpus, list_stems):
    for process_data, stems in zip(corpus, list_stems):
        process_data.stems = stems

#Lee las rutas de los archivos y devuelva una lista de rutas
def read_file_paths(path):
    # Read the file paths from the given path.
    return [ os.path.join(path, file) for file in os.listdir(path) ]

#Guarda la matriz en un archivo CSV en la ruta especificada
def write_matrix(path, matrix):
    with open(path, "w") as file:
        for row in matrix:
            file.write(",".join([ str(value) for value in row ]) + "\n")

#Recopila todos los tokens de texto de los documentos en el corpus y devuelve un conjunto de tokens únicos.
def collect_tokens(corpus):
    tokens = set(chain.from_iterable([ process_data.tokens for process_data in corpus ]))
    return tokens

#Recopila todos los términos de texto de los documentos en el corpus y devuelve un conjunto de términos únicos.
def collect_terms(corpus):
    terms = set(chain.from_iterable([ process_data.terms for process_data in corpus ]))
    return terms

#Recopila todos los stems de los documentos en el corpus y devuelve un conjunto de términos únicos.
def collect_stems(corpus):
    stems = set(chain.from_iterable([ process_data.stems for process_data in corpus ]))
    return stems

#Escribe el contenido en un archivo en la ruta especificada.
def write(path, content):
    with open(path, "w") as file:
        file.write(content)
