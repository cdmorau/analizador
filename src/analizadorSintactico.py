import sys
from src.analizadorLexico import *
 
class sintactico:
    def __init__(self,codigo):
        self.lexico=Lexer(codigo)
        self.token = self.lexico.getNextToken()
        self.resultado = "El analisis sintactico ha finalizado exitosamente."
        self.errorSintacticoEncontrado=False

    
    def salidaLexema(self, lexema_token):  
                   
        if lexema_token in self.lexico.tokens_pR.keys() or lexema_token =="id":
            return lexema_token
        elif lexema_token == "tkn_integer":
            return "valor_entero" 
        elif lexema_token == "tkn_real":
            return "valor_real"
        elif lexema_token == "tkn_str":
            return "cadena_de_caracteres"  
        elif lexema_token == "tkn_char": 
            return "caracter_simple"    
        for clave, valor in self.lexico.operadores_tokens.items():
            if valor == lexema_token[4:]:
                return clave 
        if lexema_token == "final de archivo":
            return(self.token) 
        print("No se reconoce token",lexema_token)
    
    def salidaConjuntoLexema(self, conjuntoTokens):
        conjuntoTokens.sort()
        conjunto2=[]
        for c in conjuntoTokens:
            conjunto2.append("\""+self.salidaLexema(c)+"\"")
        
        return conjunto2
    
                      
 
    def errorSintaxis(self,conjunto):
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        print(self.token,conjunto)
        self.resultado="<"+self.lexico.fila_token+":"+self.lexico.columna_token+"> Error sintactico: se encontro: \""+self.salidaLexema(self.token)+"\"; se esperaba: "+ ", ".join(self.salidaConjuntoLexema(conjunto))+"."
        self.errorSintacticoEncontrado=True
        return(self.resultado)
 
    def emparejar(self,tknEsperado):
        if (self.errorSintacticoEncontrado==True):
            return
        if ( self.token == tknEsperado ):
            self.token= self.lexico.getNextToken()
        else:
            self.errorSintaxis([tknEsperado])
 
    def S(self):
        print("S")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "procedimiento" ) or ( self.token == "funcion" ) or ( self.token == "registro" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "real","booleano","entero","inicio","caracter","id","cadena","arreglo","procedimiento","funcion","registro" ] )
 
 
    def A(self):
        print("A")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.A()
        elif( ( self.token == "caso" ) ):
            self.C()
            self.A()
        elif( ( self.token == "escriba" ) ):
            self.emparejar("escriba")
            self.E()
            self.A()
        elif( ( self.token == "lea" ) ):
            self.L()
            self.A()
        elif( ( self.token == "si" ) ):
            self.H()
            self.A()
        elif( ( self.token == "llamar" ) ):
            self.emparejar("llamar")
            self.N()
            self.A()
        elif( ( self.token == "mientras" ) ):
            self.M()
            self.A()
        elif( ( self.token == "repita" ) ):
            self.I()
            self.A()
        elif( ( self.token == "para" ) ):
            self.T()
            self.A()
        elif( ( self.token == "fin" ) or ( self.token == "retorne" ) ):
            return
        else: self.errorSintaxis( [ "caso","repita","para","llamar","mientras","escriba","fin","retorne","id","lea","si" ] )
 
 
    def D(self):
        print("D")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "funcion" ) ):
            self.emparejar("funcion")
            self.F()
            self.D()
        elif( ( self.token == "procedimiento" ) ):
            self.P()
            self.D()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "procedimiento","funcion","inicio" ] )
 
 
    def Ð(self):
        print("Ð")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) ):
            self.À()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "caracter","id","cadena","arreglo","real","entero","booleano","inicio" ] )
 
 
    def R(self):
        print("R")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) ):
            self.emparejar("registro")
            self.Å()
            self.Û()
            self.emparejar("registro")
            self.R()
        elif( ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "procedimiento" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "real","booleano","entero","inicio","caracter","id","cadena","arreglo","procedimiento","funcion","registro" ] )
 
 
    def V(self):
        print("V")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "procedimiento" ) or ( self.token == "funcion" ) or ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "real","booleano","entero","inicio","caracter","id","cadena","arreglo","procedimiento","funcion" ] )
 
 
    def F(self):
        print("F")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ī()
            self.emparejar("tkn_colon")
            self.G()
            self.Ð()
            self.emparejar("inicio")
            self.A()
            self.Ō()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def P(self):
        print("P")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "procedimiento" ) ):
            self.emparejar("procedimiento")
        else: self.errorSintaxis( [ "procedimiento" ] )
 
 
    def B(self):
        print("B")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.X()
            self.Í()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def C(self):
        print("C")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caso" ) ):
            self.emparejar("caso")
        else: self.errorSintaxis( [ "caso" ] )
 
 
    def E(self):
        print("E")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) ):
            self.U()
            self.Ú()
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str" ] )
 
 
    def L(self):
        print("L")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "lea" ) ):
            self.emparejar("lea")
        else: self.errorSintaxis( [ "lea" ] )
 
 
    def H(self):
        print("H")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "si" ) ):
            self.emparejar("si")
        else: self.errorSintaxis( [ "si" ] )
 
 
    def N(self):
        print("N")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "nueva_linea" ) ):
            self.emparejar("nueva_linea")
        else: self.errorSintaxis( [ "nueva_linea" ] )
 
 
    def M(self):
        print("M")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "mientras" ) ):
            self.emparejar("mientras")
        else: self.errorSintaxis( [ "mientras" ] )
 
 
    def I(self):
        print("I")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "repita" ) ):
            self.emparejar("repita")
        else: self.errorSintaxis( [ "repita" ] )
 
 
    def T(self):
        print("T")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "para" ) ):
            self.emparejar("para")
        else: self.errorSintaxis( [ "para" ] )
 
 
    def Y(self):
        print("Y")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Y()
        elif( ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "procedimiento" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "real","tkn_comma","booleano","entero","inicio","caracter","id","cadena","arreglo","procedimiento","funcion" ] )
 
 
    def Ý(self):
        print("Ý")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "fin" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "retorne" ) or ( self.token == "caracter" ) or ( self.token == "arreglo" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "booleano" ) or ( self.token == "inicio" ) or ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "fin","real","entero","retorne","caracter","arreglo","si","escriba","caso","repita","para","llamar","tkn_comma","mientras","booleano","inicio","id","lea","cadena" ] )
 
 
    def U(self):
        print("U")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_str" ) ):
            self.emparejar("tkn_str")
        elif( ( self.token == "tkn_char" ) ):
            self.emparejar("tkn_char")
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str" ] )
 
 
    def Ú(self):
        print("Ú")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.U()
            self.Ý()
        elif( ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "fin" ) or ( self.token == "retorne" ) or ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "si" ) or ( self.token == "escriba" ) ):
            return
        else: self.errorSintaxis( [ "caso","repita","para","llamar","tkn_comma","mientras","fin","retorne","escriba","id","lea","si" ] )
 
 
    def Z(self):
        print("Z")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.emparejar("tkn_comma")
        else: self.errorSintaxis( [ "tkn_comma" ] )
 
 
    def G(self):
        print("G")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "entero" ) ):
            self.emparejar("entero")
        elif( ( self.token == "real" ) ):
            self.emparejar("real")
        elif( ( self.token == "caracter" ) ):
            self.emparejar("caracter")
        elif( ( self.token == "booleano" ) ):
            self.emparejar("booleano")
        elif( ( self.token == "cadena" ) ):
            self.emparejar("cadena")
            self.J()
            self.K()
            self.O()
        elif( ( self.token == "arreglo" ) ):
            self.emparejar("arreglo")
            self.J()
            self.K()
            self.O()
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "caracter","id","cadena","arreglo","real","entero","booleano" ] )
 
 
    def J(self):
        print("J")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.emparejar("tkn_opening_bra")
        else: self.errorSintaxis( [ "tkn_opening_bra" ] )
 
 
    def K(self):
        print("K")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_integer" ) ):
            self.emparejar("tkn_integer")
        else: self.errorSintaxis( [ "tkn_integer" ] )
 
 
    def O(self):
        print("O")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_closing_bra" ) ):
            self.emparejar("tkn_closing_bra")
        else: self.errorSintaxis( [ "tkn_closing_bra" ] )
 
 
    def X(self):
        print("X")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_assign" ) ):
            self.emparejar("tkn_assign")
        else: self.errorSintaxis( [ "tkn_assign" ] )
 
 
    def Í(self):
        print("Í")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "tkn_integer" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) or ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_real" ) ):
            self.É()
            self.Ó()
        else: self.errorSintaxis( [ "tkn_char","tkn_integer","verdadero","falso","id","tkn_str","tkn_opening_par","tkn_real" ] )
 
 
    def Ó(self):
        print("Ó")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.É()
            self.Ó()
        elif( ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "fin" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "retorne" ) or ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "si" ) or ( self.token == "escriba" ) ):
            return
        else: self.errorSintaxis( [ "mod","fin","retorne","tkn_times","tkn_minus","si","escriba","caso","repita","tkn_div","para","llamar","mientras","tkn_closing_par","tkn_plus","id","lea","div","tkn_power" ] )
 
 
    def Q(self):
        print("Q")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_plus" ) ):
            self.emparejar("tkn_plus")
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
        elif( ( self.token == "tkn_times" ) ):
            self.emparejar("tkn_times")
        elif( ( self.token == "tkn_div" ) ):
            self.emparejar("tkn_div")
        elif( ( self.token == "tkn_power" ) ):
            self.emparejar("tkn_power")
        elif( ( self.token == "div" ) ):
            self.emparejar("div")
        elif( ( self.token == "mod" ) ):
            self.emparejar("mod")
        else: self.errorSintaxis( [ "tkn_times","mod","div","tkn_minus","tkn_div","tkn_power","tkn_plus" ] )
 
 
    def É(self):
        print("É")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_integer" ) ):
            self.emparejar("tkn_integer")
        elif( ( self.token == "tkn_real" ) ):
            self.emparejar("tkn_real")
        elif( ( self.token == "tkn_char" ) ):
            self.emparejar("tkn_char")
        elif( ( self.token == "tkn_str" ) ):
            self.emparejar("tkn_str")
        elif( ( self.token == "verdadero" ) ):
            self.emparejar("verdadero")
        elif( ( self.token == "falso" ) ):
            self.emparejar("falso")
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Á()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Í()
            self.emparejar("tkn_closing_par")
        else: self.errorSintaxis( [ "id","tkn_char","tkn_integer","tkn_str","verdadero","falso","tkn_real","tkn_opening_par" ] )
 
 
    def Á(self):
        print("Á")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.K()
            self.O()
        elif( ( self.token == "mod" ) or ( self.token == "fin" ) or ( self.token == "retorne" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_minus" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "tkn_div" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_plus" ) or ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "div" ) or ( self.token == "tkn_power" ) ):
            return
        else: self.errorSintaxis( [ "mod","fin","retorne","tkn_times","tkn_opening_bra","tkn_minus","si","escriba","caso","repita","tkn_div","para","llamar","mientras","tkn_closing_par","tkn_plus","id","lea","div","tkn_power" ] )
 
 
    def Ã(self):
        print("Ã")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
        else: self.errorSintaxis( [ "tkn_opening_par" ] )
 
 
    def Õ(self):
        print("Õ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_closing_par" ) ):
            self.emparejar("tkn_closing_par")
        else: self.errorSintaxis( [ "tkn_closing_par" ] )
 
 
    def W(self):
        print("W")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "var" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) ):
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
        else: self.errorSintaxis( [ "real","booleano","entero","caracter","id","var","cadena","arreglo" ] )
 
 
    def Ā(self):
        print("Ā")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.W()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","tkn_closing_par" ] )
 
 
    def Ē(self):
        print("Ē")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "real","booleano","entero","caracter","id","var","cadena","arreglo" ] )
 
 
    def Ī(self):
        print("Ī")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.Ã()
            self.W()
            self.Õ()
        elif( ( self.token == "tkn_colon" ) ):
            return
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_colon" ] )
 
 
    def Ō(self):
        print("Ō")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "retorne" ) ):
            self.emparejar("retorne")
            self.Í()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "fin","retorne" ] )
 
 
    def Ū(self):
        print("Ū")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def À(self):
        print("À")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
        else: self.errorSintaxis( [ "caracter","id","cadena","arreglo","real","entero","booleano" ] )
 
 
    def Å(self):
        print("Å")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) ):
            self.À()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "caracter","id","cadena","arreglo","fin","real","entero","booleano" ] )
 
 
    def Û(self):
        print("Û")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "fin" ) ):
            self.emparejar("fin")
        else: self.errorSintaxis( [ "fin" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 
