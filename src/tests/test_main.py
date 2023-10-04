import pytest

from src.analizadorLexico import *

import sys

from subprocess import check_output
from src.analizadorSintactico import *


@pytest.mark.parametrize(
    "entrada",
    [
        ("file1"),
        ("file2"),
        ("file3"),
        ("file4"),
        ("file5"),
        ("file6"),
        ("file7"),
        ("file8"),
        ("file9"),
        ("01"),
        ("02"),
        ("05"),
        ("06"),
        ("08"),
        ("12"),
        ("13")
                     
    ]
)
def test_getnew(entrada):
    
    ruta = './src/tests/filesfortest/'+entrada+".txt"  
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()  
    ruta = './src/tests/filesfortest/'+entrada+'e'+".txt"    
    with open(ruta, 'r') as archivo:
        lineas2 = archivo.readlines()
    
    for c in range(len(lineas2)):
        lineas2[c]=lineas2[c][0:-1]
    
    l=Lexer(lineas)
    a=[]
    while(True ):
        n=l.getNextTokenTest()
        if n=="<final de archivo>":
            break
        else:
            a.append(n)
            
    assert a == lineas2




@pytest.mark.parametrize(
    "nombreArchivo",
    [
        ("iniciofin"),
        ("variables"),
        ("01"),
        ("02"),
        ("03"),
        ("04"),
        ("05"),
        ("06"),
        ("07"),
        ("08"),
        ("12"),
        ("13"),
        ("14"),
        ("17"),
        ("18"),
        ("21"),
        ("22"),
        ("23"),
        ("24"),
        
        ("26"),
        ("28"),
        ("40"),
        ("41"),
        ("42"),
        ("43"),
        ("44"),
        ("si"),
        ("si_incorrecto"),
        ("si_incorrecto_2"),
        ("25"),
      
    ]
)
def test_Sintactico(nombreArchivo):
    ruta = "./src/tests/testSintactico/"+nombreArchivo+".txt"
    rutaS  = "./src/tests/testSintactico/"+nombreArchivo+" copy.txt"
    
    salida_esperada=[]
    with open(rutaS, 'r') as archivo:
        salida_esperada = archivo.readlines()

    entrada=[]
    with open(ruta, 'r') as archivo2:
        entrada = archivo2.readlines()

    sin= sintactico(entrada)
            
            
    # Verifica que la salida generada sea igual a la salida esperada
    assert salida_esperada[0] == sin.main()
    

