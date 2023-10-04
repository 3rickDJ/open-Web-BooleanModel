# Capacidad para el arreglo interno
INITIAL_CAPACITY = 5081

# Node data structure - essentially a LinkedList node
class Node:
  def __init__(self, key, value):
    self.key = key
    self.value = value
    self.next = None
  def __str__(self):
    return "<Node: (%s, %s), next: %s>" % (self.key, self.value, self.next != None)
  def __repr__(self):
    return str(self)
  
# Tabla hash con encadenamiento separado
class HashTable:
  # Inicializar la tabla hash
  def __init__(self):
    self.capacity = INITIAL_CAPACITY
    self.size = 0
    self.buckets = [None]*self.capacity

  def __str__(self):
    return "<HashTable: capacity=%d, size=%d>" % (self.capacity, self.size)
  def __repr__(self):
    return str(self)

  # Generar un hash para una key
  # Entrada:  key - string
  # Salida: Indice desde 0 hasta self.capacity
  def hash(self, key):
    hashsum = 0
    #Para cada caracter en la llave
    for idx, c in enumerate(key):
      # Sumamos el (indice + longitud de la key) ^ (codigo char actual)
      hashsum += (idx + len(key)) ** ord(c)
      # Realizar modulo para mantener la suma hash en el rango [0, self.capacity - 1]
      #Es decir para evitar muchas colisiones
      hashsum = hashsum % self.capacity
    return hashsum

  def __setitem__(self, key, value):
    self.insert(key, value)

  # Insertamos una key, calor par para la tabla hash
  # Entrada:  key - string
  #       value - anything
  # Salida: void
  def insert(self, key, value):
    # 1. Incrementamos el tamaño en +1
    self.size += 1
    # 2. Calcular el índice de la key
    index = self.hash(key)
    # Nos dirigimos al nodo correspondiente a la tabla
    node = self.buckets[index]
    # 3. Si bucket esta vacio:
    if node is None:
      # Creamos un nodo, lo añadimos y lo retornamos
      self.buckets[index] = Node(key, value)
      return
    # 4. Iterar hasta el final de la lista enlazada en el índice proporcionado
    prev = node
    while node is not None:
      prev = node
      node = node.next
    # Añadimos un nuevo nodo al final de la lista con la key/valor proporcionado
    prev.next = Node(key, value)

  def __getitem__(self, key):
    return self.find(key)

  # Buscar un valor basados en una key
  # Entrada:  key - string
  # SALIDA: Valor almacenado en key o None si no se encontro
  def find(self, key):
    # 1. Calcukar hash
    index = self.hash(key)
    # 2. Vamos al primer nodo de la lista en bucket
    node = self.buckets[index]
    # 3. Recorremos la lista enlazada en este nodo
    while node is not None and node.key != key:
      node = node.next
    # 4. Ahora nodo es el par key/valor solicitado o None
    if node is None:
      # Si nodo es vacio entonces retornamos nada
      return set()
    else:
      # Si lo encontramos entonces regresamos el valor del nodo (datos)
      return node.value

  # Eliminar un nodo almacenado en una key
  # Entarda:  key - string
  # Salida: Datos eliminados o None si no se encontro
  def remove(self, key):
    # 1. Calculamos hash
    index = self.hash(key)
    node = self.buckets[index]
    prev = None
    # 2. Iteramos hasta el nodo solicitado
    while node is not None and node.key != key:
      prev = node
      node = node.next
    # Ahora el nodo es le nodo solicitado o si no en None
    if node is None:
      # 3. Si el nodo es None entonces no eliminamos nada
      return None
    else:
      # 4. Si se encontro la llave entonces
      #Reducimos el tamaño
      self.size -= 1
      #Asignamos el valor del nodo a result
      result = node.value
      # Borramos el elemento de la lista ligada
      if prev is None:
        # Puede ser None, o la siguiente coincidencia
        self.buckets[index] = node.next 
      else:
        # Conectamos la lista ligada con el valor correspondiente para no perder secuencia
        prev.next = prev.next.next 
      #Regresamos el valor del nodo resultante
      return result
