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
