#Importamos nuestra notacion postfijo
from . import postfix_notation

#La funcion se utiliza para precesar una consulta booleana en notacion infija y evaluarla en notacion polaca inversa
def query(dictionary_stems, raw_query, path_files):
    #convertimos la consulta infija en notacion polaca inversa y la guardamos en postfix
    postfix = postfix_notation.postfix(raw_query)
    #retornamos  la consulta evaluada en notacion polaca inversa
    return evaluate_query(postfix, dictionary_stems, path_files)

#Esta funcion evalua la consulta en notacion polaca inversa
def evaluate_query(stemmed_query, data_dictionary, list_of_files):
    #Nos aseguramos que sea una lista stemmed_query (consulta en notación polaca inversa)
    assert isinstance(stemmed_query, list)
    list_of_files = set(list_of_files)
    operators = ["!", "u", "n"]
    #Inicializa una pila para evaliar la consulta
    stack = []
    print(stemmed_query)
    #Iteramos en cada termino de la notacion ...
    for term in stemmed_query:
        #Si el termino no es un operador entonces es un stem
        if term not in operators:
            assert isinstance(data_dictionary[term], set)
            #Lo agregamos al tope de la pila el termino
            stack.append(data_dictionary[term])
        else:
            if term == "!":
                #Si es una negacion entonces aplicamos la funcion complement en el tope de la lista y se agrega el resultado a la pila
                stack.append(complement(stack.pop(), list_of_files))
            elif term == "u":
                #Si es una union entonces aplicamos la funcion union y lo mismo
                stack.append(union(stack.pop(), stack.pop()))
            elif term == "n":
                #Si es una interseccion entonces aplicamos la funcion intersect y lo mismo
                stack.append(intersect(stack.pop(), stack.pop()))
    return list(stack.pop())

#Funcion de union
def union(A, B):
    return A.union(B)
#Funcion de interseccion

def intersect(A, B):
    return A.intersection(B)

#Funcion de negacion
def complement(A, universe):
    return set(universe).difference(A)
