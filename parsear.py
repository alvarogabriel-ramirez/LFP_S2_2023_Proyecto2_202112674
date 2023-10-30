
from printer import Printer
import tkinter as tk
from db import DB
from arbol import *
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.printer = Printer()
        self.db = DB()
        self.ultimaInstruccion = None

    def consume(self):
        token = self.tokens[self.index]
        self.index += 1
        return token
    
    def peek(self):
        return self.tokens[self.index]
    
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
        # self.save_and_print()
        self.show_output()
        # texto = self.printer.print()
        # for line in texto.split("\n"):
        #     print("\033[32m" + ">> " + line + "\033[0m")

    def show_output(self):
        output = self.printer.print()
        root = tk.Tk()
        root.title("Consola ")
        text = tk.Text(root, height=20, width=50)
        text.pack()
        for line in output.split("\n"):
            text.insert(tk.END, ">> " + line + "\n")
        root.mainloop()

    def imprimir(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        token = self.consume()
        if token.name != "STRING":
            print("Error: Se esperaba una cadena")
            return
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return

        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("IMPRIMIR")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("imprimir"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)

        self.printer.add(token.value)

    def imprimirln(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        token = self.consume()
        if token.name != "STRING":
            print("Error: Se esperaba una cadena")
            return
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return
        
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("IMPRIMIRLN")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("imprimirln"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)
        self.printer.addLine(token.value)

    def claves(self):
        self.consume()
        if self.consume().name != "IGUAL":
            print("Error: Se esperaba un igual")
            return
        if self.consume().name != "CORCHETEIZQUIERDO":
            print("Error: Se esperaba un corchete izquierdo")
            return
        
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return       
        valor1 = self.consume().value
        self.db.agregarClave(valor1)        
        while self.peek().name == "COMA":
            self.consume()
            if self.peek().name != "STRING":
                print("Error: Se esperaba un valor de clave")
                return
            valor1 = self.consume().value
            self.db.agregarClave(valor1)        
        if self.consume().name != "CORCHETEDERECHO":
            print("Error: Se esperaba un corchete derecho")
            return

    def registros(self):
        self.consume()
        if self.consume().name != "IGUAL":
            print("Error: Se esperaba un igual")
            return
        if self.consume().name != "CORCHETEIZQUIERDO":
            print("Error: Se esperaba un corchete izquierdo")
            return
        
        while self.peek().name == "LLAVEIZQUIERDA":#------------------------------
            self.consume()
            contador = 0

            if self.peek().name != "STRING" and self.peek().name != "NUMBER":
                print("Error: Se esperaba un valor de clave")
                return
            
            valor = self.consume().value
            self.db.agregarValor(contador, valor)
            contador += 1

            while self.peek().name == "COMA":
                self.consume()
                if self.peek().name != "STRING" and self.peek().name != "NUMBER":
                    print("Error: Se esperaba un valor de clave")
                    return
                valor = self.consume().value
                self.db.agregarValor(contador, valor)
                contador += 1

            if self.peek().name != "LLAVEDERECHA":
                print("Error: Se esperaba una llave derecha")
                return
            self.consume()# }
        self.consume()# ]
        self.db.imprimirRegistros()

    def conteo(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return 
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("CONTEO")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("conteo"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)
        self.printer.addLine(str(self.db.conteo()))

    def contarsi(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return
        clave = self.consume().value
        if self.consume().name != "COMA":
            print("Error: Se esperaba una coma")
            return
        
        if self.peek().name != "STRING" and self.peek().name != "NUMBER":
            print("Error: Se esperaba un valor de clave")
            return
        valor = self.consume().value

        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return
        
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("CONTARSI")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("contarsi"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(","))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)
        self.printer.addLine(str(self.db.contarsi(clave, valor)))

    def max(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return
        clave = self.consume().value
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return   
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("MAX")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("max"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)     
        self.printer.addLine(str(self.db.max(clave)))

    def min(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return
        clave = self.consume().value
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return   
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("MIN")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("min"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)   
        self.printer.addLine(str(self.db.min(clave)))

    def promedio(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return
        clave = self.consume().value
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return   
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("PROMEDIO")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("promedio"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)        
        self.printer.addLine(str(self.db.promedio(clave)))

    def datos(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return 
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("DATOS")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("datos"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)   
        self.printer.addLine(str(self.db.datos()))

    def sumar(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return
        clave = self.consume().value
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return      
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("SUMAR")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("sumar"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)     
        self.printer.addLine(str(self.db.sumar(clave)))

    def exportarReporte(self):
        self.consume()
        if self.consume().name != "PARENTESISIZQUIERDO":
            print("Error: Se esperaba un parentesis izquierdo")
            return
        if self.peek().name != "STRING":
            print("Error: Se esperaba un valor de clave")
            return
        titulo = self.consume().value
        if self.consume().name != "PARENTESISDERECHO":
            print("Error: Se esperaba un parentesis derecho")
            return
        if self.consume().name != "PUNTOYCOMA":
            print("Error: Se esperaba un punto y coma")
            return    
        raiz = arbol.agregarNodo("INSTRUCCION")
        instruccion = arbol.agregarNodo("EXPORTARREPORTE")
        arbol.agregarArista(raiz, instruccion)
        arbol.agregarArista(instruccion, arbol.agregarNodo("exportarReporte"))
        arbol.agregarArista(instruccion, arbol.agregarNodo("("))
        arbol.agregarArista(instruccion, arbol.agregarNodo("STRING"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(")"))
        arbol.agregarArista(instruccion, arbol.agregarNodo(";"))
        arbol.agregarArista(self.ultimaInstruccion, raiz)       
        self.db.exportarReporte(titulo)
        self.printer.addLine("Reporte exportado con exito")


    def save_and_print(self):
        texto = self.printer.print()
        for line in texto.split("\n"):
            print("\033[32m" + ">> " + line + "\033[0m")

