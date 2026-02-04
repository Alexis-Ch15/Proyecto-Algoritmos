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
        for u in usuarios:
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

def buscar_centro_binaria(centros_ordenados_por_id, cid):
    lo, hi = 0, len(centros_ordenados_por_id) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = centros_ordenados_por_id[mid].cid
        if v == cid:
            return centros_ordenados_por_id[mid]
        if v < cid:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def buscar_centro_interpolacion(centros_ordenados_por_id, cid):
    lo, hi = 0, len(centros_ordenados_por_id) - 1
    while lo <= hi and centros_ordenados_por_id[lo].cid <= cid <= centros_ordenados_por_id[hi].cid:
        lo_id = centros_ordenados_por_id[lo].cid
        hi_id = centros_ordenados_por_id[hi].cid
        if hi_id == lo_id:
            return centros_ordenados_por_id[lo] if lo_id == cid else None

        pos = lo + int((cid - lo_id) * (hi - lo) / (hi_id - lo_id))
        pos_id = centros_ordenados_por_id[pos].cid

        if pos_id == cid:
            return centros_ordenados_por_id[pos]
        if pos_id < cid:
            lo = pos + 1
        else:
            hi = pos - 1
    return None


def buscar_centro_menu(centros):
    cid = int(input("ID a buscar: "))

    print("\nMétodo:")
    print("1. Lineal")
    print("2. Binaria")
    print("3. Interpolación")
    op = input("Opción: ")

    if op == "1":
        c = buscar_centro(centros, cid)
    else:
        # Necesita lista ordenada por ID
        ordenados = merge_sort(centros, lambda x: x.cid)
        if op == "2":
            c = buscar_centro_binaria(ordenados, cid)
        elif op == "3":
            c = buscar_centro_interpolacion(ordenados, cid)
        else:
            print("Opción inválida")
            return

    if c:
        print(f"Encontrado: {c.cid} | {c.nombre} | {c.region} | {c.subregion}")
    else:
        print("No encontrado")


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

def bubble_sort(items, clave):
    arr = items[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if clave(arr[j]) > clave(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(items, clave):
    arr = items[:]
    for i in range(1, len(arr)):
        x = arr[i]
        j = i - 1
        while j >= 0 and clave(arr[j]) > clave(x):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = x
    return arr


def selection_sort(items, clave):
    arr = items[:]
    n = len(arr)
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            if clave(arr[j]) < clave(arr[min_i]):
                min_i = j
        arr[i], arr[min_i] = arr[min_i], arr[i]
    return arr


def quick_sort(items, clave):
    arr = items[:]
    _quick_sort_inplace(arr, 0, len(arr) - 1, clave)
    return arr

def _quick_sort_inplace(arr, lo, hi, clave):
    if lo >= hi:
        return
    p = _partition(arr, lo, hi, clave)
    _quick_sort_inplace(arr, lo, p - 1, clave)
    _quick_sort_inplace(arr, p + 1, hi, clave)

def _partition(arr, lo, hi, clave):
    pivot = clave(arr[hi])
    i = lo
    for j in range(lo, hi):
        if clave(arr[j]) <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i

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

def pause():
    input("\nPresione ENTER para continuar...")

def menu_principal():
    print("\n=== POLIDELIVERY ===")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    return input("Opción: ")

def menu_admin():
    print("\n--- MENÚ ADMIN ---")
    print("1. Ver centros")
    print("2. Agregar centro")
    print("3. Eliminar centro")
    print("4. Actualizar centro")          
    print("5. Ver rutas")
    print("6. Agregar ruta")
    print("7. Listar ordenado")            
    print("8. Buscar centro")              
    print("9. Guardar cambios")
    print("10. Cerrar sesión")
    return input("Opción: ")


def menu_cliente():
    print("\n--- MENÚ CLIENTE ---")
    print("1. Ver mapa")
    print("2. Ruta óptima (Dijkstra)")
    print("3. BFS")
    print("4. DFS")
    print("5. Árbol de regiones")
    print("6. Seleccionar centros para envío")     
    print("7. Ver selección y costo total")        
    print("8. Eliminar centro de selección")       
    print("9. Guardar ruta del cliente")           
    print("10. Cerrar sesión")
    return input("Opción: ")


def login(users):
    email = input("Email: ").strip()
    pw = input("Contraseña: ").strip()
    for u in users:
        if u["email"] == email and u["password"] == pw:
            return u
    return None

def register(users):
    nombre = input("Nombre: ")
    ident = input("Identificación: ")
    edad = input("Edad: ")
    email = input("Email (@gmail.com): ")
    pw = input("Contraseña: ")

    if not email_valido(email):
        print("Email inválido")
        return

    if not password_valida(pw):
        print("Contraseña débil")
        return

    users.append({
        "email": email,
        "password": pw,
        "nombre": nombre,
        "identificacion": ident,
        "edad": edad,
        "rol": "cliente"
    })
    guardar_usuarios(users)
    print("Registro exitoso")

def ver_centros(centros):
    print("\n--- CENTROS ---")
    for c in centros:
        print(f"{c.cid} | {c.nombre} | {c.region} | {c.subregion}")

def agregar_centro(centros):
    cid = int(input("ID: "))
    nombre = input("Nombre: ")
    region = input("Región: ")
    sub = input("Subregión: ")
    centros.append(Centro(cid, nombre, region, sub))
    print("Centro agregado")

def actualizar_centro(centros):
    cid = int(input("ID del centro a actualizar: "))
    c = buscar_centro(centros, cid)
    if not c:
        print("Centro no encontrado")
        return

    print("Deja vacío para mantener el valor actual.")
    nuevo_nombre = input(f"Nombre ({c.nombre}): ").strip()
    nueva_region = input(f"Región ({c.region}): ").strip()
    nueva_sub = input(f"Subregión ({c.subregion}): ").strip()

    if nuevo_nombre:
        c.nombre = nuevo_nombre
    if nueva_region:
        c.region = nueva_region
    if nueva_sub:
        c.subregion = nueva_sub

    print("Centro actualizado")

def eliminar_centro(centros, rutas):
    cid = int(input("ID del centro a eliminar: "))
    centros[:] = [c for c in centros if c.cid != cid]
    rutas[:] = eliminar_rutas_de_centro(rutas, cid)
    print("Centro y rutas asociadas eliminados")

def ver_rutas(rutas):
    print("\n--- RUTAS ---")
    for r in rutas:
        print(f"{r.a} <-> {r.b} | Distancia {r.distancia} | Costo {r.costo}")

def agregar_ruta(rutas):
    a = int(input("Centro A: "))
    b = int(input("Centro B: "))
    if existe_ruta(rutas, a, b):
        print("La ruta ya existe")
        return
    d = float(input("Distancia: "))
    c = float(input("Costo: "))
    rutas.append(Ruta(a, b, d, c))
    print("Ruta agregada")

def listar_ordenado_admin(centros, rutas):
    print("\n¿Qué quieres ordenar?")
    print("1. Centros por ID")
    print("2. Centros por nombre")
    print("3. Rutas por costo")
    print("4. Rutas por distancia")
    target = input("Opción: ")

    print("\nAlgoritmo:")
    print("1. Burbuja")
    print("2. Inserción")
    print("3. Selección")
    print("4. Merge Sort")
    print("5. Quick Sort")
    alg = input("Opción: ")

    if target == "1":
        items = centros
        key = lambda c: c.cid
    elif target == "2":
        items = centros
        key = lambda c: c.nombre.lower()
    elif target == "3":
        items = rutas
        key = lambda r: r.costo
    elif target == "4":
        items = rutas
        key = lambda r: r.distancia
    else:
        print("Opción inválida")
        return

    if alg == "1":
        ordered = bubble_sort(items, key)
    elif alg == "2":
        ordered = insertion_sort(items, key)
    elif alg == "3":
        ordered = selection_sort(items, key)
    elif alg == "4":
        ordered = merge_sort(items, key)
    elif alg == "5":
        ordered = quick_sort(items, key)
    else:
        print("Algoritmo inválido")
        return

    print("\n--- RESULTADO ORDENADO ---")
    if items is centros:
        for c in ordered:
            print(f"{c.cid} | {c.nombre} | {c.region} | {c.subregion}")
    else:
        for r in ordered:
            print(f"{r.a} <-> {r.b} | Distancia {r.distancia} | Costo {r.costo}")


# ---------------- CLIENTE ----------------

def ver_mapa(rutas):
    g = build_graph(rutas)
    for k in g:
        print(k, "->", g[k])

def ruta_optima(rutas):
    a = int(input("Origen ID: "))
    b = int(input("Destino ID: "))
    g = build_graph(rutas)
    cost, path = dijkstra_costo(g, a, b)
    if cost == math.inf:
        print("No hay ruta")
    else:
        print("Costo:", cost)
        print("Ruta:", " -> ".join(map(str, path)))

def bfs(rutas):
    start = int(input("Inicio: "))
    steps = int(input("Saltos: "))
    g = build_graph(rutas)
    print(bfs_cercanos(g, start, steps))

def dfs(rutas):
    start = int(input("Inicio: "))
    g = build_graph(rutas)
    print(dfs_recorrido(g, start))

def ver_arbol(centros):
    for line in lineas_arbol_regiones(centros):
        print(line)

def seleccionar_centros(centros, seleccion):
    ids_validos = {c.cid for c in centros}
    print("\n--- SELECCIÓN DE CENTROS ---")
    print("Ingresa IDs (mínimo 2). Escribe 0 para terminar.")

    while True:
        cid = int(input("ID: "))
        if cid == 0:
            break
        if cid not in ids_validos:
            print("ID no existe")
            continue
        if cid in seleccion:
            print("Ya está en la selección")
            continue
        seleccion.append(cid)
        print("Agregado.")

    print("Selección actual:", seleccion)
    if len(seleccion) < 2:
        print("⚠ Debes seleccionar mínimo 2 centros.")


def eliminar_de_seleccion(seleccion):
    if not seleccion:
        print("No hay selección")
        return
    cid = int(input("ID a eliminar: "))
    if cid in seleccion:
        seleccion.remove(cid)
        print("Eliminado")
    else:
        print("Ese ID no está en la selección")


def costo_total_seleccion(seleccion, rutas):
    """
    Suma el costo de ir del centro i al i+1 usando Dijkstra por COSTO.
    """
    if len(seleccion) < 2:
        return math.inf, []

    g = build_graph(rutas)
    total = 0.0
    ruta_total = []

    for i in range(len(seleccion) - 1):
        a = seleccion[i]
        b = seleccion[i + 1]
        cost, path = dijkstra_costo(g, a, b)
        if cost == math.inf:
            return math.inf, []
        total += cost

        if not ruta_total:
            ruta_total.extend(path)
        else:
            ruta_total.extend(path[1:])  # evita repetir el nodo de unión

    return total, ruta_total


def ver_seleccion_y_total(seleccion, rutas):
    if len(seleccion) < 2:
        print("Selecciona mínimo 2 centros.")
        return
    total, ruta = costo_total_seleccion(seleccion, rutas)
    if total == math.inf:
        print("No se pudo calcular (hay tramos sin conexión).")
    else:
        print("Centros seleccionados:", seleccion)
        print("Costo total:", total)
        print("Ruta total:", " -> ".join(map(str, ruta)))


def guardar_ruta_cliente(nombre_cliente, seleccion, rutas):
    if len(seleccion) < 2:
        print("Debes seleccionar mínimo 2 centros.")
        return
    total, ruta = costo_total_seleccion(seleccion, rutas)
    if total == math.inf:
        print("No se puede guardar: hay tramos sin conexión.")
        return

    filename = f"rutas-{nombre_cliente}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Cliente: {nombre_cliente}\n")
        f.write("Centros seleccionados: " + ",".join(map(str, seleccion)) + "\n")
        f.write("Ruta total: " + " -> ".join(map(str, ruta)) + "\n")
        f.write(f"Costo total: {total}\n")

    print("Ruta guardada en:", filename)


def main():
    asegurar_archivos()
    users = leer_usuarios()
    centros, rutas = leer_centros_rutas()

    while True:
        op = menu_principal()

        if op == "1":
            user = login(users)
            if not user:
                print("Credenciales incorrectas")
                continue

            if user["rol"] == "admin":
                while True:
                    op = menu_admin()
                    if op == "1":
                        ver_centros(centros)
                    elif op == "2":
                        agregar_centro(centros)
                    elif op == "3":
                        eliminar_centro(centros, rutas)
                    elif op == "4":
                        actualizar_centro(centros)
                    elif op == "5":
                        ver_rutas(rutas)
                    elif op == "6":
                        agregar_ruta(rutas)
                    elif op == "7":
                        listar_ordenado_admin(centros, rutas)
                    elif op == "8":
                        buscar_centro_menu(centros)
                    elif op == "9":
                        guardar_centros_rutas(centros, rutas)
                        print("Datos guardados")    
                    elif op == "10":
                        break
                    pause()
            else:
                seleccion = []
                while True:
                    op = menu_cliente()
                    if op == "1":
                        ver_mapa(rutas)
                    elif op == "2":
                        ruta_optima(rutas)
                    elif op == "3":
                        bfs(rutas)
                    elif op == "4":
                        dfs(rutas)
                    elif op == "5":
                        ver_arbol(centros)
                    elif op == "6":
                        seleccionar_centros(centros, seleccion)   
                    elif op == "7":
                        ver_seleccion_y_total(seleccion, rutas)   
                    elif op == "8":
                        eliminar_de_seleccion(seleccion)          
                    elif op == "9":
                        nombre_archivo = user.get("nombre", "cliente").replace(" ", "_")
                        guardar_ruta_cliente(nombre_archivo, seleccion, rutas) 
                    elif op == "10":
                        break

                    pause()

        elif op == "2":
            register(users)

        elif op == "3":
            print("Saliendo...")
            break

main()

