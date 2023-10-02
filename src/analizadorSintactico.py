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
        return(self.token) 
    
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) or ( self.token == "entero" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "caracter" ) or ( self.token == "funcion" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "inicio" ) or ( self.token == "cadena" ) or ( self.token == "procedimiento" ) ):
            self.D()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "registro","entero","id","arreglo","caracter","funcion","real","booleano","inicio","cadena","procedimiento" ] )
 
 
    def A(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.A()
        elif( ( self.token == "casos" ) ):
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
        else: self.errorSintaxis( [ "fin","repita","id","llamar","si","para","casos","escriba","lea","mientras" ] )
 
 
    def D(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) ):
            self.R()
            self.D()
        elif( ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) or ( self.token == "arreglo" ) or ( self.token == "caracter" ) or ( self.token == "cadena" ) ):
            self.V()
            self.D()
        elif( ( self.token == "funcion" ) ):
            self.emparejar("funcion")
            self.F()
            self.D()
        elif( ( self.token == "procedimiento" ) ):
            self.P()
            self.D()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "registro","entero","id","arreglo","caracter","funcion","real","booleano","inicio","cadena","procedimiento" ] )
 
 
    def Ð(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) or ( self.token == "arreglo" ) or ( self.token == "caracter" ) or ( self.token == "cadena" ) ):
            self.V()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "id","real","entero","booleano","arreglo","inicio","caracter","cadena" ] )
 
 
    def R(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) ):
            self.emparejar("registro")
        else: self.errorSintaxis( [ "registro" ] )
 
 
    def V(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) or ( self.token == "arreglo" ) or ( self.token == "caracter" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
        else: self.errorSintaxis( [ "id","real","entero","booleano","arreglo","caracter","cadena" ] )
 
 
    def F(self):
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
            self.emparejar("fin")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def P(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "procedimiento" ) ):
            self.emparejar("procedimiento")
        else: self.errorSintaxis( [ "procedimiento" ] )
 
 
    def B(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.X()
            self.Í()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def C(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "casos" ) ):
            self.emparejar("casos")
        else: self.errorSintaxis( [ "casos" ] )
 
 
    def E(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) ):
            self.U()
            self.Ú()
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str" ] )
 
 
    def L(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "lea" ) ):
            self.emparejar("lea")
        else: self.errorSintaxis( [ "lea" ] )
 
 
    def H(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "si" ) ):
            self.emparejar("si")
        else: self.errorSintaxis( [ "si" ] )
 
 
    def N(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "nueva_linea" ) ):
            self.emparejar("nueva_linea")
        else: self.errorSintaxis( [ "nueva_linea" ] )
 
 
    def M(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "mientras" ) ):
            self.emparejar("mientras")
        else: self.errorSintaxis( [ "mientras" ] )
 
 
    def I(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "repita" ) ):
            self.emparejar("repita")
        else: self.errorSintaxis( [ "repita" ] )
 
 
    def T(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "para" ) ):
            self.emparejar("para")
        else: self.errorSintaxis( [ "para" ] )
 
 
    def Y(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Y()
        elif( ( self.token == "registro" ) or ( self.token == "fin" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "caracter" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "lea" ) or ( self.token == "llamar" ) or ( self.token == "cadena" ) or ( self.token == "procedimiento" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "real" ) or ( self.token == "casos" ) or ( self.token == "escriba" ) or ( self.token == "inicio" ) or ( self.token == "mientras" ) ):
            return
        else: self.errorSintaxis( [ "registro","fin","repita","id","caracter","si","para","funcion","booleano","lea","llamar","cadena","procedimiento","entero","tkn_comma","arreglo","real","casos","escriba","inicio","mientras" ] )
 
 
    def U(self):
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.U()
            self.Y()
        elif( ( self.token == "fin" ) or ( self.token == "lea" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "casos" ) or ( self.token == "escriba" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) ):
            return
        else: self.errorSintaxis( [ "fin","repita","id","tkn_comma","llamar","si","para","casos","escriba","lea","mientras" ] )
 
 
    def Z(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.emparejar("tkn_comma")
        else: self.errorSintaxis( [ "tkn_comma" ] )
 
 
    def G(self):
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
        else: self.errorSintaxis( [ "id","real","entero","booleano","arreglo","caracter","cadena" ] )
 
 
    def J(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.emparejar("tkn_opening_bra")
        else: self.errorSintaxis( [ "tkn_opening_bra" ] )
 
 
    def K(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_integer" ) ):
            self.emparejar("tkn_integer")
        else: self.errorSintaxis( [ "tkn_integer" ] )
 
 
    def O(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_closing_bra" ) ):
            self.emparejar("tkn_closing_bra")
        else: self.errorSintaxis( [ "tkn_closing_bra" ] )
 
 
    def X(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_assign" ) ):
            self.emparejar("tkn_assign")
        else: self.errorSintaxis( [ "tkn_assign" ] )
 
 
    def Í(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "verdadero" ) or ( self.token == "falso" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "id" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
            self.É()
            self.Ó()
        else: self.errorSintaxis( [ "verdadero","falso","tkn_opening_par","id","tkn_integer","tkn_real","tkn_str","tkn_char" ] )
 
 
    def Ó(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "mod" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.É()
            self.Ó()
        elif( ( self.token == "fin" ) or ( self.token == "lea" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "casos" ) or ( self.token == "escriba" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) ):
            return
        else: self.errorSintaxis( [ "fin","tkn_minus","repita","id","si","para","tkn_power","lea","llamar","mod","tkn_closing_par","div","tkn_times","tkn_div","casos","escriba","mientras","tkn_plus" ] )
 
 
    def Q(self):
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
        else: self.errorSintaxis( [ "div","tkn_times","tkn_div","tkn_power","mod","tkn_minus","tkn_plus" ] )
 
 
    def É(self):
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
        else: self.errorSintaxis( [ "tkn_real","verdadero","tkn_str","tkn_opening_par","id","falso","tkn_integer","tkn_char" ] )
 
 
    def Á(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.K()
            self.O()
        elif( ( self.token == "fin" ) or ( self.token == "tkn_minus" ) or ( self.token == "repita" ) or ( self.token == "id" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "tkn_power" ) or ( self.token == "lea" ) or ( self.token == "llamar" ) or ( self.token == "mod" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_div" ) or ( self.token == "casos" ) or ( self.token == "escriba" ) or ( self.token == "mientras" ) or ( self.token == "tkn_plus" ) ):
            return
        else: self.errorSintaxis( [ "fin","tkn_minus","repita","id","si","para","tkn_power","lea","llamar","mod","tkn_opening_bra","tkn_closing_par","div","tkn_times","tkn_div","casos","escriba","mientras","tkn_plus" ] )
 
 
    def Ã(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
        else: self.errorSintaxis( [ "tkn_opening_par" ] )
 
 
    def Õ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_closing_par" ) ):
            self.emparejar("tkn_closing_par")
        else: self.errorSintaxis( [ "tkn_closing_par" ] )
 
 
    def W(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "booleano" ) or ( self.token == "arreglo" ) or ( self.token == "caracter" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Ā()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "id","real","entero","booleano","arreglo","caracter","cadena","tkn_closing_par" ] )
 
 
    def Ā(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.W()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","tkn_closing_par" ] )
 
 
    def Ī(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.Ã()
            self.W()
            self.Õ()
        elif( ( self.token == "tkn_colon" ) ):
            return
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_colon" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 
