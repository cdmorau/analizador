import sys

import re
import copy


class Lexer:

    def __init__(self,codigo):
        
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
        if lexema_token == "final de archivo":
            return(self.token) 
        #print("No se reconoce token",lexema_token)
    
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
        #print(self.token,conjunto)
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "procedimiento" ) or ( self.token == "inicio" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "registro" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "funcion" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "id","procedimiento","inicio","arreglo","entero","registro","cadena","real","funcion","caracter","booleano" ] )
 
 
    def A(self):
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
        else: self.errorSintaxis( [ "id","lea","mientras","repita","fin","caso","si","para","llamar","escriba" ] )
 
 
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
        else: self.errorSintaxis( [ "id","lea","mientras","retorne","repita","fin","caso","si","para","llamar","escriba" ] )
 
 
    def D(self):
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) ):
            self.À()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","id","cadena","real","inicio","caracter","booleano","entero" ] )
 
 
    def R(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) ):
            self.emparejar("registro")
            self.Å()
            self.Û()
            self.emparejar("registro")
            self.R()
        elif( ( self.token == "id" ) or ( self.token == "procedimiento" ) or ( self.token == "inicio" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "funcion" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","procedimiento","inicio","arreglo","entero","registro","cadena","real","funcion","caracter","booleano" ] )
 
 
    def V(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "procedimiento" ) or ( self.token == "inicio" ) or ( self.token == "funcion" ) ):
            return
        else: self.errorSintaxis( [ "id","procedimiento","inicio","arreglo","entero","cadena","real","funcion","caracter","booleano" ] )
 
 
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
 
 
    def P(self):
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
        if( ( self.token == "caso" ) ):
            self.emparejar("caso")
        else: self.errorSintaxis( [ "caso" ] )
 
 
    def E(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_integer" ) ):
            self.Í()
            self.Ú()
        else: self.errorSintaxis( [ "id","tkn_str","falso","tkn_opening_par","tkn_real","verdadero","tkn_char","tkn_integer" ] )
 
 
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
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ô()
        else: self.errorSintaxis( [ "id","nueva_linea" ] )
 
 
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
        elif( ( self.token == "id" ) or ( self.token == "procedimiento" ) or ( self.token == "inicio" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "funcion" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","procedimiento","inicio","arreglo","entero","cadena","real","funcion","caracter","booleano","tkn_comma" ] )
 
 
    def Ý(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "entero" ) or ( self.token == "real" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "escriba" ) or ( self.token == "caracter" ) or ( self.token == "inicio" ) or ( self.token == "retorne" ) or ( self.token == "repita" ) or ( self.token == "fin" ) or ( self.token == "arreglo" ) or ( self.token == "caso" ) or ( self.token == "cadena" ) or ( self.token == "si" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","lea","mientras","entero","real","para","llamar","escriba","caracter","inicio","retorne","repita","fin","arreglo","caso","cadena","si","booleano","tkn_comma" ] )
 
 
    def Ú(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ý()
        elif( ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "retorne" ) or ( self.token == "repita" ) or ( self.token == "fin" ) or ( self.token == "caso" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "escriba" ) ):
            return
        else: self.errorSintaxis( [ "id","lea","mientras","retorne","repita","fin","caso","si","para","llamar","escriba","tkn_comma" ] )
 
 
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
            self.Ê()
            self.O()
            self.emparejar("de")
            self.G()
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "arreglo","id","cadena","real","caracter","booleano","entero" ] )
 
 
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
            self.K()
            self.O()
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id","cadena","real","caracter","booleano","entero" ] )
 
 
    def Ê(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.K()
        elif( ( self.token == "tkn_closing_bra" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_bra","tkn_comma" ] )
 
 
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
        if( ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_integer" ) ):
            self.É()
            self.Ó()
        else: self.errorSintaxis( [ "id","tkn_str","falso","tkn_opening_par","tkn_real","verdadero","tkn_char","tkn_integer" ] )
 
 
    def Ó(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_div" ) or ( self.token == "div" ) or ( self.token == "tkn_plus" ) or ( self.token == "mod" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) ):
            self.Q()
            self.É()
            self.Ó()
        elif( ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "retorne" ) or ( self.token == "repita" ) or ( self.token == "fin" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "caso" ) or ( self.token == "si" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "escriba" ) or ( self.token == "tkn_comma" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","id","lea","mientras","para","llamar","escriba","tkn_plus","retorne","repita","fin","tkn_closing_par","tkn_minus","tkn_times","div","caso","mod","tkn_power","si","tkn_comma" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_div","div","tkn_plus","mod","tkn_power","tkn_minus","tkn_times" ] )
 
 
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
        else: self.errorSintaxis( [ "tkn_char","id","tkn_integer","tkn_opening_par","tkn_str","falso","tkn_real","verdadero" ] )
 
 
    def Á(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.K()
            self.O()
        elif( ( self.token == "tkn_div" ) or ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "escriba" ) or ( self.token == "tkn_plus" ) or ( self.token == "retorne" ) or ( self.token == "repita" ) or ( self.token == "fin" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "div" ) or ( self.token == "caso" ) or ( self.token == "mod" ) or ( self.token == "tkn_power" ) or ( self.token == "si" ) or ( self.token == "tkn_comma" ) ):
            self.Ô()
        else: self.errorSintaxis( [ "tkn_div","id","lea","mientras","para","llamar","escriba","tkn_plus","tkn_opening_bra","retorne","repita","fin","tkn_closing_par","tkn_opening_par","tkn_minus","tkn_times","div","caso","mod","tkn_power","si","tkn_comma" ] )
 
 
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
        if( ( self.token == "var" ) or ( self.token == "id" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) ):
            self.Ē()
            self.G()
            self.emparejar("id")
            self.Ā()
        else: self.errorSintaxis( [ "var","id","arreglo","entero","cadena","real","caracter","booleano" ] )
 
 
    def Ā(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.W()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_par","tkn_comma" ] )
 
 
    def Ē(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) ):
            return
        else: self.errorSintaxis( [ "var","id","arreglo","entero","cadena","real","caracter","booleano" ] )
 
 
    def Ī(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.Ã()
            self.W()
            self.Õ()
        elif( ( self.token == "id" ) or ( self.token == "inicio" ) or ( self.token == "tkn_colon" ) or ( self.token == "arreglo" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) ):
            return
        else: self.errorSintaxis( [ "id","inicio","tkn_colon","tkn_opening_par","arreglo","entero","cadena","real","caracter","booleano" ] )
 
 
    def Ō(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "retorne" ) ):
            self.emparejar("retorne")
            self.Í()
        else: self.errorSintaxis( [ "retorne" ] )
 
 
    def Ū(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def À(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
        else: self.errorSintaxis( [ "arreglo","id","cadena","real","caracter","booleano","entero" ] )
 
 
    def Å(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "cadena" ) or ( self.token == "real" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) ):
            self.À()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","id","cadena","real","fin","caracter","booleano","entero" ] )
 
 
    def Û(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "fin" ) ):
            self.emparejar("fin")
        else: self.errorSintaxis( [ "fin" ] )
 
 
    def Ô(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Î()
            self.emparejar("tkn_closing_par")
        elif( ( self.token == "tkn_div" ) or ( self.token == "id" ) or ( self.token == "lea" ) or ( self.token == "mientras" ) or ( self.token == "para" ) or ( self.token == "llamar" ) or ( self.token == "escriba" ) or ( self.token == "tkn_plus" ) or ( self.token == "retorne" ) or ( self.token == "repita" ) or ( self.token == "fin" ) or ( self.token == "tkn_closing_par" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_times" ) or ( self.token == "div" ) or ( self.token == "caso" ) or ( self.token == "mod" ) or ( self.token == "tkn_power" ) or ( self.token == "si" ) or ( self.token == "tkn_comma" ) ):
            return
        else: self.errorSintaxis( [ "tkn_div","id","lea","mientras","para","llamar","escriba","tkn_plus","retorne","repita","fin","tkn_closing_par","tkn_opening_par","tkn_minus","tkn_times","div","caso","mod","tkn_power","si","tkn_comma" ] )
 
 
    def Î(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "tkn_str" ) or ( self.token == "falso" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_real" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_integer" ) ):
            self.Í()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "id","tkn_str","falso","tkn_closing_par","tkn_opening_par","tkn_real","verdadero","tkn_char","tkn_integer" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 



s= sintactico(sys.stdin.readlines())

print(s.main())
 
