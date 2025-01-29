import re
import pandas as pd

# Leer la salida de GDB
with open("salida_gdb.txt", "r") as f:
    contenido = f.readlines()

# Variables
variables = []
reserva = []
registros = []
iteracion = 0

# Parsear registros (ejemplo: "rax            0x12345678")
for linea in contenido:
    match = re.match(r"(\w+)\s+0x([0-9a-fA-F]+)", linea)
    if match:
        registros.append([iteracion, match.group(1), match.group(2)])

# Parsear memoria (ejemplo: "0x403010: 0xFF 0x00 ...")
for linea in contenido:
    match = re.match(r"(0x[0-9a-fA-F]+):\s+(.*)", linea)
    if match:
        direccion = match.group(1)
        datos = match.group(2).split()
        if "reserva" in linea:
            reserva.append([iteracion, direccion] + datos)
        else:
            variables.append([iteracion, direccion] + datos)

    # Incrementar iteración cuando GDB ejecuta una instrucción
    if "=> 0x" in linea:  
        iteracion += 1  

# Guardar en CSV
df_variables = pd.DataFrame(variables, columns=["Iteración", "DIRECCIÓN", "[DATO]"])
df_variables.to_csv("output/variables.csv", index=False)

df_reserva = pd.DataFrame(reserva, columns=["Iteración", "DIRECCIÓN", "[DATO]"])
df_reserva.to_csv("output/reserva.csv", index=False)

df_registros = pd.DataFrame(registros, columns=["Iteración", "REGISTRO", "VALOR"])
df_registros.to_csv("output/registros.csv", index=False)

print("Tablas generadas con éxito.")
