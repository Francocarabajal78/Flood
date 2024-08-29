import random


CELDA_VACIA = ' '

class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla.
        """
        self.alto = alto
        self.ancho = ancho
        self.tablero = []
        self.colores = []
        for fila in range(self.alto):
            self.tablero.append([])
            for columna in range(self.ancho):
                self.tablero[fila].append(0)



    def mezclar_tablero(self, n_colores):
        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Argumentos:
            n_colores (int): Cantidad maxima de colores a incluir en la grilla.
        """
        for i in range(n_colores):
            self.colores.append(i)
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero[fila])):
                self.tablero[fila][columna] = random.choice(self.colores)


    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.

        Devuelve:
            Color asignado.
        """
        return self.tablero[fil][col]


    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.
        La secuencia tendrá todos los colores posibles que fueron utilizados
        para generar el tablero, sin importar cuántos de estos colores queden
        actualmente en el tablero.

        Devuelve:
            iterable: secuencia ordenada de colores.
        """
        return self.colores


    def dimensiones(self):
        """
        Dimensiones de la grilla (filas y columnas)

        Devuelve:
            (int, int): alto y ancho de la grilla en ese orden.
        """
        return self.alto, self.ancho


    def _cambiar_color(self, fil, col, color_actual, color_nuevo):


        if fil < 0 or fil >= len(self.tablero) or col < 0 or col >= len(self.tablero[0]): #Si la posición está fuera de las dimensiones del tablero, corta la recursión
            return 
        
        if self.tablero[fil][col] != color_actual: #Cuando el color de un casillero vecino no coincide con el color actual del origen, corta el llamado recursivo
            return 

        self.tablero[fil][col] = color_nuevo #El color del casillero pasa a ser el nuevo


        self._cambiar_color(fil, col+1, color_actual, color_nuevo) #Recorre derecha
        self._cambiar_color(fil+1, col, color_actual, color_nuevo) #Recorre arriba
        self._cambiar_color(fil-1, col, color_actual, color_nuevo) #Recorre abajo
        self._cambiar_color(fil, col-1, color_actual, color_nuevo) #Recorre izquierda




    def cambiar_color(self, color_nuevo):
        
        color_actual_origen = self.obtener_color(0, 0)

        if color_actual_origen != color_nuevo: #Si el color del origen es distinto al color que se quiere cambiar se ejecuta el llamado recursivo
            self._cambiar_color(0, 0, color_actual_origen, color_nuevo)



    def verificar_mejor_opcion(self, fil, col, color_actual_origen, contador, casilleros_visitados):

        """
        Devuelve cuántos casilleros del mismo color tiene la isla principal del juego.
        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.
            color_actual_origen (int): color actual del origen del tablero.
            contador (int): contador de los casilleros del mismo color de la isla principal.
            casilleros_visitados (dic): verificador de los casilleros recorridos en los llamados recursivos.
        """


        if fil < 0 or fil >= len(self.tablero) or col < 0 or col >= len(self.tablero[0]): #Si la posición está fuera de las dimensiones del tablero, corta la recursión
            return 0

        
        if self.tablero[fil][col] != color_actual_origen: #Cuando el color de un casillero vecino no coincide con el color actual del origen, corta el llamado recursivo
            return 0

        if (fil, col) in casilleros_visitados: #Si la fila y la columna ya están en el verificador, corta los llamados recursivos
            return 0

        casilleros_visitados.add((fil, col))

        contador = 1

        contador += self.verificar_mejor_opcion(fil, col+1, color_actual_origen, contador, casilleros_visitados) #Recorre derecha
        contador += self.verificar_mejor_opcion(fil+1, col, color_actual_origen, contador, casilleros_visitados) #Recorre arriba
        contador += self.verificar_mejor_opcion(fil-1, col, color_actual_origen, contador, casilleros_visitados) #Recorre abajo
        contador += self.verificar_mejor_opcion(fil, col-1, color_actual_origen, contador, casilleros_visitados) #Recorre izquierda

        return contador



    def seleccionar_color(self):

        """
        Evalua con qué color la isla principal ocupa más casilleros y devuelve la mejor opción.
        Devuelve: (int) -> mejor opción de color.

        """
        
        valor_maximo = 0
        color_maximo = None

        for color in self.obtener_posibles_colores(): #Recorro los colores dentro de la lista y al tablero lo cambio con cada uno
            contador = 0
            casilleros_visitados = set() #verificador de casilleros recorridos
            
            clon = self.clonar() #Se clona el tablero para no afectar al original
            clon.cambiar_color(color) 
            color_actual_origen = clon.obtener_color(0, 0)

            contador = clon.verificar_mejor_opcion(0, 0, color_actual_origen, contador, casilleros_visitados)

            if contador >= valor_maximo:
                valor_maximo = contador
                color_maximo = color

        return color_maximo
        




    def clonar(self):
        """
        Devuelve:
            Flood: Copia del Flood actual
        """
        clon = Flood(self.alto, self.ancho)

        clon.tablero = []
        for fila in self.tablero:
            clon.tablero.append(list(fila))

        # Copiar colores
        clon.colores = list(self.colores)
        return clon


    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color

        Devuelve:
            bool: True si toda la grilla tiene el mismo color
        """
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero[0])):
                if self.tablero[fila][columna] != self.tablero[0][0]:
                    return False
        return True
