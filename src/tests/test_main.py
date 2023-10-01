import pytest

from src.analizadorLexico import *


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
        n=l.getNextToken()
        if n=="FINAL ARCHIVO":
            break
        else:
            a.append(n)
            
    assert a == lineas2



