"""Simula la netlist con ngspice y revisa que los valores caigan en los rangos esperados.

Uso:  python3 simular.py circuito.cir

La netlist trae su bloque .control (op, tran, meas, print) y los rangos esperados
como comentarios:

    *? v(a) 1.8 2.2          v(a) tiene que dar entre 1.8 y 2.2
    *? i(v1) -0.02 -0.005    corriente que entrega V1, en A (sale negativa)

Cada nombre de un *? tiene que aparecer impreso en la salida como "nombre = valor"
(con print o meas). Sale con código 1 si ngspice falla o avisa de algo raro, si
falta un valor, o si alguno queda fuera de rango. Sin rangos *? también falla:
una simulación sin rangos no valida nada.
"""
import os
import re
import shutil
import subprocess
import sys

# ngspice imprime resultados y sale con 0 aunque haya nodos flotantes o falte la tierra
SOSPECHOSO = re.compile(r'singular matrix|\berror\b|failed|aborted|unknown|could not|no such|not found', re.I)


def main(ruta):
    ngspice = os.environ.get('NGSPICE') or shutil.which('ngspice')
    if not ngspice:
        sys.exit('No encuentro ngspice. No lo instales sin preguntar: pedile permiso al usuario para correr "sudo apt install ngspice".')

    rangos = []
    for linea in open(ruta, encoding='utf-8'):
        if linea.startswith('*?'):
            nombre, minimo, maximo = linea[2:].split()[:3]
            rangos.append((nombre.lower(), float(minimo), float(maximo)))
    if not rangos:
        sys.exit(f'{ruta} no tiene rangos "*? nombre min max": agregá al menos uno.')

    r = subprocess.run([ngspice, '-b', ruta], capture_output=True, text=True, timeout=120)
    salida = r.stdout + r.stderr
    problemas = list(dict.fromkeys(l.strip() for l in salida.splitlines() if SOSPECHOSO.search(l)))

    valores = {}
    for linea in salida.splitlines():
        m = re.match(r'\s*([\w().,#:+-]+)\s*=\s*([-+0-9.eE]+)', linea)
        if m:
            try:
                valores.setdefault(m.group(1).lower(), float(m.group(2)))
            except ValueError:
                pass

    fallas = [f'ngspice salió con código {r.returncode}'] if r.returncode else []
    fallas += [f'ngspice avisó: {p}' for p in problemas]
    for nombre, minimo, maximo in rangos:
        v = valores.get(nombre)
        if v is None:
            fallas.append(f'{nombre} no aparece en la salida (falta un print o meas)')
        elif not minimo <= v <= maximo:
            fallas.append(f'{nombre} = {v:g}, fuera de [{minimo:g}, {maximo:g}]')
        else:
            print(f'ok  {nombre} = {v:g}  [{minimo:g}, {maximo:g}]')

    for f in fallas:
        print('ERROR:', f)
    if fallas:
        print('\n--- salida de ngspice ---\n' + salida[-3000:])
        sys.exit(1)
    print(f'Simulación OK: {len(rangos)} valores en rango')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
