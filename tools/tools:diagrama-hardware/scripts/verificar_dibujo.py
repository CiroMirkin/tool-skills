"""Compara un dibujo de schemdraw con la netlist SPICE del Paso A.

Uso, al final del script del circuito:

    import sys; sys.path.insert(0, '<carpeta de la skill>/scripts')
    from verificar_dibujo import verificar
    verificar(d, {R1: 'R1', D1: 'D1', V1: 'V1', vdd: '=vcc'}, 'circuito.cir')

`nombres` mapea cada componente del dibujo a su designador en la netlist.
Lo decorativo (una antena, un cable dibujado como dibujo) va con None y no se revisa;
un componente que no está en el dict es un error.
Los símbolos de alimentación (Vdd, Vss, etiquetas) van con '=nodo'. Las tierras
(Ground*) no hace falta nombrarlas: son el nodo 0.

Qué lee de la netlist:
  R C L       nodos sin polaridad (un capacitor con polar=True: n1 es el +)
  D           ánodo cátodo
  V I         n+ n-
  Q           colector base emisor
  M J         drain gate source
  *@ U1.VIN vin   pin de un IC u opamp (anchor de schemdraw) en un nodo
  X E F G H B y las líneas con `solo-sim` son modelos: no se dibujan.

Sale con código 1 si el dibujo no coincide.
"""
import re
import sys
from schemdraw import elements as elm

CABLES = (elm.Line, elm.Wire, elm.Dot)
TIERRAS = tuple(getattr(elm, n) for n in ('Ground', 'GroundSignal', 'GroundChassis') if hasattr(elm, n))
SIMBOLOS = TIERRAS + tuple(getattr(elm, n) for n in ('Vdd', 'Vss') if hasattr(elm, n))
SIN_DIBUJO = set('XEFGHB')
TOL = 0.01


def _punto(p):
    return (round(float(p[0]) / TOL), round(float(p[1]) / TOL))


def _leer_netlist(ruta):
    """Devuelve {designador: [opciones]}; cada opción es [(anchor, nodo), ...]."""
    esperado = {}
    lineas = open(ruta, encoding='utf-8').read().splitlines()[1:]  # la 1ª línea de un .cir es el título
    en_control = False
    for linea in lineas:
        s = linea.strip()
        if s.lower().startswith('.control'):
            en_control = True
        if en_control:
            en_control = not s.lower().startswith('.endc')
            continue
        if s.startswith('*@'):
            pin, nodo = s[2:].split()[:2]
            des, anchor = pin.split('.', 1)
            esperado.setdefault(des, [[]])[0].append((anchor, nodo))
            continue
        if not s or s[0] in '*.+' or 'solo-sim' in s or s[0].upper() in SIN_DIBUJO:
            continue
        campos = re.split(r'[;$]', s)[0].split()
        des, nodos, letra = campos[0], campos[1:], campos[0][0].upper()
        if letra in 'RCL':
            a, b = nodos[:2]
            esperado[des] = [[('start', a), ('end', b)], [('start', b), ('end', a)]]
        elif letra == 'D':
            esperado[des] = [[('anodo', nodos[0]), ('catodo', nodos[1])]]
        elif letra in 'VI':
            esperado[des] = [[('mas', nodos[0]), ('menos', nodos[1])]]
        elif letra == 'Q':
            esperado[des] = [list(zip(('collector', 'base', 'emitter'), nodos))]
        elif letra in 'MJ':
            esperado[des] = [list(zip(('drain', 'gate', 'source'), nodos))]
        else:
            raise ValueError(f'No sé leer la línea "{s}". Marcala con "; solo-sim" o describila con *@.')
    return esperado


def _anchor_real(e, anchor):
    """Traduce los anchors de polaridad (anodo, mas...) al anchor de schemdraw."""
    invertido = bool(e.params.get('reverse', False))  # .reverse() da vuelta el símbolo pero no los anchors
    if anchor in ('anodo', 'catodo'):
        positivo_en = 'start'
    elif anchor in ('mas', 'menos'):
        # SourceV dibuja el + del lado de 'end'; Battery tiene la placa larga (+) en 'start'
        positivo_en = 'end' if isinstance(e, elm.Source) else 'start'
    elif anchor in ('start', 'end') and isinstance(e, (elm.Capacitor, elm.Capacitor2)) and e.params.get('polar'):
        positivo_en = 'start'
        anchor = 'mas' if anchor == 'start' else 'menos'  # en la netlist n1 es el +
    else:
        return anchor
    negativo_en = 'end' if positivo_en == 'start' else 'start'
    if invertido:
        positivo_en, negativo_en = negativo_en, positivo_en
    return positivo_en if anchor in ('anodo', 'mas') else negativo_en


def _nets(elementos):
    """Une por coincidencia de anchors: extremos de cable, uniones en T y pines."""
    padre = {}

    def raiz(a):
        padre.setdefault(a, a)
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    cables = [e for e in elementos if isinstance(e, CABLES)]
    puntas = {}
    for c in cables:
        s, t = _punto(c.absanchors['start']), _punto(c.absanchors['end'])
        padre[raiz(s)] = raiz(t)
        if not isinstance(c, elm.Dot):
            puntas[s] = puntas.get(s, 0) + 1
            puntas[t] = puntas.get(t, 0) + 1
    pines = set()
    for e in elementos:
        if not isinstance(e, CABLES):
            for nombre, p in e.absanchors.items():
                pines.add(_punto(p))
    puntos = set(padre) | pines

    def sobre(p, c):  # p está en el tramo recto del cable c, extremos incluidos
        (x1, y1), (x2, y2) = _punto(c.absanchors['start']), _punto(c.absanchors['end'])
        x, y = p
        return ((x2 - x1) * (y - y1) == (y2 - y1) * (x - x1)
                and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2))

    for c in cables:  # unión en T: un punto dentro de un tramo queda unido a ese cable
        for p in puntos:
            if sobre(p, c):
                padre[raiz(p)] = raiz(_punto(c.absanchors['start']))
    dots = {_punto(c.absanchors['start']) for c in cables if isinstance(c, elm.Dot)}
    sueltas = [p for p, n in puntas.items()
               if n == 1 and p not in pines and p not in dots
               and sum(sobre(p, c) for c in cables if not isinstance(c, elm.Dot)) == 1]
    def unir(a, b):
        padre[raiz(a)] = raiz(b)

    return raiz, unir, sueltas


def verificar(d, nombres, netlist):
    esperado = _leer_netlist(netlist)
    # lo que se mapea a None es decorativo (antena, cable dibujado como dibujo): no entra al chequeo
    elementos = [e for e in d.elements if not (e in nombres and nombres[e] is None)]
    raiz, unir, sueltas = _nets(elementos)
    errores = []
    for e in elementos:
        if not isinstance(e, CABLES + SIMBOLOS) and e not in nombres:
            errores.append(f'{type(e).__name__} dibujado sin designador: agregalo al dict, o mapealo a None si es decorativo')
    nodo_de_net, net_de_nodo = {}, {}

    def asignar(etiqueta, punto, nodo):
        net = raiz(punto)
        if nodo_de_net.get(net, nodo) != nodo:
            errores.append(f'{etiqueta} está conectado al nodo "{nodo_de_net[net]}", la netlist dice "{nodo}"')
        elif net_de_nodo.get(nodo, net) != net:
            errores.append(f'{etiqueta} debería estar en el nodo "{nodo}", pero en el dibujo no toca '
                           f'al resto de ese nodo (pin suelto o cable cortado)')
        else:
            nodo_de_net[net] = nodo
            net_de_nodo[nodo] = net

    # 1) símbolos de alimentación y tierra: los que nombran el mismo nodo son la misma net
    simbolos = []
    for e in elementos:
        if isinstance(e, SIMBOLOS):
            nombre = nombres.get(e, '=0' if isinstance(e, TIERRAS) else None)
            if not nombre or not nombre.startswith('='):
                errores.append(f'{type(e).__name__} sin nodo: nombralo con "=nodo" en el dict')
            else:
                simbolos.append((nombre[1:], _punto(e.absanchors['start'])))
    primero = {}
    for nodo, p in simbolos:
        unir(p, primero.setdefault(nodo, p))
    for nodo, p in simbolos:
        asignar(f'símbolo de {nodo}', p, nodo)

    # 2) componentes: primero los de una sola orientación, después R/C/L
    por_designador = {v: e for e, v in nombres.items() if v and not v.startswith('=')}
    for des in set(por_designador) - set(esperado):
        errores.append(f'{des} está en el dibujo pero no en la netlist')
    for des in set(esperado) - set(por_designador):
        errores.append(f'{des} está en la netlist pero no en el dibujo (o falta en el dict de nombres)')
    comunes = [des for des in esperado if des in por_designador]
    pendientes = list(comunes)
    while pendientes:
        # primero los que tienen una sola orientación o algún nodo ya ubicado
        des = next((x for x in pendientes if len(esperado[x]) == 1), None) or next(
            (x for x in pendientes if any(n in net_de_nodo for _, n in esperado[x][0])), pendientes[0])
        pendientes.remove(des)
        e = por_designador[des]
        try:
            opciones = [[(a, _punto(e.absanchors[_anchor_real(e, a)]), n) for a, n in op] for op in esperado[des]]
        except KeyError as falta:
            errores.append(f'{des} no tiene el anchor {falta} en schemdraw')
            continue
        elegida = next((op for op in opciones
                        if all(nodo_de_net.get(raiz(p), n) == n and net_de_nodo.get(n, raiz(p)) == raiz(p)
                               for _, p, n in op)), opciones[0])
        for a, p, n in elegida:
            asignar(f'{des}.{a}', p, n)

    for p in sueltas:
        errores.append(f'punta de cable sin conectar en ({p[0] * TOL:g}, {p[1] * TOL:g})')

    for e in errores:
        print('ERROR:', e)
    if errores:
        sys.exit(1)
    print(f'Dibujo OK: {len(comunes)} componentes y {len(net_de_nodo)} nodos coinciden con {netlist}')
