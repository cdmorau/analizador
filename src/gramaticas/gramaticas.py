#Palabras reservadas
palabras_reservadas_lista = ['procedimiento', 'nueva_linea', 'verdadero', 'caracter', 'registro', 'entonces', 'booleano', 'caracter', 'mientras', 'arreglo', 'escriba', 'retorne', 'funcion', 'inicio', 'llamar', 'repita', 'entero', 'cadena', 'cerrar', 'hasta', 'falso', 'abrir', 'real', 'para', 'caso', 'haga', 'sino', 'como', 'tipo', 'lea', 'var', 'fin', 'no', 'si', 'de', 'y', 'o', 'div', 'mod']

operadores_lista= ['neq', 'leq', 'geq', 'assign', 'period', 'comma', 'colon', 'closing_bra', 'opening_bra', 'closing_par', 'opening_par', 'plus', 'minus', 'times', 'div', 'power', 'equal', 'less', 'greater']

reservadas_tipos_de_dato = ['entero','real','caracter','booleano','cadena']

datos_posibles = ['tkn_integer','tkn_real','tkn_str','tkn_char','id']

"""
A: Acciones
B: Asignaciones
C: Casos
D: Antes del inicio
E: Escribir
F: Funciones
G: Tipos de dato
H: Estructuras de Si
I: Estructura de repita
J: Abrir parentesis cuadrado
K:--
L: Estructura de Lea
M: Estructura de mientras
N: Estructura de nueva linea
Ñ: Minus
O: Cerrar parentesis cuadrado
P: Estructura de procedimiento
Q: Operadores aritmeticos
R: Estructura de registro
S: Nodo inicial
T: Estructura de For o para
U: Cadenas identificadores e ids
V: Estructura para definir variables
W: ---
X: --
Y: Estructura de identificadores continuos
Z: Coma
Á: division para identificadores
É: Variables
Í: Operaciones
Ó: Nodo auxiliar operaciones
Ú: Combinación separada por comas de U
Ý: Otro Y 
À: À W Ã Õ 
È: valor inicial asignacion despues de id
Ì: valor inicial asignacion despues de id
Ò: valor inicial asignacion despues de id
Ù: valor inicial asignacion despues de id
Ä: Version 2 operacion
Ë: Version 2 operacion
Ï: iterador para .id
Ö: Variable para mod
Ü: Otro G pero sin arreglo para el retorno de funciones
Â: A que puede retornar en algun punto
Ê: corchetes de declaración de arreglo normal o binimencional
Î: Atributos
Ô: Parentecis para llamado de funciones con llamar
Û: Fin solito 
Å: Serie de registros
Ã: --
Õ: --
Ā: coma declaracion variable y coma
Ē: dospunto tipo de variable de retorno o nada
Ī: Parentesis con definicion de variables
Ū: id solito u.u

Ō-
Ů-
N̆-X
Ŏ-
Ĉ-
Ḓ-
Ḙ-
Ĝ
Ă = concatenacion de valores que no contienen identificadores
Ĕ = valores que no tienen identificadores
Ğ= continuacion caso
Ḫ= otra A
Ĭ= valor para terminar concatenacion identificadores



Ŭ--

    Ĥ Ĵ Ḽ Ṋ Ŝ Ṱ Ṷ Ŵ Ŷ Ẑ

Ḧ N̈  S̈ T̈ Ṳ Ẅ Ẍ Ÿ

Ø:
Æ:

Ȧ* Ạ* Ḃ* Ḅ* Ċ- Ḋ* Ḍ* Ė* Ẹ* Ḟ* Ġ* Ḣ* Ḥ İ Ị* Ḳ Ŀ Ḷ Ḹ Ṁ Ṃ Ṅ Ṇ Ȯ K Ọ Ṗ Ṙ Q̇ Ṛ Ṡ Ṣ Ṫ Ṭ Ụ Ṿ Ẇ Ẉ Ẋ Ẏ 
"""




estructuraGeneral = {
    # Registros VariablesDeclaradas y Funciones y procedimientos 
    'S': ['RVDinicioṬfin'],
    'Ṭ':['Ẋ','ε'],
    
    #REGISTROS INICIA, CIERRA E INICIA OTROS REGISTROS
    'R':['registroŪÅÛregistroR','ε'],
    
    #Tipos de dato y asignacion de una variable particular INICIA  Å
    'Å':['GidÝÅ','ε'],
    'Ý':['ZidÝ','ε'],

    # FIN DECLARACION DE REGISTROS
    
    
    # INICIO DECLARACIÓN DE VARIABLES FUERA DE LOS REGISTROS
    
    #Tipos de dato y asignacion de una variable, no contempla fin registro
    #G no se altera puesto que siempre habrá un identificador despues de ésta
    'V':['GidYV','ε'],
    'Y':['ZidY','ε'],
    
    # FIN DECLARACIÓN DE VARIABLES FUERA DE LOS REGISTROS
    
    
    # INICIO DECLARACIÓN FUNCIONES Y PROCEDIMIENTOS
    
    'F':['idĪtkn_colonÜÐinicioÂfin'],
    #Atributos de la funcion entre parentesis, si los hay 
    'Ī':['tkn_opening_parĒGidĀtkn_closing_par','ε'],
    'Ē':['var','ε'],
    #Declaracion de variables separada por comas
    'Ā':['ZĒGidĀ','ε'],
    #Variables de retorno, no incluyen el arreglo
    'Ü':['entero' , 'real', 'caracter' , 'booleano' , 'cadenaJtkn_integerO','id','real'],
    #Declaración de variables a nivel interno
    'Ð': ['GidÝÐ', 'ε'],
    #Acciones para funciones donde es posible retornar en cualquier parte
    'Â': ['BÂ','CÂ','escribaEÂ','leaLÂ','HÂ','llamarNÂ','MÂ','IÂ','TÂ','retorneÍÂ','ε'],
    
    
    # Estructura para tipos de dato

    #Acciones entre inicio y fin B = asignaciones<-,  E= Estructura escribir, L= Estructura Lea H= Estructuras SI,else,sino
    #C estructura Casos   # N= estructura nueva linea M=Estructura mientras  I = estructura repita T= Estructura Para   Q=eliminacion de recursividad
    'Ẋ': ['BṬ','CṬ','escribaEṬ','leaLṬ','HṬ','llamarNṬ','MṬ','ȦṬ','TṬ'],
    'D': ['funcionFD','procedimientoŪUÐinicioṬfinD', 'ε'],
    'U':['tkn_opening_parĒGidĀtkn_closing_par','ε'],
    
    
    
    # Derivados de A
    # n1<-(2/3)*5+2^2
    'B':['idÁtkn_assignÍ'],
    'C':['casoŪṆĂtkn_colonŬĞĬ'],
    'E':['Ḍ'],
    'L':['idÈÒ'],
    'H':['siĿentoncesĔḊ'],
    'N':['nueva_linea','idÙ'],
    'M':['mientrasṂhagaṬÛmientras'],
    'I':['repitaḪhastaÍ'],
    'Ȧ':['repitaḪhastaŌ'],
    
    #Version auxiliar para repita
    'Ḫ': ['BḪ','CḪ','escribaEḪ','leaLḪ','HḪ','llamarNḪ','MḪ','IḪ','TḪ','ε'],  
    #Auxiliar clonada para si 
    'Ĕ': ['BĔ','CĔ','escribaEĔ','leaLĔ','HĔ','llamarNĔ','MĔ','IĔ','TĔ','ε'],
    #Para caso
    'Ŭ': ['BŬ','CŬ','escribaEŬ','leaLŬ','HŬ','llamarNŬ','MŬ','IŬ','TŬ','ε'],
    
    #Me preocupa ese valor I
    'T':['paraŪtkn_assignÀhastaṂhagaṬÛpara'],

    #Estructura de caso
    'Ğ':['ṆĂtkn_colonŬĞ','ε'],
    'Ṇ':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso'],
    'Ĭ':['sinoṬÛcaso','Ûcaso'],
    'Ă':['ZṆĂ','ε'],
    
    
    #Estructura del si 
    'Ḋ':['sinoṬÛsi','Ûsi'],
    #Variables asociadas a LEA
    'Ò':['tkn_commaŪÈÒ','ε'],
    'È':['JÍOÌ','Ì'], 
    'Ì':['tkn_periodŪÈ','ε'],
    

    # DEFINICION DE VALOR

    'Í':['ÉÓ','tkn_opening_parËtkn_closing_parÓ','tkn_minusÍ'],
    #Operadores de todo tipo
    'Ó':['QÍ','ÆȮ','ε'],
    #Operadores relacionales
    'Ȯ':['ÉẠ','tkn_opening_parËtkn_closing_parẠ','tkn_minusȮ'],
    'Ạ':['QÍ','ε'],
    
    #Dentro de parentesis
    'Ë':['ÉÄ','tkn_opening_parËtkn_closing_parÄ','tkn_minusË'],
    #Habiendo pasado por un relacional
    'Ä':['QË','ÆḂ','ε'],
    'Ḃ':['ÉḄ','tkn_opening_parËtkn_closing_parḄ','tkn_minusḂ'],
    'Ḅ':['QË','ε'],
    
    #VALOR
    'É':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idÙ'],
    #Operadores logicos
    'Q':['tkn_plus', 'tkn_times', 'tkn_div', 'tkn_power','div','mod','y','o','tkn_minus'],
    #Operadores relacionales
    'Æ':['tkn_leq','tkn_geq','tkn_equal','tkn_less','tkn_greater','tkn_neq'],
    #VARIABLE
    'Á':['JÍÚOÁ','tkn_periodŪÁ','ε'],
    #llamado de funciones y arreglos multidimensionales
    'Ù':['JÍÚOÙ','tkn_periodŪÙ','tkn_opening_parÎtkn_closing_parÙ','ε'],
    
    'Î':['ÍÚ','ε'],
    'Ḍ':['ÍÚ'],
    'Ú':['ZÍÚ','ε'],
    #FIN DEFINICION DE VALOR


    # Antes de un numero tkn_assign,[,(,si,mientras,haga, "," mientras
    'Ṃ':['ÉṀ','tkn_opening_parËtkn_closing_parṀ','tkn_minusṂ'],
    'Ȯ':['İK','tkn_opening_parËtkn_closing_parK','tkn_minusȮ'],
    'Ṁ':['QṂ','ÆȮ','ε'],
    'K':['QṂ','ε'],
    #VALOR
    'İ':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idṪ'],
    #llamado de funciones y arreglos multidimensionales
    'Ṫ':['JÍÚOṪ','tkn_periodŪṪ','tkn_opening_parÎtkn_closing_parṪ','ε'],
    
    #VERSION AUXILIAR DE VALOR para si
    # Antes de un numero tkn_assign,[,(,si,mientras,haga, ","
    'Ŀ':['ÉỌ','tkn_opening_parËtkn_closing_parỌ','tkn_minusĿ'],
    'Ṗ':['ṢṘ','tkn_opening_parËtkn_closing_parṘ','tkn_minusṖ'],
    'Ọ':['QĿ','ÆṖ','ε'],
    'Ṙ':['QĿ','ε'],
    #VALOR
    'Ṣ':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idṄ'],
    #llamado de funciones y arreglos multidimensionales
    'Ṅ':['JÍÚOṄ','tkn_periodŪṄ','tkn_opening_parÎtkn_closing_parṄ','ε'],
    
    
    
    #VERSION AUXILIAR DE VALOR para hasta
    # Antes de un numero tkn_assign,[,(,si,mientras,haga, ","
    'À':['ØÃ','tkn_opening_parËtkn_closing_parÃ','tkn_minusÀ'],
    'W':['ÉÕ','tkn_opening_parËtkn_closing_parÕ','tkn_minusW'],
    'Ã':['QÀ','ÆW','ε'],
    'Õ':['QÀ','ε'],
    #VALOR
    'Ø':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idŎ'],
    #llamado de funciones y arreglos multidimensionales
    'Ŏ':['JÍÚOŎ','tkn_periodŪŎ','tkn_opening_parÎtkn_closing_parŎ','ε'],
    
    # #VERSION AUXILIAR DE VALOR para escribir
 
    # Antes de un numero tkn_assign,[,(,si,mientras,haga, ","
    'Ō':['ḒĜ','tkn_opening_parËtkn_closing_parĜ','tkn_minusŌ'],
    'Ů':['ḒĈ','tkn_opening_parËtkn_closing_parĈ','tkn_minusŮ'],
    'Ĝ':['ẆŌ','ẎŮ','ε'],
    'Ĉ':['ẆŌ','ε'],
    #VALOR
    'Ḓ':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idḘ'],
    'Ẏ':['tkn_leq','tkn_geq','tkn_equal','tkn_less','tkn_greater','tkn_neq'],
    #llamado de funciones y arreglos multidimensionales
    'Ḙ':['JÍĴOḘ','tkn_periodŪḘ','tkn_opening_parṾtkn_closing_parḘ','ε'],
    'Ẇ':['tkn_plus', 'tkn_times', 'tkn_div', 'tkn_power','div','mod','y','o','tkn_minus'],
    
    'Ḽ':['ÍĴ'],
    'Ĵ':['ZÍĴ','ε'],
    'Ṿ':['ÍĴ','ε'],
    
    # PALABRAS AISLADAS
    'Ū':['id'],
    'Û':['fin'],
    'Z':['tkn_comma'],
    #Palabras reservadas de tipos de dato   
    'G':['entero' , 'real', 'caracter' , 'booleano' , 'cadenaJtkn_integerO','arregloJtkn_integerÊOdeG','id'],
    #Abre corchete cuadrado
    'J':['tkn_opening_bra'],
    #Cierra corchete cuadrado
    'O':['tkn_closing_bra'],
    #Enteros seguidos de enteros para la declaración de arreglos multidimencionales
    'Ê':['Ztkn_integerÊ','ε'],
    #Comas que separan G id dentro de los registros 
    
        
    
    
    #'Ạ':['QḂ','ε'],
    
    
    
    
    
    
    # Dentro de parentesis y habiendo pasado por un relacional
    #'Ị':['ÉḄ','tkn_opening_parÍtkn_closing_parḄ','tkn_minusỊ'],
    
    
    
    
    #Version clonada para operaciones que se encuentran dentro de parentesis que evitan que O acepte la palabra fin
    
    # 'Ä':['QË','ÆỊ','ε'],
    # #Version donde ya paso por un operador relacional
    # 'Ȧ':['ÉẠ','tkn_opening_parËtkn_closing_parẠ','tkn_minusȦ'],
    # 'Ạ':['QȦ','ε'],
    #Version donde ya paso por un operador relacional y está entre parentesispppppppppppp
    # 'Ị':['ÉỤ','tkn_opening_parËtkn_closing_parỤ','tkn_minusỊ'],
    # 'Ụ':['QỊ','ε'],


    

        
    #A dentro de un caso
    #'Ḫ': ['BḪ','CḪ','escribaEḪ','leaLḪ','HḪ','llamarNḪ','MḪ','IḪ','TḪ','ε'],   
    #ara A dentro de un si
    #'Ĕ': ['BĔ','CĔ','escribaEĔ','leaLĔ','HĔ','llamarNĔ','MĔ','IĔ','TĔ','ε'],
    #ara cuando está
    #'Ŭ': ['BŬ','CŬ','escribaEŬ','leaLŬ','HŬ','llamarNŬ','MŬ','IŬ','TŬ','ε'],
    #Antes del inicio R=registros V = variables F= Funciones P=Procedimientos W=Eliminacion de recursividad


    #VERSION AUXILIAR DE VALOR para if

}

#Estructura para probar escenarios de eliminacion de recursividad




gramaticaOperador={
    
    'S':['ÉÓ','tkn_opening_parStkn_closing_parÓ','tkn_minusS'],
    
    'Ó':['QS','ε'],
    
    #Operadores aritmeticos
    'Q':['tkn_plus', 'tkn_times', 'tkn_div', 'tkn_power','div','mod','y','o','tkn_neq','tkn_leq','tkn_geq','tkn_minus','tkn_equal','tkn_less',"tkn_greater"],

    #variables
    'É':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','id'],
    
    #abre-S-cierra-T   - abre-abre-S-cierra-T-cierra-T
    #abre-abre-10.0-cierra-menos9T-cierra-T
    
    #((10.0)-9
    
}


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
