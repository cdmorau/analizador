import sys
from src.gramar2 import *
 
def errorSintaxis(conjunto):
    return(conjunto)
 
def emparejar(tknEsperado):
    if ( token == tknEsperado ):
        token= lexico.getNextToken()
    else:
        errorSintaxis([tknEsperado])
 
def S():
    if( ( token() == "dos" ) or ( token() == "seis" ) or ( token() == "cuatro" ) or ( token() == "$" ) ):
        A()
        B()
        C()
    elif( ( token() == "uno" ) or ( token() == "cuatro" ) or ( token() == "tres" ) ):
        D()
        E()
    else: errorSintaxis( [ "uno","dos","seis","tres","cuatro","$" ] )
 
 
def A():
    if( ( token() == "dos" ) ):
        emparejar("dos")
        B()
        emparejar("tres")
    else: errorSintaxis( [ "dos","seis","tres","cinco","cuatro","$" ] )
 
 
def B():
    if( ( token() == "cuatro" ) ):
        B()
        emparejar("cuatro")
        C()
        emparejar("cinco")
    else: errorSintaxis( [ "seis","tres","cinco","cuatro","$" ] )
 
 
def C():
    if( ( token() == "seis" ) ):
        emparejar("seis")
        A()
        B()
    else: errorSintaxis( [ "seis","$","cinco" ] )
 
 
def D():
    if( ( token() == "uno" ) ):
        emparejar("uno")
        A()
        E()
    elif( ( token() == "cuatro" ) or ( token() == "tres" ) ):
        B()
    else: errorSintaxis( [ "uno","cuatro","tres" ] )
 
 
def E():
    if( ( token() == "tres" ) ):
        emparejar("tres")
    else: errorSintaxis( [ "tres" ] )
 
if __name__ == "__main__":
    lexico=Lexer(sys.stdin.readlines())
    token= lexico.getNextToken()
    S()
    if (token != "FINAL ARCHIVO" ):
        errorSintaxis(["FINAL ARCHIVO"])
