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
        
        #print("No se reconoce token",lexema_token,self.lexico.lastToken)
    
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "procedimiento" ) or ( self.token == "entero" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "arreglo" ) or ( self.token == "registro" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.Ṭ()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "procedimiento","entero","funcion","booleano","cadena","inicio","caracter","id","real","arreglo","registro" ] )
 
 
    def Ṭ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "llamar" ) or ( self.token == "repita" ) or ( self.token == "escriba" ) or ( self.token == "lea" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "id" ) or ( self.token == "caso" ) ):
            self.Ẋ()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "llamar","repita","escriba","lea","si","para","mientras","id","fin","caso" ] )
 
 
    def R(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) ):
            self.emparejar("registro")
            self.Ū()
            self.Å()
            self.Û()
            self.emparejar("registro")
            self.R()
        elif( ( self.token == "procedimiento" ) or ( self.token == "entero" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "arreglo" ) ):
            return
        else: self.errorSintaxis( [ "procedimiento","entero","funcion","booleano","cadena","inicio","caracter","id","real","arreglo","registro" ] )
 
 
    def Å(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "caracter","id","entero","real","booleano","cadena","arreglo","fin" ] )
 
 
    def Ý(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "entero" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "arreglo" ) or ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","entero","booleano","cadena","inicio","caracter","id","real","arreglo","fin" ] )
 
 
    def V(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "funcion" ) or ( self.token == "inicio" ) or ( self.token == "procedimiento" ) ):
            return
        else: self.errorSintaxis( [ "procedimiento","entero","funcion","booleano","cadena","inicio","caracter","id","real","arreglo" ] )
 
 
    def Y(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Y()
        elif( ( self.token == "procedimiento" ) or ( self.token == "entero" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "arreglo" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","procedimiento","entero","funcion","booleano","cadena","inicio","caracter","id","real","arreglo" ] )
 
 
    def F(self):
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) ):
            return
        else: self.errorSintaxis( [ "var","entero","booleano","cadena","caracter","id","real","arreglo" ] )
 
 
    def Ā(self):
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
        else: self.errorSintaxis( [ "caracter","id","entero","real","booleano","cadena" ] )
 
 
    def Ð(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "arreglo" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "caracter","id","inicio","entero","real","booleano","cadena","arreglo" ] )
 
 
    def Â(self):
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
            self.Â()
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
        else: self.errorSintaxis( [ "llamar","retorne","repita","escriba","lea","si","para","mientras","id","fin","caso" ] )
 
 
    def Ẋ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.B()
            self.Ṭ()
        elif( ( self.token == "caso" ) ):
            self.C()
            self.Ṭ()
        elif( ( self.token == "escriba" ) ):
            self.emparejar("escriba")
            self.E()
            self.Ṭ()
        elif( ( self.token == "lea" ) ):
            self.emparejar("lea")
            self.L()
            self.Ṭ()
        elif( ( self.token == "si" ) ):
            self.H()
            self.Ṭ()
        elif( ( self.token == "llamar" ) ):
            self.emparejar("llamar")
            self.N()
            self.Ṭ()
        elif( ( self.token == "mientras" ) ):
            self.M()
            self.Ṭ()
        elif( ( self.token == "repita" ) ):
            self.Ȧ()
            self.Ṭ()
        elif( ( self.token == "para" ) ):
            self.T()
            self.Ṭ()
        else: self.errorSintaxis( [ "llamar","repita","escriba","lea","si","para","mientras","id","caso" ] )
 
 
    def D(self):
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
            self.Ṭ()
            self.emparejar("fin")
            self.D()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "funcion","inicio","procedimiento" ] )
 
 
    def U(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
            self.emparejar("tkn_closing_par")
        elif( ( self.token == "entero" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "arreglo" ) ):
            return
        else: self.errorSintaxis( [ "entero","tkn_opening_par","booleano","cadena","inicio","caracter","id","real","arreglo" ] )
 
 
    def B(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Á()
            self.emparejar("tkn_assign")
            self.Í()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def C(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "caso" ) ):
            self.emparejar("caso")
            self.Ū()
            self.Ṇ()
            self.Ă()
            self.emparejar("tkn_colon")
            self.Ŭ()
            self.Ğ()
            self.Ĭ()
        else: self.errorSintaxis( [ "caso" ] )
 
 
    def E(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_minus" ) ):
            self.Ḍ()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def L(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
            self.È()
            self.Ò()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def H(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "si" ) ):
            self.emparejar("si")
            self.Ŀ()
            self.emparejar("entonces")
            self.Ĕ()
            self.Ḋ()
        else: self.errorSintaxis( [ "si" ] )
 
 
    def N(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "nueva_linea" ) ):
            self.emparejar("nueva_linea")
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ù()
        else: self.errorSintaxis( [ "id","nueva_linea" ] )
 
 
    def M(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "mientras" ) ):
            self.emparejar("mientras")
            self.Ṃ()
            self.emparejar("haga")
            self.Ṭ()
            self.Û()
            self.emparejar("mientras")
        else: self.errorSintaxis( [ "mientras" ] )
 
 
    def I(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "repita" ) ):
            self.emparejar("repita")
            self.Ḫ()
            self.emparejar("hasta")
            self.Í()
        else: self.errorSintaxis( [ "repita" ] )
 
 
    def Ȧ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "repita" ) ):
            self.emparejar("repita")
            self.Ḫ()
            self.emparejar("hasta")
            self.Ō()
        else: self.errorSintaxis( [ "repita" ] )
 
 
    def Ḫ(self):
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
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "llamar","repita","hasta","escriba","lea","si","para","mientras","id","caso" ] )
 
 
    def Ĕ(self):
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
        elif( ( self.token == "fin" ) or ( self.token == "sino" ) ):
            return
        else: self.errorSintaxis( [ "llamar","repita","escriba","lea","si","para","mientras","id","sino","fin","caso" ] )
 
 
    def Ŭ(self):
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
        elif( ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "llamar","tkn_char","repita","falso","tkn_real","verdadero","escriba","lea","si","para","mientras","id","tkn_integer","tkn_str","sino","fin","caso" ] )
 
 
    def T(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "para" ) ):
            self.emparejar("para")
            self.Ū()
            self.emparejar("tkn_assign")
            self.À()
            self.emparejar("hasta")
            self.Ṃ()
            self.emparejar("haga")
            self.Ṭ()
            self.Û()
            self.emparejar("para")
        else: self.errorSintaxis( [ "para" ] )
 
 
    def Ğ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
            self.Ṇ()
            self.Ă()
            self.emparejar("tkn_colon")
            self.Ŭ()
            self.Ğ()
        elif( ( self.token == "fin" ) or ( self.token == "sino" ) ):
            return
        else: self.errorSintaxis( [ "tkn_char","tkn_str","falso","tkn_real","sino","verdadero","fin","tkn_integer" ] )
 
 
    def Ṇ(self):
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
        else: self.errorSintaxis( [ "tkn_char","tkn_str","falso","tkn_real","verdadero","tkn_integer" ] )
 
 
    def Ĭ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "sino" ) ):
            self.emparejar("sino")
            self.Ṭ()
            self.Û()
            self.emparejar("caso")
        elif( ( self.token == "fin" ) ):
            self.Û()
            self.emparejar("caso")
        else: self.errorSintaxis( [ "fin","sino" ] )
 
 
    def Ă(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Ṇ()
            self.Ă()
        elif( ( self.token == "tkn_colon" ) ):
            return
        else: self.errorSintaxis( [ "tkn_colon","tkn_comma" ] )
 
 
    def Ḋ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "sino" ) ):
            self.emparejar("sino")
            self.Ṭ()
            self.Û()
            self.emparejar("si")
        elif( ( self.token == "fin" ) ):
            self.Û()
            self.emparejar("si")
        else: self.errorSintaxis( [ "fin","sino" ] )
 
 
    def Ò(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.emparejar("tkn_comma")
            self.Ū()
            self.È()
            self.Ò()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "repita" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","retorne","tkn_char","tkn_real","hasta","verdadero","escriba","si","para","mientras","tkn_str","sino","fin","tkn_comma","repita","falso","lea","tkn_integer","id","caso" ] )
 
 
    def È(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.O()
            self.Ì()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_period" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "caso" ) ):
            self.Ì()
        else: self.errorSintaxis( [ "llamar","retorne","tkn_char","tkn_real","hasta","verdadero","escriba","si","para","mientras","tkn_period","tkn_str","sino","tkn_opening_bra","fin","tkn_comma","repita","falso","lea","tkn_integer","id","caso" ] )
 
 
    def Ì(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.È()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","retorne","tkn_char","tkn_real","hasta","verdadero","escriba","si","para","mientras","tkn_period","tkn_str","sino","fin","tkn_comma","repita","falso","lea","tkn_integer","id","caso" ] )
 
 
    def Í(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ó(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Í()
        elif( ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) ):
            self.Æ()
            self.Ȯ()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "repita" ) or ( self.token == "tkn_comma" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","hasta","verdadero","escriba","tkn_closing_bra","si","para","mientras","tkn_less","tkn_str","sino","fin","tkn_div","y","repita","tkn_leq","lea","id","div","tkn_times","tkn_power","tkn_plus","tkn_closing_par","retorne","tkn_char","tkn_real","tkn_neq","tkn_minus","tkn_geq","tkn_comma","falso","tkn_integer","o","mod","tkn_equal","tkn_greater","caso" ] )
 
 
    def Ȯ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ạ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Í()
        elif():
            return
        else: self.errorSintaxis( [ "tkn_div","y","o","tkn_minus","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ë(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ä(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) ):
            self.Æ()
            self.Ḃ()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","tkn_neq","tkn_equal","tkn_leq","tkn_greater","o","tkn_minus","tkn_less","tkn_closing_par","mod","div","tkn_geq","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ḃ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ḅ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","o","tkn_minus","tkn_closing_par","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
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
            self.Ù()
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str","falso","tkn_real","verdadero","tkn_integer" ] )
 
 
    def Q(self):
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
        else: self.errorSintaxis( [ "tkn_div","y","o","tkn_minus","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Æ(self):
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
        else: self.errorSintaxis( [ "tkn_less","tkn_neq","tkn_equal","tkn_geq","tkn_leq","tkn_greater" ] )
 
 
    def Á(self):
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
        else: self.errorSintaxis( [ "tkn_period","tkn_opening_bra","tkn_assign" ] )
 
 
    def Ù(self):
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
        elif( ( self.token == "llamar" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_str" ) or ( self.token == "entonces" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "repita" ) or ( self.token == "tkn_leq" ) or ( self.token == "lea" ) or ( self.token == "id" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_plus" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_comma" ) or ( self.token == "falso" ) or ( self.token == "tkn_integer" ) or ( self.token == "o" ) or ( self.token == "haga" ) or ( self.token == "mod" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_greater" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","hasta","tkn_opening_par","verdadero","escriba","tkn_closing_bra","si","para","mientras","tkn_less","tkn_str","entonces","sino","fin","tkn_div","y","repita","tkn_leq","lea","id","tkn_times","tkn_power","tkn_closing_par","tkn_plus","retorne","tkn_char","tkn_real","tkn_equal","tkn_period","tkn_neq","tkn_minus","tkn_opening_bra","tkn_geq","tkn_comma","falso","tkn_integer","o","haga","mod","div","tkn_greater","caso" ] )
 
 
    def Î(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_minus" ) ):
            self.Í()
            self.Ú()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus","tkn_closing_par" ] )
 
 
    def Ḍ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_minus" ) ):
            self.Í()
            self.Ú()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ú(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ú()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "caso" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "repita" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "llamar","retorne","tkn_char","tkn_real","hasta","verdadero","tkn_closing_bra","escriba","si","para","mientras","tkn_str","sino","fin","tkn_comma","repita","falso","lea","tkn_integer","id","tkn_closing_par","caso" ] )
 
 
    def Ṃ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ṁ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Ṃ()
        elif( ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) ):
            self.Æ()
            self.Ȯ()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "caso" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "repita" ) or ( self.token == "tkn_comma" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "haga" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "llamar","hasta","verdadero","escriba","tkn_closing_bra","si","para","mientras","tkn_less","tkn_str","sino","fin","tkn_div","y","repita","tkn_leq","lea","id","div","tkn_times","tkn_power","tkn_plus","tkn_closing_par","retorne","tkn_char","tkn_real","tkn_neq","tkn_minus","tkn_geq","tkn_comma","falso","tkn_integer","o","haga","mod","tkn_equal","tkn_greater","caso" ] )
 
 
    def K(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Ṃ()
        elif( ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "repita" ) or ( self.token == "tkn_comma" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "haga" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","hasta","verdadero","escriba","tkn_closing_bra","si","para","mientras","tkn_str","sino","fin","tkn_div","y","repita","lea","id","tkn_times","tkn_power","tkn_plus","tkn_closing_par","retorne","tkn_char","tkn_real","tkn_minus","tkn_comma","falso","tkn_integer","o","haga","mod","div","caso" ] )
 
 
    def İ(self):
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
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str","falso","tkn_real","verdadero","tkn_integer" ] )
 
 
    def Ṫ(self):
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
        elif( ( self.token == "llamar" ) or ( self.token == "hasta" ) or ( self.token == "verdadero" ) or ( self.token == "escriba" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_str" ) or ( self.token == "sino" ) or ( self.token == "fin" ) or ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "repita" ) or ( self.token == "lea" ) or ( self.token == "id" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "retorne" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_comma" ) or ( self.token == "falso" ) or ( self.token == "tkn_integer" ) or ( self.token == "o" ) or ( self.token == "haga" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","hasta","tkn_opening_par","verdadero","escriba","tkn_closing_bra","si","para","mientras","tkn_str","sino","fin","tkn_div","y","repita","lea","id","tkn_times","tkn_power","tkn_plus","tkn_closing_par","retorne","tkn_char","tkn_real","tkn_period","tkn_minus","tkn_opening_bra","tkn_comma","falso","tkn_integer","o","haga","mod","div","caso" ] )
 
 
    def Ŀ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ṗ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ọ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Ŀ()
        elif( ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) ):
            self.Æ()
            self.Ṗ()
        elif( ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","tkn_neq","tkn_equal","tkn_leq","tkn_greater","o","tkn_minus","tkn_less","entonces","mod","div","tkn_geq","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ṙ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.Ŀ()
        elif( ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","o","tkn_minus","entonces","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ṣ(self):
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
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str","falso","tkn_real","verdadero","tkn_integer" ] )
 
 
    def Ṅ(self):
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
        elif( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "entonces" ) or ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","tkn_opening_par","tkn_times","o","tkn_minus","entonces","tkn_period","mod","div","tkn_opening_bra","tkn_power","tkn_plus" ] )
 
 
    def À(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
            self.Ø()
            self.Ã()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ã()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.À()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def W(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
            self.É()
            self.Õ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Õ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.W()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ã(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.À()
        elif( ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) ):
            self.Æ()
            self.W()
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","tkn_neq","hasta","tkn_equal","tkn_leq","tkn_greater","o","tkn_minus","tkn_less","mod","div","tkn_geq","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Õ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Q()
            self.À()
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","y","hasta","o","tkn_minus","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ø(self):
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
            self.Ŏ()
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str","falso","tkn_real","verdadero","tkn_integer" ] )
 
 
    def Ŏ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
            self.Ŏ()
        elif( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.Ŏ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Î()
            self.emparejar("tkn_closing_par")
            self.Ŏ()
        elif( ( self.token == "hasta" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "tkn_leq" ) or ( self.token == "o" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            return
        else: self.errorSintaxis( [ "hasta","tkn_opening_par","tkn_less","tkn_period","tkn_neq","tkn_minus","tkn_opening_bra","tkn_geq","tkn_div","y","tkn_leq","o","div","mod","tkn_equal","tkn_greater","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ō(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
            self.Ḓ()
            self.Ĝ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ĝ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ō()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ů(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) ):
            self.Ḓ()
            self.Ĉ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ë()
            self.emparejar("tkn_closing_par")
            self.Ĉ()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.Ů()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ĝ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Ẇ()
            self.Ō()
        elif( ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) ):
            self.Ẏ()
            self.Ů()
        elif( ( self.token == "llamar" ) or ( self.token == "repita" ) or ( self.token == "escriba" ) or ( self.token == "lea" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "id" ) or ( self.token == "fin" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","escriba","si","para","mientras","tkn_less","caso","tkn_neq","tkn_minus","tkn_geq","fin","tkn_div","y","repita","tkn_leq","lea","o","id","div","mod","tkn_equal","tkn_greater","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ĉ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "o" ) or ( self.token == "tkn_minus" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) ):
            self.Ẇ()
            self.Ō()
        elif( ( self.token == "llamar" ) or ( self.token == "repita" ) or ( self.token == "escriba" ) or ( self.token == "lea" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "id" ) or ( self.token == "fin" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","escriba","si","para","mientras","caso","tkn_minus","fin","tkn_div","y","repita","lea","o","id","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ḓ(self):
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
            self.Ḙ()
        else: self.errorSintaxis( [ "id","tkn_char","tkn_str","falso","tkn_real","verdadero","tkn_integer" ] )
 
 
    def Ẏ(self):
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
        else: self.errorSintaxis( [ "tkn_less","tkn_neq","tkn_equal","tkn_geq","tkn_leq","tkn_greater" ] )
 
 
    def Ḙ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ĵ()
            self.O()
            self.Ḙ()
        elif( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.Ḙ()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ṿ()
            self.emparejar("tkn_closing_par")
            self.Ḙ()
        elif( ( self.token == "llamar" ) or ( self.token == "tkn_equal" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "mientras" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_geq" ) or ( self.token == "fin" ) or ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "repita" ) or ( self.token == "tkn_leq" ) or ( self.token == "lea" ) or ( self.token == "o" ) or ( self.token == "tkn_plus" ) or ( self.token == "id" ) or ( self.token == "mod" ) or ( self.token == "div" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_power" ) or ( self.token == "caso" ) ):
            return
        else: self.errorSintaxis( [ "llamar","tkn_opening_par","escriba","si","para","mientras","tkn_less","tkn_period","caso","tkn_neq","tkn_minus","tkn_opening_bra","tkn_geq","fin","tkn_div","y","repita","tkn_leq","lea","o","id","div","mod","tkn_equal","tkn_greater","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ẇ(self):
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
        else: self.errorSintaxis( [ "tkn_div","y","o","tkn_minus","mod","div","tkn_times","tkn_power","tkn_plus" ] )
 
 
    def Ḽ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_minus" ) ):
            self.Í()
            self.Ĵ()
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus" ] )
 
 
    def Ĵ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ĵ()
        elif( ( self.token == "tkn_closing_bra" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_comma","tkn_closing_bra","tkn_closing_par" ] )
 
 
    def Ṿ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_char" ) or ( self.token == "falso" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_minus" ) ):
            self.Í()
            self.Ĵ()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_char","falso","tkn_real","tkn_opening_par","verdadero","tkn_integer","id","tkn_str","tkn_minus","tkn_closing_par" ] )
 
 
    def Ū(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def Û(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "fin" ) ):
            self.emparejar("fin")
        else: self.errorSintaxis( [ "fin" ] )
 
 
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
        else: self.errorSintaxis( [ "caracter","id","entero","real","booleano","cadena","arreglo" ] )
 
 
    def J(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.emparejar("tkn_opening_bra")
        else: self.errorSintaxis( [ "tkn_opening_bra" ] )
 
 
    def O(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_closing_bra" ) ):
            self.emparejar("tkn_closing_bra")
        else: self.errorSintaxis( [ "tkn_closing_bra" ] )
 
 
    def Ê(self):
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
 
 
