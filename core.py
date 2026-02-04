import os
import re
import math
import heapq

class Centro:
    def __init__(self, cid, nombre, region, subregion):
        self.cid = int(cid)
        self.nombre = str(nombre)
        self.region = str(region)
        self.subregion = str(subregion)


class Ruta:
    def __init__(self, a, b, distancia, costo):
        self.a = int(a)
        self.b = int(b)
        self.distancia = float(distancia)
        self.costo = float(costo)

class RegionNode:
    def __init__(self, nombre):
        self.nombre = nombre
        self.children = {}
        self.centros = []

    def add(self, region, subregion, cid):
        if region not in self.children:
            self.children[region] = RegionNode(region)
        r = self.children[region]
        if subregion not in r.children:
            r.children[subregion] = RegionNode(subregion)
        r.children[subregion].centros.append(cid)

    def render(self, centros_by_id):
        out = []
        for r in sorted(self.children):
            out.append(r)
            rn = self.children[r]
            for s in sorted(rn.children):
                out.append("  - " + s)
                sn = rn.children[s]
                for cid in sorted(sn.centros):
                    c = centros_by_id.get(cid)
                    if c:
                        out.append(f"      * {c.cid} | {c.nombre}")
        return out
def asegurar_archivos():
    if not os.path.exists("centros.txt"):
        with open("centros.txt", "w", encoding="utf-8") as f:
            f.write("[CENTROS]\n")
            f.write("1|Centro Norte|Region A|Sub A1\n")
            f.write("2|Centro Sur|Region A|Sub A2\n")
            f.write("3|Centro Este|Region B|Sub B1\n")
            f.write("4|Centro Oeste|Region B|Sub B2\n")
            f.write("[RUTAS]\n")
            f.write("1|2|10|5\n")
            f.write("2|3|12|6\n")
            f.write("1|3|25|12\n")
            f.write("3|4|8|4\n")
            f.write("2|4|20|10\n")
    if not os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "w", encoding="utf-8") as f:
            f.write("admin@polidelivery.com|Admin1234|Administrador|0000000000|30|admin\n")


def leer_centros_rutas():
    centros, rutas = [], []
    mode = None
    with open("centros.txt", "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            up = line.upper()
            if up == "[CENTROS]":
                mode = "c"
                continue
            if up == "[RUTAS]":
                mode = "r"
                continue
            parts = line.split("|")
            if mode == "c" and len(parts) == 4:
                try:
                    centros.append(Centro(parts[0], parts[1], parts[2], parts[3]))
                except:
                    pass
            elif mode == "r" and len(parts) == 4:
                try:
                    rutas.append(Ruta(parts[0], parts[1], parts[2], parts[3]))
                except:
                    pass
    return centros, rutas


def guardar_centros_rutas(centros, rutas):
    with open("centros.txt", "w", encoding="utf-8") as f:
        f.write("[CENTROS]\n")
        for c in centros:
            f.write(f"{c.cid}|{c.nombre}|{c.region}|{c.subregion}\n")
        f.write("[RUTAS]\n")
        for r in rutas:
            f.write(f"{r.a}|{r.b}|{r.distancia}|{r.costo}\n")


def leer_usuarios():
    users = []
    if not os.path.exists("usuarios.txt"):
        return users
    with open("usuarios.txt", "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 6:
                continue
            users.append({
                "email": parts[0],
                "password": parts[1],
                "nombre": parts[2],
                "identificacion": parts[3],
                "edad": parts[4],
                "rol": parts[5]
            })
    return users


def guardar_usuarios(usuarios):
    with open("usuarios.txt", "w", encoding="utf-8") as f:
        for usuario in usuarios:
            f.write(f"{u['email']}|{u['password']}|{u['nombre']}|{u['identificacion']}|{u['edad']}|{u['rol']}\n")

def email_valido(s):
    return re.match(r"^[A-Za-z0-9._%+-]+@gmail\.com$", s) is not None


def password_valida(contrasenia):
    if len(contrasenia) < 8:
        return False
    return any("a" <= c <= "z" for c in contrasenia) and any("A" <= c <= "Z" for c in contrasenia) and any("0" <= c <= "9" for c in contrasenia)


def buscar_centro(centros, cid):
    for c in centros:
        if c.cid == cid:
            return c
    return None


def merge_sort(items, clave_orden):
    lista = items[:]
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio], clave_orden)
    derecha = merge_sort(lista[medio:], clave_orden)
    mezclaFinal = []
    indiceIzquierda = 0
    indiceDerecha = 0
    while indiceIzquierda < len(izquierda) and indiceDerecha < len(derecha):
        if clave_orden(izquierda[indiceIzquierda]) <= clave_orden(derecha[indiceDerecha]):
            mezclaFinal.append(izquierda[indiceIzquierda])
            indiceIzquierda += 1
        else:
            mezclaFinal.append(derecha[indiceDerecha])
            indiceDerecha += 1
    mezclaFinal.extend(izquierda[indiceIzquierda:])
    mezclaFinal.extend(derecha[indiceDerecha:])
    return mezclaFinal

def build_graph(rutas):
    g = {}
    for r in rutas:
        g.setdefault(r.a, []).append((r.b, r.distancia, r.costo))
        g.setdefault(r.b, []).append((r.a, r.distancia, r.costo))
    return g

def dijkstra_costo(grafo, inicio, destino):
    if inicio == destino:
        return 0.0, [inicio]

    distancias = {}
    previo = {}

    for nodo in grafo:
        distancias[nodo] = math.inf
        previo[nodo] = None

    distancias[inicio] = 0.0
    cola_prioridad = [(0.0, inicio)]
    visitados = {}

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if visitados.get(nodo_actual):
            continue

        visitados[nodo_actual] = True

        if nodo_actual == destino:
            break

        for vecino, _, costo in grafo.get(nodo_actual, []):
            nueva_distancia = distancia_actual + costo
            if nueva_distancia < distancias.get(vecino, math.inf):
                distancias[vecino] = nueva_distancia
                previo[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

    if distancias.get(destino, math.inf) == math.inf:
        return math.inf, []

    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = previo.get(actual)

    camino.reverse()
    return distancias[destino], camino

def bfs_cercanos(grafo, inicio, max_saltos):
    if inicio not in grafo:
        return []

    cola = [inicio]
    indice = 0
    niveles = {inicio: 0}
    resultado = []

    while indice < len(cola):
        nodo_actual = cola[indice]
        indice += 1
        resultado.append(nodo_actual)

        if niveles[nodo_actual] >= max_saltos:
            continue

        for vecino, _, _ in grafo.get(nodo_actual, []):
            if vecino not in niveles:
                niveles[vecino] = niveles[nodo_actual] + 1
                cola.append(vecino)

    return resultado

def dfs_recorrido(grafo, inicio):
    visitados = {}
    resultado = []
    pila = [inicio]

    while pila:
        nodo_actual = pila.pop()

        if visitados.get(nodo_actual):
            continue

        visitados[nodo_actual] = True
        resultado.append(nodo_actual)

        vecinos = [v for (v, _, _) in grafo.get(nodo_actual, [])]
        for vecino in reversed(vecinos):
            if not visitados.get(vecino):
                pila.append(vecino)

    return resultado

def lineas_arbol_regiones(centros):
    root = RegionNode("ROOT")
    for c in centros:
        root.add(c.region, c.subregion, c.cid)
    by = {c.cid: c for c in centros}
    return root.render(by)

def existe_ruta(rutas, a, b):
    for r in rutas:
        if (r.a == a and r.b == b) or (r.a == b and r.b == a):
            return True
    return False
    
def eliminar_rutas_de_centro(rutas, cid):
    return [r for r in rutas if r.a != cid and r.b != cid]
