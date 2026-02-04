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


def guardar_usuarios(users):
    with open("usuarios.txt", "w", encoding="utf-8") as f:
        for u in users:
            f.write(f"{u['email']}|{u['password']}|{u['nombre']}|{u['identificacion']}|{u['edad']}|{u['rol']}\n")

def email_valido(s):
    return re.match(r"^[A-Za-z0-9._%+-]+@gmail\.com$", s) is not None


def password_valida(pw):
    if len(pw) < 8:
        return False
    return any("a" <= c <= "z" for c in pw) and any("A" <= c <= "Z" for c in pw) and any("0" <= c <= "9" for c in pw)


def buscar_centro(centros, cid):
    for c in centros:
        if c.cid == cid:
            return c
    return None


def merge_sort(items, key_fn):
    a = items[:]
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], key_fn)
    right = merge_sort(a[mid:], key_fn)
    out = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if key_fn(left[i]) <= key_fn(right[j]):
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


