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
        if lexema_token=='$':
            return ("final de archivo")
        if lexema_token == "final de archivo":
            return(self.token) 
        print("No se reconoce token",lexema_token)
    
    def salidaConjuntoLexema(self, conjuntoTokens):
        conjuntoTokens.sort()
        conjunto2=[]
        for c in conjuntoTokens:
            conjunto2.append("\""+self.salidaLexema(c)+"\"")
        
        return conjunto2
    
    def seEsperaba(self,lexema_token):
        if (lexema_token == "tkn_integer") or (lexema_token == "tkn_str") or (lexema_token == "tkn_real") or (lexema_token == "tkn_char") or (lexema_token == "id"):
            return self.lexico.lexema_token
        else: return(self.salidaLexema(lexema_token))
    
                      
 
    def errorSintaxis(self,conjunto):
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        print(self.token,conjunto)
        self.resultado="<"+self.lexico.fila_token+":"+self.lexico.columna_token+"> Error sintactico: se encontro: \""+self.seEsperaba(self.token)+"\"; se esperaba: "+ ", ".join(self.salidaConjuntoLexema(conjunto))+"."
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
        if( ( self.token == "caracter" ) or ( self.token == "procedimiento" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "inicio" ) or ( self.token == "entero" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "funcion" ) or ( self.token == "registro" ) or ( self.token == "booleano" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "caracter","procedimiento","cadena","real","inicio","entero","id","arreglo","funcion","registro","booleano" ] )
 
 
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
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "caso","lea","fin","mientras","para","repita","id","llamar","si","escriba" ] )
 
 
    def Â(self):
        print("Â")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.Â()
        elif( ( self.token == "caso" ) ):
            self.C()
            self.Â()
        elif( ( self.token == "escriba" ) ):
            self.emparejar("escriba")
            self.E()
            self.Â()
        elif( ( self.token == "lea" ) ):
            self.L()
            self.A()
        elif( ( self.token == "si" ) ):
            self.H()
            self.Â()
        elif( ( self.token == "llamar" ) ):
            self.emparejar("llamar")
            self.N()
            self.Â()
        elif( ( self.token == "mientras" ) ):
            self.M()
            self.Â()
        elif( ( self.token == "repita" ) ):
            self.I()
            self.Â()
        elif( ( self.token == "para" ) ):
            self.T()
            self.Â()
        elif( ( self.token == "retorne" ) ):
            self.Ō()
            self.Â()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "caso","lea","fin","mientras","para","retorne","repita","id","llamar","si","escriba" ] )
 
 
    def D(self):
        print("D")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "funcion" ) ):
            self.emparejar("funcion")
            self.F()
            self.D()
        elif( ( self.token == "procedimiento" ) ):
            self.emparejar("procedimiento")
            self.P()
            self.D()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "procedimiento","inicio","funcion" ] )
 
 
    def Ð(self):
        print("Ð")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "booleano" ) ):
            self.À()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "entero","caracter","id","cadena","arreglo","real","inicio","booleano" ] )
 
 
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
        elif( ( self.token == "caracter" ) or ( self.token == "procedimiento" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "inicio" ) or ( self.token == "entero" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "caracter","procedimiento","cadena","real","inicio","entero","id","arreglo","funcion","registro","booleano" ] )
 
 
    def V(self):
        print("V")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "procedimiento" ) or ( self.token == "inicio" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "caracter","procedimiento","cadena","real","inicio","entero","id","arreglo","funcion","booleano" ] )
 
 
    def F(self):
        print("F")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ī()
            self.emparejar("tkn_colon")
            self.Ü()
            self.Ð()
            self.emparejar("inicio")
            self.Â()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def P(self):
        print("P")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ī()
            self.Ð()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "id" ] )
 
 
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
        if( ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_str" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) ):
            self.Í()
            self.Ú()
        else: self.errorSintaxis( [ "verdadero","tkn_minus","tkn_real","tkn_integer","tkn_char","falso","tkn_str","id","tkn_opening_par" ] )
 
 
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
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ô()
        else: self.errorSintaxis( [ "nueva_linea","id" ] )
 
 
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
        elif( ( self.token == "caracter" ) or ( self.token == "procedimiento" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "inicio" ) or ( self.token == "entero" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "caracter","procedimiento","cadena","real","inicio","tkn_comma","entero","id","arreglo","funcion","booleano" ] )
 
 
    def Ý(self):
        print("Ý")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "caracter" ) or ( self.token == "para" ) or ( self.token == "inicio" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "booleano" ) or ( self.token == "caso" ) or ( self.token == "cadena" ) or ( self.token == "lea" ) or ( self.token == "fin" ) or ( self.token == "real" ) or ( self.token == "mientras" ) or ( self.token == "retorne" ) or ( self.token == "entero" ) or ( self.token == "llamar" ) ):
            return
        else: self.errorSintaxis( [ "caracter","para","inicio","tkn_comma","repita","id","arreglo","si","escriba","booleano","caso","cadena","lea","fin","real","mientras","retorne","entero","llamar" ] )
 
 
    def Ú(self):
        print("Ú")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ý()
        elif( ( self.token == "caso" ) or ( self.token == "lea" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "para" ) or ( self.token == "retorne" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "si" ) or ( self.token == "escriba" ) ):
            return
        else: self.errorSintaxis( [ "caso","lea","fin","mientras","para","retorne","tkn_comma","repita","id","llamar","si","escriba" ] )
 
 
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
            self.Ê()
            self.O()
            self.emparejar("de")
            self.G()
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "entero","caracter","id","cadena","arreglo","real","booleano" ] )
 
 
    def Ü(self):
        print("Ü")
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
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "entero","caracter","id","cadena","real","booleano" ] )
 
 
    def Ê(self):
        print("Ê")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.K()
        elif( ( self.token == "tkn_closing_bra" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_bra","tkn_comma" ] )
 
 
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
 
 
    def Ë(self):
        print("Ë")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) or ( self.token == "tkn_str" ) or ( self.token == "id" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
            self.É()
            self.Ä()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ä()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ë()
        else: self.errorSintaxis( [ "verdadero","tkn_minus","tkn_real","tkn_integer","tkn_char","falso","tkn_str","id","tkn_opening_par" ] )
 
 
    def Ä(self):
        print("Ä")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_less" ) or ( self.token == "o" ) or ( self.token == "tkn_greater" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "div","tkn_div","tkn_power","tkn_plus","tkn_leq","tkn_minus","tkn_times","tkn_equal","tkn_geq","mod","y","tkn_neq","tkn_less","tkn_closing_par","o","tkn_greater" ] )
 
 
    def Í(self):
        print("Í")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) or ( self.token == "tkn_str" ) or ( self.token == "id" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
            self.É()
            self.Ó()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ó()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Í()
        else: self.errorSintaxis( [ "verdadero","tkn_minus","tkn_real","tkn_integer","tkn_char","falso","tkn_str","id","tkn_opening_par" ] )
 
 
    def Ó(self):
        print("Ó")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_less" ) or ( self.token == "o" ) or ( self.token == "tkn_greater" ) ):
            self.Q()
            self.Í()
        elif( ( self.token == "caso" ) or ( self.token == "lea" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "para" ) or ( self.token == "retorne" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "llamar" ) or ( self.token == "si" ) or ( self.token == "escriba" ) ):
            return
        else: self.errorSintaxis( [ "div","tkn_equal","tkn_minus","tkn_times","para","llamar","tkn_comma","repita","mod","id","tkn_closing_par","tkn_greater","si","escriba","tkn_div","caso","tkn_power","tkn_plus","tkn_leq","lea","fin","mientras","retorne","tkn_geq","y","tkn_neq","tkn_less","o" ] )
 
 
    def Q(self):
        print("Q")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_plus" ) ):
            self.emparejar("tkn_plus")
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
        elif( ( self.token == "y" ) ):
            self.emparejar("y")
        elif( ( self.token == "o" ) ):
            self.emparejar("o")
        elif( ( self.token == "tkn_neq" ) ):
            self.emparejar("tkn_neq")
        elif( ( self.token == "tkn_leq" ) ):
            self.emparejar("tkn_leq")
        elif( ( self.token == "tkn_geq" ) ):
            self.emparejar("tkn_geq")
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
        elif( ( self.token == "tkn_equal" ) ):
            self.emparejar("tkn_equal")
        elif( ( self.token == "tkn_less" ) ):
            self.emparejar("tkn_less")
        elif( ( self.token == "tkn_greater" ) ):
            self.emparejar("tkn_greater")
        else: self.errorSintaxis( [ "div","tkn_div","tkn_power","tkn_plus","tkn_leq","tkn_minus","tkn_times","tkn_equal","tkn_geq","mod","y","tkn_neq","tkn_less","o","tkn_greater" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_char","verdadero","falso","tkn_str","id","tkn_real","tkn_integer" ] )
 
 
    def Á(self):
        print("Á")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.K()
            self.O()
        elif( ( self.token == "div" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "para" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) or ( self.token == "mod" ) or ( self.token == "id" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_greater" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "caso" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_leq" ) or ( self.token == "fin" ) or ( self.token == "tkn_plus" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "retorne" ) or ( self.token == "tkn_geq" ) or ( self.token == "y" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "llamar" ) ):
            self.Ô()
        else: self.errorSintaxis( [ "div","tkn_equal","tkn_minus","tkn_times","para","llamar","tkn_comma","repita","mod","id","tkn_closing_par","tkn_greater","si","escriba","tkn_div","caso","tkn_power","tkn_leq","fin","tkn_plus","lea","mientras","retorne","tkn_opening_bra","tkn_geq","y","tkn_neq","tkn_less","tkn_opening_par","o" ] )
 
 
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
        if( ( self.token == "caracter" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "var" ) or ( self.token == "entero" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
        else: self.errorSintaxis( [ "caracter","cadena","real","var","entero","id","arreglo","booleano" ] )
 
 
    def Ā(self):
        print("Ā")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.W()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_par","tkn_comma" ] )
 
 
    def Ē(self):
        print("Ē")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "caracter","cadena","real","var","entero","id","arreglo","booleano" ] )
 
 
    def Ī(self):
        print("Ī")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.Ã()
            self.W()
            self.Õ()
        elif( ( self.token == "caracter" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "inicio" ) or ( self.token == "entero" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "tkn_colon" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "caracter","cadena","real","inicio","entero","id","tkn_opening_par","arreglo","tkn_colon","booleano" ] )
 
 
    def Ō(self):
        print("Ō")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "retorne" ) ):
            self.emparejar("retorne")
            self.Í()
        else: self.errorSintaxis( [ "retorne" ] )
 
 
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
        if( ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
        else: self.errorSintaxis( [ "entero","caracter","id","cadena","arreglo","real","booleano" ] )
 
 
    def Å(self):
        print("Å")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "booleano" ) ):
            self.À()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "entero","caracter","id","cadena","arreglo","real","fin","booleano" ] )
 
 
    def Û(self):
        print("Û")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "fin" ) ):
            self.emparejar("fin")
        else: self.errorSintaxis( [ "fin" ] )
 
 
    def Ô(self):
        print("Ô")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Î()
            self.emparejar("tkn_closing_par")
        elif( ( self.token == "div" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "para" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) or ( self.token == "mod" ) or ( self.token == "id" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_greater" ) or ( self.token == "o" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_leq" ) or ( self.token == "fin" ) or ( self.token == "tkn_plus" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "retorne" ) or ( self.token == "tkn_geq" ) or ( self.token == "y" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_less" ) or ( self.token == "llamar" ) ):
            return
        else: self.errorSintaxis( [ "div","tkn_equal","tkn_minus","tkn_times","para","llamar","tkn_comma","repita","mod","id","tkn_closing_par","tkn_greater","si","escriba","caso","tkn_div","tkn_power","tkn_leq","fin","tkn_plus","lea","mientras","retorne","tkn_geq","y","tkn_neq","tkn_less","tkn_opening_par","o" ] )
 
 
    def Î(self):
        print("Î")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_str" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) ):
            self.Í()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "verdadero","tkn_minus","tkn_real","tkn_integer","tkn_char","falso","tkn_str","id","tkn_opening_par","tkn_closing_par" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 
