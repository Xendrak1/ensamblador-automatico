import re
import pandas as pd
import os
from typing import List, Dict

def log_debug(msg: str) -> None:
    print(f"DEBUG: {msg}")

def parse_memoria(linea: str) -> tuple[str, List[str]] | None:
    match = re.match(r"0x([0-9a-fA-F]+):\s+((?:0x[0-9a-fA-F]+\s*)+)", linea.strip())
    if match:
        direccion = '0x' + match.group(1)
        datos = [val.strip() for val in match.group(2).split() if val.strip()]
        return direccion, datos
    return None

def parse_registro(linea: str) -> tuple[str, str] | None:
    match = re.match(r"(\w+)\s+0x([0-9a-fA-F]+)", linea.strip())
    if match:
        return match.group(1), '0x' + match.group(2)
    return None

def main():
    os.makedirs("output", exist_ok=True)

    try:
        with open("gdb.log", "r") as f:
            contenido = f.readlines()
        log_debug(f"Leídas {len(contenido)} líneas del log")
    except FileNotFoundError:
        print("Error: No se encontró el archivo gdb.log")
        return 1
    
    variables: List[Dict[str, str]] = []
    reserva: List[Dict[str, str]] = []
    registros: List[Dict[str, str]] = []
    iteracion = 0

    for num_linea, linea in enumerate(contenido, 1):
        linea = linea.strip()
        if any(cmd in linea for cmd in ['x/32xb', '(gdb)', '=>']):
            continue

        reg_result = parse_registro(linea)
        if reg_result:
            nombre_reg, valor = reg_result
            registros.append({
                'iteracion': iteracion,
                'registro': nombre_reg,
                'valor': valor
            })
            continue

        mem_result = parse_memoria(linea)
        if mem_result:
            direccion, datos = mem_result
            data_dict = {
                'iteracion': iteracion,
                'direccion': direccion,
                'datos': datos
            }
            if "reserva" in linea.lower():
                reserva.append(data_dict)
            else:
                variables.append(data_dict)

    try:
        if registros:
            df = pd.DataFrame(registros)
            df.to_csv("output/registros.csv", index=False)
            print(f"✓ Guardados {len(registros)} registros")

        if variables:
            df = pd.DataFrame(variables)
            df.to_csv("output/variables.csv", index=False)
            print(f"✓ Guardadas {len(variables)} variables")

        if reserva:
            df = pd.DataFrame(reserva)
            df.to_csv("output/reserva.csv", index=False)
            print(f"✓ Guardadas {len(reserva)} reservas")

        if not any([registros, variables, reserva]):
            print("\n⚠ No se encontraron datos para procesar")
            print("\nMuestra del contenido del log:")
            for i, linea in enumerate(contenido[:10]):
                print(f"{i+1:2d}: {linea.strip()}")

    except Exception as e:
        print(f"Error al guardar CSVs: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())