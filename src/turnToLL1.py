from gramaticas.gramaticas import *
import re


def eliminarRecursividadPorLaIzquierda(nodoNoTerminal,gramatica):
    
    abc="ABCDEFGHIJKLMNOPQRTUVWXYZ"
    nuevoNodo= abc[len(gramatica)]
    
    producciones= gramatica.get(nodoNoTerminal)
    postRecursivas=[]
    prodNoRecursivas=[]
    nuevasProducciones=[]
    
    for produccion in producciones:
        if produccion[0]==nodoNoTerminal:
            postRecursivas.append(produccion[1:len(produccion)])   
        else:
            prodNoRecursivas.append(produccion)
    
    gramatica[nodoNoTerminal]=[]
    for p in prodNoRecursivas:
        if p != 'ε':    
            gramatica.get(nodoNoTerminal).append(p+nuevoNodo)
        else:
            gramatica.get(nodoNoTerminal).append(nuevoNodo)
        
    
    gramatica[nuevoNodo]=[]
    for pr in postRecursivas:
        prod=pr+nuevoNodo
        gramatica.get(nuevoNodo).append(prod)
    
    gramatica.get(nuevoNodo).append('ε')
    
    return gramatica



def eliminarFactoresComunesPorLaIzquierda(nodoNoTerminal,gramatica):
    
    producciones= gramatica.get(nodoNoTerminal)   
    abc="ABCDEFGHIJKLMNOPQRTUVWXYZ"
    nuevoNodo= abc[len(gramatica)]
    
    inicialesTerminales = set()
    min= r'^[a-z]'
    produccionesAEliminar=[]
    inicialesRepetidos=[]
    produccionesPostRepetidos=[]
    for produccion in producciones:
        
        if re.match(min,produccion):
            p=""
            for indiceletra in range(len(produccion)):
                if re.match(min,produccion[indiceletra]):
                    p=p+produccion[indiceletra]
                    
            
            inicialesTerminales.update({p})
        
        
    #Calculo los iniciales repetidos
    
    for inicialTerminal in inicialesTerminales:
        cont=0
        for produccion in producciones:  
            if re.match(inicialTerminal,produccion):
                cont= cont+1
            if cont>1:
                inicialesRepetidos.append(producciones)
    
    #Establezco las producciones que eliminare  
    for inicialRepetido in inicialesRepetidos:
        for produccion in producciones:
            if re.match(inicialRepetido,produccion):
                produccionesAEliminar.append(produccion)
                produccionesPostRepetidos.append(produccion[len(inicialRepetido),len(produccion)])
                
    #Elimino las producciones
                
    
        
    
            
            
    
    return inicialesTerminales
        
        


g=gramaticaOperador
eliminarFactoresComunesPorLaIzquierda('A',g)

print("{")
for nodo in g.keys():
    print(nodo+":"+ str(g.get(nodo)) )
print("}")     

