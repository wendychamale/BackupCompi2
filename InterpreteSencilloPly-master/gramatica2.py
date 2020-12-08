# -----------------------------------------------------------------------------
# Rainman Sián
# 26-02-2020
#
# Ejemplo interprete sencillo con Python utilizando ply en Ubuntu
# ----------------------------------------------------------------------------
# comentario extra-

reservadas = {
    'show':'show',
    'databases':'databases',
    'select':'select',
    'distinct':'distinct',
    'from':'from',
    'alter':'alter',
    'rename':'rename',
    'to':'to',
    'owner':'owner',
    'table':'table',
    'add':'add',
    'column':'column',
    'set':'set',
    'not':'not',
    'null':'null',
    'check':'check',
    'constraint':'constraint',
    'unique':'unique',
    'foreign':'foreign',
    'key':'key',
    'replace':'replace',
    'if':'if',
    'exist':'exist',
    'mode':'mode',
    'inherits':'inherits',
    'primary':'primary',
    'references':'references',
    'default':'default',
    'type':'type',
    'enum':'enum',
    'drop':'drop',
    'update':'update',
    'where':'where',
    'smallint': 'smallint',
    'integer': 'integer',
    'bigint': 'bigint',
    'decimal': 'decimal',
    'numeric': 'numeric',
    'real': 'real',
    'double': 'double',
    'precision': 'precision',
    'money': 'money',
    'character': 'character',
    'varyng': 'varyng',
    'char': 'char',
    'timestamp': 'timestamp',
    'without': 'without',
    'time': 'time',
    'zone': 'zone',
    'date': 'date',
    'interval':'interval',
    'boolean':'boolean',
    'true':'true',
    'false':'false',
    'year':'year',
    'month':'month',
    'day':'day',
    'hour':'hour',
    'minute':'minute',
    'second':'second',
    'in':'in',
    'like':'like',
    'ilike':'ilike',
    'similar':'similar',
    'and':'and',
    'or':'or',
    'between':'between',
    'symetric':'symetric',
    'isnull':'isnull',
    'notnull':'notnull',
    'unknown':'unknown',
    'insert':'insert',
    'into':'into'
}

tokens = [
            'mas'
            'menos'
            'elevado'
            'multiplicacion'
            'division'
            'modulo'
            'similar'
            'menor'
            'mayor'
            'igual'
            'menor_igual'
            'mayor_igual'
            'diferente1'
            'diferente2'
            'and'
            'or'
            'ptcoma'
            'llavea'
            'llavec'
            'para'
            'parac'
            'dospuntos'
            'coma'
            'punto'
            'int'
            'decimal'
            'varchar'
            'char'
            'id'
         ] + list(reservadas.values())

# Tokenst_mas = r'\+'
t_menos = r'-'
t_elevado= r'^'
t_multiplicacion = r'\*'
t_division =r'/'
t_modulo= r'%'
t_menor =r'<'
t_mayor =r'>'
t_igual =r'='
t_menor_igual =r'<='
t_mayor_igual =r'>='
t_diferente1=r'<>'
t_diferente2=r'!='
t_simboloor=r'\|'
t_llavea = r'{'
t_llavec = r'}'
t_para = r'\('
t_parc = r'\)'
t_ptcoma =r';'
t_dospuntos=r':'
t_coma=r','
t_punto=r'.'



def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error no se puede convertir %d", t.value)
        t.value = 0
    return t


def t_int(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor numerico incorrecto %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'id')  
    return t


def t_varchar(t):
    r'\'.*?\''
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'--.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left', 'CONCAT'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'UMENOS'),
)

# Definición de la gramática



def p_init(t):
    'init            : instrucciones'


def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'


def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion '


def p_instruccion(t):
    '''instruccion      : imprimir_instr
                        | definicion_instr
                        | asignacion_instr
                        | mientras_instr
                        | if_instr
                        | if_else_instr'''


def p_instruccion_imprimir(t):
    'imprimir_instr     : IMPRIMIR PARIZQ expresion_cadena PARDER PTCOMA'


def p_instruccion_definicion(t):
    'definicion_instr   : NUMERO ID PTCOMA'

#hola
def p_asignacion_instr(t):
    'asignacion_instr   : ID IGUAL expresion_numerica PTCOMA'


def p_mientras_instr(t):
    'mientras_instr     : MIENTRAS PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'


def p_if_instr(t):
    'if_instr           : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'


def p_if_else_instr(t):
    'if_else_instr      : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER ELSE LLAVIZQ instrucciones LLAVDER'


def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica'''


def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'


def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_numerica PARDER'



def p_expresion_number(t):
    '''expresion_numerica : ENTERO
                        | DECIMAL'''


def p_expresion_id(t):
    'expresion_numerica   : ID'


def p_expresion_concatenacion(t):
    'expresion_cadena     : expresion_cadena CONCAT expresion_cadena'


def p_expresion_cadena(t):
    'expresion_cadena     : CADENA'


def p_expresion_cadena_numerico(t):
    'expresion_cadena     : expresion_numerica'


def p_expresion_logica(t):
    '''expresion_logica : expresion_numerica MAYQUE expresion_numerica
                        | expresion_numerica MENQUE expresion_numerica
                        | expresion_numerica IGUALQUE expresion_numerica
                        | expresion_numerica NIGUALQUE expresion_numerica'''


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()


def parse(input):
    return parser.parse(input)
