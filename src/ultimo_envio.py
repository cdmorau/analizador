
import re
import copy
import sys


class Lexer:

    def __init__(self,codigo):
        for i in range(len(codigo)):
            codigo[i] = codigo[i].replace("\t", " " * 4)
        
        self.size=str(len(codigo)+1)
        
        self.newToken=False
        
        self.nToken=-1
        
        self.lastToken=""
        self.fila_token = "1"
        self.columna_token = "1"
        
        self.inside_comment=False
        self.inside_comilla=False
        
        #lexema
        self.lexema= ""
        
        #Array codigo
        self.codigo=codigo
        
        #linea actual
        self.linea=""
        
        #fila y columna
        
        self.fila = 1
        self.columna=1
        
        #array tokens
        self.tkns=[]
        
        #Flag para errores
        self.errorflag = False
        
        
        
        #Palabras reservadas
        self.tokens_pR = {
            "procedimiento":"procedimiento",
            "nueva_linea":"nueva_linea",
            "verdadero":"verdadero",
            "caracter":"caracter",
            "registro":"registro",
            "entonces":"entonces",
            "booleano":"booleano",
            "caracter":"caracter",
            "mientras":"mientras",
            "arreglo":"arreglo",
            "escriba":"escriba",
            "retorne":"retorne",
            "funcion":"funcion",
            "inicio":"inicio",
            "llamar":"llamar",
            "repita":"repita",
            "entero":"entero",
            "cadena":"cadena",
            "cerrar":"cerrar",
            "hasta":"hasta",
            "falso":"falso",
            "abrir":"abrir",
            "real":"real",
            "para":"para",
            "caso":"caso",
            "haga":"haga",
            "sino":"sino",
            "como":"como",
            "tipo":"tipo",
            "lea":"lea",
            "var":"var",
            "fin":"fin",
            "no":"no",
            "si":"si",
            "de":"de",
            "y":"y",
            "o":"o",
            "div":"div",
            "mod":"mod",
            
        }
        
        #Operadores
        self.operadores_tokens = {
            '<>': 'neq',
            '<=': 'leq',
            '>=': 'geq',
            '<-': 'assign',
            '.': 'period',
            ',': 'comma',
            ':': 'colon',
            ']': 'closing_bra',
            '[': 'opening_bra',
            ')': 'closing_par',
            '(': 'opening_par',
            '+': 'plus',
            '-': 'minus',
            '*': 'times',
            '/': 'div',
            '^': 'power',
            '=': 'equal',
            '<': 'less',
            '>': 'greater',
        }

        
        self.funciones = {
            'expresion_real': self.real,
            'expresion_identificador': self.identificador,
            'expresion_integer': self.integer,
            'expresion_string': self.string,
            'expresion_char': self.char,
            'expresion_palabra_reservada': self.palabra_reservada,
            'expresion_operador': self.operador
        }

        self.expresiones_regulares = {
            'expresion_real': r'[0-9][0-9]*\.[0-9][0-9]*',
            'expresion_identificador': r'^[_a-zA-Z][a-zA-Z0-9_]*',
            'expresion_integer': r'[0-9][0-9]*',
            'expresion_string': r'"[^"]{0,}"',
            'expresion_char': r"'[^']'",
            'expresion_palabra_reservada': re.compile('|'.join(re.escape(k) for k in self.tokens_pR.keys())),
            'expresion_operador': re.compile('|'.join(re.escape(k) for k in self.operadores_tokens.keys()))
        }
        
        
  
    def palabra_reservada(self):
        return "<"+self.lexema +","+str(self.fila)+","+str(self.columna)+">"
    
    def identificador(self):
        return "<id,"+self.lexema+","+str(self.fila)+","+str(self.columna)+">"

    def integer(self):
        return "<tkn_integer,"+self.lexema+","+str(self.fila)+","+str(self.columna)+">"

    def real(self):
        return "<tkn_real,"+self.lexema+","+str(self.fila)+","+str(self.columna)+">"
        
    def string(self):
        return "<tkn_str,"+self.lexema[1:len(self.lexema)-1]+","+str(self.fila)+","+str(self.columna)+">"
        
    def char(self):
        return "<tkn_char,"+self.lexema[1:len(self.lexema)-1]+","+str(self.fila)+","+str(self.columna)+">"

    def operador(self):
        return "<tkn_"+self.operadores_tokens.get(self.lexema)+","+str(self.fila)+","+str(self.columna)+">"


    #Paso de lineas 
    def getTokens(self):
        
        tinicial=len(self.tkns)

        for lin in self.codigo:
            self.linea = lin 
            self.columna=1      
            self.getToken()
            if self.newToken==True:
                self.newToken=False
                break
            
            self.fila = self.fila+1     
            
            
        tfinal=len(self.tkns)
        
        if tinicial==tfinal:
            self.tkns.append("<final de archivo>")
        
        return self.tkns
       
    #Devuelve tokens de una linea
    def getToken(self):
        #Cadena de tokens que será devuelta
        
        
        if self.linea == "" :
            return self.tkns
        #Eliminar espacios
        self.eliminar_espacios()
        self.reemplazar_comentarios2()
        
        if self.linea == "" :
            return self.tkns
        
        self.eliminar_espacios()
        
        if self.linea == "" :
            return self.tkns
        #Eliminar espacios
        
        #Versión en minuscula de la cadena
        self.linea2= copy.deepcopy(self.linea).lower()
        
        max=0
        referencia=""
        
        #Hacer que el error sea cierto a menos que encuentre una coincidencia
        
        for refe, regex in self.expresiones_regulares.items():
            m = re.match(regex,self.linea2)
            
            if m:
                if len(m.group()) >= max:
                    max = len(m.group())
                    referencia=refe
                    self.lexema=m.group()
                    if refe== 'expresion_string' or refe == 'expresion_char':
                        self.lexema= re.match(regex,self.linea).group()
                    
        #Enviar error
        if referencia=="" or re.match(r'\/\*',self.linea):
            tkn= self.errorTes()
            
            self.enviarToken(tkn)
            return self.tkns
        #Guardar token
        else:
            token = self.funciones[referencia]()
            self.enviarToken(token)
        
        return self.tkns

    #Elimina todos los comentarios y los convierte en espacios
    def eliminar_espacios(self):
        inicio=0
        
        #Eliminación de espacios en blanco
        while self.linea[inicio]==" " or self.linea[inicio] == ' ':
            self.columna = self.columna+1
            inicio= inicio+1
            if inicio>=len(self.linea):
                break
        #Eliminación de saltos de linea
        self.linea=self.linea[inicio:len(self.linea)].rstrip("\n")
        
        return self.columna
    
    #Envia los token y actualiza variables globales
    def enviarToken(self,tkn):
        self.tkns.append(tkn)
        self.borrarTokenDelCodigo()
        self.columna=1
        self.fila=1
        self.linea=""
        self.newToken=True
        if self.errorflag==True:
            self.tkns.append("<final de archivo>")
          
 
    #Reemplaza por espacios en blanco
    def reemplazar_comentarios(self,codigo):
        # Unir todas las líneas en una sola cadena
        codigo_str = "".join(codigo)
        # Expresión regular para comentarios de una línea y comentarios de varias líneas
        # Reemplazamos los comentarios con un espacio en blanco en lugar de una cadena vacía
        codigo_str = re.sub(r'/\*.*?\*/', lambda x: x.group().replace('\n', '*/\n/*'), codigo_str, flags=re.DOTALL)
        
        codigo_sin_comentarios = re.sub(r'//.*?$|/\*.*?\*/', ' ', codigo_str, flags=re.MULTILINE|re.DOTALL)

        # Dividir la cadena por saltos de línea para obtener una lista de líneas de código y devolver esta lista
        return codigo_sin_comentarios.split('\n')
    
    def reemplazar_comentarios2(self):
    
        
        #Si encuentro un comentario de linea al principio lo elimino
        if re.match(r'\/\/.*',self.linea):
            self.linea = ""
        #Si ya estaba dentro de un comentario
        elif (self.inside_comment):
            #Busco un cierre
            if "*/" in self.linea:
                #Reemplazo por espacios el cierre a la izquierda
                self.linea = re.sub(r'.*?\*/', ' ' * len(re.match(r'.*?\*/',self.linea).group()), self.linea, count=1)
                self.eliminar_espacios()
                self.inside_comment=False
            else: 
                #Elimino la linea
                self.linea = ""
                
        #Si no estaba dentro de un comentario
        else:
            #Si encuentro un comentario de linea al principio lo elimino
            if re.match(r'\/\/.*',self.linea):
                self.line = ""
                
            #Si encuentro el inicio de un comentario
            elif re.match(r'/\*.*',self.linea):
                self.inside_comment=True
                #Si tambíen encuentro el final del comentario en la misma linea
                if "*/" in self.linea[2:len(self.linea)]:
                    #Reemplazo por espacios en blanco el comentario de bloque
                    self.inside_comment=False
                    self.linea = re.sub(r'/\*.*?\*/', ' ' * len(re.match(r'/\*.*?\*/',self.linea).group()), self.linea, count =1)

                    self.eliminar_espacios()
                    
                #Si solo encontré el inicio 
                else: 
                    self.linea = ""
        
        if self.linea == "" :
            return 
        
        self.eliminar_espacios()
        
        if re.match(r'/\*.*',self.linea):
            self.reemplazar_comentarios2()
                    
    
    def borrarTokenDelCodigo(self):
        
        if self.lexema !="":

            reemplazo = " "*len(self.lexema)
            inicio = self.codigo[self.fila-1][:self.columna-1]
            fin = self.codigo[self.fila-1][self.columna-1+len(self.lexema):]
            
            self.codigo[self.fila-1] = inicio+reemplazo+fin


        
    #Manejo de errores
    def errorTes(self):
        
        self.errorflag=True
        
        return ">>> Error lexico (linea: "+str(self.fila)+", posicion: "+str(self.columna)+")"

    def getNextToken(self):
        self.getTokens()
        self.nToken=self.nToken+1
        self.lastToken = self.tkns[self.nToken]
        
        elementos= self.lastToken[1:len(self.lastToken)-1].split(',')
        
        self.tipo_token = elementos[0]
        
        if self.lastToken!="<final de archivo>":
            self.lexema_token = elementos[len(elementos)-3]
            self.fila_token = elementos[len(elementos)-2]
            self.columna_token = elementos[len(elementos)-1]
        elif self.lastToken=="<final de archivo>":
            self.fila_token = str(int(self.fila_token)+1)
            self.columna_token = "1"
            self.fila_token = self.size
        
        return self.tipo_token
        
    def getNextTokenTest(self):
        self.getTokens()
        self.nToken=self.nToken+1
        self.lastToken = self.tkns[self.nToken]
        
        elementos= self.lastToken[1:len(self.lastToken)-1].split(',')
        
        self.tipo_token = elementos[0]
        
        self.fila_token = elementos[len(elementos)-2]
        self.columna_token = elementos[len(elementos)-1]    
        
        
            
        return self.tkns[self.nToken]

 
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
        if( ( self.token == "inicio" ) or ( self.token == "booleano" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "procedimiento" ) or ( self.token == "caracter" ) or ( self.token == "registro" ) or ( self.token == "real" ) or ( self.token == "cadena" ) or ( self.token == "funcion" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.Ṭ()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "inicio","booleano","id","arreglo","entero","procedimiento","caracter","registro","real","cadena","funcion" ] )
 
 
    def Ṭ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "escriba" ) or ( self.token == "id" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "lea" ) or ( self.token == "repita" ) ):
            self.Ẋ()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "escriba","id","para","si","fin","caso","llamar","mientras","lea","repita" ] )
 
 
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
        elif( ( self.token == "inicio" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "procedimiento" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "real" ) or ( self.token == "cadena" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "inicio","booleano","id","arreglo","entero","procedimiento","caracter","registro","real","cadena","funcion" ] )
 
 
    def Å(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "booleano" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "booleano","caracter","fin","id","arreglo","entero","real","cadena" ] )
 
 
    def Ý(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "inicio" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "real" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "inicio","fin","id","arreglo","entero","caracter","tkn_comma","booleano","real","cadena" ] )
 
 
    def V(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "booleano" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "inicio" ) or ( self.token == "procedimiento" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "inicio","id","arreglo","entero","procedimiento","caracter","booleano","real","cadena","funcion" ] )
 
 
    def Y(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Y()
        elif( ( self.token == "inicio" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "procedimiento" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "real" ) or ( self.token == "cadena" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "inicio","id","arreglo","entero","procedimiento","caracter","tkn_comma","booleano","real","cadena","funcion" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_colon","tkn_opening_par" ] )
 
 
    def Ē(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "booleano" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "id","arreglo","entero","caracter","booleano","real","cadena","var" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_closing_par","tkn_comma" ] )
 
 
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
        else: self.errorSintaxis( [ "booleano","caracter","id","entero","real","cadena" ] )
 
 
    def Ð(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "booleano" ) or ( self.token == "caracter" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "booleano","inicio","caracter","id","arreglo","entero","real","cadena" ] )
 
 
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
        else: self.errorSintaxis( [ "escriba","id","para","si","retorne","fin","caso","llamar","mientras","lea","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "escriba","id","para","si","caso","llamar","mientras","lea","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "inicio","procedimiento","funcion" ] )
 
 
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
        elif( ( self.token == "inicio" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "real" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "inicio","id","arreglo","entero","tkn_opening_par","caracter","booleano","real","cadena" ] )
 
 
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
            self.emparejar("tkn_integer")
            self.Ă()
            self.emparejar("tkn_colon")
            self.Ŭ()
            self.Ğ()
            self.Ĭ()
        else: self.errorSintaxis( [ "caso" ] )
 
 
    def E(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_minus" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) ):
            self.Ḍ()
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
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
        else: self.errorSintaxis( [ "nueva_linea","id" ] )
 
 
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
        else: self.errorSintaxis( [ "escriba","id","para","si","caso","llamar","mientras","hasta","lea","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "escriba","id","para","si","fin","sino","caso","llamar","mientras","lea","repita" ] )
 
 
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
        elif( ( self.token == "fin" ) or ( self.token == "sino" ) or ( self.token == "tkn_integer" ) ):
            return
        else: self.errorSintaxis( [ "escriba","id","para","si","fin","sino","caso","tkn_integer","llamar","mientras","lea","repita" ] )
 
 
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
        if( ( self.token == "tkn_integer" ) ):
            self.emparejar("tkn_integer")
            self.Ă()
            self.emparejar("tkn_colon")
            self.Ŭ()
            self.Ğ()
        elif( ( self.token == "fin" ) or ( self.token == "sino" ) ):
            return
        else: self.errorSintaxis( [ "fin","sino","tkn_integer" ] )
 
 
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
            self.emparejar("tkn_integer")
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
        elif( ( self.token == "escriba" ) or ( self.token == "fin" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "lea" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "escriba","fin","para","si","id","sino","retorne","caso","tkn_integer","llamar","mientras","hasta","lea","tkn_comma","repita" ] )
 
 
    def È(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.O()
            self.Ì()
        elif( ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_period" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "lea" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) ):
            self.Ì()
        else: self.errorSintaxis( [ "escriba","para","si","caso","tkn_integer","tkn_opening_bra","tkn_period","fin","id","sino","retorne","llamar","mientras","hasta","lea","tkn_comma","repita" ] )
 
 
    def Ì(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.È()
        elif( ( self.token == "escriba" ) or ( self.token == "fin" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "lea" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "escriba","para","si","caso","tkn_integer","tkn_period","fin","id","sino","retorne","llamar","mientras","hasta","lea","tkn_comma","repita" ] )
 
 
    def Í(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ó(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Í()
        elif( ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_neq" ) ):
            self.Æ()
            self.Ȯ()
        elif( ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "lea" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_greater","caso","tkn_integer","tkn_leq","id","sino","retorne","tkn_less","tkn_neq","mientras","lea","tkn_power","tkn_comma","tkn_equal","tkn_minus","tkn_times","escriba","para","si","tkn_plus","tkn_closing_bra","fin","tkn_closing_par","o","llamar","tkn_div","hasta","mod","y","tkn_geq","div","repita" ] )
 
 
    def Ȯ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ạ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Í()
        elif():
            return
        else: self.errorSintaxis( [ "tkn_times","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","div" ] )
 
 
    def Ë(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ä(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_neq" ) ):
            self.Æ()
            self.Ḃ()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","tkn_equal","tkn_leq","tkn_greater","tkn_closing_par","tkn_less","tkn_neq","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","tkn_geq","div" ] )
 
 
    def Ḃ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ḅ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","tkn_closing_par","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","div" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_real","id","falso","verdadero","tkn_integer","tkn_str","tkn_char" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_times","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","div" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_leq","tkn_greater","tkn_equal","tkn_less","tkn_geq","tkn_neq" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_assign","tkn_period","tkn_opening_bra" ] )
 
 
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
        elif( ( self.token == "tkn_greater" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "entonces" ) or ( self.token == "tkn_leq" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "mientras" ) or ( self.token == "lea" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_comma" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "fin" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "o" ) or ( self.token == "llamar" ) or ( self.token == "haga" ) or ( self.token == "hasta" ) or ( self.token == "tkn_div" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_geq" ) or ( self.token == "div" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_greater","tkn_opening_par","caso","tkn_integer","entonces","tkn_leq","id","sino","retorne","tkn_less","tkn_neq","mientras","lea","tkn_power","tkn_comma","tkn_equal","tkn_minus","tkn_times","escriba","para","si","tkn_opening_bra","tkn_plus","tkn_closing_bra","tkn_period","fin","tkn_closing_par","o","llamar","haga","hasta","tkn_div","mod","y","tkn_geq","div","repita" ] )
 
 
    def Î(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_minus" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) ):
            self.Í()
            self.Ú()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_real","id","tkn_closing_par","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ḍ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_minus" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) ):
            self.Í()
            self.Ú()
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ú(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ú()
        elif( ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "lea" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "escriba","para","si","caso","tkn_integer","tkn_closing_bra","fin","id","sino","retorne","tkn_closing_par","llamar","mientras","hasta","lea","tkn_comma","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "booleano","caracter","id","arreglo","entero","real","cadena" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_closing_bra","tkn_comma" ] )
 
 
    def Ṃ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ṁ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Ṃ()
        elif( ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_neq" ) ):
            self.Æ()
            self.Ȯ()
        elif( ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "haga" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "lea" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_greater","caso","tkn_integer","tkn_leq","id","sino","retorne","tkn_less","tkn_neq","mientras","lea","tkn_power","tkn_comma","tkn_equal","tkn_minus","tkn_times","escriba","para","si","tkn_plus","tkn_closing_bra","fin","tkn_closing_par","o","haga","llamar","tkn_div","hasta","mod","y","tkn_geq","div","repita" ] )
 
 
    def K(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Ṃ()
        elif( ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "hasta" ) or ( self.token == "haga" ) or ( self.token == "lea" ) or ( self.token == "tkn_comma" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","escriba","para","si","caso","tkn_integer","tkn_plus","tkn_closing_bra","fin","id","sino","retorne","tkn_closing_par","o","llamar","mientras","tkn_div","hasta","haga","tkn_power","mod","lea","y","tkn_minus","tkn_comma","div","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_real","id","falso","verdadero","tkn_integer","tkn_str","tkn_char" ] )
 
 
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
        elif( ( self.token == "tkn_times" ) or ( self.token == "escriba" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "sino" ) or ( self.token == "retorne" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "o" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "tkn_div" ) or ( self.token == "hasta" ) or ( self.token == "haga" ) or ( self.token == "tkn_power" ) or ( self.token == "mod" ) or ( self.token == "lea" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_comma" ) or ( self.token == "div" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","escriba","para","si","tkn_opening_par","caso","tkn_integer","tkn_opening_bra","tkn_plus","tkn_closing_bra","tkn_period","fin","id","sino","retorne","tkn_closing_par","o","llamar","mientras","tkn_div","hasta","haga","tkn_power","mod","lea","y","tkn_minus","tkn_comma","div","repita" ] )
 
 
    def Ŀ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ṗ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ọ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Ŀ()
        elif( ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_neq" ) ):
            self.Æ()
            self.Ṗ()
        elif( ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "entonces","tkn_times","tkn_equal","tkn_leq","tkn_greater","tkn_less","tkn_neq","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","tkn_geq","div" ] )
 
 
    def Ṙ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.Ŀ()
        elif( ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "entonces","tkn_times","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","div" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_real","id","falso","verdadero","tkn_integer","tkn_str","tkn_char" ] )
 
 
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
        elif( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "y" ) or ( self.token == "tkn_power" ) or ( self.token == "entonces" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            return
        else: self.errorSintaxis( [ "tkn_minus","tkn_times","tkn_period","tkn_opening_par","o","tkn_div","tkn_opening_bra","tkn_power","entonces","tkn_plus","y","mod","div" ] )
 
 
    def À(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def W(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ã(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.À()
        elif( ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_neq" ) ):
            self.Æ()
            self.W()
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","tkn_equal","tkn_leq","tkn_greater","tkn_less","tkn_neq","o","tkn_div","hasta","tkn_power","tkn_plus","mod","y","tkn_minus","tkn_geq","div" ] )
 
 
    def Õ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Q()
            self.À()
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","o","tkn_div","hasta","tkn_power","tkn_plus","mod","y","tkn_minus","div" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_real","id","falso","verdadero","tkn_integer","tkn_str","tkn_char" ] )
 
 
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
        elif( ( self.token == "tkn_times" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "hasta" ) or ( self.token == "tkn_power" ) or ( self.token == "mod" ) or ( self.token == "tkn_equal" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_geq" ) or ( self.token == "div" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","tkn_greater","tkn_opening_par","tkn_opening_bra","tkn_plus","tkn_period","tkn_leq","tkn_less","tkn_neq","o","tkn_div","hasta","tkn_power","mod","tkn_equal","y","tkn_minus","tkn_geq","div" ] )
 
 
    def Ō(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ů(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) ):
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
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ĝ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Ẇ()
            self.Ō()
        elif( ( self.token == "tkn_leq" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_neq" ) ):
            self.Ẏ()
            self.Ů()
        elif( ( self.token == "escriba" ) or ( self.token == "id" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "fin" ) or ( self.token == "caso" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "lea" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","escriba","tkn_greater","para","si","caso","tkn_plus","tkn_leq","id","fin","tkn_less","tkn_neq","o","llamar","mientras","tkn_div","lea","tkn_power","mod","tkn_equal","y","tkn_minus","tkn_geq","div","repita" ] )
 
 
    def Ĉ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_times" ) or ( self.token == "o" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "div" ) ):
            self.Ẇ()
            self.Ō()
        elif( ( self.token == "escriba" ) or ( self.token == "id" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "fin" ) or ( self.token == "caso" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "lea" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","escriba","para","si","caso","tkn_plus","fin","id","o","llamar","mientras","tkn_div","lea","tkn_power","mod","y","tkn_minus","div","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_real","id","falso","verdadero","tkn_integer","tkn_str","tkn_char" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_leq","tkn_greater","tkn_equal","tkn_less","tkn_geq","tkn_neq" ] )
 
 
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
        elif( ( self.token == "tkn_times" ) or ( self.token == "escriba" ) or ( self.token == "tkn_greater" ) or ( self.token == "para" ) or ( self.token == "si" ) or ( self.token == "caso" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_leq" ) or ( self.token == "id" ) or ( self.token == "fin" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_neq" ) or ( self.token == "o" ) or ( self.token == "llamar" ) or ( self.token == "mientras" ) or ( self.token == "tkn_div" ) or ( self.token == "lea" ) or ( self.token == "tkn_power" ) or ( self.token == "mod" ) or ( self.token == "tkn_equal" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_geq" ) or ( self.token == "div" ) or ( self.token == "repita" ) ):
            return
        else: self.errorSintaxis( [ "tkn_times","escriba","tkn_greater","para","si","tkn_opening_par","caso","tkn_opening_bra","tkn_plus","tkn_period","tkn_leq","id","fin","tkn_less","tkn_neq","o","llamar","mientras","tkn_div","lea","tkn_power","mod","tkn_equal","y","tkn_minus","tkn_geq","div","repita" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_times","o","tkn_div","tkn_power","tkn_plus","mod","y","tkn_minus","div" ] )
 
 
    def Ḽ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_minus" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) ):
            self.Í()
            self.Ĵ()
        else: self.errorSintaxis( [ "tkn_real","id","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
 
    def Ĵ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ĵ()
        elif( ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_closing_bra" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_par","tkn_closing_bra","tkn_comma" ] )
 
 
    def Ṿ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_real" ) or ( self.token == "id" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_integer" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_minus" ) or ( self.token == "verdadero" ) or ( self.token == "falso" ) ):
            self.Í()
            self.Ĵ()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_real","id","tkn_closing_par","tkn_opening_par","tkn_str","tkn_integer","tkn_char","tkn_minus","verdadero","falso" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 



s= sintactico(sys.stdin.readlines())

print(s.main())
 
