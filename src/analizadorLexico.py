
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

