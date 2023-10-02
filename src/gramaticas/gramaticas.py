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
W:
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
È: 
Ì: 
Ò: 
Ù:
Ä:
Ë:
Ï:
Ö:
Ü:
Â:
Ê:
Î:
Ô:
Û: Fin solito 
Å: Serie de registros
Ã: Abre parentesis
Õ: Cierra parentesis
Ā: coma declaracion variable y coma
Ē: dospunto tipo de variable de retorno o nada
Ī: Parentesis con definicion de variables
Ō: retorne sintaxis
Ū: id solito u.u

"""

estructuraGeneral = {
    # Registros VariablesDeclaradas y Funciones y procedimientos 
    'S': ['RVDinicioAfin'],
    
    #Acciones entre inicio y fin B = asignaciones<-,  E= Estructura escribir, L= Estructura Lea H= Estructuras SI,else,sino
    #C estructura Casos   # N= estructura nueva linea M=Estructura mientras  I = estructura repita T= Estructura Para   Q=eliminacion de recursividad
    'A': ['BA','CA','escribaEA','LA','HA','llamarNA','MA','IA','TA','ε'],
    
    
    #Antes del inicio R=registros V = variables F= Funciones P=Procedimientos W=Eliminacion de recursividad
    'D': ['funcionFD','PD', 'ε'],
    'Ð': ['ÀÐ', 'ε'],
    
    # Derivados de D
    'R':['registroÅÛregistroR','ε'],
    'V':['GidYV','ε'],
    'F':['idĪtkn_colonGÐinicioAŌfin'],
    'P':['procedimiento'],
    
    # Derivados de A
    # n1<-(2/3)*5+2^2
    'B':['idXÍ'],
    'C':['caso'],
    'E':['UÚ'],
    'L':['lea'],
    'H':['si'],
    'N':['nueva_linea'],
    'M':['mientras'],
    'I':['repita'],
    'T':['para'],
    
    # Otras estructuras
    # Estructura de identificador individual seguido de cualquier otro valor antes del inicial
    'Y':['ZidY','ε'],
    'Ý':['ZidÝ','ε'],
    
    #Cadenas caracteres e identificadores separados por comas
    'U':['tkn_str','tkn_char','id'],
    'Ú':['ZUÝ','ε'],
    'Z':['tkn_comma'],
    # Estructura para tipos de dato
    'G':['entero' , 'real', 'caracter' , 'booleano' , 'cadenaJKO','arregloJKO','id'],
    # Estructura para definir tamaño
    'J':['tkn_opening_bra'],
    'K':['tkn_integer'],
    'O':['tkn_closing_bra'],
    'X':['tkn_assign'],
    #operaciones
    'Í':['ÉÓ'],
    'Ó':['QÉÓ','ε'],
    #Operadores aritmeticos
    'Q':['tkn_plus', 'tkn_minus', 'tkn_times', 'tkn_div', 'tkn_power','div','mod'],
    #variables
    'É':['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso','idÁ','tkn_opening_parÍtkn_closing_par'],
    #distinciones id normal y llamado de arreglo
    'Á':['JKO','ε'],
    #Variables para determinar declaraciones de variables separadas por comas y encerradas en parentesis
    'Ã':['tkn_opening_par'],
    'Õ':['tkn_closing_par'],
    'W':['ĒGidĀ'],
    'Ā':['ZW','ε'],
    'Ē':['var','ε'],
    'Ī':['ÃWÕ','ε'],
    'Ō':['retorneÍ','ε'],
    'Ū':['id'],
    
    'À':['GidÝ'],
    'Å':['ÀÅ','ε'],
    'Û':['fin'],
    
    
    
    
    
    
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

