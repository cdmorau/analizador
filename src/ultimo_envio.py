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
        if lexema_token=='final de archivo':
            self.lexico.fila_token= str(int(self.lexico.fila_token))
            return ("final de archivo")
        if lexema_token=='$':
            self.lexico.fila_token= str(int(self.lexico.fila_token)+1)
            return ("fin de archivo")
        
        #print("No se reconoce token",lexema_token,self.lexico.lastToken)
    
    def salidaConjuntoLexema(self, conjuntoTokens):
        
        conjunto2=[]
        for c in range(len(conjuntoTokens)):
            
            if conjuntoTokens[c] in ["tkn_char","tkn_str","tkn_caracter","tkn_integer","tkn_real"] or (conjuntoTokens[c] in self.lexico.tokens_pR.keys()) or (conjuntoTokens[c] =="id"):
                conjuntoTokens[c]=self.salidaLexema(conjuntoTokens[c])

            
        conjuntoTokens.sort()
        #print(conjuntoTokens)
        for d in range(len(conjuntoTokens)):
            #print(d)

            if "tkn_" == conjuntoTokens[d][0:4]:
                conjuntoTokens[d]="\""+self.salidaLexema(conjuntoTokens[d])+"\""
            else:
                conjuntoTokens[d]="\""+ conjuntoTokens[d] +"\""
        #print(conjuntoTokens)
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
        if( ( self.token == "arreglo" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "registro" ) or ( self.token == "entero" ) or ( self.token == "procedimiento" ) ):
            self.R()
            self.V()
            self.D()
            self.emparejar("inicio")
            self.A()
            self.emparejar("fin")
        else: self.errorSintaxis( [ "arreglo","inicio","caracter","funcion","booleano","cadena","id","real","registro","entero","procedimiento" ] )
 
 
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
        else: self.errorSintaxis( [ "caso","escriba","si","fin","mientras","repita","id","llamar","lea","para" ] )
 
 
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
        elif( ( self.token == "fin" ) or ( self.token == "tkn_integer" ) or ( self.token == "sino" ) or ( self.token == "tkn_colon" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) ):
            return
        else: self.errorSintaxis( [ "caso","verdadero","escriba","si","fin","mientras","repita","id","llamar","tkn_integer","lea","sino","tkn_colon","falso","tkn_str","para","tkn_char","tkn_real" ] )
 
 
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
        elif( ( self.token == "sino" ) or ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "caso","escriba","si","fin","mientras","repita","id","llamar","sino","lea","para" ] )
 
 
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
        else: self.errorSintaxis( [ "caso","escriba","si","fin","mientras","repita","id","llamar","lea","retorne","para" ] )
 
 
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
        elif( ( self.token == "hasta" ) ):
            return
        else: self.errorSintaxis( [ "caso","escriba","si","hasta","mientras","repita","id","llamar","lea","para" ] )
 
 
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
        else: self.errorSintaxis( [ "funcion","inicio","procedimiento" ] )
 
 
    def Ð(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Ð()
        elif( ( self.token == "inicio" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","id","inicio","caracter","real","booleano","entero","cadena" ] )
 
 
    def R(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "registro" ) ):
            self.emparejar("registro")
            self.Å()
            self.Û()
            self.emparejar("registro")
            self.R()
        elif( ( self.token == "arreglo" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "procedimiento" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","inicio","caracter","funcion","booleano","cadena","id","real","registro","entero","procedimiento" ] )
 
 
    def V(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Y()
            self.V()
        elif( ( self.token == "funcion" ) or ( self.token == "inicio" ) or ( self.token == "procedimiento" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","inicio","caracter","funcion","booleano","procedimiento","id","real","entero","cadena" ] )
 
 
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
            self.U()
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
            self.Ù()
            self.emparejar("tkn_assign")
            self.Í()
        else: self.errorSintaxis( [ "id" ] )
 
 
    def C(self):
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
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) ):
            self.Í()
            self.Ú()
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real" ] )
 
 
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
            self.Ã()
            self.emparejar("entonces")
            self.Ĕ()
            self.Ă()
        else: self.errorSintaxis( [ "si" ] )
 
 
    def N(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "nueva_linea" ) ):
            self.emparejar("nueva_linea")
        elif( ( self.token == "id" ) ):
            self.emparejar("id")
            self.Ô()
        else: self.errorSintaxis( [ "nueva_linea","id" ] )
 
 
    def M(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "mientras" ) ):
            self.emparejar("mientras")
            self.Ã()
            self.emparejar("haga")
            self.A()
            self.Û()
            self.emparejar("mientras")
        else: self.errorSintaxis( [ "mientras" ] )
 
 
    def I(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "repita" ) ):
            self.emparejar("repita")
            self.Ŭ()
            self.emparejar("hasta")
            self.Ă()
        else: self.errorSintaxis( [ "repita" ] )
 
 
    def T(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "para" ) ):
            self.emparejar("para")
            self.Ū()
            self.emparejar("tkn_assign")
            self.Í()
            self.Ĉ()
            self.Í()
            self.emparejar("haga")
            self.A()
            self.Û()
            self.emparejar("para")
        else: self.errorSintaxis( [ "para" ] )
 
 
    def Ḓ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
        elif():
            return
        else: self.errorSintaxis( [ "tkn_opening_bra" ] )
 
 
    def Ĉ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "hasta" ) ):
            self.emparejar("hasta")
        else: self.errorSintaxis( [ "hasta" ] )
 
 
    def Ğ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "sino","falso","verdadero","tkn_str","tkn_char","tkn_real","fin","tkn_integer" ] )
 
 
    def Ĭ(self):
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
        else: self.errorSintaxis( [ "falso","verdadero","tkn_str","tkn_char","tkn_real","tkn_integer" ] )
 
 
    def Ă(self):
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
 
 
    def Ã(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) ):
            self.À()
            self.Ů()
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real" ] )
 
 
    def Ů(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "o" ) or ( self.token == "y" ) ):
            self.Õ()
            self.À()
            self.Ů()
        elif( ( self.token == "tkn_closing_par" ) or ( self.token == "haga" ) or ( self.token == "entonces" ) ):
            return
        else: self.errorSintaxis( [ "haga","entonces","o","y","tkn_closing_par" ] )
 
 
    def Õ(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "y" ) ):
            self.emparejar("y")
        elif( ( self.token == "o" ) ):
            self.emparejar("o")
        else: self.errorSintaxis( [ "o","y" ] )
 
 
    def W(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
            self.É()
            self.Ō()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.W()
            self.emparejar("tkn_closing_par")
            self.Ō()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.W()
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real" ] )
 
 
    def Ō(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_div" ) ):
            self.X()
            self.Ë()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "div","mod","tkn_geq","tkn_minus","tkn_less","tkn_equal","tkn_greater","tkn_leq","tkn_power","tkn_neq","tkn_plus","tkn_times","tkn_div","tkn_closing_par" ] )
 
 
    def À(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
            self.É()
            self.K()
        elif( ( self.token == "tkn_opening_par" ) ):
            self.emparejar("tkn_opening_par")
            self.Ã()
            self.emparejar("tkn_closing_par")
            self.K()
        elif( ( self.token == "tkn_minus" ) ):
            self.emparejar("tkn_minus")
            self.À()
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real" ] )
 
 
    def K(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_geq" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_div" ) ):
            self.X()
            self.À()
        elif( ( self.token == "haga" ) or ( self.token == "entonces" ) or ( self.token == "o" ) or ( self.token == "y" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "div","mod","haga","tkn_geq","tkn_minus","y","tkn_less","tkn_equal","entonces","tkn_greater","o","tkn_leq","tkn_power","tkn_neq","tkn_plus","tkn_times","tkn_div","tkn_closing_par" ] )
 
 
    def X(self):
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
        else: self.errorSintaxis( [ "div","mod","tkn_geq","tkn_minus","tkn_less","tkn_equal","tkn_greater","tkn_leq","tkn_power","tkn_neq","tkn_plus","tkn_times","tkn_div" ] )
 
 
    def Y(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Y()
        elif( ( self.token == "arreglo" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "funcion" ) or ( self.token == "booleano" ) or ( self.token == "cadena" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "procedimiento" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","inicio","caracter","funcion","booleano","tkn_comma","procedimiento","id","real","entero","cadena" ] )
 
 
    def Ý(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.emparejar("id")
            self.Ý()
        elif( ( self.token == "arreglo" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "fin" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","inicio","caracter","booleano","tkn_comma","fin","id","real","entero","cadena" ] )
 
 
    def Ò(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.emparejar("tkn_comma")
            self.Ū()
            self.È()
            self.Ò()
        elif( ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "tkn_integer" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "hasta" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "caso" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) ):
            return
        else: self.errorSintaxis( [ "escriba","si","tkn_integer","repita","sino","hasta","falso","lea","caso","tkn_comma","fin","mientras","tkn_colon","id","llamar","verdadero","tkn_str","para","tkn_char","tkn_real" ] )
 
 
    def Ú(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_comma" ) ):
            self.Z()
            self.Í()
            self.Ú()
        elif( ( self.token == "tkn_closing_bra" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "tkn_integer" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "hasta" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "caso" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_bra","escriba","si","tkn_integer","repita","sino","hasta","falso","lea","caso","tkn_comma","fin","mientras","tkn_colon","id","llamar","retorne","verdadero","tkn_str","para","tkn_char","tkn_real","tkn_closing_par" ] )
 
 
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
        else: self.errorSintaxis( [ "arreglo","id","caracter","real","booleano","entero","cadena" ] )
 
 
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
        else: self.errorSintaxis( [ "id","caracter","real","booleano","entero","cadena" ] )
 
 
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
 
 
    def Ë(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real" ] )
 
 
    def Ä(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_geq" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_times" ) or ( self.token == "o" ) ):
            self.Q()
            self.Ë()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "div","mod","tkn_geq","y","tkn_minus","tkn_div","tkn_equal","tkn_less","tkn_greater","tkn_leq","tkn_power","tkn_neq","tkn_plus","tkn_times","o","tkn_closing_par" ] )
 
 
    def Í(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_integer" ) ):
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
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real" ] )
 
 
    def Ó(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_geq" ) or ( self.token == "y" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_div" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_less" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_leq" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_plus" ) or ( self.token == "tkn_times" ) or ( self.token == "o" ) ):
            self.Q()
            self.Í()
        elif( ( self.token == "haga" ) or ( self.token == "tkn_closing_bra" ) or ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "tkn_integer" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "hasta" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "caso" ) or ( self.token == "tkn_comma" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "retorne" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_bra","y","escriba","tkn_integer","sino","lea","tkn_plus","div","mod","tkn_comma","tkn_less","mientras","tkn_colon","retorne","tkn_power","tkn_neq","tkn_str","para","tkn_real","haga","si","hasta","repita","falso","tkn_times","tkn_div","o","tkn_geq","caso","fin","tkn_equal","tkn_greater","id","llamar","tkn_leq","verdadero","tkn_minus","tkn_char","tkn_closing_par" ] )
 
 
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
        else: self.errorSintaxis( [ "div","mod","tkn_geq","y","tkn_minus","tkn_div","tkn_equal","tkn_less","tkn_greater","tkn_leq","tkn_power","tkn_neq","tkn_plus","tkn_times","o" ] )
 
 
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
        else: self.errorSintaxis( [ "id","falso","verdadero","tkn_str","tkn_char","tkn_real","tkn_integer" ] )
 
 
    def Á(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.Ú()
            self.O()
        elif( ( self.token == "tkn_closing_bra" ) or ( self.token == "y" ) or ( self.token == "escriba" ) or ( self.token == "tkn_integer" ) or ( self.token == "sino" ) or ( self.token == "lea" ) or ( self.token == "tkn_plus" ) or ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_comma" ) or ( self.token == "tkn_less" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "retorne" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "haga" ) or ( self.token == "tkn_opening_par" ) or ( self.token == "si" ) or ( self.token == "entonces" ) or ( self.token == "hasta" ) or ( self.token == "repita" ) or ( self.token == "falso" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "tkn_geq" ) or ( self.token == "caso" ) or ( self.token == "fin" ) or ( self.token == "tkn_equal" ) or ( self.token == "tkn_greater" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "tkn_leq" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_closing_par" ) ):
            self.Ô()
        else: self.errorSintaxis( [ "tkn_closing_bra","y","escriba","tkn_integer","sino","lea","tkn_plus","div","mod","tkn_comma","tkn_less","mientras","tkn_colon","retorne","tkn_power","tkn_neq","tkn_str","para","tkn_real","haga","tkn_opening_par","tkn_opening_bra","si","entonces","hasta","repita","falso","tkn_times","tkn_div","o","tkn_geq","caso","fin","tkn_equal","tkn_greater","id","llamar","tkn_leq","verdadero","tkn_minus","tkn_char","tkn_closing_par" ] )
 
 
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
        elif( ( self.token == "tkn_assign" ) ):
            return
        else: self.errorSintaxis( [ "tkn_opening_bra","tkn_period","tkn_assign" ] )
 
 
    def È(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_bra" ) ):
            self.J()
            self.Í()
            self.O()
            self.Ì()
        elif( ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "tkn_integer" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "hasta" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "caso" ) or ( self.token == "tkn_comma" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) or ( self.token == "tkn_period" ) ):
            self.Ì()
        else: self.errorSintaxis( [ "tkn_opening_bra","escriba","si","tkn_integer","repita","sino","hasta","falso","lea","caso","tkn_comma","fin","mientras","tkn_colon","id","llamar","verdadero","tkn_str","para","tkn_char","tkn_real","tkn_period" ] )
 
 
    def Ì(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_period" ) ):
            self.emparejar("tkn_period")
            self.Ū()
            self.È()
        elif( ( self.token == "escriba" ) or ( self.token == "si" ) or ( self.token == "tkn_integer" ) or ( self.token == "repita" ) or ( self.token == "sino" ) or ( self.token == "hasta" ) or ( self.token == "falso" ) or ( self.token == "lea" ) or ( self.token == "caso" ) or ( self.token == "tkn_comma" ) or ( self.token == "fin" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) ):
            return
        else: self.errorSintaxis( [ "escriba","si","tkn_integer","repita","sino","hasta","falso","lea","caso","tkn_comma","fin","mientras","tkn_colon","id","llamar","verdadero","tkn_str","para","tkn_char","tkn_real","tkn_period" ] )
 
 
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
 
 
    def Ē(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "var" ) ):
            self.emparejar("var")
        elif( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","caracter","var","booleano","id","real","entero","cadena" ] )
 
 
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
        elif( ( self.token == "arreglo" ) or ( self.token == "inicio" ) or ( self.token == "caracter" ) or ( self.token == "booleano" ) or ( self.token == "id" ) or ( self.token == "real" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","tkn_opening_par","inicio","caracter","booleano","id","real","entero","cadena" ] )
 
 
    def Ū(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "id" ) ):
            self.emparejar("id")
        else: self.errorSintaxis( [ "id" ] )
 
 
    def Å(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "arreglo" ) or ( self.token == "id" ) or ( self.token == "caracter" ) or ( self.token == "real" ) or ( self.token == "booleano" ) or ( self.token == "entero" ) or ( self.token == "cadena" ) ):
            self.G()
            self.emparejar("id")
            self.Ý()
            self.Å()
        elif( ( self.token == "fin" ) ):
            return
        else: self.errorSintaxis( [ "arreglo","id","caracter","real","fin","booleano","entero","cadena" ] )
 
 
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
        elif( ( self.token == "tkn_closing_bra" ) or ( self.token == "escriba" ) or ( self.token == "y" ) or ( self.token == "tkn_integer" ) or ( self.token == "sino" ) or ( self.token == "lea" ) or ( self.token == "tkn_plus" ) or ( self.token == "div" ) or ( self.token == "mod" ) or ( self.token == "tkn_comma" ) or ( self.token == "tkn_less" ) or ( self.token == "mientras" ) or ( self.token == "tkn_colon" ) or ( self.token == "retorne" ) or ( self.token == "tkn_power" ) or ( self.token == "tkn_neq" ) or ( self.token == "tkn_str" ) or ( self.token == "para" ) or ( self.token == "tkn_real" ) or ( self.token == "haga" ) or ( self.token == "si" ) or ( self.token == "hasta" ) or ( self.token == "repita" ) or ( self.token == "entonces" ) or ( self.token == "falso" ) or ( self.token == "tkn_times" ) or ( self.token == "tkn_div" ) or ( self.token == "o" ) or ( self.token == "caso" ) or ( self.token == "tkn_geq" ) or ( self.token == "fin" ) or ( self.token == "tkn_equal" ) or ( self.token == "id" ) or ( self.token == "llamar" ) or ( self.token == "tkn_greater" ) or ( self.token == "tkn_leq" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_closing_bra","escriba","y","tkn_integer","sino","lea","tkn_plus","div","mod","tkn_comma","tkn_less","mientras","tkn_colon","retorne","tkn_power","tkn_neq","tkn_str","para","tkn_real","haga","tkn_opening_par","si","hasta","repita","entonces","falso","tkn_times","tkn_div","o","caso","tkn_geq","fin","tkn_equal","id","llamar","tkn_greater","tkn_leq","verdadero","tkn_minus","tkn_char","tkn_closing_par" ] )
 
 
    def Î(self):
        if (self.errorSintacticoEncontrado==True):
            return
        if( ( self.token == "tkn_opening_par" ) or ( self.token == "tkn_integer" ) or ( self.token == "id" ) or ( self.token == "falso" ) or ( self.token == "verdadero" ) or ( self.token == "tkn_minus" ) or ( self.token == "tkn_str" ) or ( self.token == "tkn_char" ) or ( self.token == "tkn_real" ) ):
            self.Í()
            self.Ú()
        elif( ( self.token == "tkn_closing_par" ) ):
            return
        else: self.errorSintaxis( [ "tkn_opening_par","tkn_integer","id","falso","verdadero","tkn_minus","tkn_str","tkn_char","tkn_real","tkn_closing_par" ] )
 
    def main(self):
        self.S()
        if (self.errorSintacticoEncontrado==True):
            return(self.resultado)
        if (self.token != "final de archivo" ):
            return self.errorSintaxis(["final de archivo"])
        return(self.resultado)
 
 




s= sintactico(sys.stdin.readlines())

print(s.main())
 
