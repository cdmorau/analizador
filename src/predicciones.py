
import re 
import pandas as pd
from gramaticas.gramaticas import *


class predicciones:
    def __init__(self,gram,inicio):
        self.inicio = inicio
        self.gram = self.traducir(gram)
        self.primerosNoTerminales = self.primerosAll()
        self.siguientesNoTerminales = self.siguientesAll()
        self.prediccionNoTerminales = self.prediccionAll()
        self.esLL1 = self.isLL1()
   
    def separar(self,cadena):
        # Usamos una expresión regular para separar las mayúsculas de las minúsculas
        partes = re.findall(r'[A-Z]|[a-z_]+', cadena)
        
        # Concatenamos las mayúsculas individuales y las cadenas de minúsculas
        resultado = []
        buffer_mayusculas = ""
        
        for parte in partes:
            if parte.isupper():
                buffer_mayusculas += parte
            else:
                if buffer_mayusculas:
                    resultado.extend(list(buffer_mayusculas))
                    buffer_mayusculas = ""
                resultado.append(parte)
        
        if buffer_mayusculas:
            resultado.extend(list(buffer_mayusculas))
        
        return resultado
    
    def traducir(self,gram):
        for k in gram.keys():

            for i in range(len(gram.get(k))) :
                if gram.get(k)[i] == 'ε':
                    gram.get(k)[i]=['ε']
                else:
                    gram.get(k)[i]=self.separar( gram.get(k)[i] )    
                
        return gram
    
    def nodo_has_empty(self,nodoNoTerminal):
        producciones= self.gram.get(nodoNoTerminal)
        
        cont=0
        for p in producciones:
            if 'ε' in p:
                return True
            if p[0].islower() or p[0] == "_":
                cont=cont+1
        if cont==len(producciones):
            return False

        for p in producciones:

            mayusculas= True
            for cadena in p:
                if cadena.islower() or cadena == "_":
                    mayusculas=False
            
            if mayusculas:
                
                vacio=True
                for cadena in p:
                    if self.nodo_has_empty(cadena):
                        continue
                    else:
                        vacio = False
                if vacio:
                    return True    
          
        return False
          
    def primeros(self,produccion,noTerminal,noTerminalesContenidos):
        
        conjuntoPrimeros=set()
        has_empty = self.nodo_has_empty(noTerminal)
        
        # if produccion[0] in noTerminalesContenidos:
        #     if self.nodo_has_empty(produccion[0]):
        #         return self.primeros(self,produccion[1:],noTerminal,noTerminalesContenidos)
        #     else:
        #         return conjuntoPrimeros
        
        
        

        #Si el elemento es vacio añado el vacio
        if produccion[0] =='ε':
            conjuntoPrimeros.add(produccion[0])
        elif produccion[0].islower() or produccion[0] == "_":
            
            conjuntoPrimeros.add(produccion[0])
        #Si el elemento es un caracter en mayusculas
        elif produccion[0].isupper():
            
            
            for nodo in produccion:
                #En caso de encontrar recursión
                if nodo==noTerminal:
                    if has_empty==True:
                        continue
                    else:
                        break
                
                if nodo.isupper():   
                    if nodo in noTerminalesContenidos:
                        
                        if self.nodo_has_empty(nodo)==False: 
                            break
                        else:
                            continue
                    else:
                        noTerminalesContenidos.append(nodo)
                        
                        #Calculo el conjunto de primeros del nodo que ya comprobé es no terminal
                        primerosNoTerminal = self.primerosNodo(nodo,noTerminalesContenidos)                       
                        #Descarto la cadena vacia
                        primerosNoTerminal.discard('ε')
                        #Uno ambos conjuntos
                        conjuntoPrimeros.update(primerosNoTerminal) 
                        #Si la cadena vacia no está en el conjunto de primeros de dicho nodo rompo el ciclo porque ya encontre un nodo con todos los primeros terminales
                        if self.nodo_has_empty(nodo)==False: 
                            break
                
                if nodo.islower() or nodo=="_":
                    conjuntoPrimeros.add(nodo)
                    break
                    
        return conjuntoPrimeros  
                              
    def primerosNodo(self,nodoNoTerminal,noTerminalesContenidos):
        
        conjuntoPrimeros=set()
        listaProduccionesTerminal = self.gram.get(nodoNoTerminal)
        
        
        for produccion in listaProduccionesTerminal:
            conjuntoPrimeros.update(self.primeros(produccion,nodoNoTerminal,noTerminalesContenidos))
        
        return conjuntoPrimeros
                    
    def primerosAll(self):
        conjuntosPrimeros = {}
        for k in self.gram.keys():
            noTerminalesContenidos=[]
            conjuntosPrimeros[k]=self.primerosNodo(k,noTerminalesContenidos)
        return conjuntosPrimeros
    
    def siguientes(self,produccion,nodoNoTerminal,nodo_busqueda_siguientes,noterminalesContenidos):
        #En este caso la producción se mira aislada y el nodoNoTerminal no es necesariamente el asociado a la producción
        conjuntoSiguientes=set()
        
        if nodo_busqueda_siguientes== self.inicio:
            conjuntoSiguientes.add('$')    
        
        for indice_nodo in range(len(produccion)):
            
                    
            if produccion[indice_nodo]==nodo_busqueda_siguientes:
                
                
                
                #En caso de encontrar el nodoNoTerminal como ultimo termino de la producción particular
                if indice_nodo == len(produccion)-1:
                    if (nodoNoTerminal not in noterminalesContenidos):
                        #En este caso se agrega el conjunto de siguientes de la producción particular
                        noterminalesContenidos.append(nodoNoTerminal,)
                        
                        conjuntoSiguientes.update(self.siguientesNodo(nodoNoTerminal,noterminalesContenidos))
                        
                        
                    elif self.nodo_has_empty(nodoNoTerminal):
                        continue
                    
                    

                
                elif indice_nodo < len(produccion)-1:
                    nodo_siguiente = produccion[indice_nodo+1]
                    if nodo_siguiente.islower() or nodo_siguiente=="_":
                        
                        conjuntoSiguientes.add(nodo_siguiente)
                    
                        
                    elif nodo_siguiente.isupper():
                        #Si encuentro en el siguiente nodo un nodo no terminal, al conjunto de siguientes se agregan el conjunto de primeros del nodo encontrado
                        conjuntoSiguientes.update(self.primerosNoTerminales[nodo_siguiente])
                        if self.nodo_has_empty(nodo_siguiente):
                            #Elimino la cadena vacia del conjunto, ya que debio agregarse en el conjunto de primeros
                            conjuntoSiguientes.discard('ε')
                            #Determinar si el nodo siguiente al siguiente existe, si no existe se agregan los siguientes del nodo no terminal actual
                            if indice_nodo== len(produccion)-2:
                                if (nodoNoTerminal not in noterminalesContenidos):
                                    #En este caso se agrega el conjunto de siguientes de la producción particular
                                    noterminalesContenidos.append(nodoNoTerminal)
                                    conjuntoSiguientes.update(self.siguientesNodo(nodoNoTerminal,noterminalesContenidos))
                                elif self.nodo_has_empty(nodoNoTerminal):
                                    continue
                                
                            #En en caso de que exista el nodo siguiente al siguiente
                            #Se calcula ahora con la función siguientes una producción que inicie con el nodo al que le estamos buscando los siguientes
                            #Y que continue con la misma producción cortada desde el nodo siguiente al siguiente
                            else:
                                nueva_produccion=[nodo_busqueda_siguientes] 
                                nueva_produccion= nueva_produccion  +  produccion[indice_nodo+2  :  len(produccion)]
                                conjuntoSiguientes.update(self.siguientes(nueva_produccion,nodoNoTerminal,nodo_busqueda_siguientes,noterminalesContenidos))
                            

        return conjuntoSiguientes
    
    def siguientesNodo(self,nodo_busqueda_S,noTerminalesContenidos):
        
        
        conjuntoSiguientes=set()
        
        for nodoNoTerminal in self.gram.keys():
            
            for produccion in self.gram[nodoNoTerminal]:
                
                conjuntoSiguientes.update(self.siguientes(produccion,nodoNoTerminal,nodo_busqueda_S,noTerminalesContenidos))
        
        
        
        return conjuntoSiguientes     
    
    def siguientesAll(self):
        #Revisa los nodos no terminales ya almacenados
        
        conjuntosSiguientes = {}
        for nodoNoTerminal in self.gram.keys():
            noTerminalesContenidos=[]
            conjuntosSiguientes[nodoNoTerminal]=self.siguientesNodo(nodoNoTerminal,noTerminalesContenidos)
            
        return conjuntosSiguientes
    
    def prediccion(self,produccion,nodoNoTerminal):
        
        conjuntoPrediccion=set()
        
        if produccion[0]=='ε':
            conjuntoPrediccion.update(self.siguientesNoTerminales[nodoNoTerminal])
        
        elif produccion[0].islower() or produccion[0]=="_":
            conjuntoPrediccion.add(produccion[0])
        
        elif produccion[0].isupper():
            conjuntoPrediccion.update(self.primerosNoTerminales[produccion[0]])
            conjuntoPrediccion.discard('ε')
            
            
            if self.nodo_has_empty(produccion[0]):
                
                if produccion[1:len(produccion)] == []:
                    conjuntoPrediccion.update(self.siguientesNoTerminales[nodoNoTerminal])
                else:
                    
                    conjuntoPrediccion.update(self.prediccion(produccion[1:len(produccion)],nodoNoTerminal))
        return conjuntoPrediccion
    
    def prediccionAll(self):
        conjuntosPrediccion = {}
        
        for nodoNoTerminal in self.gram.keys():
            
            for produccion in self.gram[nodoNoTerminal]:
                
                conjuntosPrediccion[nodoNoTerminal+" => "+''.join(produccion)] = self.prediccion(produccion,nodoNoTerminal)
        
        return conjuntosPrediccion
    
    def imprimir(self):
        
        # Convierte los conjuntos en listas
        data_modificado_primeros = {key: list(value) for key, value in self.primerosNoTerminales.items()}
        data_modificado_siguientes = {key: list(value) for key, value in self.siguientesNoTerminales.items()}
        data_modificado_prediccion = {key: list(value) for key, value in self.prediccionNoTerminales.items()}

        
        # Construimos el pandas.
        dfprimeros = pd.DataFrame([data_modificado_primeros])
        dfsiguientes = pd.DataFrame([data_modificado_siguientes])
        dfprediccion = pd.DataFrame([data_modificado_prediccion]).transpose()
        
        
        dfprediccion.columns = ['PREDICCION']
        nombres_filas = ['PRIMEROS', 'SIGUIENTES']
        prim_seg =pd.concat([dfprimeros,dfsiguientes])
        prim_seg.index=nombres_filas
        
        
        
        with open('src/prediccion/prediccion.txt', 'w', encoding="utf-8") as f:
            f.write(dfprediccion.to_string())
            f.write('\n'*5)
            f.write(prim_seg.transpose().to_string())
    
    def isLL1(self):
        
        for nodoNoTerminal in self.primerosNoTerminales.keys():
            conjuntoPrueba=set()
            for produccion in self.prediccionNoTerminales.keys():
                if produccion[0] == nodoNoTerminal:
                    #Si la intersección de conjutos es 0 se agrega el conjunto
                    if len(conjuntoPrueba & self.prediccionNoTerminales.get(produccion))==0:
                        conjuntoPrueba.update(self.prediccionNoTerminales.get(produccion))
                    #Si hay elementos en ella retornar Falso
                    else:
                        
                        return False
        return True
                              


p = predicciones(estructuraGeneral,'S')
p.imprimir()
print(p.isLL1())







