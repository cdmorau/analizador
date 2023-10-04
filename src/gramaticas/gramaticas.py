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
K: Entero
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
W: NPi
X: Less
Y: Estructura de identificadores continuos
Z: Coma
Á: division para identificadores
É: Variables
Í: Operaciones
Ó: Nodo auxiliar operaciones
Ú: Combinación separada por comas de U
Ý: Otro Y
À: Identificadores que terminan en fin para los registrods
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
Ã: Abre parentesis
Õ: Cierra parentesis
Ā: coma declaracion variable y coma
Ē: dospunto tipo de variable de retorno o nada
Ī: Parentesis con definicion de variables
Ō: retorne sintaxis
Ū: id solito u.u

'Ã' condicion
'Õ' y y o 
'X' operador sin y o o
'K'concatena operadores con valores
'À' valores concatenados
'Ō', variable axuliar de K
'W', valores concatenados entre parentesis
Ů = concatenacion de y y o
Ă = concatenacion de valores que no contienen identificadores
Ĕ = valores que no tienen identificadores
Ğ= continuacion caso
Ḫ= otra A
Ĭ= valor para terminar concatenacion identificadores

N̆= otra A
Ŏ
Ŭ

Ĉ Ḓ Ḙ Ĝ Ĥ Ĵ Ḽ Ṋ Ŝ Ṱ Ṷ Ŵ X̂ Ŷ Ẑ

Ḧ N̈  S̈ T̈ Ṳ Ẅ Ẍ Ÿ

Ø:
Æ:
"""


estructuraGeneral = {
    # Registros VariablesDeclaradas y Funciones y procedimientos 
    'S': ['RVDinicioAfin'],
    
    #Acciones entre inicio y fin B = asignaciones<-,  E= Estructura escribir, L= Estructura Lea H= Estructuras SI,else,sino
    #C estructura Casos   # N= estructura nueva linea M=Estructura mientras  I = estructura repita T= Estructura Para   Q=eliminacion de recursividad
    'A': ['BA','CA','escribaEA','leaLA','HA','llamarNA','MA','IA','TA','ε'],
    #A dentro de un caso
    'Ḫ': ['BḪ','CḪ','escribaEḪ','leaLḪ','HḪ','llamarNḪ','MḪ','IḪ','TḪ','ε'],
    
    #Para A dentro de un si
    'Ĕ': ['BĔ','CĔ','escribaEĔ','leaLĔ','HĔ','llamarNĔ','MĔ','IĔ','TĔ','ε'],
    
    #Para funciones
    'Â': ['BÂ','CÂ','escribaEÂ','leaLA','HÂ','llamarNÂ','MÂ','IÂ','TÂ','retorneÍÂ','ε'],
    
    #Para cuando está
    'Ŭ': ['BŬ','CŬ','escribaEŬ','leaLŬ','HŬ','llamarNŬ','MŬ','IŬ','TŬ','ε'],
    
    
    #Antes del inicio R=registros V = variables F= Funciones P=Procedimientos W=Eliminacion de recursividad
    'D': ['funcionFD','procedimientoPD', 'ε'],
    'Ð': ['GidÝÐ', 'ε'],
    
    # Derivados de D
    'R':['registroÅÛregistroR','ε'],
    'V':['GidYV','ε'],
    'F':['idĪtkn_colonÜÐinicioÂfin'],
    'P':['idUÐinicioAfin'],
    
    # Derivados de A
    # n1<-(2/3)*5+2^2
    'B':['idÙtkn_assignÍ'],
    'C':['casoŪĬḪtkn_colonḪĞ'],
    'E':['ÍÚ'],
    'L':['idÈÒ'],
    'H':['siÃentoncesĔĂ'],
    'N':['nueva_linea','idÔ'],
    'M':['mientrasÃhagaAÛmientras'],
    'I':['repitaŬhastaĂ'],
    #Me preocupa ese valor I
    'T':['paraŪtkn_assignÍĈÍhagaAÛpara'],
    
    #Inicio de asignaciones
    'Ḓ':['JÍÚO','ε'],
    
    #
    'Ĉ':['hasta'],
    
    #Estructura de caso
    
    'Ğ':['ĬĂtkn_colonḪĞ','sinoḪÛcaso','Ûcaso'],
    'Ĭ':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso'],
    'Ă':['ZĬĂ','ε'],
    
    
    #Estructura del si 
    #Condicion
    'Ă':['sinoAÛsi','Ûsi'],
    'Ã':['ÀŮ'],
    
    'Ů':['ÕÀŮ','ε'],
    
    'Õ':['y','o'],
    #Version clonada donde el operador no puede ser y o o
    

    'W':['ÉŌ','tkn_opening_parWtkn_closing_parŌ','tkn_minusW',],
    'Ō':['XË','ε'],

    'À':['ÉK','tkn_opening_parÃtkn_closing_parK','tkn_minusÀ'],
    'K':['XÀ','ε'],
    
    'X':['tkn_plus', 'tkn_times', 'tkn_div', 'tkn_power','div','mod','tkn_neq','tkn_leq','tkn_geq','tkn_minus','tkn_equal','tkn_less',"tkn_greater"],
    
    
    
    
    
    # Otras estructuras
    # Estructura de identificador individual seguido de cualquier otro valor antes del inicial
    'Y':['ZidY','ε'],
    'Ý':['ZidÝ','ε'],
    'Ò':['tkn_commaŪÈÒ','ε'],
    #Cadenas caracteres e identificadores separados por comas
    #'U':['tkn_str','tkn_char','id'],# puedo no necesitarlo
    'Ú':['ZÍÚ','ε'],
    'Z':['tkn_comma'],
    # Estructura para tipos de dato
    'G':['entero' , 'real', 'caracter' , 'booleano' , 'cadenaJtkn_integerO','arregloJtkn_integerÊOdeG','id'],
    'Ü':['entero' , 'real', 'caracter' , 'booleano' , 'cadenaJtkn_integerO','id','real'],
    'Ê':['Ztkn_integerÊ','ε'],
    # Estructura para definir tamaño
    'J':['tkn_opening_bra'],

    'O':['tkn_closing_bra'],
    
    #operaciones
    
    #x <- -3+(5.76*2/x mod (10.0)-9
    #Í
    #-Í
    #-ÉÓ
    #-3Ó
    #-3+Í
    #-3+(Í)
    #-3+(ÉÓ)
    #-3+(5.76Ó)Ó
    #-3+(5.76*Í)Ó
    #-3+(5.76*2Ó)Ó
    #-3+(5.76*2/xÓ)Ó
    #-3+(5.76*2/xmodÍ)Ó
    #-3+(5.76*2/xmod(Í)Ó)Ó
    #-3+(5.76*2/xmod(ÉÓ)Ó)Ó
    #-3+(5.76*2/xmod(-ÍÓ)Ó)Ó
    #-3+(5.76*2/xmod(-9ÓÓ)Ó)Ó

    
    
    
    #Version clonada para operaciones que se encuentran dentro de parentesis que evitan que O acepte la palabra fin
    'Ë':['ÉÄ','tkn_opening_parËtkn_closing_parÄ','tkn_minusË'],
    'Ä':['QË','ε'],

    'Í':['ÉÓ','tkn_opening_parËtkn_closing_parÓ','tkn_minusÍ'],
    'Ó':['QÍ','ε'],
    #'Ë':['ε','QÍ'],
    
    #Operadores aritmeticos
    'Q':['tkn_plus', 'tkn_times', 'tkn_div', 'tkn_power','div','mod','y','o','tkn_neq','tkn_leq','tkn_geq','tkn_minus','tkn_equal','tkn_less',"tkn_greater"],

    #valores
    'É':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idÁ'],
    
    #distinciones id normal y llamado de arreglo
    'Á':['JÍÚO','Ô'],
    #llamado de funciones y arreglos multidimensionales
    'Ù':['JÍÚOÙ','tkn_periodŪÙ','ε'],
    
    
    'È':['JÍOÌ','Ì'], 
    'Ì':['tkn_periodŪÈ','ε'],
    
    #Variables para determinar declaraciones de variables separadas por comas y encerradas en parentesis

    
    'Ā':['ZĒGidĀ','ε'],
    'Ē':['var','ε'],
    'Ī':['tkn_opening_parĒGidĀtkn_closing_par','ε'],
    'U':['tkn_opening_parĒGidĀtkn_closing_par','ε'],
    
    
    'Ū':['id'],
    
    
    'Å':['GidÝÅ','ε'],
    'Û':['fin'],
    'Ô':['tkn_opening_parÎtkn_closing_par','ε'],
    'Î':['ÍÚ','ε']
    
    
    #Parentesis que permite estar vacio o tener una serie de valores semarados por comas 

    
    #Letras sin usar J, K, Ñ, O, U, X, Z 
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

