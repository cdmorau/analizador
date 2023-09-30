from predicciones import *

class generarCodigoAnalizador:
    def __init__(self,gram,inicio):
        self.elementos_gramatica= predicciones(gram,inicio)
        self.gram= self.elementos_gramatica.gram
        self.conjuntoPredicciones= self.elementos_gramatica.prediccionNoTerminales
    
    
    def generarCadenaDeOrPrediccion(self,setPrediccion):
        
        cadena = "( "
        for pred in setPrediccion:
            
            cadena = cadena +"( token() == "+ "\""+pred+"\""+" ) or "
            
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
                codigo.append("        "+nodo+"()")
            else:
                codigo.append( "        emparejar(" + "\""+nodo+"\""")" )
        return codigo
            
    
    def generar_funcion_nodo_no_terminal(self,nodoNoTerminal):
        codigo=[]
        
        codigo.append("def "+nodoNoTerminal+"():")
        cont=0
        for keypred in self.conjuntoPredicciones.keys():
            if keypred[0]==nodoNoTerminal:
                cont=cont+1
                conjunto= self.conjuntoPredicciones.get(keypred)
                if keypred[5:len(keypred)] =='ε':
                    continue
                if cont==1:
                    codigo.append("    if"+self.generarCadenaDeOrPrediccion(conjunto)+":")
                else:
                    codigo.append("    elif"+self.generarCadenaDeOrPrediccion(conjunto)+":")
                codigo = codigo+self.algoritmoProduccion(self.elementos_gramatica.separar(keypred[5:len(keypred)]))
                    
                    
        codigo.append("    else: errorSintaxis( "+self.cadenaconjunto(nodoNoTerminal)+" )")
        
        return codigo
    
    def generarCodigoGeneral(self):
        codigo=[]
        inicio=self.elementos_gramatica.inicio 
        codigo.append("import sys")
        codigo.append("from src.gramar2 import *")
        codigo.append(" ")
        codigo.append("def errorSintaxis(conjunto):")
        codigo.append("    return(conjunto)")
        codigo.append(" ")
        codigo.append("def emparejar(tknEsperado):")
        codigo.append("    if ( token == tknEsperado ):")
        codigo.append("        token= lexico.getNextToken()")
        codigo.append("    else:")
        codigo.append("        errorSintaxis([tknEsperado])")
        

        for nodoNoTerminal in self.elementos_gramatica.gram.keys():
            codigo.append(" ")
            codigo=codigo+self.generar_funcion_nodo_no_terminal(nodoNoTerminal)
            codigo.append(" ")

        
        codigo.append("if __name__ == \"__main__\":")
        codigo.append("    lexico=Lexer(sys.stdin.readlines())")
        codigo.append("    token= lexico.getNextToken()")
        codigo.append("    "+inicio+"()")
        codigo.append("    if (token != \"FINAL ARCHIVO\" ):")
        codigo.append("        errorSintaxis([\"FINAL ARCHIVO\"])")
        
        with open('src/analizadorSintactico.py', 'w', encoding="utf-8") as f:
            for linea in codigo:
                f.write(linea+"\n")
        return codigo
        
        
        
        
                         

generador=generarCodigoAnalizador(ejercicio1,'S')
generador.elementos_gramatica.imprimir()

generador.generarCodigoGeneral()

print(generador.elementos_gramatica.esLL1)
codigo=generador.generar_funcion_nodo_no_terminal('B')

for linea in codigo:
    print(linea)


            
        
        
        

