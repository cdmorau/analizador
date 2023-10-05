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
        if lexema_token=='final de archivo':
            self.lexico.fila_token= self.lexico.size
            return ("final de archivo")
        if lexema_token=='$':
            self.lexico.fila_token= self.lexico.size
            return ("fin de archivo")
        
        print("No se reconoce token",lexema_token,self.lexico.lastToken)
    
    def salidaConjuntoLexema(self, conjuntoTokens):
        
        conjunto2=[]
        for c in range(len(conjuntoTokens)):
            
            if conjuntoTokens[c] in ["tkn_char","tkn_str","tkn_caracter","tkn_integer","tkn_real"] or (conjuntoTokens[c] in self.lexico.tokens_pR.keys()) or (conjuntoTokens[c] =="id"):
                conjuntoTokens[c]=self.salidaLexema(conjuntoTokens[c])

            
        conjuntoTokens.sort()

        for d in range(len(conjuntoTokens)):


            if "tkn_" == conjuntoTokens[d][0:4]:
                conjuntoTokens[d]="\""+self.salidaLexema(conjuntoTokens[d])+"\""
            else:
                conjuntoTokens[d]="\""+ conjuntoTokens[d] +"\""

        return conjuntoTokens   

    
    def seEsperaba(self,lexema_token):
        if (lexema_token == "tkn_integer") or (lexema_token == "tkn_str") or (lexema_token == "tkn_real") or (lexema_token == "tkn_char") or (lexema_token == "id"):
            return self.lexico.lexema_token
        else: return(self.salidaLexema(lexema_token))
    
                      
 
    def errorSintaxis(self,conjunto):
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        print(self.token,conjunto)
        t=self.seEsperaba(self.token)
        self.resultado="<"+self.lexico.fila_token+":"+self.lexico.columna_token+"> Error sintactico: se encontro: \""+t+"\"; se esperaba: "+ ", ".join(self.salidaConjuntoLexema(conjunto))+"."
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
        if( ( self.token == "id" ) or ( self.token == "procedimiento" ) or ( self.token == "registro" ) or ( self.token == "cadena" ) or ( self.token == "funcion" ) or ( self.token == "caracter" ) or ( self.token == "inicio" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "id","procedimiento","registro","cadena","funcion","caracter","inicio","real","entero","arreglo","booleano" ] )
 
 
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
        elif( ( self.token == "id" ) or ( self.token == "procedimiento" ) or ( self.token == "cadena" ) or ( self.token == "funcion" ) or ( self.token == "caracter" ) or ( self.token == "inicio" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","procedimiento","registro","cadena","funcion","caracter","inicio","real","entero","arreglo","booleano" ] )
 
 
    def Å(self):
        print("Å")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "caracter","real","id","cadena","entero","fin","arreglo","booleano" ] )
 
 
    def Ý(self):
        print("Ý")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "caracter" ) or ( self.token == "inicio" ) or ( self.token == "real" ) or ( self.token == "fin" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","cadena","caracter","inicio","tkn_comma","real","fin","entero","arreglo","booleano" ] )
 
 
    def V(self):
        print("V")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "inicio" ) or ( self.token == "funcion" ) or ( self.token == "procedimiento" ) ):
            return
        else: self.errorSintaxis( [ "id","procedimiento","cadena","funcion","caracter","inicio","real","entero","arreglo","booleano" ] )
 
 
    def Y(self):
        print("Y")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Y()
        elif( ( self.token == "id" ) or ( self.token == "procedimiento" ) or ( self.token == "cadena" ) or ( self.token == "funcion" ) or ( self.token == "caracter" ) or ( self.token == "inicio" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","procedimiento","cadena","funcion","caracter","inicio","tkn_comma","real","entero","arreglo","booleano" ] )
 
 
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
 
 
    def Ī(self):
        print("Ī")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
            self.emparejar("tkn_closing_par")
        elif( ( self.token == "tkn_colon" ) ):
            return
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_colon" ] )
 
 
    def Ē(self):
        print("Ē")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "cadena" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","cadena","var","caracter","real","entero","arreglo","booleano" ] )
 
 
    def Ā(self):
        print("Ā")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","tkn_closing_par" ] )
 
 
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
            self.emparejar("tkn_integer")
            self.O()
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "caracter","real","id","cadena","entero","booleano" ] )
 
 
    def Ð(self):
        print("Ð")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "caracter","inicio","real","id","cadena","entero","arreglo","booleano" ] )
 
 
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
            self.emparejar("lea")
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
            self.emparejar("retorne")
            self.Í()
            self.Â()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "para","id","caso","repita","mientras","si","escriba","llamar","retorne","fin","lea" ] )
 
 
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
            self.emparejar("lea")
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
        else: self.errorSintaxis( [ "para","id","caso","repita","mientras","si","escriba","llamar","fin","lea" ] )
 
 
    def Ḫ(self):
        print("Ḫ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.Ḫ()
        elif( ( self.token == "caso" ) ):
            self.C()
            self.Ḫ()
        elif( ( self.token == "escriba" ) ):
            self.emparejar("escriba")
            self.E()
            self.Ḫ()
        elif( ( self.token == "lea" ) ):
            self.emparejar("lea")
            self.L()
            self.Ḫ()
        elif( ( self.token == "si" ) ):
            self.H()
            self.Ḫ()
        elif( ( self.token == "llamar" ) ):
            self.emparejar("llamar")
            self.N()
            self.Ḫ()
        elif( ( self.token == "mientras" ) ):
            self.M()
            self.Ḫ()
        elif( ( self.token == "repita" ) ):
            self.I()
            self.Ḫ()
        elif( ( self.token == "para" ) ):
            self.T()
            self.Ḫ()
        elif( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "sino" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "tkn_str" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","tkn_integer","id","caso","repita","falso","tkn_char","sino","verdadero","mientras","si","escriba","llamar","tkn_colon","fin","tkn_str","lea" ] )
 
 
    def Ĕ(self):
        print("Ĕ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.Ĕ()
        elif( ( self.token == "caso" ) ):
            self.C()
            self.Ĕ()
        elif( ( self.token == "escriba" ) ):
            self.emparejar("escriba")
            self.E()
            self.Ĕ()
        elif( ( self.token == "lea" ) ):
            self.emparejar("lea")
            self.L()
            self.Ĕ()
        elif( ( self.token == "si" ) ):
            self.H()
            self.Ĕ()
        elif( ( self.token == "llamar" ) ):
            self.emparejar("llamar")
            self.N()
            self.Ĕ()
        elif( ( self.token == "mientras" ) ):
            self.M()
            self.Ĕ()
        elif( ( self.token == "repita" ) ):
            self.I()
            self.Ĕ()
        elif( ( self.token == "para" ) ):
            self.T()
            self.Ĕ()
        elif( ( self.token == "sino" ) or ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "para","id","caso","repita","sino","mientras","si","escriba","llamar","fin","lea" ] )
 
 
    def Ŭ(self):
        print("Ŭ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.Ŭ()
        elif( ( self.token == "caso" ) ):
            self.C()
            self.Ŭ()
        elif( ( self.token == "escriba" ) ):
            self.emparejar("escriba")
            self.E()
            self.Ŭ()
        elif( ( self.token == "lea" ) ):
            self.emparejar("lea")
            self.L()
            self.Ŭ()
        elif( ( self.token == "si" ) ):
            self.H()
            self.Ŭ()
        elif( ( self.token == "llamar" ) ):
            self.emparejar("llamar")
            self.N()
            self.Ŭ()
        elif( ( self.token == "mientras" ) ):
            self.M()
            self.Ŭ()
        elif( ( self.token == "repita" ) ):
            self.I()
            self.Ŭ()
        elif( ( self.token == "para" ) ):
            self.T()
            self.Ŭ()
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "para","id","caso","repita","mientras","si","escriba","llamar","hasta","lea" ] )
 
 
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
            self.Ū()
            self.U()
            self.Ð()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
            self.D()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "inicio","funcion","procedimiento" ] )
 
 
    def U(self):
        print("U")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
            self.emparejar("tkn_closing_par")
        elif( ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "caracter" ) or ( self.token == "inicio" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "arreglo" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","cadena","tkn_opening_par","caracter","inicio","real","entero","arreglo","booleano" ] )
 
 
    def B(self):
        print("B")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Á()
            self.emparejar("tkn_assign")
            self.Í()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def C(self):
        print("C")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caso" ) ):
            self.emparejar("caso")
            self.Ū()
            self.Ĭ()
            self.Ḫ()
            self.emparejar("tkn_colon")
            self.Ḫ()
            self.Ğ()
        else: self.errorSintaxis( [ "caso" ] )
 
 
    def E(self):
        print("E")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.Ḍ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def L(self):
        print("L")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.È()
            self.Ò()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def H(self):
        print("H")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "si" ) ):
            self.emparejar("si")
            self.Ṃ()
            self.emparejar("entonces")
            self.Ĕ()
            self.Ḋ()
        else: self.errorSintaxis( [ "si" ] )
 
 
    def N(self):
        print("N")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "nueva_linea" ) ):
            self.emparejar("nueva_linea")
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ù()
        else: self.errorSintaxis( [ "id","nueva_linea" ] )
 
 
    def M(self):
        print("M")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "mientras" ) ):
            self.emparejar("mientras")
            self.Ŀ()
            self.emparejar("haga")
            self.A()
            self.Û()
            self.emparejar("mientras")
        else: self.errorSintaxis( [ "mientras" ] )
 
 
    def I(self):
        print("I")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "repita" ) ):
            self.emparejar("repita")
            self.Ŭ()
            self.emparejar("hasta")
            self.Í()
        else: self.errorSintaxis( [ "repita" ] )
 
 
    def T(self):
        print("T")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "para" ) ):
            self.emparejar("para")
            self.Ū()
            self.emparejar("tkn_assign")
            self.Í()
            self.emparejar("hasta")
            self.Ŀ()
            self.emparejar("haga")
            self.A()
            self.Û()
            self.emparejar("para")
        else: self.errorSintaxis( [ "para" ] )
 
 
    def Ğ(self):
        print("Ğ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.Ĭ()
            self.Ă()
            self.emparejar("tkn_colon")
            self.Ḫ()
            self.Ğ()
        elif( ( self.token == "sino" ) ):
            self.emparejar("sino")
            self.Ḫ()
            self.Û()
            self.emparejar("caso")
        elif( ( self.token == "fin" ) ):
            self.Û()
            self.emparejar("caso")
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","fin","sino","falso","tkn_char","verdadero","tkn_str" ] )
 
 
    def Ĭ(self):
        print("Ĭ")
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
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","falso","tkn_char","verdadero","tkn_str" ] )
 
 
    def Ă(self):
        print("Ă")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Ĭ()
            self.Ă()
        elif( ( self.token == "tkn_colon" ) ):
            return
        else: self.errorSintaxis( [ "tkn_colon","tkn_comma" ] )
 
 
    def Ḋ(self):
        print("Ḋ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "sino" ) ):
            self.emparejar("sino")
            self.A()
            self.Û()
            self.emparejar("si")
        elif( ( self.token == "fin" ) ):
            self.Û()
            self.emparejar("si")
        else: self.errorSintaxis( [ "sino","fin" ] )
 
 
    def Ò(self):
        print("Ò")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.emparejar("tkn_comma")
            self.Ū()
            self.È()
            self.Ò()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "llamar" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "mientras" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "lea" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","tkn_integer","caso","repita","sino","llamar","tkn_colon","fin","id","falso","tkn_char","verdadero","mientras","si","escriba","tkn_comma","hasta","tkn_str","lea" ] )
 
 
    def È(self):
        print("È")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.O()
            self.Ì()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "llamar" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "mientras" ) or ( self.token == "tkn_period" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "tkn_comma" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "lea" ) ):
            self.Ì()
        else: self.errorSintaxis( [ "para","tkn_real","tkn_integer","caso","repita","sino","llamar","tkn_colon","fin","tkn_opening_bra","id","falso","tkn_char","verdadero","mientras","tkn_period","si","escriba","tkn_comma","hasta","tkn_str","lea" ] )
 
 
    def Ì(self):
        print("Ì")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.È()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "llamar" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "mientras" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "tkn_comma" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "lea" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","tkn_integer","caso","repita","sino","llamar","tkn_colon","fin","id","falso","tkn_char","verdadero","mientras","tkn_period","si","escriba","tkn_comma","hasta","tkn_str","lea" ] )
 
 
    def Í(self):
        print("Í")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ó(self):
        print("Ó")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Í()
        elif( ( self.token == "tkn_greater" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) ):
            self.Æ()
            self.Ḃ()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "llamar" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "mientras" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "retorne" ) or ( self.token == "tkn_comma" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "lea" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","div","tkn_colon","tkn_div","tkn_geq","o","falso","tkn_power","tkn_minus","mientras","tkn_plus","si","hasta","tkn_equal","tkn_leq","tkn_times","tkn_str","mod","lea","tkn_integer","caso","repita","tkn_neq","sino","y","tkn_greater","llamar","fin","id","tkn_less","tkn_char","verdadero","escriba","retorne","tkn_comma","tkn_closing_par","tkn_closing_bra" ] )
 
 
    def Ḃ(self):
        print("Ḃ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.É()
            self.Ḅ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ḅ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ḃ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ḅ(self):
        print("Ḅ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Í()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "llamar" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "mientras" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "retorne" ) or ( self.token == "tkn_comma" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "lea" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","div","tkn_colon","tkn_div","o","falso","tkn_power","tkn_minus","mientras","tkn_plus","si","hasta","tkn_str","tkn_times","lea","mod","tkn_integer","caso","repita","sino","y","llamar","fin","id","tkn_char","verdadero","escriba","retorne","tkn_comma","tkn_closing_par","tkn_closing_bra" ] )
 
 
    def Ë(self):
        print("Ë")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ä(self):
        print("Ä")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_greater" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) ):
            self.Æ()
            self.Ȧ()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_less","tkn_power","tkn_minus","tkn_neq","div","y","tkn_plus","tkn_equal","tkn_greater","tkn_div","tkn_geq","tkn_closing_par","o","tkn_leq","tkn_times","mod" ] )
 
 
    def Ȧ(self):
        print("Ȧ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.É()
            self.Ạ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ạ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ȧ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ạ(self):
        print("Ạ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_power","tkn_minus","div","y","tkn_plus","tkn_div","tkn_closing_par","o","tkn_times","mod" ] )
 
 
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
            self.Ù()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_char","verdadero","tkn_str" ] )
 
 
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
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
        else: self.errorSintaxis( [ "tkn_power","tkn_minus","div","y","tkn_plus","tkn_div","o","tkn_times","mod" ] )
 
 
    def Æ(self):
        print("Æ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_leq" ) ):
            self.emparejar("tkn_leq")
        elif( ( self.token == "tkn_geq" ) ):
            self.emparejar("tkn_geq")
        elif( ( self.token == "tkn_equal" ) ):
            self.emparejar("tkn_equal")
        elif( ( self.token == "tkn_less" ) ):
            self.emparejar("tkn_less")
        elif( ( self.token == "tkn_greater" ) ):
            self.emparejar("tkn_greater")
        elif( ( self.token == "tkn_neq" ) ):
            self.emparejar("tkn_neq")
        else: self.errorSintaxis( [ "tkn_greater","tkn_geq","tkn_leq","tkn_less","tkn_neq","tkn_equal" ] )
 
 
    def Á(self):
        print("Á")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
            self.Á()
        elif( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.Á()
        elif( ( self.token == "tkn_assign" ) ):
            return
        else: self.errorSintaxis( [ "tkn_assign","tkn_period","tkn_opening_bra" ] )
 
 
    def Ù(self):
        print("Ù")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
            self.Ù()
        elif( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.Ù()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Î()
            self.emparejar("tkn_closing_par")
            self.Ù()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "div" ) or ( self.token == "tkn_colon" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_geq" ) or ( self.token == "o" ) or ( self.token == "entonces" ) or ( self.token == "falso" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "mientras" ) or ( self.token == "si" ) or ( self.token == "tkn_plus" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_equal" ) or ( self.token == "lea" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_leq" ) or ( self.token == "haga" ) or ( self.token == "mod" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "tkn_neq" ) or ( self.token == "y" ) or ( self.token == "llamar" ) or ( self.token == "tkn_greater" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "retorne" ) or ( self.token == "tkn_comma" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_closing_bra" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","div","tkn_colon","tkn_div","tkn_geq","o","entonces","falso","tkn_power","tkn_minus","mientras","si","tkn_plus","hasta","tkn_str","tkn_equal","lea","tkn_times","tkn_leq","haga","mod","tkn_integer","caso","repita","sino","tkn_neq","y","llamar","tkn_greater","fin","tkn_opening_bra","id","tkn_less","tkn_char","tkn_opening_par","verdadero","tkn_period","escriba","retorne","tkn_comma","tkn_closing_par","tkn_closing_bra" ] )
 
 
    def Î(self):
        print("Î")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.Í()
            self.Ú()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_closing_par","tkn_str" ] )
 
 
    def Ḍ(self):
        print("Ḍ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.Í()
            self.Ú()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ú(self):
        print("Ú")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ú()
        elif( ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "caso" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "llamar" ) or ( self.token == "tkn_colon" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "mientras" ) or ( self.token == "si" ) or ( self.token == "escriba" ) or ( self.token == "retorne" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "hasta" ) or ( self.token == "tkn_str" ) or ( self.token == "lea" ) ):
            return
        else: self.errorSintaxis( [ "para","tkn_real","tkn_integer","caso","repita","sino","llamar","tkn_colon","fin","id","falso","tkn_char","verdadero","mientras","si","escriba","retorne","tkn_comma","tkn_closing_par","tkn_closing_bra","hasta","tkn_str","lea" ] )
 
 
    def Ṃ(self):
        print("Ṃ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.É()
            self.Ṁ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ṁ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ṃ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ȯ(self):
        print("Ȯ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.İ()
            self.K()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.K()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ȯ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ṁ(self):
        print("Ṁ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Ṃ()
        elif( ( self.token == "tkn_greater" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) ):
            self.Æ()
            self.Ȯ()
        elif( ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "tkn_less","tkn_power","tkn_minus","tkn_neq","div","y","tkn_plus","tkn_equal","tkn_greater","tkn_div","tkn_geq","o","tkn_leq","entonces","tkn_times","mod" ] )
 
 
    def K(self):
        print("K")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Ṃ()
        elif( ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "tkn_power","tkn_minus","div","y","tkn_plus","tkn_div","o","entonces","tkn_times","mod" ] )
 
 
    def İ(self):
        print("İ")
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
            self.Ṫ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_char","verdadero","tkn_str" ] )
 
 
    def Ṫ(self):
        print("Ṫ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
            self.Ṫ()
        elif( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.Ṫ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Î()
            self.emparejar("tkn_closing_par")
            self.Ṫ()
        elif( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "entonces" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            return
        else: self.errorSintaxis( [ "tkn_power","tkn_minus","tkn_opening_par","mod","div","tkn_period","y","tkn_plus","tkn_div","o","entonces","tkn_times","tkn_opening_bra" ] )
 
 
    def Ŀ(self):
        print("Ŀ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.É()
            self.Ọ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ọ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ŀ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ṗ(self):
        print("Ṗ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "tkn_char" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) ):
            self.Ṣ()
            self.Ṙ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ṙ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ṗ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_minus","tkn_char","tkn_opening_par","verdadero","tkn_str" ] )
 
 
    def Ọ(self):
        print("Ọ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Ŀ()
        elif( ( self.token == "tkn_greater" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) ):
            self.Æ()
            self.Ṗ()
        elif( ( self.token == "haga" ) ):
            return
        else: self.errorSintaxis( [ "tkn_less","tkn_power","tkn_minus","tkn_neq","div","y","tkn_plus","tkn_equal","tkn_greater","tkn_div","tkn_geq","o","tkn_leq","haga","tkn_times","mod" ] )
 
 
    def Ṙ(self):
        print("Ṙ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            self.Q()
            self.Ŀ()
        elif( ( self.token == "haga" ) ):
            return
        else: self.errorSintaxis( [ "tkn_power","tkn_minus","div","y","tkn_plus","tkn_div","o","haga","tkn_times","mod" ] )
 
 
    def Ṣ(self):
        print("Ṣ")
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
            self.Ṅ()
        else: self.errorSintaxis( [ "tkn_real","tkn_integer","id","falso","tkn_char","verdadero","tkn_str" ] )
 
 
    def Ṅ(self):
        print("Ṅ")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
            self.Ṅ()
        elif( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.Ṅ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Î()
            self.emparejar("tkn_closing_par")
            self.Ṅ()
        elif( ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) or ( self.token == "y" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "haga" ) or ( self.token == "tkn_times" ) or ( self.token == "mod" ) ):
            return
        else: self.errorSintaxis( [ "tkn_power","tkn_minus","tkn_opening_par","mod","div","tkn_period","y","tkn_plus","tkn_div","o","haga","tkn_times","tkn_opening_bra" ] )
 
 
    def Ū(self):
        print("Ū")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def Û(self):
        print("Û")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "fin" ) ):
            self.emparejar("fin")
        else: self.errorSintaxis( [ "fin" ] )
 
 
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
            self.emparejar("tkn_integer")
            self.O()
        elif( ( self.token == "arreglo" ) ):
            self.emparejar("arreglo")
            self.J()
            self.emparejar("tkn_integer")
            self.Ê()
            self.O()
            self.emparejar("de")
            self.G()
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "caracter","real","id","cadena","entero","arreglo","booleano" ] )
 
 
    def J(self):
        print("J")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.emparejar("tkn_opening_bra")
        else: self.errorSintaxis( [ "tkn_opening_bra" ] )
 
 
    def O(self):
        print("O")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_closing_bra" ) ):
            self.emparejar("tkn_closing_bra")
        else: self.errorSintaxis( [ "tkn_closing_bra" ] )
 
 
    def Ê(self):
        print("Ê")
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("tkn_integer")
            self.Ê()
        elif( ( self.token == "tkn_closing_bra" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","tkn_closing_bra" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 
