;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;nasm -f elf64 -g -F dwarf -o grupoC_110821.o grupoC_110821.asm
;ld -o grupoC_110821 grupoC_110821.o
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
;0000000000401550    direccion donde se alojan los programas ensamblador en el x64dbg	

section .data

X1 DD -0.79
X2 DQ +0.79
NOMBRE DB   "inf221sxz", 0  ; USAR ESTAS MISMAS CADENAS NO MODIFICAR
REGISTRO DB "012045679", 0  ; USAR ESTAS MISMAS CADENAS NO MODIFICAR

section .bss

X3 RESD 1
X4 RESW 1
X5 RESB 1
X6 RESD 1

section .text
global _start
_start:
    JMP LIMPIAR

INICIO:
    MOV RAX, [rel X1]
    MOV RBX, [rel X2]
    MOV RCX, [rel NOMBRE]
    MOV RDX, [rel REGISTRO]
    JMP SALTAR

SALTOX:
    JMP SALTO2

SALTOX1:
    JMP SALTO3

SALTAR:
    ;---1---
    MOV AX, [RCX]
    MOV BX, [RDX]
    NEG BX
    OR AX, BX
    MOV BX, [RDX + 2]
    NEG BX
    AND BX, [RDX + 4]

    ;---2---
    JMP SALTOX

SALTO2:
    MOV AX, [RCX + 2]
    MOV BX, [RDX + 3]
    NEG BX
    DEC AX
    MOV BX, [RCX + 6]
    NEG BX
    MOV BX, [RCX + 5]

    ;---2---
    JMP SALTOX4

SALTOX4:
    MOV AX, [RCX + 3]
    MOV BX, [RDX + 7]
    NEG BX
    ADD AX, BX
    MOV BX, [RCX + 11]
    NEG BX
    XOR BX, [RCX + 10]
    JMP SALTO3

SALTO3:
    MOV DWORD [rel X3], -1
    MOV ECX, X3
    MOV ECX, [ECX]
    AND ECX, EDX
    MOV WORD [rel X4], 0XFFFF
    MOV DX, [rel X4]
    OR EDX, [rel X3]
    JMP FIN

LIMPIAR:
    MOV RAX, "87654231"   ; entran de izquierda a derecha las cadenas
    MOV RBX, "12345678"
    MOV RCX, "11110000"
    MOV RDX, "00001111"
    XOR R8, R8
    XOR R9, R9
    XOR R10, R10
    XOR R11, R11
    XOR R12, R12
    XOR R13, R13
    XOR R14, R14
    XOR R15, R15
    JMP INICIO

FIN:
    MOV DWORD [rel X3], EAX
    MOV WORD [rel X4], BX
    MOV BYTE [rel X5], CH
    MOV DWORD [rel X6], EDX

    ; Salida limpia en Linux
    MOV RAX, 60
    XOR RDI, RDI
    SYSCALL
