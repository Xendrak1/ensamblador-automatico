name: Ensamblador x86_64 Debug Workflow

on:
  push:
    paths:
      - '**.asm'
      - '.github/workflows/ensamblador.yml'
      - 'scripts/**'

jobs:
  build-and-debug:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Instalar dependencias
      run: |
        sudo apt-get update
        sudo apt-get install -y nasm gdb python3-pandas
        
    - name: Verificar versiones
      run: |
        nasm --version
        gdb --version
        python3 --version
        
    - name: Compilar ensamblador
      run: |
        nasm -f elf64 -g -F dwarf programa.asm -o programa.o
        ld -o programa programa.o
        
    - name: Verificar ejecutable
      run: |
        file programa
        ls -l programa
        readelf -h programa
        
    - name: Preparar script GDB
      run: |
        cat > debug.gdb << 'EOF'
        set pagination off
        set logging file gdb.log
        set logging enabled on
        file programa
        break _start
        run
        info registers
        x/32xb $rsp
        backtrace
        quit
        EOF
        
    - name: Ejecutar GDB
      run: |
        gdb -batch -x debug.gdb
        cat gdb.log
        
    - name: Procesar resultados
      run: |
        mkdir -p output
        python3 scripts/procesar_gdb.py
        ls -la gdb.log output/
        
    - name: Subir resultados
      uses: actions/upload-artifact@v4
      with:
        name: debug-results
        path: |
          output/*.csv
          gdb.log
        retention-days: 5
