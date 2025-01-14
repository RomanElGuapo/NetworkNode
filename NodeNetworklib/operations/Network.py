import matplotlib.pyplot as plt
import numpy as np

class Red:
    def __init__(self, archivo):
        # Tenemos que cargar el archivo como argumento
        self.archivo = archivo
        self.cargar_archivo()

    def cargar_archivo(self):
        # Diccionario donde guardaremos los datos de nuestra red
        self.red = {}
        with open(self.archivo, 'r') as regulacion:
            lineas = regulacion.readlines()[1:]
            for linea in lineas:
                # Asignamos los valores regulador, regulado y efecto en base al archivo separando por tabuladores
                regulador, regulado, efecto = linea.strip().split('\t')
                # Si el regulador no se encuentra en la red o si es igual al regulado, evitamos self-loops
                if regulador != regulado:
                    if regulador not in self.red:
                        self.red[regulador] = []
                        self.red[regulador].append((regulado, efecto))
                    else:
                        self.red[regulador].append((regulado, efecto))
                    if regulado not in self.red:
                        self.red[regulado] = []
                        self.red[regulado].append((regulador, efecto))
                    else:
                        self.red[regulado].append((regulador, efecto))

    def k(self, nodo):
        # Con len, contamos la longitud asociada al nodo, en dado caso de que nodo no esté, devuelve una lista vacía
        return len(self.red.get(nodo, []))

    def ck(self, nodo):
        # Conseguimos los vecinos de un nodo, pero también llamamos al efecto porque es parte de la tupla
        vecinos = self.red.get(nodo, [])
        nv = 0
        # Hacemos la suma de las conexiones que hay entre los vecinos de cada uno de los vecinos
        for vecino, _ in vecinos:
            vecinos_dvecino = set(self.red.get(vecino, []))
            for pos_vecino, _ in vecinos_dvecino:
                if pos_vecino in set(v for v, _ in vecinos):
                    nv += 1
        kv = self.k(nodo)
        # Recuerda que si tiene un kv < 2, tiene un coeficiente de clustering indeterminado, no 0
        coef_clustering = 'None' if kv < 2 else ((2 * nv) / (kv * (kv - 1)))
        return coef_clustering

    def plot_ck(self):
        nodos = list(self.red.keys())
        grados = [self.k(nodo) for nodo in nodos if self.k(nodo) > 2]
        grados_unicos = sorted(set((grados)))
        # Se saca el promedio del coeficiente de clustering de los nodos que comparten el mismo grado
        coef_clust_promedio = [np.mean([self.ck(nodo) for nodo in nodos if self.k(nodo) == grado]) for grado in grados_unicos]
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=[16, 6])
        # Escala linear
        axs[0].scatter(grados_unicos, coef_clust_promedio, color='r')
        axs[0].set_title('C(k) linear')
        axs[0].set_xlabel('k')
        axs[0].set_ylabel('Ck')
        axs[0].grid(True)
        # Escala logarítmica
        axs[1].scatter(grados_unicos, coef_clust_promedio, color='b')
        axs[1].set_title('C(k) log')
        axs[1].set_xlabel('k')
        axs[1].set_ylabel('Ck')
        axs[1].grid(True)
        axs[1].set_xscale('log')
        axs[1].set_yscale('log')

        plt.tight_layout()
        plt.show()

    def plot_pk(self):
        # Calcular P(k) para todos los nodos
        nodos = list(self.red.keys())
        grados = [self.k(nodo) for nodo in nodos]
        frecuencias = {k: grados.count(k) for k in set(grados)}
        keys = list(frecuencias.keys())
        values = [frecuencias[k] for k in keys]
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
        # Escala linear
        axs[0].scatter(keys, values, marker='o', color='g')
        axs[0].set_title('P(k) - Linear')
        axs[0].set_xlabel('Grado (k)')
        axs[0].set_ylabel('Frecuencia')
        axs[0].grid(True)
        # Escala logaritmica
        axs[1].scatter(keys, values, color='purple')
        axs[1].set_title('P(k) - Log-log')
        axs[1].set_xlabel('k')
        axs[1].set_ylabel('Frecuencia (log)')
        axs[1].set_xscale('log')
        axs[1].set_yscale('log')
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()