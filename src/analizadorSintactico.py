def emparejar(tknEsperado):
    if ( token == tknEsperado ):
        token= lexico.getNextToken()
    else:
        errorSintaxis([tknEsperado])
def S():
    if( ( token() == "$" ) or ( token() == "dos" ) or ( token() == "cuatro" ) or ( token() == "seis" ) ):
        A()
        B()
        C()
    elif( ( token() == "cuatro" ) or ( token() == "tres" ) or ( token() == "uno" ) ):
        D()
        E()
    else: errorSintaxis( [ "$","tres","uno","dos","cuatro","seis" ] )
def A():
    if( ( token() == "dos" ) ):
        emparejar("dos")
        B()
        emparejar("tres")
    else: errorSintaxis( [ "$","cuatro","cinco","dos","tres","seis" ] )
def B():
    if( ( token() == "cuatro" ) ):
        B()
        emparejar("cuatro")
        C()
        emparejar("cinco")
    else: errorSintaxis( [ "$","tres","cinco","cuatro","seis" ] )
def C():
    if( ( token() == "seis" ) ):
        emparejar("seis")
        A()
        B()
    else: errorSintaxis( [ "$","seis","cinco" ] )
def D():
    if( ( token() == "uno" ) ):
        emparejar("uno")
        A()
        E()
    elif( ( token() == "cuatro" ) or ( token() == "tres" ) ):
        B()
    else: errorSintaxis( [ "cuatro","tres","uno" ] )
def E():
    if( ( token() == "tres" ) ):
        emparejar("tres")
    else: errorSintaxis( [ "tres" ] )
if __name__ == "__main__":
    token= lexico.getNextToken()
    S()
    if (token != TOKFinArchivo ):
        errorSintaxis([TOKFinArchivo])
