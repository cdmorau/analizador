from predicciones import *

class generarCodigoAnalizador:
    def __init__(self,referenciGramatica,inicio):
        self.elementos_gramatica = predicciones(referenciGramatica,inicio)
        self.gram= self.elementos_gramatica.gram
        self.conjuntoPredicciones= self.elementos_gramatica.prediccionNoTerminales
        self.nodoactual="S"
    
    
    def generarCadenaDeOrPrediccion(self,setPrediccion):
        
        cadena = "( "
        for pred in setPrediccion:
            
            cadena = cadena +"( self.token == "+ "\""+pred+"\""+" ) or "
            
        cadena = cadena[0:len(cadena)-3]
        cadena = cadena + ")"
        
        return cadena
    
    def cadenaconjunto(self,nodoNoTerminal):
        
        conjuntoPrediccionesNodoNoTerminal=set()
        
        #Obtengo el conjunto de conjuntos de prediccion de un nodo particular
        for keypred in self.conjuntoPredicciones.keys():
            if keypred[0] == nodoNoTerminal:
                conjuntoPrediccionesNodoNoTerminal.update(self.conjuntoPredicciones.get(keypred))
        
        cadena = "[ "
        
        for pred in conjuntoPrediccionesNodoNoTerminal:
            cadena= cadena+ "\""+pred+"\""+","
            
        cadena = cadena[0:len(cadena)-1]
        cadena = cadena + " ]"
        
        return cadena
        
    def algoritmoProduccion(self,prod):
        
        codigo=[]

        for nodo in prod:
            if nodo.isupper():
                codigo.append("            self."+nodo+"()")
            else:
                #codigo.append("            print (\"Aqui anexo: \"+  self.lexico.lexema+\"  "+self.nodoactual+""+"\")")
                codigo.append("            self.emparejar(" + "\""+nodo+"\""")" )
                
        return codigo
            
    
    def generar_funcion_nodo_no_terminal(self,nodoNoTerminal):
        codigo=[]
        self.nodoactual = nodoNoTerminal
        codigo.append("    def "+nodoNoTerminal+"(self):")
        #codigo.append("        print(\""+nodoNoTerminal+"\")")
        codigo.append("        if (self.errorSintacticoEncontrado==True):")
        codigo.append("            return")
        
        
        cont=len(codigo)
        
        vacio=False
        for keypred in self.conjuntoPredicciones.keys():
            
            if keypred[0]==nodoNoTerminal:
                
                conjunto= self.conjuntoPredicciones.get(keypred)
                if cont==len(codigo):
                    cont=cont+1
                    codigo.append("        if"+self.generarCadenaDeOrPrediccion(conjunto)+":")
                    
                else:
                    codigo.append("        elif"+self.generarCadenaDeOrPrediccion(conjunto)+":")
                if keypred[5:len(keypred)][0] == 'ε':
                    #codigo.append("            print (\"Aqui salto\")")
                    codigo.append("            return"            )
                else:    
                    codigo = codigo+self.algoritmoProduccion(self.elementos_gramatica.separar(keypred[5:len(keypred)]))
               
        codigo.append("        else: self.errorSintaxis( "+self.cadenaconjunto(nodoNoTerminal)+" )")
        
        return codigo
    
    def generarCodigoGeneral(self):
        codigo=[]
        inicio=self.elementos_gramatica.inicio 
        codigo.append("import sys")
        codigo.append("from src.analizadorLexico import *")
        codigo.append(" ")
        codigo.append("class sintactico:")
        codigo.append("    def __init__(self,codigo):")
        codigo.append("        self.lexico=Lexer(codigo)")
        codigo.append("        self.token = self.lexico.getNextToken()")
        codigo.append("        self.resultado = \"El analisis sintactico ha finalizado exitosamente.\"")
        codigo.append("        self.errorSintacticoEncontrado=False")

        codigo.append("""
    
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
        
        #print(\"No se reconoce token\",lexema_token,self.lexico.lastToken)
    
    def salidaConjuntoLexema(self, conjuntoTokens):
        
        conjunto2=[]
        for c in range(len(conjuntoTokens)):
            
            if conjuntoTokens[c] in ["tkn_char","tkn_str","tkn_caracter","tkn_integer","tkn_real"] or (conjuntoTokens[c] in self.lexico.tokens_pR.keys()) or (conjuntoTokens[c] =="id"):
                conjuntoTokens[c]=self.salidaLexema(conjuntoTokens[c])
            
            
        conjuntoTokens.sort()

        for d in range(len(conjuntoTokens)):


            if "tkn_" == conjuntoTokens[d][0:4]:
                conjuntoTokens[d]=\"\\"\"+self.salidaLexema(conjuntoTokens[d])+\"\\\"\"
            else:
                conjuntoTokens[d]=\"\\"\"+ conjuntoTokens[d] +\"\\\"\"

        return conjuntoTokens   

    
    def seEsperaba(self,lexema_token):
        
        if (lexema_token == "tkn_integer") or (lexema_token == "tkn_str") or (lexema_token == "tkn_real") or (lexema_token == "tkn_char") or (lexema_token == "id"):
            return self.lexico.lexema_token
        else: return(self.salidaLexema(lexema_token))
    
                      """)
        
        codigo.append(" ")
        
        codigo.append("    def errorSintaxis(self,conjunto):")
        codigo.append("        if (self.errorSintacticoEncontrado==True):")
        codigo.append("            return(self.resultado)")
        #codigo.append("        print(self.token,conjunto)")
        error ="\"<\"+self.lexico.fila_token+\":\"+self.lexico.columna_token+\"> Error sintactico: se encontro: \\\"\"+t+\"\\\"; se esperaba: \"+ \", \".join(self.salidaConjuntoLexema(conjunto))+\".\""
        codigo.append("        t=self.seEsperaba(self.token)")
        codigo.append("        self.resultado="+error)
        codigo.append("        self.errorSintacticoEncontrado=True")
        codigo.append("        return(self.resultado)")
        
        
        
        codigo.append(" ")
        codigo.append("    def emparejar(self,tknEsperado):")
        codigo.append("        if (self.errorSintacticoEncontrado==True):")
        codigo.append("            return")
        codigo.append("        if ( self.token == tknEsperado ):")
        codigo.append("            self.token= self.lexico.getNextToken()")
        codigo.append("        else:")
        codigo.append("            self.errorSintaxis([tknEsperado])")
        

        for nodoNoTerminal in self.elementos_gramatica.gram.keys():
            codigo.append(" ")
            codigo=codigo+self.generar_funcion_nodo_no_terminal(nodoNoTerminal)
            codigo.append(" ")

        
        codigo.append("    def main(self):")
        codigo.append("        self."+inicio+"()")
        codigo.append("        if (self.errorSintacticoEncontrado==True):")
        codigo.append("            return(self.resultado)")
        codigo.append("        if (self.token != \"final de archivo\" ):")
        codigo.append("            return self.errorSintaxis([\"final de archivo\"])")
        codigo.append("        return(self.resultado)")
        codigo.append(" ")
        codigo.append(" ")


        
        with open('src/analizadorSintactico.py', 'w', encoding="utf-8") as f:
            for linea in codigo:
                f.write(linea+"\n")
        return codigo
        
        
        
        
        
                         

generador=generarCodigoAnalizador(estructuraGeneral,'S')
generador.elementos_gramatica.imprimir()

generador.generarCodigoGeneral()

codigo=generador.generar_funcion_nodo_no_terminal('A')


            
        
        
        

