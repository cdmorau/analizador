import pytest

from src.gramar2 import Token


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
    
    l=Token(lineas)
    a=l.tkns
    while(True ):
        l.getTokens()
        if l.tkns[len(l.tkns)-1]=="FINAL ARCHIVO":
            break
            
    assert l.tkns[:len(l.tkns)-1] == lineas2



