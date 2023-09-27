
import re
import copy
import sys

class Token:
    def __init__(self):
        
        #Flag para errores
        self.errorflag = False
        
        #Regex de patrones 
        self.other ={
            "real":r'[0-9][0-9]*\.[0-9][0-9]*',
            "id":r'^[_a-zA-Z][a-zA-Z0-9_]*$',
            "integer":r'[0-9][0-9]*',
            "str":r'".*?"',
            "char":r"'.?'",
        }
        
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
            "es":"es",
            "y":"y",
            "o":"o",
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

        


    #Devuelve tokens de una linea
    def getToken(self,linea,fila,columna):
        #Cadena de tokens que será devuelta
        tkns=[]
        inicio=0
        if linea == "" :
            return tkns
        #Eliminación de espacios en blanco
        while linea[inicio]==" " or linea[inicio] == ' ':
            columna = columna+1
            inicio= inicio+1
            if inicio>=len(linea):
                break
        #Eliminación de saltos de linea
        linea=linea[inicio:len(linea)].rstrip("\n")
        #Versión en minuscula de la cadena
        linea2= copy.deepcopy(linea).lower()
        #Bool de comillas dobles
        com= False
        #Bool de comillas simples
        com2 = False
        
        
        for c in range(len(linea)):
            #Palabra siguiente
            ps=linea[c+1:len(linea)]

            #Condiciones de salto al siguiente caracter en caso de comillas
            if linea[c]=="\""  and com2==False:
                com = not com   
            if com and c!=len(linea)-1:
                continue
            if linea[c]=="\'" and com == False :
                com2 = not com2
            if com2 and c!=len(linea)-1:
                continue
        
            #Palabra a analizar
            palabra_temporal = linea[0:c+1]
            psiv=False

            # Condición de salto al siguiente caracter hasta obtener un error o una linea a analizar
            if re.match(r"[a-zA-Z_0-9]",ps) :
                continue


            # Se evalúa si se trata de un identificador mal escrito
            if re.match(r'^[0-9][0-9]*[_a-zA-Z][a-zA-Z0-9_]*$',linea[0:c+1]):
                print(palabra_temporal)
                n= re.match(r'^[0-9][0-9]*',linea[0:c+1]).group()
                p= re.match(r'[_a-zA-Z][a-zA-Z0-9_]*$',linea[len(n):c+1]).group()
                tkn= "<tkn_integer,"+n+","+str(fila)+","+str(columna)+">"
                tkns.append(tkn)
                tkn= self.errorTes(p,fila,columna+len(n))
                tkns.append(tkn)
                break
            
            #Se evalua si es una palabra reservada
            for k in self.tokens_pR.keys():
                if linea2[0:c+1]==k:
                    
                    tkn= "<"+k+","+str(fila)+","+str(columna)+">"
                    tkns.append(tkn)
                    tkns= tkns + self.getToken(ps,fila,columna+len(linea2[0:c+1]))
                    return tkns
            
            #Bool para reales
            poi=False
            #Se evalua para identificador o variables
            for i in self.other.keys():
                
                m=re.match(self.other.get(i),linea2[0:c+1])
                
                if m:
                    
                        

                    if linea[c+1:len(linea)]!="":
                        if i=="integer"and linea[c+1:len(linea)][0] ==".":
                            poi = True
                            break
                        
                    if i== "id":
                        
                        tkn= "<id,"+m.group()+","+str(fila)+","+str(columna)+">"
                    elif i!="str" and i!="char":
                        
                        tkn= "<tkn_"+i+","+m.group()+","+str(fila)+","+str(columna)+">"
                    else:
                        
                        tkn= "<tkn_"+i+","+linea[1:c]+","+str(fila)+","+str(columna)+">"
                    
                    tkns.append(tkn)
                    
                    tkns= tkns + self.getToken(ps,fila,columna+len(m.group()))
                    return tkns

            if poi:
                continue
            
            
            #Se evalua para operadores
            for j in self.operadores_tokens.keys():
                
                m=re.match(re.escape(j),linea[0:c+2])
                
                if m:
                    tkn= "<tkn_"+self.operadores_tokens.get(j)+","+str(fila)+","+str(columna)+">"
                    tkns.append(tkn)
                    if len(j)==1:
                        tkns= tkns + self.getToken(linea[1:len(linea)],fila,columna+1)
                    if len(j)==2:
                        tkns= tkns + self.getToken(linea[2:len(linea)],fila,columna+2)
                        
                    return tkns
            
            #Generación de errores con cadenas no coincidentes
            
            
            tkn= self.errorTes(linea[0:c+1],fila,columna)
            tkns.append(tkn)
            break
        
        return tkns
    
    #Paso de lineas 
    def getTokens(self,lineas):
        
        lineas=self.reemplazar_comentarios(lineas)

        tkns=[]
        fila=1
        for lin in lineas:
            columna=1       
            tkns=tkns+self.getToken(lin,fila,columna)
            fila = fila+1     
            if self.errorflag == True:
                break
        
        return tkns
 
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
    
    #Manejo de errores
    def errorTes(self,palabra,fila,columna):
        
        self.errorflag=True
        
        return ">>> Error lexico (linea: "+str(fila)+", posicion: "+str(columna)+")"

        
       
            
