import re
import sys

class Lexer:
    def __init__(self):
        self.operadores_tokens = {
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
            '<>': 'neq',
            '<': 'less',
            '<=': 'leq',
            '>': 'greater',
            '>=': 'geq',
        }
        # Expresiones regulares para identificar tokens
        self.regex_id = r'[a-zA-Z_]\w*'  # Identificador
        self.regex_integer = r'\d+'
        self.regex_real = r'\d+\.\d+'
        self.regex_str = r'".*?"'  # Cadena entre comillas dobles
        self.regex_char = r"'.{1}'"  # Carácter entre comillas simples
        # Palabras reservadas
        # Palabras reservadas en español para el lenguaje LPP
        self.reserved_words = set(["procedimiento",
                                   "funcion",
                                   "var",
                                   "retorne",
                                   "llamar",
                                   "inicio",
                                   "nueva_linea",
                                   "fin",
                                   "si",
                                   "sino",
                                   "mientras",
                                   "haga",
                                   "repita",
                                   "hasta",
                                   "entero",
                                   "cadena",
                                   "caracter",
                                   "lea",
                                   "escriba",
                                   "y",
                                   "o",
                                   "no",
                                   "verdadero",
                                   "falso",
                                   "entonces",
                                   "booleano",
                                   "real",
                                   "para",
                                   "caso",
                                   "caracter",
                                   "arreglo",
                                   "de",
                                   "cerrar",
                                   "abrir",
                                   "como",
                                   "tipo",
                                   "es",
                                   "registro",
                                   ])
        self.fila=1
        self.current_line=1
        self.tokens=[]
        self.in_comment_block=False
        self.lcolumnas=[]
        self.errorflag=False
    
    
    
    def principal(self, lineas):
        
        fila=1
        columna=1
        lineatkns =[]
        
        for line in lineas:  
            # Eliminar comentarios de línea (//)
            line = re.sub(r'\/\/.*', '', line)
        
            # Buscar inicio de comentario de bloque (/*)
            if '/*' in line:
                self.in_comment_block = True
                if '*/' in line.split('/*', 1)[1]:
                    a=len(line.split('/*', 1)[1])-len(line.split('*/', 1)[1])
                    line = line.split('/*', 1)[0]+((" ")*a)+line.split('*/', 1)[1]
                    self.in_comment_block = False
                else:
                    line = line.split('/*', 1)[0]
            
            if self.in_comment_block:
                # Si estamos dentro de un comentario de bloque, buscar el cierre */
                if '*/' in line:
                    
                    self.in_comment_block = False                    
                    line = line.split('*/', 1)[1]
                else:
                    fila+=1
                    continue
        
            
            
            
            
            lineatkns= lineatkns + self.getTokensLinea(line,fila, columna)
            if(self.errorflag) :
                break
            fila+=1
        
        return lineatkns      
    
    def getTokensLinea(self,linea,fila,columna):
        
        tokns=[]
        inicio = 0
        if (self.errorflag==True):
            return []
        
        linea = linea.rstrip()
        
        #Elimino los espacios al inicio de la linea  y por tanto corro la columna
        if linea=='' or linea==[] or len(linea)==0 :
            return tokns
        
        while (linea[0]==" "):
            columna= columna+1             
            linea=linea[1:len(linea)]
            if len(linea)==1:
                tokns.append(self.get_token(linea,fila,columna))
                return tokns
        
        if linea=='\"' or linea==[] or linea=="\"" or linea=="\n" or linea=='' :
            return tokns
        
        
        #Me aseguro que la linea tenga más de un caracter
        if len(linea)==1:
            tokns.append(self.get_token(linea,fila,columna))
            return tokns
        
        realyletra = r'\d+\.\d+[^\d]'
        potencial_real = r'\d+\.'

        linea = linea.rstrip()
        
        
        for i in range(0,len(linea)):
            
            #palabra que al principio tiene un caracter y va incrementando
            #con certeza se que tiene al menos 2 y uno de ellos no es espacio
            palabra_temporal = linea[0:i+1]
            
            
            if palabra_temporal==[] or len(linea)==0 or palabra_temporal==None:
                return tokns       
            
            if self.isvalid(palabra_temporal[i])=="e":
                if (len(linea)>0):
                    tokns.append(self.get_token(palabra_temporal[inicio:i],fila,columna))
                    columna=columna+i
                if self.errorflag==False:
                    tokns.append(self.get_token(palabra_temporal[i:i+1],fila,columna))
                
                return tokns
                    
            
            if re.fullmatch(r'\d+\.\d+[^0-9]$',palabra_temporal):
                tokns.append(self.get_token(palabra_temporal[inicio:i],fila,columna))
                columna=columna+i
                tokns = tokns + self.getTokensLinea(linea[i:len(linea)],fila,columna)
                columna = columna+1
                return tokns
                    
                
            
            elif(palabra_temporal[i] in self.operadores_tokens):
                
                
                if re.match(potencial_real,palabra_temporal) and i<len(linea)-1:
                    if re.match(self.regex_real,palabra_temporal+linea[i+1]):
                        continue
                
                else: 
                    return self.casosEspecial(linea,i,columna,fila,tokns)
                          
            elif linea[i] == "\"":
                
                if (i>0):
                    tokns.append(self.get_token(palabra_temporal[inicio:i],fila,columna))
                    columna=columna+i
                for j in range (i+1,len(linea)):
                    if linea[j] == "\"":
                        tokns.append(self.get_token(linea[i:j+1],fila,columna))
                        columna=columna+len(linea[i:j+1])
                        tokns = tokns + self.getTokensLinea(linea[j+1:len(linea)],fila,columna)
                        return tokns
                self.errorflag= True
                tokns.append(self.get_token("<<<error",fila,columna))
                return tokns
            
            elif linea[i] == "\'":
                
                if (i>0):
                    tokns.append(self.get_token(palabra_temporal[inicio:i],fila,columna))
                    columna=columna+i
                for j in range (i+1,len(linea)):
                    if linea[j] == "\'":
                        tokns.append(self.get_token(linea[i:j+1],fila,columna))
                        columna=columna+len(linea[i:j+1])
                        tokns = tokns + self.getTokensLinea(linea[j+1:len(linea)],fila,columna)
                        return tokns
                self.errorflag= True
                tokns.append(self.get_token("<<<error",fila,columna))
                return tokns
                        
            #Si es el fin de la linea envio la palabra para obtener un token
            elif (i+1==len(linea)):
                tokns.append(self.get_token(palabra_temporal,fila,columna))
                return tokns
            
            #Si el caracter es un espacio envío la palabra actual antes del espacio
            elif (linea[i]==" "):            
                tokns.append(self.get_token(palabra_temporal[inicio:i],fila,columna))
                columna= columna+i
                
                tokns = tokns + self.getTokensLinea(linea[i:len(linea)],fila,columna)
                return tokns
        return tokns
            
    
    def isvalid(self,leter):
        if leter not in self.operadores_tokens and leter not in ["\""]+["\'"]+[" "] and re.fullmatch(r'[^a-zA-Z0-9-_]',leter):  
            return "e"
        else:
            return "c"
    
    def get_token(self,word,fila,columna):
         
        a= word
        word=word.lower()
        
        if word in self.reserved_words:
            
            token= "<"+word+","+str(fila)+","+str(columna)+">"
        
        elif word in self.operadores_tokens:
            token= "<tkn_"+self.operadores_tokens.get(word)+","+str(fila)+","+str(columna)+">"
        
         
        elif re.fullmatch(self.regex_id, word):
            token= "<id,"+word+","+str(fila)+","+str(columna)+">"
        
        elif re.match(self.regex_real,word):
            token= "<tkn_real,"+str(word).rstrip()+","+str(fila)+","+str(columna)+">"
        
        elif re.fullmatch(self.regex_integer,word):
            token= "<tkn_integer,"+str(word).rstrip()+","+str(fila)+","+str(columna)+">"
        
        elif re.fullmatch(self.regex_char,word):
            token= "<tkn_char,"+a[1:len(word)-1]+","+str(fila)+","+str(columna)+">"
        
        elif re.fullmatch(self.regex_str,word):
            token= "<tkn_str,"+a[1:len(word)-1]+","+str(fila)+","+str(columna)+">"
        
        else:
            self.errorflag= True
            token= ">>> Error lexico (linea: "+str(fila)+", posicion: "+str(columna)+")"
                    
        print(token)
        return(token+"\n")           
    
    
    def casosEspecial(self,linea,c,columna,fila,tkns):
        
        a=c-1
        s=c+1
        aa=c-2
        ss=c+2
        
        ae = (a)>=0
        se = (s)<len(linea)
        aae = aa>=0
        sse = aa<len(linea)
        
        if ae:
            acio= linea[a]+linea[c] in self.operadores_tokens
        else:
            acio= False     
        if se:
            csio= linea[c]+linea[s] in self.operadores_tokens
        else: 
            csio= False
            

              
        #Envio palabra anterior
        # Cuando el simbolo anterior existe y cuando anterior y actual juntos no son un operador
        if (ae) and (acio==False): 
            tkns.append(self.get_token(linea[0:c],fila,columna))
            columna= columna + len(linea[0:c])
        
        # Envio palabra anterior al anterior
        # Cuando el simbolo anterior al anterior existe y anterior y actual juntos son un operador
        if (aae) and (acio): 
            tkns.append(self.get_token(linea[0:a],fila,columna))
            columna = columna + len(linea[0:a])
        
        #Envio el anterior y actual
        if (acio):
            tkns.append(self.get_token(linea[a:s],fila,columna))
            columna = columna + 2
        #Envio solo el actual
        if (acio==False) and (csio==False):
            tkns.append(self.get_token(linea[c:s],fila,columna))
            columna = columna + 1
            
        #Envio el actual y el siguiente
        if (csio):
            tkns.append(self.get_token(linea[c:ss],fila,columna))
            columna = columna + 2
            

        # Envio palabra siguiente
        # Cuando el simbolo siguiente existe y el actual con el siguiente no son un operador
        if (se) and (csio==False):
            tkns = tkns+self.getTokensLinea(linea[s:len(linea)],fila,columna)
            columna = columna + len(linea[s:len(linea)])
        
        #Envio palabra siguiente a la siguiente
        #Cuando existe una letra siguiente a la siguiente y el actual con el siguiente son un operador especial
        if (sse) and (csio):
            tkns = tkns+self.getTokensLinea(linea[ss:len(linea)],fila,columna)
            columna = columna + len(linea[ss:len(linea)])
        
        return tkns
            
    

# l=Lexer()

# l.principal(sys.stdin.readlines())