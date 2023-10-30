from collections import namedtuple

Token = namedtuple("Token", ["name", "value", "line", "col"])

line = 1
col = 1

reservadas = {
    "imprimir": "IMPRIMIR",
    "Claves": "CLAVES",
    "Registros": "REGISTROS",
    "imprimirln": "IMPRIMIRLN",
    "conteo": "CONTEO",
    "promedio": "PROMEDIO",
    "contarsi": "CONTARSI",
    "datos": "DATOS",
    "sumar": "SUMAR",
    "max": "MAX",
    "min": "MIN",
    "exportarReporte": "EXPORTARREPORTE",
    "(" : "PARENTESISIZQUIERDO",
    ")" : "PARENTESISDERECHO",
    "{" : "LLAVEIZQUIERDA",
    "}" : "LLAVEDERECHA",
    "[" : "CORCHETEIZQUIERDO",
    "]" : "CORCHETEDERECHO",
    "," : "COMA",
    ":" : "DOSPUNTOS",
    ";" : "PUNTOYCOMA",
    "'''": "COMENTARIO_MULTILINEA",
    "#": "COMENTARIO",
    "=" : "IGUAL"
}


# String
def tokenize_string(input_str, i):
    token = ""
    for char in input_str:
        if char == '"':
            return [token, i]
        token += char
        i += 1
    print("Error: String no cerrado")


#numero
def tokenize_number(input_str, i):
    token = ""
    isDecimal = False
    for char in input_str:
        if char.isdigit():
            token += char
            i += 1
        elif char == "." and not isDecimal:
            token += char
            i += 1
            isDecimal = True
        else:
            break
    if isDecimal:
        return [float(token), i]
    return [int(token), i]

def tokenize_input(input_str):
    global line, col
    result_tokens = []
    i=0
    while i < len(input_str):
        char = input_str[i]
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            else:
                col += 1
            i += 1   
        elif char == '#':     
            while i < len(input_str) and input_str[i] != "\n":
                i += 1
            line += 1
            col = 1
        elif char == '"':
            string, pos = tokenize_string(input_str[ i + 1 :], i )
            col += len(string) + 1
            i = pos + 2
            token = Token("STRING", string, line, col)
            result_tokens.append(token)
        elif char.isalpha():
            j = i
            while j < len(input_str) and input_str[j].isalpha():
                j += 1
            word = input_str[i:j]
            if word in reservadas:
                col += len(word)
                token = Token(reservadas[word], word, line, col)
                result_tokens.append(token)
            i = j
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos 
            token = Token("NUMBER", number, line, col)
            result_tokens.append(token)
        elif char in reservadas:
            col += 1
            token = Token(reservadas[char], char, line, col)
            result_tokens.append(token)
            i += 1
        elif char == "'":
            j = i + 3
            while j < len(input_str) and input_str[j:j+3] != "'''":
                j += 1
            if j == len(input_str):
                print("Error: comentario multilinea no cerrado")
            else:
                col += j - i
                i = j + 3
        else:
            print(
                "Error: Caracter desconocido: {",
                char,
                "} en la linea: ",
                line + 1,
                "y columna: ",
                col + 1,
            )
            i += 1
            col += 1
        
    return result_tokens