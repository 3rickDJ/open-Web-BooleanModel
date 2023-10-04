from boolean_model.corpus import corpus
from boolean_model.query import query

class BooleanModel:
    def __init__(self, path=None):
        #Si se proporciono una ruta para el archivo entonces si se ejecutara el codigo
        if path:
            self.load_corpus(path)
            self.path = path

    def query(self, raw_query):
        #Retornamos la lista de documentos que satisfagan a la consulta realizada por el usuario
        return query.query(self.dictionary_stems, raw_query, self.path_files)

    def load_corpus(self, path):
        self.path = path
        # Leemos el corpus
        #Almacenamos en dictionary_stems el diccionario recuperado de los stems->documents
        # Almacenamos en path_files la lista recuperada de rutas a los documentos
        self.dictionary_stems, self.path_files = corpus.read_corpus(path)
