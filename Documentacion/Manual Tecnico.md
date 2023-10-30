# Proyecto 2 - Manual Técnico
Alvaro Gabriel Ramirez Alvarez - 202112674

En este manual presenta el desarrollo y la lógica del siguiente código desde el punto de vista del programador.

# Main.py
Este código es un programa de interfaz gráfica de usuario (GUI) en Python utilizando la biblioteca Tkinter. La GUI permite realizar:
## Abrir archivos
 Cuando se hace clic en el botón **Abrir**, se abre un cuadro de diálogo que permite al usuario seleccionar un archivo .bizdata para abrirlo en el editor de texto en la interfaz.
 ```python
        def open_file(self):
        global filepath
        filepath = askopenfilename(
            filetypes=[("Archivos .bizdata", "*.bizdata")]
        )
        if not filepath:
            return
        
        self.txtArea.delete(1.0,tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txtArea.insert(tk.END, text)
        self.ventana.title(f"Proyecto 2 - {filepath.split('/')[-1]}")

``` 

## Analizar texto
 Cuando se hace clic en el botón **Analizar**, el programa toma el texto contenido en el editor de texto de la interfaz y lo pasa a una función llamada analizar, que debe estar definida en un módulo llamado "analizador". Esta función realiza el análisis sintáctico. 
```python
    def analizar_texto(self):
        print("Analizando...")
        with open(filepath, "r") as input_file:
            text = input_file.read()
        tokens = tokenize_input(text)
        parser = Parser(tokens)
        parser.parse()
        arbol.generarGrafica()

``` 
## Guardar archivos
 Cuando se hace clic en el botón **Guardar**, se abre un cuadro de diálogo que permite al usuario seleccionar una ubicación y un nombre de archivo para guardar el contenido actual del editor de texto.

 ```python
     def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="json",
            filetypes=[("Archivos .bizdata", "*.bizdata")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txtArea.get(1.0, tk.END)
            output_file.write(text)
        self.ventana.title(f"Proyecto 2 - {filepath.split('/')[-1]}")
 ```

# Arbol.py

Este código define una clase Arbol que utiliza la biblioteca graphviz para crear y manipular gráficas. Puede agregar nodos con etiquetas, configurar el estilo de los nodos, agregar aristas entre nodos y generar y guardar la gráfica en el sistema de archivos.

```python
class Arbol:
    def __init__(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.dot = graphviz.Digraph(comment=f"Graph {timestr}")
        self.counter = 0

```

## Clase Parser

La clase `Parser` es una parte fundamental de un programa más grande. Su función principal es analizar una secuencia de tokens y ejecutar acciones basadas en los tokens encontrados. A continuación, se describe su funcionamiento:

```python
        def parse(self):

        raiz = arbol.agregarNodo("INICIO")
        self.ultimaInstruccion = raiz
        while self.index < len(self.tokens):
            name=self.peek().name
            if name == "IMPRIMIR":
                self.imprimir()
            elif name == "IMPRIMIRLN":
                self.imprimirln()
            elif name == "CLAVES":
                self.claves()
            elif name == "REGISTROS":
                self.registros()
            elif name == "CONTEO":
                self.conteo()
            elif name == "CONTARSI":
                self.contarsi()
            elif name == "MAX":
                self.max()
            elif name == "MIN":
                self.min()
            elif name == "PROMEDIO":
                self.promedio()
            elif name == "DATOS":
                self.datos()
            elif name == "SUMAR":
                self.sumar()
            elif name == "EXPORTARREPORTE":
                self.exportarReporte()

            else:
                print("Error: Token no reconocido")
                return
            print(self.ultimaInstruccion)
            if self.index < len(self.tokens):
                self.ultimaInstruccion = arbol.agregarNodo("LISTA_INSTRUCCIONES")
                arbol.agregarArista(raiz, self.ultimaInstruccion)
                raiz = self.ultimaInstruccion
```

### Método `consume`

Este método avanza el índice y devuelve el token en la posición actual.

### Método `peek`

Este método devuelve el token en la posición actual sin avanzar el índice.

### Método `parse`

Este es el método principal de análisis. Realiza las siguientes acciones:

- Inicializa un nodo raíz con el nombre "INICIO" en el árbol.
- Establece el atributo `ultimaInstruccion` en este nodo raíz.
- Entra en un bucle while para procesar los tokens hasta que se llegue al final de la lista de tokens.
- Dentro del bucle, verifica el nombre del token actual (utilizando `peek().name`) y realiza diferentes acciones basadas en el nombre del token. Las acciones se implementan en métodos como `imprimir`, `imprimirln`, `claves`, etc.
- Si el nombre del token actual no se reconoce, se imprime un mensaje de error y se retorna.
- Después de procesar un token, se actualiza `ultimaInstruccion` y la estructura del árbol.
- Finalmente, se llama al método `show_output`, que muestra la consola.


# GRAMATICA
```python
INICIO -> LISTA_INSTRUCCIONES

LISTA_INSTRUCCIONES -> INSTRUCCION LISTA_INSTRUCCIONES
                    | Epsilon


INSTRUCCION -> INS_CLAVES
            |  INS_REGISTROS
            |  INS_IMPRIMIR            
            |  INS_IMPRIMIRLN
            |  INS_CONTEO
            |  INS_PROMEDIO
            |  INS_CONTARSI
            |  INS_DATOS
            |  INS_SUMAR
            |  INS_MAX
            |  INS_MIN
            |  INS_EXPORTARREPORTE

INS_CLAVES -> Claves igual corchetea LISTA_CLAVES corchetec
    LISTA_CLAVES -> cadena LISTA_CLAVES coma
    INS_CLAVES -> LISTA_CLAVES corchetec 

INS_REGISTROS -> Registros igual corchetea LISTA_REGISTROS 
    LISTA_REGISTROS -> cadena LISTA_REGISTROS coma
    INS_CLAVES -> LISTA_REGISTROS corchetec
            


INS_IMPRIMIR -> imprimir string parena string parenc puntoycoma
INS_IMPRIMIRLN -> imprimirln parena cadena parenc puntoycoma
INS_CONTEO -> conteo parena parenc puntoycoma
INS_CONTARSI -> contarsi parena cadena coma entero parenc puntoycoma
INS_DATOS -> datos parena parenc puntoycoma
INS_PROMEDIO -> promedio parena cadena parenc puntoycoma
INS_SUMAR -> sumar parena cadena parenc puntoycoma
INS_MAX -> max parena cadena parenc puntoycoma
INS_MIN -> min parena cadena parenc puntoycoma
INS_EXPORTARREPORTE -> exportarReporte parena cadena parenc puntoycoma









```     



