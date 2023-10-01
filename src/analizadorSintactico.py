import sys
from src.analizadorLexico import *
 
def errorSintaxis(conjunto):
    return(conjunto)
 
def emparejar(tknEsperado):
    if ( token == tknEsperado ):
        token= lexico.getNextToken()
    else:
        errorSintaxis([tknEsperado])
 
def S():
    if( ( token == "procedimiento" ) or ( token == "inicio" ) or ( token == "booleano" ) or ( token == "real" ) or ( token == "caracter" ) or ( token == "funcion" ) or ( token == "registro" ) or ( token == "entero" ) or ( token == "cadenaopening_bratkn_integerclosing_bra" ) ):
        D()
        emparejar("inicio")
        A()
        emparejar("fin")
    else: errorSintaxis( [ "procedimiento","inicio","booleano","real","caracter","funcion","registro","entero","cadenaopening_bratkn_integerclosing_bra" ] )
 
 
def A():
    if( ( token == "asignaciones" ) ):
        B()
        A()
    elif( ( token == "casos" ) ):
        C()
        A()
    elif( ( token == "escribir" ) ):
        E()
        A()
    elif( ( token == "estructura" ) ):
        L()
        A()
    elif( ( token == "estructurassi" ) ):
        H()
        A()
    elif( ( token == "estructuranuevalinea" ) ):
        N()
        A()
    elif( ( token == "estructuramientras" ) ):
        M()
        A()
    elif( ( token == "estructurarepita" ) ):
        I()
        A()
    elif( ( token == "estructuradefor" ) ):
        T()
        A()
    else: errorSintaxis( [ "estructuradefor","estructura","casos","asignaciones","fin","estructurassi","escribir","estructuramientras","estructuranuevalinea","estructurarepita" ] )
 
 
def D():
    if( ( token == "registro" ) ):
        R()
        D()
    elif( ( token == "entero" ) or ( token == "booleano" ) or ( token == "real" ) or ( token == "caracter" ) or ( token == "cadenaopening_bratkn_integerclosing_bra" ) ):
        V()
        D()
    elif( ( token == "funcion" ) ):
        F()
        D()
    elif( ( token == "procedimiento" ) ):
        P()
        D()
    else: errorSintaxis( [ "procedimiento","inicio","booleano","real","caracter","funcion","registro","entero","cadenaopening_bratkn_integerclosing_bra" ] )
 
 
def R():
    if( ( token == "registro" ) ):
        emparejar("registro")
    else: errorSintaxis( [ "registro" ] )
 
 
def V():
    if( ( token == "entero" ) or ( token == "booleano" ) or ( token == "real" ) or ( token == "caracter" ) or ( token == "cadenaopening_bratkn_integerclosing_bra" ) ):
        G()
        emparejar("id")
        Y()
    else: errorSintaxis( [ "entero","booleano","real","caracter","cadenaopening_bratkn_integerclosing_bra" ] )
 
 
def F():
    if( ( token == "funcion" ) ):
        emparejar("funcion")
    else: errorSintaxis( [ "funcion" ] )
 
 
def P():
    if( ( token == "procedimiento" ) ):
        emparejar("procedimiento")
    else: errorSintaxis( [ "procedimiento" ] )
 
 
def B():
    if( ( token == "asignaciones" ) ):
        emparejar("asignaciones")
    else: errorSintaxis( [ "asignaciones" ] )
 
 
def C():
    if( ( token == "casos" ) ):
        emparejar("casos")
    else: errorSintaxis( [ "casos" ] )
 
 
def E():
    if( ( token == "escribir" ) ):
        emparejar("escribir")
    else: errorSintaxis( [ "escribir" ] )
 
 
def L():
    if( ( token == "estructura" ) ):
        emparejar("estructura")
        L()
        emparejar("ea")
    else: errorSintaxis( [ "estructura" ] )
 
 
def H():
    if( ( token == "estructurassi" ) ):
        emparejar("estructurassi")
    else: errorSintaxis( [ "estructurassi" ] )
 
 
def N():
    if( ( token == "estructuranuevalinea" ) ):
        emparejar("estructuranuevalinea")
    else: errorSintaxis( [ "estructuranuevalinea" ] )
 
 
def M():
    if( ( token == "estructuramientras" ) ):
        emparejar("estructuramientras")
    else: errorSintaxis( [ "estructuramientras" ] )
 
 
def I():
    if( ( token == "estructurarepita" ) ):
        emparejar("estructurarepita")
    else: errorSintaxis( [ "estructurarepita" ] )
 
 
def T():
    if( ( token == "estructuradefor" ) ):
        emparejar("estructuradefor")
    else: errorSintaxis( [ "estructuradefor" ] )
 
 
def Y():
    if( ( token == "commaid" ) ):
        emparejar("commaid")
        Y()
    else: errorSintaxis( [ "procedimiento","inicio","booleano","real","caracter","funcion","registro","entero","commaid","cadenaopening_bratkn_integerclosing_bra" ] )
 
 
def G():
    if( ( token == "entero" ) ):
        emparejar("entero")
    elif( ( token == "real" ) ):
        emparejar("real")
    elif( ( token == "caracter" ) ):
        emparejar("caracter")
    elif( ( token == "booleano" ) ):
        emparejar("booleano")
    elif( ( token == "cadenaopening_bratkn_integerclosing_bra" ) ):
        emparejar("cadenaopening_bratkn_integerclosing_bra")
    else: errorSintaxis( [ "entero","booleano","real","caracter","cadenaopening_bratkn_integerclosing_bra" ] )
 
if __name__ == "__main__":
    lexico=Lexer(sys.stdin.readlines())
    token= lexico.getNextToken()
    S()
    if (token != "FINAL ARCHIVO" ):
        errorSintaxis(["FINAL ARCHIVO"])
