import os
import re
import math
import heapq

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
    if not os.path.exists("centros.txt"):
        return centros, rutas
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
                    centros.append({
                        "cid": int(parts[0]),
                        "nombre": str(parts[1]),
                        "region": str(parts[2]),
                        "subregion": str(parts[3]),
                    })
                except:
                    pass
            elif mode == "r" and len(parts) == 4:
                try:
                    rutas.append({
                        "a": int(parts[0]),
                        "b": int(parts[1]),
                        "distancia": float(parts[2]),
                        "costo": float(parts[3]),
                    })
                except:
                    pass
    return centros, rutas

def guardar_centros_rutas(centros, rutas):
    with open("centros.txt", "w", encoding="utf-8") as f:
        f.write("[CENTROS]\n")
        for c in centros:
            f.write(f"{c['cid']}|{c['nombre']}|{c['region']}|{c['subregion']}\n")
        f.write("[RUTAS]\n")
        for r in rutas:
            f.write(f"{r['a']}|{r['b']}|{r['distancia']}|{r['costo']}\n")

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

def identificacion_valida(ident):
    return len(ident) == 10 and ident.isdigit()

def edad_valida(edad):
    return edad.isdigit() and int(edad) > 0

def buscar_centro(centros, cid):
    for c in centros:
        if c["cid"] == cid:
            return c
    return None

def merge_sort(items, clave_orden):
    lista = items[:]
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio], clave_orden)
    derecha = merge_sort(lista[medio:], clave_orden)
    mezcla = []
    i = 0
    j = 0
    while i < len(izquierda) and j < len(derecha):
        if clave_orden(izquierda[i]) <= clave_orden(derecha[j]):
            mezcla.append(izquierda[i])
            i += 1
        else:
            mezcla.append(derecha[j])
            j += 1
    mezcla.extend(izquierda[i:])
    mezcla.extend(derecha[j:])
    return mezcla

def build_graph(rutas):
    g = {}
    for r in rutas:
        a = r["a"]
        b = r["b"]
        d = r["distancia"]
        c = r["costo"]
        g.setdefault(a, []).append((b, d, c))
        g.setdefault(b, []).append((a, d, c))
    return g

def dijkstra_cost(g, start, goal):
    if start == goal:
        return 0.0, [start]
    dist = {}
    prev = {}
    for k in g:
        dist[k] = math.inf
        prev[k] = None
    dist[start] = 0.0
    pq = [(0.0, start)]
    seen = {}
    while pq:
        d, u = heapq.heappop(pq)
        if seen.get(u):
            continue
        seen[u] = True
        if u == goal:
            break
        for v, _, cost in g.get(u, []):
            nd = d + cost
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dist.get(goal, math.inf) == math.inf:
        return math.inf, []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return dist[goal], path

def bfs_near(g, start, max_steps):
    if start not in g:
        return []
    q = [start]
    head = 0
    steps = {start: 0}
    out = []
    while head < len(q):
        u = q[head]
        head += 1
        out.append(u)
        if steps[u] >= max_steps:
            continue
        for v, _, _ in g.get(u, []):
            if v not in steps:
                steps[v] = steps[u] + 1
                q.append(v)
    return out
    #centro y rutas con diccionarios
def dfs_traverse(g, start):
    seen = {}
    out = []
    stack = [start]
    while stack:
        u = stack.pop()
        if seen.get(u):
            continue
        seen[u] = True
        out.append(u)
        neigh = [v for (v, _, _) in g.get(u, [])]
        for v in reversed(neigh):
            if not seen.get(v):
                stack.append(v)
    return out

def lineas_arbol_regiones(centros):
    arbol = {}
    centros_by_id = {}
    for c in centros:
        centros_by_id[c["cid"]] = c
        reg = c["region"]
        sub = c["subregion"]
        if reg not in arbol:
            arbol[reg] = {}
        if sub not in arbol[reg]:
            arbol[reg][sub] = []
        arbol[reg][sub].append(c["cid"])
    out = []
    for reg in sorted(arbol):
        out.append(reg)
        for sub in sorted(arbol[reg]):
            out.append("  - " + sub)
            for cid in sorted(arbol[reg][sub]):
                c = centros_by_id.get(cid)
                if c:
                    out.append(f"      * {c['cid']} | {c['nombre']}")
    return out

def existe_ruta(rutas, a, b):
    for r in rutas:
        if (r["a"] == a and r["b"] == b) or (r["a"] == b and r["b"] == a):
            return True
    return False

def eliminar_rutas_de_centro(rutas, cid):
    return [r for r in rutas if r["a"] != cid and r["b"] != cid]

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
    print("7. Listar ordenado (Merge Sort)")
    print("8. Buscar centro (Lineal)")
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
    if not identificacion_valida(ident):
        print("***** Error *****\nLa identificación debe tener 10 dígitos.\nIntentelo de nuevo.")
        return
    if not edad_valida(edad):
        print("***** Error *****\nLa edad no puede ser negativa.\nIntentelo de nuevo.")
        return
    if not email_valido(email):
        print("***** Error *****\nEmail inválido.\nIntentelo de nuevo.")
        return
    if not password_valida(pw):
        print("***** Error *****\nLa contraseña es debil.\nIntentelo de nuevo.")
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
        print(f"{c['cid']} | {c['nombre']} | {c['region']} | {c['subregion']}")

def agregar_centro(centros):
    cid = int(input("ID: "))
    if buscar_centro(centros, cid):
        print("Ese ID ya existe")
        return
    nombre = input("Nombre: ")
    region = input("Región: ")
    sub = input("Subregión: ")
    centros.append({"cid": cid, "nombre": nombre, "region": region, "subregion": sub})
    print("Centro agregado")

def actualizar_centro(centros):
    cid = int(input("ID del centro a actualizar: "))
    c = buscar_centro(centros, cid)
    if not c:
        print("Centro no encontrado")
        return
    print("Deja vacío para mantener el valor actual.")
    nuevo_nombre = input(f"Nombre ({c['nombre']}): ").strip()
    nueva_region = input(f"Región ({c['region']}): ").strip()
    nueva_sub = input(f"Subregión ({c['subregion']}): ").strip()
    if nuevo_nombre:
        c["nombre"] = nuevo_nombre
    if nueva_region:
        c["region"] = nueva_region
    if nueva_sub:
        c["subregion"] = nueva_sub
    print("Centro actualizado")

def eliminar_centro(centros, rutas):
    cid = int(input("ID del centro a eliminar: "))
    if not buscar_centro(centros, cid):
        print("Centro no encontrado")
        return
    centros[:] = [c for c in centros if c["cid"] != cid]
    rutas[:] = eliminar_rutas_de_centro(rutas, cid)
    print("Centro y rutas asociadas eliminados")

def ver_rutas(rutas, centros):
    print("\n--- RUTAS ---")
    nombres = {c["cid"]: c["nombre"] for c in centros}
    for r in rutas:
        nombre_a = nombres.get(r["a"], str(r["a"]))
        nombre_b = nombres.get(r["b"], str(r["b"]))
        print(f"{nombre_a} <-> {nombre_b} | Distancia {r['distancia']}km | Costo ${r['costo']}")

def agregar_ruta(rutas, centros):
    a = int(input("Centro A: "))
    b = int(input("Centro B: "))
    if a == b:
        print("No puedes crear una ruta del centro al mismo centro")
        return
    ids = {c["cid"] for c in centros}
    if a not in ids or b not in ids:
        print("Uno de los IDs no existe")
        return
    if existe_ruta(rutas, a, b):
        print("La ruta ya existe")
        return
    d = float(input("Distancia: "))
    c = float(input("Costo: "))
    rutas.append({"a": a, "b": b, "distancia": d, "costo": c})
    print("Ruta agregada")

def listar_ordenado_admin(centros, rutas):
    print("\n¿Qué quieres ordenar?")
    print("1. Centros por ID")
    print("2. Centros por nombre")
    print("3. Rutas por costo")
    print("4. Rutas por distancia")
    target = input("Opción: ")
    if target == "1":
        items = centros
        key = lambda c: c["cid"]
    elif target == "2":
        items = centros
        key = lambda c: c["nombre"].lower()
    elif target == "3":
        items = rutas
        key = lambda r: r["costo"]
    elif target == "4":
        items = rutas
        key = lambda r: r["distancia"]
    else:
        print("Opción inválida")
        return
    ordered = merge_sort(items, key)
    print("\n--- RESULTADO ORDENADO ---")
    if items is centros:
        for c in ordered:
            print(f"{c['cid']} | {c['nombre']} | {c['region']} | {c['subregion']}")
    else:
        for r in ordered:
            print(f"{r['a']} <-> {r['b']} | Distancia {r['distancia']}km | Costo ${r['costo']}")
##----Funciones del Menu con nuevo llamado, (Diccionario)