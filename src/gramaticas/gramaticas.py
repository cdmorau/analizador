#Palabras reservadas
palabras_reservadas_lista = ['procedimiento', 'nueva_linea', 'verdadero', 'caracter', 'registro', 'entonces', 'booleano', 'caracter', 'mientras', 'arreglo', 'escriba', 'retorne', 'funcion', 'inicio', 'llamar', 'repita', 'entero', 'cadena', 'cerrar', 'hasta', 'falso', 'abrir', 'real', 'para', 'caso', 'haga', 'sino', 'como', 'tipo', 'lea', 'var', 'fin', 'no', 'si', 'de', 'y', 'o', 'div', 'mod']

operadores_lista= ['neq', 'leq', 'geq', 'assign', 'period', 'comma', 'colon', 'closing_bra', 'opening_bra', 'closing_par', 'opening_par', 'plus', 'minus', 'times', 'div', 'power', 'equal', 'less', 'greater']

reservadas_tipos_de_dato = ['entero','real','caracter','booleano','cadena']

datos_posibles = ['tkn_integer','tkn_real','tkn_str','tkn_char','id']



estructuraGeneral = {
    #D=Declaraciones A=Acciones
    'S': ['DinicioAfin'],
    
    #Acciones entre inicio y fin B = asignaciones<-,  E= Estructura escribir, L= Estructura Lea H= Estructuras SI,else,sino
    #C estructura Casos   # N= estructura nueva linea M=Estructura mientras  I = estructura repita T= Estructura Para D   Q=eliminacion de recursividad
    'A': ['BA','CA','EA','LA','HA','NA','MA','IA','TA','ε'],
    
    
    #Antes del inicio R=registros V = variables F= Funciones P=Procedimientos W=Eliminacion de recursividad
    'D': ['RD','VD','FD','PD', 'ε'],
    
    
    # Derivados de D
    'R':['registro'],
    'V':['GidY'],
    'F':['funcion'],
    'P':['procedimiento'],
    
    # Derivados de A
    'B':['asignaciones'],
    'C':['casos'],
    'E':['escribir'],
    'L':['estructuraLea'],
    'H':['estructurassi'],
    'N':['estructuranuevalinea'],
    'M':['estructuramientras'],
    'I':['estructurarepita'],
    'T':['estructuradefor'],
    
    # Otras estructuras
    # Estructura de identificador individual seguido de cualquier otro valor antes del inicial
    'Y':['commaidY','ε'],
    # Estructura para tipos de dato
    'G':['entero' , 'real', 'caracter' , 'booleano' , 'cadena' + 'opening_bra' + 'tkn_integer' + 'closing_bra'],
    # Estructura para arreglos
    
    
    #Letras sin usar J, K, Ñ, O, U, X, Z 
}

#Estructura para probar escenarios de eliminacion de recursividad

gramaticaRecursiva={

    #Acciones entre inicio y fin B = asignaciones<-,  E= Estructura escribir, L= Estructura Lea S= Estructuras SI,else,sino
    #C estructura Casos   # N= estructura nueva linea M=Estructura mientras  I = estructura repita T= Estructura Para D   Q=eliminacion de recursividad
    'S': ['BQ','Q'],
    'Q': ['BQ','ε'],
    'B': ['adios'],
    
}




gramatica1 = {
    'S': ['AunoBC', 'Sdos'],
    'A': ['BCD', 'Atres', 'ε'],
    'B': ['DcuatroCtres', 'ε'],
    'C': ['cincoDB', 'ε'],
    'D': ['seis', 'ε'],
}
gramatica2 = {
    'S': ['ABuno'],
    'A': ['dosB', 'ε'],
    'B': ['CD', 'tres', 'ε'],
    'C': ['cuatroAB', 'cinco'],
    'D': ['seis', 'ε'],
    
}

gramatica3 = {
    'A': ['BC','bad'],
    'B': ['bigCboss','ε'],
    'C': ['cat','cow'],
}

gramatica4 = {
    'A': ['Buno','dos'],
    'B': ['dos'],
}

gramaticaConRecursividad = {
    'E': ['EopsumaT','T'],
}

gramaticaConFactorComun = {
    'A': ['palabraT','palabraB','palabraC','dadoT','dadoB','dadoC'],
    'T': ['abc','B'],
    'B': ['abcd','C'],
    'C': ['abcde','A'],
    
}

ejercicio1 = {
    'S': ['ABC', 'DE'],
    'A': ['dosBtres', 'ε'],
    'B': ['BcuatroCcinco', 'ε'],
    'C': ['seisAB', 'ε'],
    'D': ['unoAE', 'B'],
    'E': ['tres'] 
}

ejercicio2 = {
    'S': ['Buno', 'dosC','ε'],
    'A': ['StresBC','cuatro', 'ε'],
    'B': ['AcincoCseis', 'ε'],
    'C': ['sieteB', 'ε'],
}

ejercicio3 = {
    'S': ['ABC', 'Suno'],
    'A': ['dosBC', 'ε'],
    'B': ['Ctres', 'ε'],
    'C': ['cuatroB', 'ε'],
}

